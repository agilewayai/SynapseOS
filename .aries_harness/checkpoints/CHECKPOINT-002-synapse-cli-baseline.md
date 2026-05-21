# Checkpoint: Synapse CLI Baseline

## Artifact Header

- Artifact ID: `CHECKPOINT-002`
- Artifact type: `longrun-checkpoint`
- Status: `active`
- Owner: `Arthur`
- Canonical path: `.aries_harness/checkpoints/CHECKPOINT-002-synapse-cli-baseline.md`
- Source of truth: `this file`
- Created: `2026-05-21`
- Last reviewed: `2026-05-21`
- Upstream links: `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, `ADR-0004`, `DOM-002`
- Downstream links: `TRACE-001`, `AUDIT-001`, `EVAL.md`, `STATE.md`

## Runtime IDs

- Run ID: `RUN-2026-05-21-synapse-cli-baseline`
- Task ID / Slice ID: `STORY-002B`, `STORY-002C`, `STORY-002D`, `STORY-002E`, `STORY-002F`
- Checkpoint ID: `CHECKPOINT-002`
- Trace ID: `TRACE-001`
- Eval Report ID: `aries-eval-synapseos`
- Audit Log ID: `AUDIT-001`
- Approval Request ID: `n/a`

## Objective

Complete the SynapseOS initialization layer baseline by implementing a local `synapse-cli` with prerequisite diagnosis, repo-local initialization metadata, adapter listing, install planning/application, generic host installation, manifest evidence, and verification.

## Completed Work

- Added `init/` as the initialization layer with `init/SKILL.md`.
- Added the `init/synapse_cli/` package with parser, adapters, prerequisite checks, installer, and verification modules.
- Added root executable `synapse-cli`.
- Added adapters for `claude-code`, `codex`, `cursor`, `opencode`, `openclaw`, `hermes`, and `generic`.
- Added generic explicit-target dry-run, approved install, idempotent copy install, manifest writing, and verification.
- Added install payload coverage for `synapse-cli`, docs, `xuan-master`, `archon`, `prism`, `optimization`, and `init`.
- Added `tests/test_synapse_cli.py`.
- Added `.gitignore` for Python caches and repo-local generated output.
- Added `DOM-002` domain analysis pack with bounded contexts, domain language, invariants, UML, and source traceability.
- Refreshed README, getting-started docs, AGENTS, and Aries Harness state, eval, task stack, memory, trace, audit, register, story, spec, architecture, ADR, and risk surfaces.

## In Progress

- No active implementation work remains in this slice.

## Next Step

If resuming development, start with named host adapter hardening or uninstall/rollback planning. If preparing a release commit, review and commit the current working tree after checking status:

```sh
git status --short --branch
```

## Blockers / Risks

- No active blocker.
- Named adapters currently provide baseline detection, target resolution, and file verification; host-native smoke checks remain future hardening.
- Automatic prerequisite installation is intentionally deferred. `doctor` reports structured prerequisite state and remediation hints, but does not install system tools.
- `synapse-cli` is repo-local; global packaging is deferred.

## Verification Performed

- `python3 -m unittest discover -s tests` passed.
- `./synapse-cli --help` passed.
- `./synapse-cli doctor --json` passed and includes structured missing/installable prerequisite fields.
- `./synapse-cli list-agents --json` passed.
- Generic dry-run/install/verify smoke check passed.
- Generic verification now confirms the installed root includes `synapse-cli`.
- `git diff --check` passed.

## Verification Still Needed

- None for the local implementation slice.

## Context State

- Context operation: `continue`
- Hot files: `synapse-cli`, `init/synapse_cli/`, `tests/test_synapse_cli.py`, `.aries_harness/references/domain/DOM-002-synapseos-initialization-domain.md`, `.aries_harness/STATE.md`, `.aries_harness/TASK_STACK.md`, `.aries_harness/EVAL.md`
- Resume strategy: start from this checkpoint, inspect `git status --short --branch`, then choose the next slice from `.aries_harness/TASK_STACK.md`.
