## 1. Write design.md

- [x] 1.1 Create `design.md` in `openspec/changes/improve-roboflow-train-skill/` with Context section describing the current skill and tech stack
- [x] 1.2 Add Architecture Overview section with ASCII diagram of the six pipeline stages
- [x] 1.3 Add Component Responsibilities section covering all seven components (`train_model`, `COCODetectionDataset`, `ObjectDetector`, `_find_annotation_file`, `_resolve_img_dir`, `_compute_map`, `train_env`)
- [x] 1.4 Add Data Flow section with end-to-end data flow diagram from `roboflow_url` input to `model.pt` / `None` output
- [x] 1.5 Add Decisions section with entries D1–D6 (Flyte runtime, Faster RCNN, custom mAP, Adam/epochs, temp dir, validation fallback), each with rationale and alternatives considered
- [x] 1.6 Add Risks/Trade-offs section as a table with at least five risks and their mitigations
- [x] 1.7 Add Migration Plan section (documentation-only, no code changes)
- [x] 1.8 Add Open Questions section listing follow-up items (hyperparameter exposure, torchmetrics upgrade, full-model save)

## 2. Verify against spec

- [x] 2.1 Confirm `design.md` contains all required sections per spec requirement "Design document exists for roboflow_train skill"
- [x] 2.2 Confirm all six pipeline stages are present in the Architecture Overview per spec requirement "Architecture overview is documented"
- [x] 2.3 Confirm all seven components have a documented responsibility per spec requirement "Component responsibilities are documented"
- [x] 2.4 Confirm each decision entry includes chosen approach, rationale, and at least one alternative per spec requirement "Key design decisions are recorded with rationale"
- [x] 2.5 Confirm at least five risks with mitigations are present per spec requirement "Risks and trade-offs are enumerated"
