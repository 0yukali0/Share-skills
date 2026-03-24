---
name: roboflow_ray_train
description: Download a Roboflow COCO dataset and train a Faster RCNN object detection model using Flyte + Ray Train + PyTorch Lightning on CPU, returning model.pt if accuracy meets the requirement.
license: Apache License 2.0
metadata:
  author: yuteng
  version: "2.0"
---

Download a Roboflow COCO dataset, train a Faster RCNN object detection model using Flyte + Ray Train + PyTorch Lightning (CPU), evaluate mAP@0.5, and return `model.pt` if the accuracy requirement is met.

## When to Use

Use this skill when the user wants to:
- Train an object detection model on a Roboflow dataset using distributed CPU training
- Fine-tune Faster RCNN on a custom COCO-format dataset with Flyte + Ray Train
- Automate training and accuracy validation in one step

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--roboflow_url` | `str` | Yes | Direct download URL to a Roboflow COCO dataset zip, or a local path to an extracted dataset directory |
| `--accuracy_request` | `float` | Yes | Minimum mAP@0.5 threshold (e.g. `0.5` = 50%). The model is only saved if this is met |
| `--output` | `str` | No | Output path for model.pt (default: `model.pt`) |

## Output

- `model.pt` — saved to the current directory if `mAP@0.5 >= accuracy_request`
- `None` — returned if the accuracy requirement is not satisfied

## Steps

1. Execute:
   ```
   flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train \
       --roboflow_url <url_or_path> \
       --accuracy_request <float> \
       --output model.pt
   ```

## What It Does

1. **Downloads** the dataset zip from `roboflow_url` (or uses a local path)
2. **Detects** `train` and `valid`/`val` annotation files in standard Roboflow COCO layout
3. **Launches** Ray Train with 2 CPU workers using `TorchTrainer` + `RayDDPStrategy` (cluster provisioned via `RayJobConfig` on Kubernetes, or local Ray in `--local` mode)
4. **Trains** Faster RCNN (ResNet-50 FPN backbone, ImageNet pretrained) for 10 epochs with Adam optimizer
5. **Evaluates** mAP@0.5 on the validation split (falls back to train split if no validation split exists)
6. **Saves** `model.pt` (state dict) and returns the path if `mAP@0.5 >= accuracy_request`, otherwise returns `None`

## Expected Dataset Layout

Roboflow COCO exports typically follow this structure:

```
dataset/
  train/
    images/
      img1.jpg
      ...
    _annotations.coco.json
  valid/
    images/
      ...
    _annotations.coco.json
```

Other common layouts (flat annotations folder, `val` instead of `valid`, etc.) are also detected automatically.

## Dependencies

- `flyte` (already in pyproject.toml)
- `flyteplugins-ray` (already in pyproject.toml)
- `ray[all]` (already in pyproject.toml)
- `torch`
- `torchvision`
- `pytorch-lightning`
- `requests`
- `Pillow`

## Example Invocations

**Train with a remote Roboflow export URL:**
```
flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train \
    --roboflow_url "https://app.roboflow.com/ds/XXXXXXXX?key=YOUR_API_KEY" \
    --accuracy_request 0.5
```

**Train from a local extracted dataset:**
```
flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train \
    --roboflow_url "/data/my_dataset" \
    --accuracy_request 0.6 \
    --output model.pt
```

## Example Output

```
Downloading dataset from https://...
Train annotations: /tmp/.../dataset/train/_annotations.coco.json
Val annotations:   /tmp/.../dataset/valid/_annotations.coco.json
(Ray) Starting 2 CPU workers...
Epoch 10/10: train_loss=0.312 ...
Evaluating model ...
mAP@0.5: 0.5831  (required: 0.5000)
Model saved to model.pt
```

Or if accuracy is not met:

```
mAP@0.5: 0.3214  (required: 0.5000)
Accuracy 0.3214 is below required 0.5000. Returning None.
```

## Notes

- CPU-only training (no GPU required)
- Uses 2 Ray workers by default (`ScalingConfig(num_workers=2, use_gpu=False)`)
- Accuracy is measured as **mAP@0.5** (mean Average Precision at IoU threshold 0.5)
- The model head is replaced to match the number of classes in the dataset; the backbone uses ImageNet pretrained weights
- `accuracy_request` should be between `0.0` and `1.0`
- On Kubernetes with Flyte, `RayJobConfig` provisions an ephemeral KubeRay cluster per execution and tears it down automatically

## Shared Filesystem Requirement

When running on a **distributed Ray cluster** (multiple machines), all workers must be able to read the extracted dataset directory. Use a shared network mount (NFS, EFS, etc.) or a distributed object store. For local/single-machine Ray, this is not an issue.
