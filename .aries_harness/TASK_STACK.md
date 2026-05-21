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

- No active implementation slice is locked after the `synapse-cli` baseline completion

## Ready Next

- Implement `STORY-003C`: add OpenClaw-native verification evidence to `synapse-cli verify --agent openclaw`
- Implement `STORY-003F`: add the optional reviewed shell one-link OpenClaw installer script with dry-run, target override, conflict checks, verification, and learning prompt
- Implement `STORY-004B`: add Hermes-native verification evidence to `synapse-cli verify --agent hermes`
- Evaluate `STORY-004C`: Hermes registry/native package distribution after the direct-SKILL installer stabilizes
- Harden named host adapters with host-native smoke checks where available
- Add uninstall or rollback planning if operator workflow needs a safe removal path
- Package `synapse-cli` for global invocation after the repo-local baseline is stable
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
- Implemented the `synapse-cli` baseline with prerequisite diagnosis, initialization metadata, adapter listing, dry-run/install/verify flows, generic host installation, tests, and `DOM-002` domain analysis on `2026-05-21`
- Added the OpenClaw quick-install spec package and detailed `docs/OPENCLAW_INSTALL.md` guide on `2026-05-21`
- Added the OpenClaw chatbox paste-link install prompt at `install/openclaw-chat-install.md` on `2026-05-21`
- Added the Hermes direct-SKILL chatbox installer at `install/hermes-chat-install/SKILL.md` and detailed `docs/HERMES_INSTALL.md` guide on `2026-05-21`
