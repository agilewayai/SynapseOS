# Task Stack

## Artifact Header

- artifact id: `aries-task-stack-synapseos`
- artifact type: `task_stack`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/TASK_STACK.md`
- source of truth: `this file`
- upstream links: `MISSION.md`, `STATE.md`
- downstream links: `JOURNAL.md`, `EVAL.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `when a task starts, completes, or is reprioritized`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## Active

- No active slice is locked after the `xuan-master` and `archon` structural refactors; pick the next item from `Ready Next`

## Ready Next

- Implement `STORY-002B`: create the first `synapse-cli` skeleton with help, command parsing, `doctor`, `list-agents`, and `--json` shape
- Implement `STORY-002C`: add read-only prerequisite runtime diagnosis and remediation hints
- Decide and document the public product identity relative to the internal layer names `Xuan Master`, `Archon`, and `Prism`
- Define lightweight verification rules for docs and helper scripts
- Run a focused cleanup on `optimization/` to replace the remaining Hermes-era environment assumptions with repo-local guidance

## Later

- Generate a first `history/` projection once the repo has more tracked activity
- Add durable memory cards when repeated decisions or lessons emerge
- Expand the decision log into `decisions/` if architectural tradeoffs increase

## Done

- Initialized Git, linked `origin`, and pushed `main`
- Bootstrapped `.aries_harness/` on `2026-05-21`
- Distilled the current project into request-to-architecture artifacts on `2026-05-21`
- Added dedicated `xuan-master/`, `archon/`, and `prism/` layer entrypoints and refreshed the related skill definitions on `2026-05-21`
- Moved the `Xuan Master` catalog and 27-model kernel under `xuan-master/` and refreshed the linked architecture artifacts on `2026-05-21`
- Moved the `Archon` interview and enabled components under `archon/` and refreshed the linked architecture artifacts on `2026-05-21`
- Added the `REQ-002` / `SPEC-002` / `STORY-002` / `ARCH-002` / `ADR-0004` initialization-layer specification package on `2026-05-21`
- Added the public `README.md`, `docs/GETTING_STARTED.md`, and Apache-2.0 `LICENSE` baseline on `2026-05-21`
