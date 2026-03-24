"""Train an object detection model on a Roboflow COCO dataset using Flyte + Ray Train + PyTorch Lightning.

Inputs:
    roboflow_url: str        - HTTPS URL to a Roboflow COCO dataset zip, or a local directory path
    accuracy_request: float  - minimum mAP@0.5 required (e.g. 0.5 = 50%)
    output: str              - output path for model.pt (default: model.pt)

Output:
    Path to model.pt if mAP@0.5 >= accuracy_request, else None

Usage:
    flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train \\
        --roboflow_url <url_or_path> \\
        --accuracy_request <float> \\
        --output model.pt
"""

import json
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

import flyte
import requests
import torch
from flyteplugins.ray import RayJobConfig, WorkerNodeConfig
from torch.utils.data import DataLoader, Dataset


# ── Flyte task environment ────────────────────────────────────────────────────

train_env = flyte.TaskEnvironment(
    name="roboflow-ray-detector",
    image=flyte.Image.from_debian_base(name="ray", python_version=(3, 13)).with_pip_packages(
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "pytorch-lightning>=2.0.0",
        "ray[default]>=2.0.0",
        "flyteplugins-ray",
        "Pillow>=10.0.0",
        "requests>=2.32.0",
        "numpy>=1.24.0",
        "pandas",
        "pyarrow"
    ),
    resources=flyte.Resources(
        cpu=("2", "4"),
        memory=("4Gi", "22Gi"),
        disk="50Gi",
        shm="8Gi",
    ),
)

ray_config = RayJobConfig(
    worker_node_config=[WorkerNodeConfig(group_name="workers", replicas=2)],
    shutdown_after_job_finishes=True,
)


# ── Driver-only helpers ───────────────────────────────────────────────────────
# These run only on the driver process. They are NOT pickled for Ray workers.


class COCODetectionDataset(Dataset):
    """COCO-format dataset used by the driver for evaluation."""

    def __init__(self, img_dir: Path, annotations_file: Path):
        self.img_dir = img_dir

        with open(annotations_file) as f:
            coco = json.load(f)

        self.images = {img["id"]: img for img in coco["images"]}
        self.ann_by_image: dict[int, list] = {}
        for ann in coco["annotations"]:
            self.ann_by_image.setdefault(ann["image_id"], []).append(ann)
        self.image_ids = list(self.images.keys())

        cats = sorted({ann["category_id"] for ann in coco["annotations"]})
        self.cat_to_label = {c: i + 1 for i, c in enumerate(cats)}

    def __len__(self) -> int:
        return len(self.image_ids)

    def __getitem__(self, idx: int):
        from PIL import Image
        from torchvision import transforms as T

        image_id = self.image_ids[idx]
        img_info = self.images[image_id]
        img_path = self.img_dir / img_info["file_name"]

        img = Image.open(img_path).convert("RGB")
        img_tensor = T.ToTensor()(img)

        anns = self.ann_by_image.get(image_id, [])
        boxes, labels = [], []
        for ann in anns:
            x, y, w, h = (float(v) for v in ann["bbox"])
            if w > 0 and h > 0:
                boxes.append([x, y, x + w, y + h])
                labels.append(self.cat_to_label[ann["category_id"]])

        target = {
            "boxes": torch.tensor(boxes, dtype=torch.float32)
            if boxes
            else torch.zeros((0, 4), dtype=torch.float32),
            "labels": torch.tensor(labels, dtype=torch.int64)
            if labels
            else torch.zeros((0,), dtype=torch.int64),
            "image_id": torch.tensor([image_id]),
        }
        return img_tensor, target


def _collate_fn(batch):
    return tuple(zip(*batch))


