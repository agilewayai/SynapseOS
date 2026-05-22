# Evaluation

## Artifact Header

- artifact id: `aries-eval-synapseos`
- artifact type: `eval_report`
- status: `active`
- owner: `Arthur`
- canonical path: `.aries_harness/EVAL.md`
- source of truth: `this file`
- upstream links: `MISSION.md`, `TASK_STACK.md`, `STATE.md`
- downstream links: `JOURNAL.md`
- verification state: `initialized`
- last reviewed: `2026-05-21`
- next review or refresh trigger: `after any substantial repo change`
- run id: `pending`
- task id or slice id: `bootstrap`
- checkpoint id: `n/a`
- approval request id: `n/a`
- trace id: `pending`
- eval report id: `aries-eval-synapseos`
- audit log id: `pending`

## Acceptance Checks

- `.aries_harness/` exists at the project root
- Canonical root docs exist and are readable
- Managed directories exist with tracked placeholders
- Hot memory and cold recall surfaces are explicitly separated
- The files describe this specific repository rather than generic template text
- Request-to-architecture artifacts exist for the current repository baseline
- The canonical layers have dedicated loadable skill entrypoints
- The `Xuan Master` catalog and 27-model kernel are nested under `xuan-master/` and referenced consistently
- The `Archon` interview and enabled surfaces are nested under `archon/` and referenced consistently
- The initialization-layer request/spec/story/architecture/ADR package exists and is linked to the `synapse-cli` implementation
- `README.md`, `docs/GETTING_STARTED.md`, and Apache-2.0 `LICENSE` exist for public onboarding
- `synapse-cli` exists as a repo-local executable with `doctor`, `init`, `list-agents`, `install`, and `verify`
- `init/` exists as the initialization layer with a loadable `SKILL.md`
- Host adapters exist for `claude-code`, `codex`, `cursor`, `opencode`, `gemini`, `antigravity`, `antigravity-cli`, `openclaw`, `hermes`, and `generic`
- Grouped host dry-run, approved install, update-mode refresh, conflict blocking, manifest output, and verification are covered by tests
- `DOM-002` exists as the initialization and host-installation domain package
- `REQ-003`, `SPEC-003`, `STORY-003`, `ARCH-003`, and `ADR-0005` exist for OpenClaw quick-install shaping
- `docs/OPENCLAW_INSTALL.md` exists and documents chatbox install mode, safe local install, shell one-link target UX, OpenClaw-native verification, update, and troubleshooting
- `install/openclaw-chat-install.md` exists as the paste-link OpenClaw chatbox installation prompt
- `REQ-004`, `SPEC-004`, `STORY-004`, `ARCH-004`, and `ADR-0006` exist for Hermes chatbox installation
- `docs/HERMES_INSTALL.md` exists and documents Hermes direct-SKILL chatbox install, safe local install, Hermes-native verification, update, and troubleshooting
- `install/hermes-chat-install/SKILL.md` exists as the Hermes direct-link installer skill

## Current Result

- Acceptance status: `pass`
- Verification method: `unit tests, CLI smoke checks, generic install/verify smoke check, artifact ID search, OpenClaw docs reference check, license scan, markdown diff check, and file-content review`
- Latest checks: `python3 -m unittest tests/test_synapse_cli.py`; `python3 -m py_compile init/synapse_cli/adapters.py init/synapse_cli/installer.py init/synapse_cli/main.py`; `./synapse-cli list-agents --json`; default adapter dry-run smoke checks; Gemini and Antigravity dry-run smoke checks
- Remaining gaps: `no generated history yet; optimization docs still have some Hermes-era examples; named host adapters need host-native smoke hardening beyond baseline target resolution; optional OpenClaw shell one-link script is specified but not implemented`
