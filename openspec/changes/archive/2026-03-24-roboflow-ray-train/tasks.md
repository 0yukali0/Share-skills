## 1. Project Structure

- [x] 1.1 Create directory `skill_impl/roboflow_ray_train/`
- [x] 1.2 Create directory `skills/roboflow_ray_train/`

## 2. roboflow_ray_train.py

- [x] 2.1 Copy helper functions and classes from `roboflow_train.py` into the new file: `COCODetectionDataset`, `_collate_fn`, `_find_annotation_file`, `_resolve_img_dir`, `_compute_map`
- [x] 2.2 Define `train_loop_per_worker(config)` that reads `dataset_path` and `num_classes` from config, defines `COCODetectionDataset`, `ObjectDetector`, `_collate_fn` as local classes inside the function, and trains with `pl.Trainer` using `RayDDPStrategy` and `RayTrainReportCallback`
- [x] 2.3 Define `train_model(roboflow_url, accuracy_request, output="model.pt")` that downloads/extracts the dataset, determines `num_classes`, launches `TorchTrainer` with `ScalingConfig(num_workers=2, use_gpu=False)`, retrieves the best checkpoint, evaluates mAP@0.5, and saves `model.pt` if threshold is met

## 3. skill.md

- [x] 3.1 Write `skills/roboflow_ray_train/skill.md` documenting inputs (`roboflow_url`, `accuracy_request`), output (`model.pt` path or `None`), dependencies (`ray[train]`, `torch`, `torchvision`, `pytorch-lightning`), and the shared-filesystem requirement for distributed clusters
