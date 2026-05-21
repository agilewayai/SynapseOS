# Request Brief

## Document Control

- Request ID: `REQ-001`
- Artifact type: `request`
- Objective mode: `documentation_alignment`
- Title: `Canonical baseline for the SynapseOS skills stack and layered architecture`
- Status: `active`
- Owner: `Arthur`
- Review date: `2026-05-21`
- Parent refs: `.aries_harness/MISSION.md`
- Child refs: `SPEC-001`, `STORY-001`, `ARCH-001`, `ADR-0002`, `ADR-0003`, `TRACE-001`
- Source of truth: `this file`

## Belongs Here

- Request source: operator request to apply `aries-harness-request-to-architecture` and distill the current project spec and architecture
- Problem statement: the repository already communicates its purpose and system shape, but that truth is spread across `AGENTS.md`, `xuan-master/00-entry/SKILL.md`, `enabled/`, `interview/`, `optimization/`, and a few helper scripts; canonical layer names and their physical repo mapping also needed to be made explicit
- Current pain or anti-pattern:
  - no single canonical request/spec/architecture pack exists
  - public identity and internal layer naming were previously conflated
  - executable seams are small but implicit
  - some helper scripts still encode legacy Hermes-era assumptions
- Why now: the repository now has Git history and a project-local Aries Harness, so the next safe step is to make the current product and architecture inspectable without replaying chat
- Intended user or operator outcome: a maintainer or coding agent can identify what this repository is, how it is consumed, where its architectural boundaries sit, and how `Xuan Master`, `Archon`, and `Prism` map onto the current repo
- Business value:
  - reduces onboarding and resume cost for future operators
  - lowers drift between product framing and implementation structure
  - gives future refactor, packaging, and publication work a stable upstream reference
- Success signals:
  - a linked request/spec/story/architecture artifact set exists under `.aries_harness/`
  - the artifact set names the current system layers and primary files correctly
  - future slices can point to these artifacts instead of rebuilding intent from scratch
  - the canonical internal layer names are explicitly recorded
- Target quality attributes: `inspectability`, `traceability`, `agent-agnostic clarity`, `low ceremony`, `refreshability`
- Scope boundary: distill the current repository contract and architecture only; do not redesign the product in this pass
- Constraints:
  - preserve the current corpus and layering as the baseline
  - mixed English and Chinese source material must remain understandable as-is
  - the repository is documentation-first, with only small helper scripts
  - `Prism` now has a dedicated entrypoint, but its deeper domain assets are still intentionally sparse
- Non-goals:
  - rewriting all user-facing documentation
  - adding new cognitive models, scenes, or runtime features
  - migrating agent integrations or publishing flows
  - creating a full domain analysis package in this pass

## Keep Out

- Detailed step-by-step implementation tasks
- Full architecture tradeoff analysis
- Test execution logs or release notes

## Delivery Links

- Spec package: `.aries_harness/references/specs/SPEC-001-repository-baseline.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-001-baseline-alignment-pack.md`
- Domain package: `pending`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-001-repository-layered-architecture.md`
- Value traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Refresh Triggers

- What should force this brief to be reviewed:
  - the canonical project identity changes
  - the canonical internal layer names or their repo mapping changes
  - the repository stops being a documentation-first knowledge base
  - a new top-level layer, execution surface, or publishing model is introduced
- Audit log entry: `AUDIT-001`

## Notes For Non-Feature Objectives

This is a `documentation_alignment` objective, not a net-new feature request. The intent is to make the existing repository contract explicit and durable, not to invent a new product surface.
