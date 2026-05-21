# Value Traceability Matrix

## Artifact header

- Artifact ID: `TRACE-001`
- Artifact type: `value-traceability-matrix`
- Status: `active`
- Owner: `Arthur`
- Canonical path: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`
- Source of truth: `this file`
- Upstream links: `REQ-001`, `SPEC-001`, `STORY-001`, `ARCH-001`
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
| `REQ-001` | `SPEC-001` | `STORY-001A` | `pending` | `ARCH-001` | `ADR-0002`; `ADR-0003` | `AGENTS.md`; `00-entry/SKILL.md`; `enabled/SKILL.md`; `interview/SKILL.md`; `optimization/SKILL.md`; `.aries_harness/` | `file inspection of repo surfaces and artifact cross-links` | `.aries_harness/EVAL.md`; `AUDIT-001` | `n/a` |
| `REQ-001` | `SPEC-001` | `STORY-001B` | `pending` | `ARCH-001` | `ADR-0003` | `AGENTS.md`; `00-entry/SKILL.md`; `enabled/SKILL.md`; `interview/SKILL.md` | `documentation diff and file inspection for Xuan Master / Archon / Prism alignment` | `AUDIT-001` | `pending` |
| `REQ-001` | `SPEC-001` | `STORY-001C` | `pending` | `ARCH-001` | `ADR-0002`; `ADR-0003` | `enabled/scripts/model-selector.py`; `optimization/scripts/full_audit.py`; `optimization/scripts/recover_from_session.py` | `pending script-contract review and local checks` | `pending` | `pending` |
| `REQ-001` | `SPEC-001` | `STORY-001D` | `pending` | `ARCH-001` | `ADR-0003` | `prism/SKILL.md`; `prism/domains/README.md`; `AGENTS.md`; `00-entry/SKILL.md` | `file inspection of the new Prism layer surface and updated architecture docs` | `REVIEW-001`; `AUDIT-001` | `n/a` |

## Tracking Notes

- Stale row: `none`
- Missing link: `domain package is intentionally pending`
- Audit follow-up: `refresh this matrix in the same pass as naming alignment, script hardening, or future domain extraction`
