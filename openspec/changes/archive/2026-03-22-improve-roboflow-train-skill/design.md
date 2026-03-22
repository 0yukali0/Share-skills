# Design: roboflow_train Skill — Architecture & Design Document

## Context

The `roboflow_train` skill (`skill_impl/roboflow_train/roboflow_train.py`) trains an object detection model on a Roboflow COCO dataset and returns `model.pt` if the accuracy threshold is met. It is implemented as a single Flyte task and exposed as a Claude Code skill via `skills/roboflow_train/SKILL.md`.

Currently there is no design document. This document captures the existing architecture, component responsibilities, data flow, and key design decisions so contributors have a reference for maintenance and extension.

**Current tech stack:**
- Runtime: Flyte (`@train_env.task` decorator, `flyte run --local`)
- ML framework: PyTorch + PyTorch Lightning
- Model: Faster RCNN ResNet-50 FPN (torchvision)
- Dataset format: COCO JSON
- Evaluation metric: mAP@0.5 (custom implementation)

---

## Goals / Non-Goals

**Goals:**
- Document the overall architecture and component boundaries
- Explain the data flow from dataset URL/path → trained model
- Record key design decisions and their rationale
- Identify known trade-offs and risks

**Non-Goals:**
- Changing any existing behaviour or code
- Introducing new features or configuration options
- Supporting dataset formats other than COCO JSON

---

## Architecture Overview

```
User / Claude
    │
    ▼ flyte run --local roboflow_train.py train_model
┌───────────────────────────────────────────────┐
│               train_model (Flyte task)         │
│                                               │
│  1. Dataset acquisition                       │
│     ├── HTTP download (URL) → unzip → dir     │
│     └── Local path passthrough                │
│                                               │
│  2. Annotation discovery                      │
│     └── _find_annotation_file() × {train, val}│
│                                               │
│  3. Dataset construction                      │
│     └── COCODetectionDataset (train + val)    │
│                                               │
│  4. Training                                  │
│     └── ObjectDetector (pl.LightningModule)   │
│         └── pl.Trainer (max_epochs=10)        │
│                                               │
│  5. Evaluation                                │
│     └── _compute_map() → mAP@0.5             │
│                                               │
│  6. Output gate                               │
│     ├── mAP ≥ threshold → save model.pt       │
│     └── mAP < threshold → return None        │
└───────────────────────────────────────────────┘
```

---

## Component Responsibilities

### `train_model` (Flyte task)
Top-level orchestrator. Handles dataset acquisition, wires all components together, applies the accuracy gate, and produces the output. All side effects (network I/O, file I/O) live here.

### `COCODetectionDataset` (torch Dataset)
Reads a COCO JSON annotation file and the associated image directory. Maps category IDs to contiguous labels (background = 0). Returns `(image_tensor, target_dict)` per sample. Lazy image loading via PIL.

### `ObjectDetector` (pl.LightningModule)
Wraps `fasterrcnn_resnet50_fpn` with ImageNet pretrained weights. Replaces the classification head (`FastRCNNPredictor`) to match the dataset's class count. Uses Adam optimizer at `lr=1e-4`. The Lightning module only handles training; inference is done directly on `detector.model`.

### `_find_annotation_file(dataset_dir, split)`
Annotation discovery heuristic. Tries a priority-ordered list of canonical Roboflow/COCO paths, then falls back to a recursive glob that validates JSON structure (`annotations` + `images` keys). Handles `valid` vs `val` naming variants.

### `_resolve_img_dir(ann_file)`
Returns `ann_file.parent/images` if it exists, otherwise falls back to `ann_file.parent`. Covers both Roboflow layout (`split/images/`) and flat layouts.

### `_compute_map(model, dataloader, iou_threshold, device)`
Custom single-class mAP@IoU implementation. Sorts predictions by confidence, matches against ground-truth boxes using IoU, accumulates TP/FP, computes precision-recall curve via `torch.trapz`, and averages AP across all images. **Does not use torchmetrics or pycocotools** — see Decisions.

### `train_env` (Flyte TaskEnvironment)
Declares the container image (Debian + Python 3.13) and resource requests:
- CPU: 2–4 cores; Memory: 2–12 GiB; Disk: 50 GiB; SHM: 8 GiB; GPU: 1

---

## Data Flow

```
roboflow_url (str)
    │
    ├─ starts with http(s):// ──► requests.get() ──► zip_path
    │                                                    │
    │                                             zipfile.extractall()
    │                                                    │
    └─ local path ────────────────────────────► dataset_dir (Path)
                                                         │
                                        _find_annotation_file(train)
                                        _find_annotation_file(val)
                                                         │
                                              COCODetectionDataset
                                                         │
                                                   DataLoader ×2
                                                         │
                                              ObjectDetector.fit()
                                                         │
                                              _compute_map() → float
                                                         │
                                        ┌────────────────┴──────────────┐
                                        │ mAP ≥ accuracy_request        │ mAP < threshold
                                        ▼                               ▼
                                  torch.save() → model.pt         return None
```

