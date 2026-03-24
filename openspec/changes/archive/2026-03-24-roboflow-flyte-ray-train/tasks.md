## 1. Dependencies

- [x] 1.1 Install `flyte` and `flyteplugins-ray` with `source .venv/bin/activate && uv add flyte flyteplugins-ray`
- [x] 1.2 Verify `from flyteplugins.ray import RayJobConfig, WorkerNodeConfig` imports without error

## 2. Rewrite `roboflow_ray_train.py`

- [x] 2.1 Add `flyte.TaskEnvironment` and `RayJobConfig` / `WorkerNodeConfig` imports at the top of the file
- [x] 2.2 Define a `train_env` using `flyte.TaskEnvironment` with required pip packages (torch, torchvision, pytorch-lightning, ray[default], flyteplugins-ray, requests, Pillow)
- [x] 2.3 Configure `RayJobConfig` with 2 CPU worker nodes (`WorkerNodeConfig(group_name="workers", replicas=2)`) and `shutdown_after_job_finishes=True`
- [x] 2.4 Decorate `roboflow_ray_train` function with `@train_env.task` using the `RayJobConfig` as `task_config`
- [x] 2.5 Remove manual `ray.init(ignore_reinit_error=True)` call (Flyte/Ray integration handles initialization)
- [x] 2.6 Keep `train_loop_per_worker` closure pattern intact for correct cloudpickle serialization
- [x] 2.7 Update the `__main__` block (or remove it) — invocation is now via `flyte run`, not `python`

## 3. Update `SKILL.md`

- [x] 3.1 Change the invocation in Steps section to `flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train --roboflow_url <url> --accuracy_request <float>`
- [x] 3.2 Update Example Invocations to use `flyte run --local` syntax
- [x] 3.3 Update Dependencies section to include `flyte` and `flyteplugins-ray`
- [x] 3.4 Remove the "Architecture Notes" section about cloudpickle/closure (or update to reference Flyte Ray integration)

## 4. Verification

- [ ] 4.1 Run `flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train --roboflow_url <url> --accuracy_request 0.6 --output model.pt` and confirm it completes without error (manual test)
- [ ] 4.2 Confirm `model.pt` is saved when mAP@0.5 meets the threshold (manual test)
- [ ] 4.3 Confirm `None` is returned and no file is saved when mAP@0.5 is below the threshold (manual test)
