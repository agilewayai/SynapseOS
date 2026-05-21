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

Most repo content is Markdown, and helper scripts beyond the new `synapse-cli` tests do not yet have an explicit verification routine.

Mitigation: define a lightweight validation checklist before broader script changes.

### Host Adapter Drift

The named agent hosts can change command names, configuration paths, or skill loading conventions outside this repository's control.

Mitigation: keep adapter target resolution isolated in `init/synapse_cli/adapters.py`, require explicit overrides, and add host-native smoke checks only where the host exposes a stable local interface.

### Remote Install Prompt Trust

The OpenClaw quick-install target intentionally reduces friction, but remote prompts and shell installers can reduce inspectability if they are published without safety constraints.

Mitigation: keep `synapse-cli install --agent openclaw` as the safe local baseline, require dry-run and target display in the chatbox prompt and any shell one-link script, and document the local review path next to the quick command.

### Hermes Skill Reload Drift

Hermes may install files successfully while the current session does not immediately show newly added skills.

Mitigation: verify payload integrity with `synapse-cli verify --agent hermes`, verify host visibility with `hermes skills list` and `hermes skills check`, and document that a new Hermes session may be required.

### Harness Staleness

A harness is only useful if the root docs stay current.

Mitigation: update `STATE.md`, `TASK_STACK.md`, and `EVAL.md` as part of every substantial repo change.
