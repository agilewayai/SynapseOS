# State

## Artifact Header

- artifact id: `aries-state-synapseos`
- artifact type: `state`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/STATE.md`
- source of truth: `this file`
- upstream links: `MISSION.md`, `TASK_STACK.md`
- downstream links: `JOURNAL.md`, `EVAL.md`, `RISKS.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `before and after substantial work`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `pending`
- audit log id: `pending`

## Current Phase

`Summarize`

## Current Status

- Repo purpose is documented in `AGENTS.md` and model directories
- Aries Harness bootstrap is now the canonical recovery surface
- Request, spec, story, architecture, traceability, and audit artifacts now exist under `.aries_harness/`
- Canonical layer naming is now clarified as `Xuan Master` core, `Archon` enabler, and `Prism` specialist
- The three canonical layers now have dedicated top-level entrypoints: `xuan-master/`, `archon/`, and `prism/`
- The `Xuan Master` catalog and all 27 model directories now live physically under `xuan-master/`
- The `Archon` interview and enabled components now live physically under `archon/`
- Harness artifacts and entry docs now reference the nested `xuan-master/` core layout consistently
- Harness artifacts and entry docs now reference the nested `archon/` enabler layout consistently
- A new initialization-layer artifact family now exists as `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, and `ADR-0004`
- The initialization layer is now implemented under `init/` with the repo-local `synapse-cli` entrypoint
- `synapse-cli` supports `doctor`, `init`, `list-agents`, `install`, and `verify`
- Host adapters exist for `claude-code`, `codex`, `cursor`, `opencode`, `openclaw`, `hermes`, and `generic`
- The generic adapter supports explicit-target dry-run, approved install, manifest output, idempotent copy install, and verification
- Domain package `DOM-002` now captures the initialization and host-installation domain model
- OpenClaw quick-install shaping now exists as `REQ-003`, `SPEC-003`, `STORY-003`, `ARCH-003`, `ADR-0005`, and `docs/OPENCLAW_INSTALL.md`
- OpenClaw chatbox install mode now exists as `install/openclaw-chat-install.md` and is linked from `docs/OPENCLAW_INSTALL.md`
- Hermes chatbox install mode now exists as `install/hermes-chat-install/SKILL.md` and is linked from `docs/HERMES_INSTALL.md`
- The repository now has a GitHub-facing `README.md` and `docs/GETTING_STARTED.md`
- The project license is now Apache-2.0 in `LICENSE` and public docs
- No generated history surface exists yet

## Working Assumptions

- This repository is currently docs-first, with a small number of helper scripts
- Verification is primarily structural unless a task changes executable scripts
- Single-agent operation is the default until the repo needs explicit orchestration

## Next Safe Action

Optionally commit and push the completed `synapse-cli`, OpenClaw, and Hermes install baselines if requested. The next development slice should implement host-native verification for OpenClaw or Hermes.
