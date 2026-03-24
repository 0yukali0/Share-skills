## Why

The existing `roboflow_ray_train` skill runs Ray Train directly via `python`, bypassing Flyte's orchestration layer. By adopting the Flyte Ray integration (`flyteplugins-ray`), the skill gains Kubernetes-native Ray cluster provisioning via KubeRay, Flyte lifecycle management, and a consistent invocation pattern (`flyte run`) matching the `roboflow_train` skill.

## What Changes

- Rewrite `skill_impl/roboflow_ray_train/roboflow_ray_train.py` to use Flyte + Ray integration:
  - Wrap the training task with `RayJobConfig` (worker nodes, head node config)
  - Expose a Flyte task `roboflow_ray_train` callable via `flyte run`
  - Replace manual `ray.init(ignore_reinit_error=True)` call with conditional `ray.init()`
- Update `skills/roboflow_ray_train/SKILL.md` to document the new invocation (`flyte run ... roboflow_ray_train`)
- Add `flyte` and `flyteplugins-ray` dependencies

## Capabilities

### New Capabilities

### Modified Capabilities
- `roboflow-ray-train`: Invocation changes from `python roboflow_ray_train.py` to `flyte run skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train`; Ray cluster is now managed by Flyte/KubeRay via `RayJobConfig`

## Impact

- Modified: `skill_impl/roboflow_ray_train/roboflow_ray_train.py`
- Modified: `skills/roboflow_ray_train/SKILL.md`
- New dependencies: `flyte`, `flyteplugins-ray`
