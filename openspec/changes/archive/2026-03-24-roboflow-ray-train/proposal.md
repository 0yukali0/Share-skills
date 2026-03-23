## Why

The existing `roboflow-train` skill trains on a single machine. Using Ray Train with PyTorch Lightning enables distributed training across multiple CPU workers, improving scalability for large Roboflow COCO datasets.

## What Changes

- Add `skill_impl/roboflow_ray_train/roboflow_ray_train.py` — distributed training implementation using Ray Train + PyTorch Lightning on CPU
- Add `skills/roboflow_ray_train/skill.md` — skill definition with inputs, outputs, and usage
- The training loop wraps the existing Faster RCNN / Lightning module in a `RayTrainReportCallback` and launches via `TorchTrainer`
- Output is `model.pt` (state dict)

## Capabilities

### New Capabilities

- `roboflow-ray-train`: Train a COCO object detection model on a Roboflow dataset using Ray Train + PyTorch Lightning (CPU), outputting `model.pt`

### Modified Capabilities

## Impact

- New files only; no existing code modified
- New dependencies: `ray[train]`, `torch`, `torchvision`, `pytorch-lightning`
- Runs on CPU workers in a Ray cluster or local Ray runtime
