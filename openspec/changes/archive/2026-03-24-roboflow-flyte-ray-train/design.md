## Context

The `roboflow_ray_train` skill currently runs distributed training by calling `python roboflow_ray_train.py` directly. This change adopts the `flyteplugins-ray` integration so the task is submitted via `flyte run`, matching the `roboflow_train` skill pattern.

## Goals / Non-Goals

**Goals:**
- Submit via `flyte run skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train`
- Use `RayJobConfig` from `flyteplugins.ray` to declare the Ray cluster topology
- Preserve existing training logic (Faster RCNN, mAP@0.5, dataset handling)
- Install `flyte` and `flyteplugins-ray` via `uv add`

**Non-Goals:**
- GPU support, autoscaling, changes to `roboflow_train` skill

## Decisions

### Task decoration
Use `@train_env.task` with `flyte.TaskEnvironment` (same pattern as `roboflow_train.py`). Attach `plugin_config = RayJobConfig(...)` to the task object after decoration for Kubernetes/KubeRay deployment serialization.

### Ray initialization
Call `ray.init()` conditionally (`if not ray.is_initialized()`) in the function body for local mode. `RayFunctionTask.pre()` handles this automatically in cluster mode.

### Dependency installation
`source .venv/bin/activate && uv add flyte flyteplugins-ray`

## Risks / Trade-offs

- **KubeRay not available locally** → `flyte run --local` uses local Ray cluster; functionally equivalent.
- **cloudpickle closure size** → already validated in current implementation; no change.

## Migration Plan

1. `source .venv/bin/activate && uv add flyte flyteplugins-ray` ✓
2. Rewrite `roboflow_ray_train.py` with `@train_env.task` + `RayJobConfig` ✓
3. Update `SKILL.md` invocation
4. Test with `flyte run --local`
