# Value Traceability Matrix

## Artifact header

- Artifact ID: `TRACE-001`
- Artifact type: `value-traceability-matrix`
- Status: `active`
- Owner: `Arthur`
- Canonical path: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`
- Source of truth: `this file`
- Upstream links: `REQ-001`, `SPEC-001`, `STORY-001`, `ARCH-001`, `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`
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
| `REQ-002` | `SPEC-002` | `STORY-002A` | `pending` | `ARCH-002` | `ADR-0004` | `.aries_harness/references/requests/REQ-002-synapseos-initialization-layer.md`; `.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md`; `.aries_harness/references/stories/STORY-002-initialization-layer-pack.md`; `.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md` | `file inspection and artifact ID search` | `AUDIT-001` | `n/a` |
| `REQ-002` | `SPEC-002` | `STORY-002B` | `pending` | `ARCH-002` | `ADR-0004` | `future synapse-cli entrypoint`; `future initialization layer surface` | `future CLI parser smoke checks` | `pending` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002C` | `pending` | `ARCH-002` | `ADR-0004` | `future prerequisite checker`; `future synapse-cli doctor` | `future doctor output checks` | `pending` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002D` | `pending` | `ARCH-002` | `ADR-0004` | `future agent host adapters` | `future adapter dry-run and verification checks` | `pending` | `pending` |
| `REQ-002` | `SPEC-002` | `STORY-002E` | `pending` | `ARCH-002` | `ADR-0004` | `future generic host adapter` | `future explicit-target install verification` | `pending` | `pending` |

## Tracking Notes

- Stale row: `none`
- Missing link: `domain package is intentionally pending`
- Audit follow-up: `refresh this matrix in the same pass as naming alignment, script hardening, initialization-layer implementation, or future domain extraction`
