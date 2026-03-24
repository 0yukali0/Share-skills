## MODIFIED Requirements

### Requirement: Train using Ray Train and PyTorch Lightning on CPU
The skill SHALL use Flyte's Ray integration (`RayJobConfig` from `flyteplugins.ray`) to declare a Ray cluster with 2 CPU worker nodes. The training logic SHALL use `ray.train.torch.TorchTrainer` with a PyTorch Lightning `Trainer` configured for CPU-only distributed training. All dataset and model classes SHALL be defined inside `train_loop_per_worker` to ensure correct serialization by Ray workers.

#### Scenario: Distributed training launches via Flyte
- **WHEN** `flyte run skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train` is called
- **THEN** Flyte provisions a Ray cluster using `RayJobConfig` and runs the training job

#### Scenario: Worker receives dataset path
- **WHEN** a Ray worker starts
- **THEN** it reads the dataset path from `train_loop_config` and loads the COCO dataset locally

## MODIFIED Requirements

### Requirement: skill.md documents the skill interface
The skill SHALL include a `skills/roboflow_ray_train/SKILL.md` file that documents the inputs, outputs, dependencies, and invocation via `flyte run`.

#### Scenario: SKILL.md documents flyte run invocation
- **WHEN** the skill is deployed
- **THEN** `skills/roboflow_ray_train/SKILL.md` documents invocation as `flyte run --local skill_impl/roboflow_ray_train/roboflow_ray_train.py roboflow_ray_train --roboflow_url <url> --accuracy_request <float> --output <path>`

## ADDED Requirements

### Requirement: Flyte Ray integration dependencies installed
The project SHALL have `flyte` and `flyteplugins-ray` installed via `uv add flyte flyteplugins-ray` in the virtual environment.

#### Scenario: Dependencies available
- **WHEN** the skill is run
- **THEN** `import flyte` and `from flyteplugins.ray import RayJobConfig` succeed without error
