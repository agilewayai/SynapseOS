# Risks

## Artifact Header

- artifact id: `aries-risks-synapseos`
- artifact type: `risk_register`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/RISKS.md`
- source of truth: `this file`
- upstream links: `MISSION.md`, `STATE.md`
- downstream links: `TASK_STACK.md`, `EVAL.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `when new work introduces a meaningful operating risk`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## Active Risks

### Identity And Layer Naming Drift

The local folder name `Cogna`, the repository name `SynapseOS`, and the evolving product framing can drift if the external identity is not explicit. Separately, the layer names `Xuan Master`, `Archon`, and `Prism` can drift from the physical directory layout if the mapping is not documented.

Mitigation: keep the public identity explicit in repo-facing docs and keep the architecture mapping explicit in the request/spec/architecture artifacts.

### Verification Thinness

Most repo content is Markdown, and helper scripts do not yet have an explicit verification routine.

Mitigation: define a lightweight validation checklist before broader script changes.

### Harness Staleness

A harness is only useful if the root docs stay current.

Mitigation: update `STATE.md`, `TASK_STACK.md`, and `EVAL.md` as part of every substantial repo change.
