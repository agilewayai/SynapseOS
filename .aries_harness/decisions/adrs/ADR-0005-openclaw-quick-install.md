# ADR-0005: Adopt An OpenClaw-Native Quick Install Path

## Document Control

- Artifact ID: `ADR-0005`
- Artifact type: `adr`
- Status: `accepted`
- Owner: `Arthur`
- Parent refs: `REQ-003`, `SPEC-003`, `ARCH-003`
- Child refs: `STORY-003`
- Verification state: `accepted by OpenClaw installation shaping`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Context

SynapseOS now has a baseline `synapse-cli` installer with an `openclaw` adapter. OpenClaw users still need a smoother channel-chat path that matches OpenClaw's native skill model and provides a quick learning experience immediately after installation.

OpenClaw exposes a skill system centered on `SKILL.md` folders, configured skill roots, and CLI verification commands such as `openclaw skills check`. SynapseOS should use those native surfaces instead of treating OpenClaw as a generic filesystem target only.

## Decision

Adopt an OpenClaw-optimized installation path with four layers:

- keep `synapse-cli install --agent openclaw` as the safe local baseline
- provide `install/openclaw-chat-install.md` as a paste-link chatbox prompt that tells OpenClaw how to clone, dry-run, install, verify, and teach SynapseOS
- specify a future optional shell one-link installer that delegates to the local baseline and includes dry-run, target display, conflict checks, verification, and learning prompt behavior
- keep future OpenClaw-native package or ClawHub publication as a separate packaging slice

SynapseOS should install into OpenClaw as direct native skills named `xuan_master`, `archon`, `prism`, `synapse_init`, and `optimization`, backed by a managed `synapseos/` payload copy. This preserves the multi-skill stack while avoiding reliance on OpenClaw versions that may not enumerate grouped family directories.

The installer should also detect the previous grouped-only layout and update it in place when the existing `synapseos/` directory contains SynapseOS payload markers and there are no conflicting direct skill entries. The dry-run output must distinguish this from an unrecognized existing `synapseos/` directory.

## Consequences

### Positive

- OpenClaw users get a lower-friction adoption path.
- The local baseline remains inspectable and safe.
- The chatbox mode gives users one link and one short prompt without requiring immediate remote shell execution.
- OpenClaw-native verification becomes a first-class acceptance signal.
- Users with the early grouped-only install can upgrade without manual cleanup.
- Future packaging can build on a stable OpenClaw target shape.

### Negative

- The repository gains OpenClaw-specific documentation and validation expectations.
- Chatbox mode depends on OpenClaw tool permissions and web access.
- A hosted shell one-link script will require careful trust, safety, and update handling.
- Direct native package installation may require an additional OpenClaw-specific package surface.

## Follow-Up

- Maintain `docs/OPENCLAW_INSTALL.md`.
- Maintain `install/openclaw-chat-install.md`.
- Add OpenClaw-native verification to `synapse-cli verify --agent openclaw` in a future coding slice.
- Implement a reviewed `install/openclaw.sh` shell one-link installer only after its safety behavior is tested.
- Evaluate ClawHub or native OpenClaw package publication after the local and one-link paths stabilize.
