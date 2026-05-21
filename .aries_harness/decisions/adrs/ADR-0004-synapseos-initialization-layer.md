# ADR-0004: Add A SynapseOS Initialization Layer And synapse-cli Contract

## Document Control

- Artifact ID: `ADR-0004`
- Artifact type: `adr`
- Status: `accepted`
- Owner: `Arthur`
- Parent refs: `REQ-002`, `SPEC-002`, `ARCH-002`
- Child refs: `STORY-002`
- Verification state: `accepted by operator request and artifact shaping`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Context

SynapseOS is becoming a multi-agent skills stack. The current repository explains the skill layers, but it does not yet provide a first-class installation layer or a stable command interface for setting up supported agent hosts.

The requested installer must cover prerequisite runtime checking and installation planning, plus host-specific installation for Claude Code, Codex, Cursor, OpenCode, OpenClaw, Hermes, and a generic host path.

## Decision

Add a dedicated SynapseOS `Initialization Layer` for first-run setup and host installation, with `synapse-cli` as the user-facing command interface.

The initialization layer owns:

- prerequisite runtime detection
- optional prerequisite install planning
- local initialization metadata
- agent host adapter registry
- dry-run install planning
- approved install execution
- install manifests and verification reports

Supported first-design adapters are:

- `claude-code`
- `codex`
- `cursor`
- `opencode`
- `openclaw`
- `hermes`
- `generic`

## Consequences

### Positive

- Installation becomes inspectable and repeatable across agent hosts
- Host-specific behavior has a clear owner and can evolve independently
- The generic adapter keeps SynapseOS installable for non-listed agent hosts
- Future packaging work has a stable command contract to build around

### Negative

- The repository gains another layer to document, test, and keep aligned
- Host adapters can drift as third-party agent configuration models change
- Prerequisite installation requires strict policy to avoid unsafe side effects

## Follow-Up

- Implement the `synapse-cli` skeleton from `STORY-002B`
- Implement read-only prerequisite diagnosis from `STORY-002C`
- Add host adapters incrementally after the CLI and safety model are stable
- Decide the physical repo name for the initialization layer during the first implementation slice
