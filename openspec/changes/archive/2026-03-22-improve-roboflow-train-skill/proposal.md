## Why

The `roboflow_train` skill lacks a formal design document, making it difficult for contributors to understand its architecture, extension points, and trade-offs. A design document will serve as the authoritative reference for anyone looking to maintain, debug, or extend the skill.

## What Changes

- Add `design.md` that documents the current architecture, data flow, component responsibilities, and key design decisions of the `roboflow_train` skill
- Document the Flyte task environment configuration and resource allocation rationale
- Document the dataset resolution strategy (URL vs. local path, annotation file discovery)
- Document the training pipeline (Faster RCNN + PyTorch Lightning) and evaluation approach (custom mAP@0.5)

## Capabilities

### New Capabilities

- `roboflow-train-design`: Formal design documentation covering architecture, data flow, components, and design decisions for the roboflow_train skill

### Modified Capabilities

<!-- No existing spec-level requirements are changing — this is documentation only -->

## Impact

- `skills/roboflow_train/SKILL.md` — may receive cross-reference links to design doc
- `openspec/specs/roboflow-train-design/spec.md` — new spec capturing documented requirements
- No code changes; no breaking changes