def _find_annotation_file(dataset_dir: Path, split: str) -> Optional[Path]:
    """Locate the COCO annotation JSON for a given split name."""
    candidates = [
        dataset_dir / split / "_annotations.coco.json",
        dataset_dir / split / "annotations.json",
        dataset_dir / f"{split}.json",
        dataset_dir / "annotations" / f"{split}.json",
        dataset_dir / "annotations" / f"instances_{split}.json",
        dataset_dir / "annotations" / f"instances_{split}2017.json",
    ]
    for c in candidates:
        if c.exists():
            return c

    for p in dataset_dir.rglob("*.json"):
        if split in p.stem or split in p.parent.name:
            try:
                with open(p) as f:
                    data = json.load(f)
                if "annotations" in data and "images" in data:
                    return p
            except Exception:
                continue

    return None


def _resolve_img_dir(ann_file: Path) -> Path:
    candidate = ann_file.parent / "images"
    return candidate if candidate.is_dir() else ann_file.parent


def _build_detection_model(num_classes: int):
    """Reconstruct Faster RCNN for driver-side evaluation."""
    from torchvision.models.detection import (
        FasterRCNN_ResNet50_FPN_Weights,
        fasterrcnn_resnet50_fpn,
    )
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

    model = fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


def _compute_map(
    model, dataloader, iou_threshold: float = 0.5, device: str = "cpu"
) -> float:
    """Compute mean Average Precision at a given IoU threshold."""
    from torchvision.ops import box_iou

    model.eval()
    model.to(device)
    all_ap: list[float] = []

    with torch.no_grad():
        for images, targets in dataloader:
            images = [img.to(device) for img in images]
            predictions = model(images)

            for pred, target in zip(predictions, targets):
                gt_boxes = target["boxes"]
                pred_boxes = pred["boxes"].cpu()
                pred_scores = pred["scores"].cpu()

                if len(gt_boxes) == 0:
                    all_ap.append(0.0 if len(pred_boxes) > 0 else 1.0)
                    continue
                if len(pred_boxes) == 0:
                    all_ap.append(0.0)
                    continue

                order = pred_scores.argsort(descending=True)
                pred_boxes = pred_boxes[order]

                matched = torch.zeros(len(gt_boxes), dtype=torch.bool)
                tp, fp = [], []
                for pb in pred_boxes:
                    ious = box_iou(pb.unsqueeze(0), gt_boxes).squeeze(0)
                    best_iou, best_idx = ious.max(dim=0)
                    if best_iou >= iou_threshold and not matched[best_idx]:
                        tp.append(1)
                        fp.append(0)
                        matched[best_idx] = True
                    else:
                        tp.append(0)
                        fp.append(1)

                tp_cum = torch.tensor(tp, dtype=torch.float32).cumsum(0)
                fp_cum = torch.tensor(fp, dtype=torch.float32).cumsum(0)
                precision = tp_cum / (tp_cum + fp_cum)
                recall = tp_cum / len(gt_boxes)
                ap = torch.trapz(precision, recall).item()
                all_ap.append(ap)

    return sum(all_ap) / len(all_ap) if all_ap else 0.0


# ── Flyte task ────────────────────────────────────────────────────────────────


