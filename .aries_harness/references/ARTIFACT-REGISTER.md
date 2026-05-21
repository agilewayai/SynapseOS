# Artifact Register

## Artifact header

- Artifact ID: `REG-001`
- Artifact type: `artifact-register`
- Status: `active`
- Owner: `Arthur`
- Canonical path: `.aries_harness/references/ARTIFACT-REGISTER.md`
- Source of truth: `this file`
- Upstream links: `REQ-001`, `SPEC-001`, `STORY-001`, `ARCH-001`, `ADR-0003`, `REQ-002`, `SPEC-002`, `STORY-002`, `ARCH-002`, `ADR-0004`, `DOM-002`, `REQ-003`, `SPEC-003`, `STORY-003`, `ARCH-003`, `ADR-0005`, `REQ-004`, `SPEC-004`, `STORY-004`, `ARCH-004`, `ADR-0006`
- Downstream links: `TRACE-001`, `POL-001`, `AUDIT-001`, `REVIEW-001`
- Verification state: `initialized`
- Last reviewed: `2026-05-21`
- Next review / refresh trigger: `refresh in the same pass as any meaningful request/spec/story/architecture/ADR update`

## Runtime links

- Run ID: `pending`
- Task ID / Slice ID: `distill-current-project-baseline`
- Checkpoint ID: `n/a`
- Approval Request ID: `n/a`
- Trace ID: `TRACE-001`
- Eval Report ID: `pending`
- Audit Log ID: `AUDIT-001`

