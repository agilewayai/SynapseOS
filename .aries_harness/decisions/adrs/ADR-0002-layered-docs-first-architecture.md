# ADR-0002: Preserve A Layered Docs-First Knowledge Architecture

## Document Control

- Artifact ID: `ADR-0002`
- Artifact type: `adr`
- Status: `accepted`
- Owner: `Arthur`
- Parent refs: `REQ-001`, `SPEC-001`, `ARCH-001`
- Child refs: `none`
- Verification state: `accepted by repository inspection`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Context

The current repository is not a conventional application. Its primary product is a structured knowledge corpus: a catalog, 27 model modules, and higher-order orchestration and optimization layers expressed mostly as Markdown. Small scripts exist, but they support routing, audit, and recovery rather than define the main user-facing contract.

At the same time, the repository has accumulated multiple framing names (`Cogna`, `Meta-Engine`, `SynapseOS`) and some helper scripts still carry Hermes-era runtime assumptions. Without a written architecture decision, future work could accidentally turn the repo into an ad hoc collection of documents or drift toward script-defined behavior.

## Decision

Preserve the repository as a layered, docs-first knowledge architecture with these rules:

1. `SKILL.md` files remain the primary product contract.
2. Each cognitive model stays independently loadable from its own directory.
3. The higher-order layers stay separated by responsibility, with their canonical naming clarified by `ADR-0003`:
   - `Xuan Master` core
   - `Archon` calibration and enabled orchestration
   - `Prism` specialist routing
   - `optimization` loop
   - Aries governance
4. Helper scripts remain supporting surfaces and must not become the sole source of routing or corpus-policy truth.
5. Future naming and operability cleanup should align with this layered model rather than replace it with a monolithic runtime.

## Consequences

### Positive

- Another operator can understand the product by reading files rather than tracing a large executable system
- The corpus remains portable across multiple agent environments
- Architecture changes can be expressed as document and boundary deltas rather than hidden implementation details

### Negative

- Consistency depends on disciplined documentation refresh and audit
- Drift between docs and helper scripts remains possible until script hardening is done
- Naming clarity still needs follow-on work

### Follow-Up

- Use `STORY-001B` to align public naming
- Use `STORY-001C` to review helper-script assumptions and repo-local verification rules
- Use `STORY-001D` to decide how explicitly `Prism` materializes in the repo
