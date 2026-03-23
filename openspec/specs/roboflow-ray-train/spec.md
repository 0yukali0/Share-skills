### Requirement: Accept Roboflow COCO dataset input
The skill SHALL accept a `roboflow_url` parameter that is either an HTTPS URL to a Roboflow COCO zip file or a local filesystem path to an extracted dataset directory.

#### Scenario: URL input
- **WHEN** `roboflow_url` starts with `http://` or `https://`
- **THEN** the system downloads and extracts the zip before training

#### Scenario: Local path input
- **WHEN** `roboflow_url` is a local path
- **THEN** the system uses that directory directly without downloading

### Requirement: Train using Ray Train and PyTorch Lightning on CPU
The skill SHALL use `ray.train.torch.TorchTrainer` with a PyTorch Lightning `Trainer` configured for CPU-only distributed training. All dataset and model classes SHALL be defined inside `train_loop_per_worker` to ensure correct serialization by Ray workers.

#### Scenario: Distributed training launches
- **WHEN** `train_model` is called
- **THEN** Ray initializes CPU workers and runs `train_loop_per_worker` on each

#### Scenario: Worker receives dataset path
- **WHEN** a Ray worker starts
- **THEN** it reads the dataset path from `train_loop_config` and loads the COCO dataset locally

### Requirement: Output model.pt when accuracy threshold is met
The skill SHALL save the trained model weights to `model.pt` and return its path if the evaluated mAP@0.5 is greater than or equal to `accuracy_request`. Otherwise it SHALL return `None`.

#### Scenario: Accuracy met
- **WHEN** mAP@0.5 ≥ `accuracy_request`
- **THEN** model weights are saved to `model.pt` and the path is returned

#### Scenario: Accuracy not met
- **WHEN** mAP@0.5 < `accuracy_request`
- **THEN** the function returns `None` and no file is saved

### Requirement: skill.md documents the skill interface
The skill SHALL include a `skills/roboflow_ray_train/skill.md` file that documents the inputs, outputs, dependencies, and shared-filesystem requirement.

#### Scenario: skill.md exists
- **WHEN** the skill is deployed
- **THEN** `skills/roboflow_ray_train/skill.md` exists and lists `roboflow_url` and `accuracy_request` as inputs and `model.pt` path as output