@train_env.task
def roboflow_ray_train(
    roboflow_url: str,
    accuracy_request: float,
    output: Optional[str] = "model.pt",
) -> Optional[str]:
    """Download a Roboflow COCO dataset, train with Flyte + Ray Train + PyTorch Lightning on CPU,
    and return the path to model.pt if mAP@0.5 >= accuracy_request, else None."""
    import os

    import ray
    from ray.train import Checkpoint, ScalingConfig
    from ray.train.torch import TorchTrainer

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        # ── Step 1: Obtain dataset directory ──────────────────────────────────
        if roboflow_url.startswith(("http://", "https://")):
            print(f"Downloading dataset from {roboflow_url} ...")
            resp = requests.get(roboflow_url, stream=True, timeout=300)
            resp.raise_for_status()
            zip_path = tmp / "dataset.zip"
            with open(zip_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            dataset_dir = tmp / "dataset"
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(dataset_dir)
        else:
            dataset_dir = Path(roboflow_url)
            if not dataset_dir.exists():
                print(f"Error: path not found: {roboflow_url}", file=sys.stderr)
                return None

        # ── Step 2: Locate annotation files ───────────────────────────────────
        train_ann = _find_annotation_file(dataset_dir, "train")
        val_ann = _find_annotation_file(dataset_dir, "valid") or _find_annotation_file(
            dataset_dir, "val"
        )

        if train_ann is None:
            print(
                "Error: could not find train annotations in dataset.", file=sys.stderr
            )
            return None

        print(f"Train annotations: {train_ann}")
        if val_ann:
            print(f"Val annotations:   {val_ann}")
        else:
            print("No validation split found; using train set for evaluation.")

        # ── Step 3: Determine number of classes ───────────────────────────────
        with open(train_ann) as f:
            coco_meta = json.load(f)
        num_classes = len(coco_meta["categories"]) + 1  # +1 for background

        # ── Step 4: Build eval dataloader (driver-side) ───────────────────────
        eval_ann = val_ann or train_ann
        eval_ds = COCODetectionDataset(_resolve_img_dir(eval_ann), eval_ann)
        eval_loader = DataLoader(
            eval_ds,
            batch_size=4,
            shuffle=False,
            collate_fn=_collate_fn,
            num_workers=2,
        )

        # ── Step 5: Define train_loop_per_worker as a closure ─────────────────
        # Defined inside roboflow_ray_train so cloudpickle serialises it as a
        # closure (full bytecode), not by module reference. This is required
        # because roboflow_ray_train.py is NOT present in the Ray worker
        # environment. All classes used by workers are also defined locally here.

        def train_loop_per_worker(config):
            import json
            import os
            import tempfile
            from pathlib import Path as _Path

            import pytorch_lightning as pl
            import ray.train
            import torch
            from PIL import Image
            from ray.train import Checkpoint
            from ray.train.lightning import (
                RayDDPStrategy,
                RayLightningEnvironment,
                RayTrainReportCallback,
                prepare_trainer,
            )
            from torch.utils.data import DataLoader, Dataset
            from torchvision import transforms as T

            _train_ann = config["train_ann_path"]
            _train_img_dir = config["train_img_dir"]
            _nc = config["num_classes"]
            _epochs = config.get("max_epochs", 10)

            class _COCODetectionDataset(Dataset):
                def __init__(self, img_dir, annotations_file):
                    self.img_dir = _Path(img_dir)
                    with open(annotations_file) as f:
                        coco = json.load(f)
                    self.images = {img["id"]: img for img in coco["images"]}
                    self.ann_by_image: dict = {}
                    for ann in coco["annotations"]:
                        self.ann_by_image.setdefault(ann["image_id"], []).append(ann)
                    self.image_ids = list(self.images.keys())
                    cats = sorted({ann["category_id"] for ann in coco["annotations"]})
                    self.cat_to_label = {c: i + 1 for i, c in enumerate(cats)}

                def __len__(self):
                    return len(self.image_ids)

                def __getitem__(self, idx):
                    image_id = self.image_ids[idx]
                    img_info = self.images[image_id]
                    img_path = self.img_dir / img_info["file_name"]
                    img = Image.open(img_path).convert("RGB")
                    img_tensor = T.ToTensor()(img)
                    anns = self.ann_by_image.get(image_id, [])
                    boxes, labels = [], []
                    for ann in anns:
                        x, y, w, h = (float(v) for v in ann["bbox"])
                        if w > 0 and h > 0:
                            boxes.append([x, y, x + w, y + h])
                            labels.append(self.cat_to_label[ann["category_id"]])
                    target = {
                        "boxes": torch.tensor(boxes, dtype=torch.float32)
                        if boxes
                        else torch.zeros((0, 4), dtype=torch.float32),
                        "labels": torch.tensor(labels, dtype=torch.int64)
                        if labels
                        else torch.zeros((0,), dtype=torch.int64),
                        "image_id": torch.tensor([image_id]),
                    }
                    return img_tensor, target

            def _cf(batch):
                return tuple(zip(*batch))

            class _ObjectDetector(pl.LightningModule):
                def __init__(self, num_classes: int, lr: float = 1e-4):
                    from torchvision.models.detection import (
                        FasterRCNN_ResNet50_FPN_Weights,
                        fasterrcnn_resnet50_fpn,
                    )
                    from torchvision.models.detection.faster_rcnn import (
                        FastRCNNPredictor,
                    )

                    super().__init__()
                    self.save_hyperparameters()
                    self.model = fasterrcnn_resnet50_fpn(
                        weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT
                    )
                    in_features = (
                        self.model.roi_heads.box_predictor.cls_score.in_features
                    )
                    self.model.roi_heads.box_predictor = FastRCNNPredictor(
                        in_features, num_classes
                    )

                def training_step(self, batch, batch_idx):
                    images, targets = batch
                    loss_dict = self.model(list(images), list(targets))
                    loss = sum(loss_dict.values())
                    self.log("train_loss", loss, prog_bar=True)
                    return loss

                def configure_optimizers(self):
                    return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)

            train_ds = _COCODetectionDataset(_train_img_dir, _train_ann)
            train_loader = DataLoader(
                train_ds,
                batch_size=4,
                shuffle=True,
                collate_fn=_cf,
                num_workers=2,
            )
            detector = _ObjectDetector(num_classes=_nc)

            trainer = pl.Trainer(
                max_epochs=_epochs,
                devices="auto",
                accelerator="cpu",
                strategy=RayDDPStrategy(),
                callbacks=[RayTrainReportCallback()],
                plugins=[RayLightningEnvironment()],
                enable_progress_bar=False,
            )
            trainer = prepare_trainer(trainer)
            trainer.fit(detector, train_loader)

            ckpt_dir = tempfile.mkdtemp()
            torch.save(
                detector.model.state_dict(),
                os.path.join(ckpt_dir, "model_state.pt"),
            )
            ray.train.report(
                {"final": True},
                checkpoint=Checkpoint.from_directory(ckpt_dir),
            )

        # ── Step 6: Launch Ray TorchTrainer ───────────────────────────────────
        if not ray.is_initialized():
            ray.init()
        ray_trainer = TorchTrainer(
            train_loop_per_worker=train_loop_per_worker,
            scaling_config=ScalingConfig(num_workers=1, use_gpu=False),
            train_loop_config={
                "train_ann_path": str(train_ann),
                "train_img_dir": str(_resolve_img_dir(train_ann)),
                "num_classes": num_classes,
                "max_epochs": 10,
            },
        )
        result = ray_trainer.fit()

        # ── Step 7: Load state dict from checkpoint ───────────────────────────
        if result.checkpoint is None:
            print("Error: no checkpoint returned from training.", file=sys.stderr)
            return None

        with result.checkpoint.as_directory() as ckpt_dir:
            state_dict = torch.load(
                os.path.join(ckpt_dir, "model_state.pt"),
                map_location="cpu",
            )

        # ── Step 8: Evaluate mAP@0.5 ──────────────────────────────────────────
        eval_model = _build_detection_model(num_classes)
        eval_model.load_state_dict(state_dict)

        print("Evaluating model ...")
        map_score = _compute_map(eval_model, eval_loader, device="cpu")
        print(f"mAP@0.5: {map_score:.4f}  (required: {accuracy_request:.4f})")

        # ── Step 9: Save model.pt if threshold met ────────────────────────────
        if map_score >= accuracy_request:
            output_path = output or "model.pt"
            torch.save(eval_model.state_dict(), output_path)
            print(f"Model saved to {output_path}")
            return output_path

        print(
            f"Accuracy {map_score:.4f} is below required {accuracy_request:.4f}. "
            "Returning None."
        )
        return None


# Attach RayJobConfig for Kubernetes/KubeRay deployment via Flyte
roboflow_ray_train.plugin_config = ray_config
