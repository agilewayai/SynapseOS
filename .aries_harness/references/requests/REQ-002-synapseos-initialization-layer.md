# Request Brief

## Document Control

- Request ID: `REQ-002`
- Artifact type: `request`
- Objective mode: `functional_capability`
- Title: `SynapseOS initialization layer and agent installation CLI`
- Status: `active`
- Owner: `Arthur`
- Review date: `2026-05-21`
- Parent refs: `.aries_harness/MISSION.md`, `REQ-001`
- Child refs: `SPEC-002`, `STORY-002`, `ARCH-002`, `ADR-0004`, `DOM-002`, `TRACE-001`
- Source of truth: `this file`

## Belongs Here

- Request source: operator request to add and implement a SynapseOS installation initialization layer
- Problem statement: SynapseOS has a clearer layered skill architecture, and agent users need a repeatable way to check prerequisites, install required runtime support, and place SynapseOS assets into supported agent hosts
- Intended user or operator outcome: a maintainer or coding agent can run a documented `synapse-cli` flow to diagnose the local environment, initialize SynapseOS, install it into supported agent hosts, and verify that the host can load the expected entrypoints
- Target agent hosts:
  - `claude-code`
  - `codex`
  - `cursor`
  - `opencode`
  - `openclaw`
  - `hermes`
  - `generic`
- Business value:
  - lowers first-run setup cost for new operators
  - gives multi-agent distribution a stable installation contract
  - makes host-specific install behavior auditable instead of hidden in ad hoc notes
  - creates a foundation for future packaging, release, and support work
- Success signals:
  - a request/spec/story/architecture package exists for the initialization layer
  - `synapse-cli` command expectations are explicit and implemented as a repo-local baseline
  - prerequisite checking and optional installation policy are documented
  - supported agent hosts and the generic host path are listed with acceptance rules
  - future hardening slices can point to this artifact set
- Target quality attributes: `idempotence`, `portability`, `diagnostic clarity`, `explicit operator control`, `host adapter isolation`, `repo-local verification`
- Scope boundary: define the target initialization layer and CLI contract, then maintain implementation evidence separately from the cognitive skill content
- Constraints:
  - installation must preserve the existing docs-first skill corpus
  - host-specific path resolution must be adapter-owned and verifiable
  - external downloads, package installation, or writes outside the repo must be dry-run visible and approval-gated
  - the generic host path must work without requiring one of the named agent platforms
- Non-goals:
  - implementing external package publishing in this baseline
  - publishing to external package registries
  - replacing each agent host's native configuration model
  - adding cloud deployment or production runtime operations
  - changing the meaning of the `Xuan Master`, `Archon`, or `Prism` skill content

## Keep Out

- Low-level implementation details better owned by `init/synapse_cli/` and tests
- Exact third-party host filesystem paths unless verified during implementation
- Release packaging instructions
- Runtime logs from CLI executions

## Delivery Links

- Spec package: `.aries_harness/references/specs/SPEC-002-synapseos-initialization-layer.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-002-initialization-layer-pack.md`
- Domain package: `.aries_harness/references/domain/DOM-002-synapseos-initialization-domain.md`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-002-synapseos-initialization-layer.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0004-synapseos-initialization-layer.md`
- Value traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Refresh Triggers

- What should force this brief to be reviewed:
  - a supported agent host is added, removed, or renamed
  - the `synapse-cli` command contract changes
  - prerequisite installation policy changes
  - the initialization layer gains a physical repo surface
  - installer behavior writes outside the repo in a new way
- Audit log entry: `AUDIT-001`

## Notes For Non-Feature Objectives

This is both a `functional_capability` and an `operability_governance` objective. The feature is the initialization and installation flow; the governance requirement is that the flow be inspectable, reversible where practical, and explicit about prerequisites and external writes.
