# Value Traceability Matrix

## Artifact header

- Artifact ID: `TRACE-001`
- Artifact type: `value-traceability-matrix`
- Status: `active`
- Owner: `Arthur`
- Canonical path: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`
- Source of truth: `this file`
- Upstream links: `REQ-001`, `SPEC-001`, `STORY-001`, `ARCH-001`, `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, `DOM-002`, `REQ-003`, `SPEC-003`, `STORY-003`, `ARCH-003`, `REQ-004`, `SPEC-004`, `STORY-004`, `ARCH-004`
- Downstream links: `future runs`, `future history projections`
- Verification state: `initialized`
- Last reviewed: `2026-05-21`
- Next review / refresh trigger: `update whenever a linked artifact or delivery slice meaningfully changes`

## Runtime links

- Run ID: `pending`
- Task ID / Slice ID: `distill-current-project-baseline`
- Checkpoint ID: `n/a`
- Approval Request ID: `n/a`
- Trace ID: `TRACE-001`
- Eval Report ID: `pending`
- Audit Log ID: `AUDIT-001`

| Request | Spec | Story slice | Domain artifact | Architecture artifact | ADR | Code or module | Test or verification | Runtime evidence | Release evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `REQ-001` | `SPEC-001` | `STORY-001A` | `pending` | `ARCH-001` | `ADR-0002`; `ADR-0003` | `AGENTS.md`; `xuan-master/SKILL.md`; `xuan-master/00-entry/SKILL.md`; `archon/enabled/SKILL.md`; `archon/interview/SKILL.md`; `optimization/SKILL.md`; `.aries_harness/` | `file inspection of repo surfaces and artifact cross-links` | `.aries_harness/EVAL.md`; `AUDIT-001` | `n/a` |
| `REQ-001` | `SPEC-001` | `STORY-001B` | `pending` | `ARCH-001` | `ADR-0003` | `README.md`; `docs/GETTING_STARTED.md`; `LICENSE`; `AGENTS.md`; `xuan-master/SKILL.md`; `xuan-master/00-entry/SKILL.md`; `archon/enabled/SKILL.md`; `archon/interview/SKILL.md` | `documentation diff, license scan, and file inspection for public entrypoint and Xuan Master / Archon / Prism alignment` | `AUDIT-001` | `pending` |
| `REQ-001` | `SPEC-001` | `STORY-001C` | `pending` | `ARCH-001` | `ADR-0002`; `ADR-0003` | `archon/enabled/scripts/model-selector.py`; `optimization/scripts/full_audit.py`; `optimization/scripts/recover_from_session.py` | `pending script-contract review and local checks` | `pending` | `pending` |
| `REQ-001` | `SPEC-001` | `STORY-001D` | `pending` | `ARCH-001` | `ADR-0003` | `prism/SKILL.md`; `prism/domains/README.md`; `AGENTS.md`; `xuan-master/00-entry/SKILL.md` | `file inspection of the new Prism layer surface and updated architecture docs` | `REVIEW-001`; `AUDIT-001` | `n/a` |
| `REQ-002` | `SPEC-002` | `STORY-002A` | `DOM-002` | `ARCH-002` | `ADR-0004` | `.aries_harness/references/requests/REQ-002-synapseos-initialization-layer.md`; `.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md`; `.aries_harness/references/stories/STORY-002-initialization-layer-pack.md`; `.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md` | `file inspection and artifact ID search` | `AUDIT-001` | `n/a` |
| `REQ-002` | `SPEC-002` | `STORY-002B` | `DOM-002` | `ARCH-002` | `ADR-0004` | `synapse-cli`; `init/SKILL.md`; `init/synapse_cli/main.py`; `init/synapse_cli/__init__.py` | `./synapse-cli --help`; `python3 -m unittest discover -s tests` | `AUDIT-001`; `CHECKPOINT-002` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002C` | `DOM-002` | `ARCH-002` | `ADR-0004` | `init/synapse_cli/prerequisites.py`; `init/synapse_cli/main.py` | `./synapse-cli doctor --json`; `tests/test_synapse_cli.py` | `AUDIT-001`; `CHECKPOINT-002` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002D` | `DOM-002` | `ARCH-002` | `ADR-0004` | `init/synapse_cli/adapters.py` | `./synapse-cli list-agents --json`; `tests/test_synapse_cli.py` | `AUDIT-001`; `CHECKPOINT-002` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002E` | `DOM-002` | `ARCH-002` | `ADR-0004` | `init/synapse_cli/installer.py`; `init/synapse_cli/adapters.py` | `adapter matrix dry-run/install/update smoke check`; `tests/test_synapse_cli.py` | `AUDIT-001`; `CHECKPOINT-002` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002F` | `DOM-002` | `ARCH-002` | `ADR-0004` | `init/synapse_cli/installer.py`; `synapse-cli` | `./synapse-cli verify --agent generic --target <tmp> --json`; `tests/test_synapse_cli.py` | `AUDIT-001`; `CHECKPOINT-002` | `pending` |
| `REQ-003` | `SPEC-003` | `STORY-003A` | `n/a` | `ARCH-003` | `ADR-0005` | `docs/OPENCLAW_INSTALL.md`; `.aries_harness/references/requests/REQ-003-openclaw-quick-install.md`; `.aries_harness/references/specs/SPEC-003-openclaw-quick-install.md`; `.aries_harness/references/stories/STORY-003-openclaw-quick-install.md`; `.aries_harness/decisions/architecture/ARCH-003-openclaw-quick-install.md` | `file inspection, artifact ID search, and OpenClaw docs reference check` | `AUDIT-001` | `pending` |
| `REQ-003` | `SPEC-003` | `STORY-003B` | `n/a` | `ARCH-003` | `ADR-0005` | `install/openclaw-chat-install.md`; `docs/OPENCLAW_INSTALL.md` | `file inspection, prompt link scan, and openclaw dry-run plan check` | `AUDIT-001` | `pending` |
| `REQ-003` | `SPEC-003` | `STORY-003C` | `DOM-002 refresh likely` | `ARCH-003` | `ADR-0005` | `future OpenClaw-native verification in init/synapse_cli` | `future openclaw skills check --json evidence` | `pending` | `pending` |
| `REQ-003` | `SPEC-003` | `STORY-003F` | `DOM-002 refresh if manifest changes` | `ARCH-003` | `ADR-0005` | `future install/openclaw.sh shell one-link installer` | `future dry-run, temp-target install, synapse verify, and OpenClaw check` | `pending` | `pending` |
| `REQ-004` | `SPEC-004` | `STORY-004A` | `n/a` | `ARCH-004` | `ADR-0006` | `install/hermes-chat-install/SKILL.md`; `docs/HERMES_INSTALL.md`; `.aries_harness/references/requests/REQ-004-hermes-chat-install.md`; `.aries_harness/references/specs/SPEC-004-hermes-chat-install.md`; `.aries_harness/references/stories/STORY-004-hermes-chat-install.md`; `.aries_harness/decisions/architecture/ARCH-004-hermes-chat-install.md` | `file inspection, artifact ID search, hermes skills install --help, and hermes dry-run plan check` | `AUDIT-001` | `pending` |
| `REQ-004` | `SPEC-004` | `STORY-004B` | `DOM-002 refresh likely` | `ARCH-004` | `ADR-0006` | `future Hermes-native verification in init/synapse_cli` | `future hermes skills list/check evidence` | `pending` | `pending` |

## Tracking Notes

- Stale row: `none`
- Missing link: `host-native smoke evidence is pending for named adapters`
- Audit follow-up: `refresh this matrix in the same pass as naming alignment, script hardening, initialization-layer hardening, or future domain extraction`
