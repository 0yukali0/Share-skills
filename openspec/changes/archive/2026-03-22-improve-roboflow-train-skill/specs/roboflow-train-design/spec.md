## ADDED Requirements

### Requirement: Design document exists for roboflow_train skill
The project SHALL include a `design.md` document that covers the architecture, data flow, component responsibilities, and key design decisions for the `roboflow_train` skill.

#### Scenario: Design document is present
- **WHEN** a contributor navigates to the change directory
- **THEN** `design.md` SHALL exist and contain sections for Context, Architecture Overview, Component Responsibilities, Data Flow, Decisions, Risks/Trade-offs, Migration Plan, and Open Questions

### Requirement: Architecture overview is documented
The design document SHALL describe the high-level architecture of the `train_model` Flyte task, including its major stages: dataset acquisition, annotation discovery, dataset construction, training, evaluation, and output gate.

#### Scenario: All pipeline stages documented
- **WHEN** a contributor reads the Architecture Overview section
- **THEN** each of the six pipeline stages (acquire, discover, construct, train, evaluate, gate) SHALL be present with a brief description

### Requirement: Component responsibilities are documented
The design document SHALL describe the responsibilities of each major component: `train_model`, `COCODetectionDataset`, `ObjectDetector`, `_find_annotation_file`, `_resolve_img_dir`, `_compute_map`, and `train_env`.

#### Scenario: Each component has a documented responsibility
- **WHEN** a contributor reads the Component Responsibilities section
- **THEN** each component SHALL have at least one sentence describing its single responsibility

### Requirement: Key design decisions are recorded with rationale
The design document SHALL record at least the following design decisions with a rationale and alternatives considered: runtime choice (Flyte), model selection (Faster RCNN), evaluation metric implementation (custom mAP vs. torchmetrics), optimiser/epoch defaults, temp directory strategy, and validation split fallback.

#### Scenario: Each decision includes alternatives considered
- **WHEN** a contributor reads the Decisions section
- **THEN** each decision entry SHALL include the chosen approach, the rationale, and at least one alternative that was considered and rejected

### Requirement: Risks and trade-offs are enumerated
The design document SHALL enumerate known risks and trade-offs with a corresponding mitigation or note for each.

#### Scenario: Risks are tabulated
- **WHEN** a contributor reads the Risks/Trade-offs section
- **THEN** at least five risks SHALL be listed, each with a mitigation strategy
