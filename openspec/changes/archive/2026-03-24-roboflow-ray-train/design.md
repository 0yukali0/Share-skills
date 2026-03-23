## Context

The project already has `roboflow-train` which uses PyTorch Lightning on a single process. This change adds a parallel skill `roboflow-ray-train` that wraps the Lightning training logic with Ray Train's `TorchTrainer`, enabling distributed CPU training across multiple Ray workers.

Reference: https://docs.ray.io/en/latest/train/getting-started-pytorch-lightning.html

## Goals / Non-Goals

**Goals:**
- Implement `roboflow_ray_train.py` using Ray Train + PyTorch Lightning on CPU
- Accept `roboflow_url` (Roboflow COCO zip URL or local path) and `accuracy_request` as inputs
- Output `model.pt` if mAP@0.5 ≥ `accuracy_request`, else `None`
- Write `skill.md` describing the skill interface

**Non-Goals:**
- GPU support (CPU only for now)
- Modifying the existing `roboflow-train` skill
- Hyperparameter tuning

## Decisions

### 1. Define all classes inside `train_loop_per_worker`

Ray workers serialize the `train_loop_per_worker` function via cloudpickle and execute it in a remote process that has no access to the original script file. Therefore, all classes needed by workers (`COCODetectionDataset`, `ObjectDetector`, `_collate_fn`) must be defined **inside** `train_loop_per_worker` as local definitions so they are captured in the closure.

**Alternative**: Top-level class definitions — rejected because Ray workers cannot import the source file; this would cause `AttributeError` or `ModuleNotFoundError` at runtime.

### 2. Use `TorchTrainer` with `RayTrainReportCallback` and `RayDDPStrategy`

Inside `train_loop_per_worker`, create a `pl.Trainer` configured with:
- `RayDDPStrategy()` — handles distributed data-parallel communication
- `RayTrainReportCallback()` — reports metrics back to the Ray driver
- `accelerator="cpu"`, `devices="auto"`

This is the canonical pattern from the Ray + PyTorch Lightning docs.

### 3. Dataset download on driver, path passed via `config`

The driver downloads and extracts the dataset zip to a temp directory, then passes the extracted path string through `TorchTrainer`'s `train_loop_config`. Workers receive this path from `ray.train.get_context().get_metadata()` or directly from the config dict.

**Alternative**: Each worker downloads independently — rejected, wastes bandwidth and causes race conditions.

### 4. mAP evaluation runs on the driver after training

After `TorchTrainer.fit()` completes, the driver loads the best checkpoint from `result.checkpoint`, reconstructs the model, and runs `_compute_map` locally (single-process, CPU). This function is defined at the top level since it only runs on the driver.

### 5. `ScalingConfig(num_workers=2, use_gpu=False)`

Defaults to 2 CPU workers. Sufficient for local development and small clusters.

## Risks / Trade-offs

- **Shared filesystem** → Workers must be able to read the extracted dataset path. On distributed clusters, a shared mount is required. Mitigation: documented in `skill.md`.
- **Closure size** → Defining all classes inside the worker function increases pickle size slightly. Acceptable trade-off for correctness.
- **mAP evaluation is single-process** → Evaluated on the driver after training. Correct but not parallelized.