---

## Decisions

### D1: Flyte as task runtime
**Choice:** Flyte `@task` decorator with `flyte run --local`.
**Rationale:** Consistent with other skills in this repo. Provides reproducible containerised execution, declarative resource allocation, and GPU scheduling without requiring the user to manage Docker directly.
**Alternative considered:** Plain Python script — simpler but loses reproducibility, resource limits, and GPU auto-allocation.

### D2: Faster RCNN ResNet-50 FPN as base model
**Choice:** `fasterrcnn_resnet50_fpn` with ImageNet pretrained weights; replace only the classification head.
**Rationale:** Well-established two-stage detector with strong out-of-the-box accuracy on small custom datasets. Transfer learning from ImageNet minimises the epochs needed to reach usable mAP. ResNet-50 FPN provides a good accuracy/speed trade-off.
**Alternative considered:** YOLO-family models — faster inference, but require a separate library and non-COCO annotation conversion; SSD — simpler but lower accuracy on small datasets.

### D3: Custom mAP@0.5 over torchmetrics/pycocotools
**Choice:** Hand-rolled per-image AP computation using `torchvision.ops.box_iou`.
**Rationale:** Avoids adding `torchmetrics` or `pycocotools` as dependencies, keeping the container image small. The implementation is sufficient for the binary pass/fail accuracy gate.
**Trade-off:** Does not compute per-class AP or the full COCO suite (AP@[.5:.95]). Accumulates per-image AP and averages — this is image-level mAP, not the standard category-level COCO mAP. For a threshold gate this is acceptable; for published benchmarks it would need pycocotools.

### D4: Adam optimizer at fixed lr=1e-4, 10 epochs
**Choice:** Adam, lr=1e-4, 10 epochs, batch size 4.
**Rationale:** Conservative defaults that converge reliably on small Roboflow datasets without exhausting the 12 GiB memory limit. No learning rate schedule to keep the implementation simple.
**Trade-off:** May underfit on large or difficult datasets. Users needing higher accuracy should adjust epochs or lr via code modification (not yet exposed as parameters).

### D5: Temp directory for HTTP downloads
**Choice:** `tempfile.TemporaryDirectory()` for download and extraction.
**Rationale:** Avoids leaving dataset artifacts on the worker after the task completes. The only durable output is `model.pt`.
**Trade-off:** If the task is killed mid-run, the temp dir is cleaned up by the OS; no resume capability.

### D6: Validation fallback to train split
**Choice:** If no `valid`/`val` split is found, evaluate on the train split.
**Rationale:** Some Roboflow exports ship without a validation split. Falling back avoids a hard failure and still gives a signal for the accuracy gate.
**Trade-off:** mAP on train data is optimistic; the model may not generalise. Logged explicitly to stdout so the user is aware.

---

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Image-level mAP ≠ COCO category-level mAP | Documented in D3; acceptable for a threshold gate; upgrade to pycocotools if precise benchmarking is needed |
| 10 epochs may be insufficient for large datasets | Users can fork the skill and increase `max_epochs`; exposing it as a parameter is a natural next step |
| No checkpoint/resume on failure | Temp directory approach means all progress is lost on crash; add `ModelCheckpoint` callback if robustness is required |
| Memory pressure on datasets with large images | 12 GiB memory ceiling + batch size 4 handles most Roboflow exports; oversized images may OOM |
| `torch.trapz` deprecated in PyTorch ≥ 2.1 | Replace with `torch.trapezoid` when upgrading PyTorch |
| Annotation discovery heuristic may miss exotic layouts | The fallback `rglob` covers most cases; exotic layouts require manual `--roboflow_url` pointing to an extracted directory |

---

## Migration Plan

This change is documentation-only. No code is modified.

1. Write and merge `design.md` (this document) into `openspec/changes/improve-roboflow-train-skill/`
2. Optionally publish `design.md` alongside `SKILL.md` in `skills/roboflow_train/` for discoverability

Rollback: delete the file. No runtime impact.

---

## Open Questions

- Should `max_epochs`, `lr`, and `batch_size` be exposed as optional task parameters? (follow-up change)
- Should evaluation switch to `torchmetrics.detection.MeanAveragePrecision` for category-level mAP? (follow-up change)
- Should `model.pt` include the full model (not just state dict) for easier loading by downstream consumers?