| Artifact ID | Type | Canonical path | Owner | Phase | Status | Verification state | Last reviewed | Source of truth | Refresh trigger | Runtime links | Upstream links | Downstream links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `REQ-001` | `request` | `.aries_harness/references/requests/REQ-001-repository-baseline.md` | `Arthur` | `intake` | `active` | `distilled from current repo` | `2026-05-21` | `that file` | `project identity, internal layer names, purpose, or scope changes` | `TRACE-001; AUDIT-001` | `MISSION.md; AGENTS.md` | `SPEC-001; STORY-001; ARCH-001; ADR-0003` |
| `SPEC-001` | `spec` | `.aries_harness/references/specs/SPEC-001-repository-baseline.md` | `Arthur` | `shaping` | `active` | `distilled from current repo` | `2026-05-21` | `that file` | `layer contract, model count, or integration guidance changes` | `TRACE-001; AUDIT-001` | `REQ-001` | `STORY-001; ARCH-001; ADR-0002; ADR-0003` |
| `STORY-001` | `story-pack` | `.aries_harness/references/stories/STORY-001-baseline-alignment-pack.md` | `Arthur` | `slice-planning` | `active` | `baseline slices defined` | `2026-05-21` | `that file` | `active or next slice changes` | `TRACE-001; AUDIT-001` | `REQ-001; SPEC-001` | `ARCH-001; ADR-0002; ADR-0003` |
| `ARCH-001` | `architecture` | `.aries_harness/decisions/architecture/ARCH-001-repository-layered-architecture.md` | `Arthur` | `design` | `active` | `distilled from current repo` | `2026-05-21` | `that file` | `layer boundaries, layer mapping, or script responsibilities change` | `TRACE-001; AUDIT-001` | `REQ-001; SPEC-001` | `ADR-0002; ADR-0003` |
| `ADR-0002` | `adr` | `.aries_harness/decisions/adrs/ADR-0002-layered-docs-first-architecture.md` | `Arthur` | `design` | `accepted` | `accepted by repository inspection` | `2026-05-21` | `that file` | `architecture decision meaning changes` | `AUDIT-001` | `ARCH-001` | `STORY-001B; STORY-001C` |
| `ADR-0003` | `adr` | `.aries_harness/decisions/adrs/ADR-0003-canonical-layer-names.md` | `Arthur` | `design` | `accepted` | `accepted by operator clarification and document refresh` | `2026-05-21` | `that file` | `canonical internal layer names or their repo mapping change` | `AUDIT-001` | `REQ-001; SPEC-001; ARCH-001` | `STORY-001B; STORY-001D` |
| `POL-001` | `artifact-refresh-policy` | `.aries_harness/references/ARTIFACT-REFRESH-POLICY.md` | `Arthur` | `governance` | `active` | `initialized` | `2026-05-21` | `that file` | `artifact handling rules change` | `AUDIT-001` | `REQ-001; SPEC-001; STORY-001; ARCH-001` | `REG-001; TRACE-001` |
| `TRACE-001` | `value-traceability-matrix` | `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md` | `Arthur` | `governance` | `active` | `updated for synapse-cli baseline` | `2026-05-21` | `that file` | `artifact links or delivery evidence changes` | `AUDIT-001` | `REQ-001; SPEC-001; STORY-001; ARCH-001; REQ-002; SPEC-002; STORY-002; ARCH-002; DOM-002` | `future runs and history` |
| `AUDIT-001` | `artifact-audit-log` | `.aries_harness/references/ARTIFACT-AUDIT-LOG.md` | `Arthur` | `governance` | `active` | `initialized` | `2026-05-21` | `that file` | `meaningful artifact change occurs` | `n/a` | `REG-001` | `future review and history` |
| `REVIEW-001` | `harness-audit` | `.aries_harness/references/reviews/REVIEW-001-skill-layer-structure.md` | `Arthur` | `review` | `active` | `reviewed and partially remediated` | `2026-05-21` | `that file` | `after the next structure or operability-hardening pass` | `TRACE-001; AUDIT-001` | `REQ-001; SPEC-001; ARCH-001` | `STORY-001C` |
| `REQ-002` | `request` | `.aries_harness/references/requests/REQ-002-synapseos-initialization-layer.md` | `Arthur` | `intake` | `active` | `shaped from operator request` | `2026-05-21` | `that file` | `initialization layer scope, supported hosts, or CLI contract changes` | `TRACE-001; AUDIT-001` | `MISSION.md; REQ-001` | `SPEC-002; STORY-002; ARCH-002; ADR-0004` |
| `SPEC-002` | `spec` | `.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md` | `Arthur` | `shaping` | `active` | `installation contract implemented as local baseline` | `2026-05-21` | `that file` | `synapse-cli commands, prerequisite policy, adapter contract, or acceptance changes` | `TRACE-001; AUDIT-001` | `REQ-002` | `STORY-002; ARCH-002; ADR-0004; DOM-002` |
| `STORY-002` | `story-pack` | `.aries_harness/references/stories/STORY-002-initialization-layer-pack.md` | `Arthur` | `slice-planning` | `active` | `baseline implementation accepted` | `2026-05-21` | `that file` | `implementation slice status, scope, or verification changes` | `TRACE-001; AUDIT-001` | `REQ-002; SPEC-002` | `ARCH-002; ADR-0004; DOM-002` |
| `ARCH-002` | `architecture` | `.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md` | `Arthur` | `design` | `active` | `architecture implemented as local baseline` | `2026-05-21` | `that file` | `layer shape, CLI surface, adapter model, or installer evidence changes` | `TRACE-001; AUDIT-001` | `REQ-002; SPEC-002` | `ADR-0004; STORY-002; DOM-002` |
| `ADR-0004` | `adr` | `.aries_harness/decisions/adrs/ADR-0004-synapseos-initialization-layer.md` | `Arthur` | `design` | `accepted` | `accepted and implemented as local baseline` | `2026-05-21` | `that file` | `initialization layer decision or CLI contract changes materially` | `AUDIT-001` | `REQ-002; SPEC-002; ARCH-002` | `STORY-002; DOM-002` |
| `DOM-002` | `domain-analysis-pack` | `.aries_harness/references/domain/DOM-002-synapseos-initialization-domain.md` | `Arthur` | `domain-design` | `active` | `derived from SPEC-002 and current synapse-cli implementation` | `2026-05-21` | `that file` | `synapse-cli commands, adapter model, install manifest, verification rules, or prerequisite policy change` | `TRACE-001; AUDIT-001` | `REQ-002; SPEC-002; STORY-002; ARCH-002; ADR-0004` | `init/; synapse-cli; tests/test_synapse_cli.py` |
| `REQ-003` | `request` | `.aries_harness/references/requests/REQ-003-openclaw-quick-install.md` | `Arthur` | `intake` | `active` | `shaped from operator request and OpenClaw docs` | `2026-05-21` | `that file` | `OpenClaw install UX, interface assumptions, or quick-link goal changes` | `TRACE-001; AUDIT-001` | `REQ-002; SPEC-002; ARCH-002` | `SPEC-003; STORY-003; ARCH-003; ADR-0005` |
| `SPEC-003` | `spec` | `.aries_harness/references/specs/SPEC-003-openclaw-quick-install.md` | `Arthur` | `shaping` | `active` | `OpenClaw quick-install contract defined` | `2026-05-21` | `that file` | `OpenClaw skill interface, one-link installer contract, or verification expectations change` | `TRACE-001; AUDIT-001` | `REQ-003` | `STORY-003; ARCH-003; ADR-0005` |
| `STORY-003` | `story-pack` | `.aries_harness/references/stories/STORY-003-openclaw-quick-install.md` | `Arthur` | `slice-planning` | `active` | `guide and chatbox prompt slices accepted; implementation slices ready` | `2026-05-21` | `that file` | `OpenClaw quick-install slice status, scope, or verification changes` | `TRACE-001; AUDIT-001` | `REQ-003; SPEC-003` | `ARCH-003; ADR-0005` |
| `ARCH-003` | `architecture` | `.aries_harness/decisions/architecture/ARCH-003-openclaw-quick-install.md` | `Arthur` | `design` | `active` | `OpenClaw install architecture defined` | `2026-05-21` | `that file` | `OpenClaw target shape, verification, one-link installer, or package layout changes` | `TRACE-001; AUDIT-001` | `REQ-003; SPEC-003` | `ADR-0005; STORY-003` |
| `ADR-0005` | `adr` | `.aries_harness/decisions/adrs/ADR-0005-openclaw-quick-install.md` | `Arthur` | `design` | `accepted` | `accepted by OpenClaw installation shaping` | `2026-05-21` | `that file` | `OpenClaw quick-install trust model or target strategy changes materially` | `AUDIT-001` | `REQ-003; SPEC-003; ARCH-003` | `STORY-003` |
| `REQ-004` | `request` | `.aries_harness/references/requests/REQ-004-hermes-chat-install.md` | `Arthur` | `intake` | `active` | `shaped from operator request and local Hermes CLI evidence` | `2026-05-21` | `that file` | `Hermes install UX, interface assumptions, or direct-SKILL goal changes` | `TRACE-001; AUDIT-001` | `REQ-002; SPEC-002; ARCH-002` | `SPEC-004; STORY-004; ARCH-004; ADR-0006` |
| `SPEC-004` | `spec` | `.aries_harness/references/specs/SPEC-004-hermes-chat-install.md` | `Arthur` | `shaping` | `active` | `Hermes direct-SKILL install contract defined` | `2026-05-21` | `that file` | `Hermes skill interface, installer skill, or verification expectations change` | `TRACE-001; AUDIT-001` | `REQ-004` | `STORY-004; ARCH-004; ADR-0006` |
| `STORY-004` | `story-pack` | `.aries_harness/references/stories/STORY-004-hermes-chat-install.md` | `Arthur` | `slice-planning` | `active` | `installer skill and guide slice accepted; verification slice ready` | `2026-05-21` | `that file` | `Hermes install slice status, scope, or verification changes` | `TRACE-001; AUDIT-001` | `REQ-004; SPEC-004` | `ARCH-004; ADR-0006` |
| `ARCH-004` | `architecture` | `.aries_harness/decisions/architecture/ARCH-004-hermes-chat-install.md` | `Arthur` | `design` | `active` | `Hermes install architecture defined` | `2026-05-21` | `that file` | `Hermes target shape, verification, installer skill, or package layout changes` | `TRACE-001; AUDIT-001` | `REQ-004; SPEC-004` | `ADR-0006; STORY-004` |
| `ADR-0006` | `adr` | `.aries_harness/decisions/adrs/ADR-0006-hermes-chat-install.md` | `Arthur` | `design` | `accepted` | `accepted by Hermes installation shaping` | `2026-05-21` | `that file` | `Hermes direct-SKILL install strategy changes materially` | `AUDIT-001` | `REQ-004; SPEC-004; ARCH-004` | `STORY-004` |
