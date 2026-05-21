# ADR-0003: Adopt Canonical Layer Names For The Skills Stack

## Document Control

- Artifact ID: `ADR-0003`
- Artifact type: `adr`
- Status: `accepted`
- Owner: `Arthur`
- Parent refs: `REQ-001`, `SPEC-001`, `ARCH-001`
- Child refs: `none`
- Verification state: `accepted by operator clarification and document refresh`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Context

The repository already had a layered architecture, but the naming of those layers was uneven. Existing docs referred to a cognitive kernel, enabled layer, and interview layer, while the broader repo framing also mixed `Meta-Engine`, `Cogna`, and `SynapseOS`. The operator clarified the intended internal architecture naming more precisely:

- `Xuan Master` is the core
- `Archon` is the enabler layer
- `Prism` is the specialist layer

Without an explicit ADR, those names could drift or be applied inconsistently across entry docs, harness artifacts, and future packaging work.

## Decision

Use the following canonical internal layer names:

1. `Xuan Master`
   - the meta-cognition core
   - the 27-model knowledge kernel
2. `Archon`
   - the enabler layer
   - calibration, orchestration, actions, document generation, PDF generation, and similar execution abilities
   - currently implemented primarily through `archon/interview/` and `archon/enabled/`
3. `Prism`
   - the specialist layer
   - routing and mapping into deeper domain-specific and specialized work
   - currently exposed through `prism/SKILL.md` with future domain assets under `prism/domains/`

Treat `optimization/` as a cross-cutting improvement loop rather than part of the named three-layer stack.

## Consequences

### Positive

- Internal architecture can be discussed with clearer intent
- Entry docs and design artifacts have a stable language for future work
- The repo can evolve toward more explicit specialist surfaces without renaming the whole system again

### Negative

- Layer entrypoints and their nested subtree surfaces still need explicit mapping in docs
- `Prism` still needs deeper specialist-domain assets beyond its current minimal repo surface

### Follow-Up

- Keep entry docs and harness artifacts aligned to these names
- Decide how deeply `Prism` should grow beyond its new dedicated repo-local entrypoint
