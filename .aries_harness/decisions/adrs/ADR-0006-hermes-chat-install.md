# ADR-0006: Adopt A Hermes Direct-SKILL Chatbox Installer

## Document Control

- Artifact ID: `ADR-0006`
- Artifact type: `adr`
- Status: `accepted`
- Owner: `Arthur`
- Parent refs: `REQ-004`, `SPEC-004`, `ARCH-004`
- Child refs: `STORY-004`
- Verification state: `accepted by Hermes installation shaping`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Context

SynapseOS has a baseline `synapse-cli` installer with a `hermes` adapter. Hermes Agent also has a native skill management surface that can install a direct HTTP(S) URL to a `SKILL.md` file.

That makes Hermes different from purely filesystem-oriented hosts: SynapseOS can provide a small Hermes installer skill as the chatbox bootstrap. The installer skill can then clone SynapseOS, run `synapse-cli`, install the full skill family, verify the payload, and instruct the user how to start.

## Decision

Adopt `install/hermes-chat-install/SKILL.md` as the Hermes-native chatbox installer skill.

The Hermes installation path has three layers:

- keep `synapse-cli install --agent hermes` as the safe local baseline
- provide a direct-link Hermes installer skill that delegates to `synapse-cli`
- defer registry/native package publication to a later packaging slice

SynapseOS should install into Hermes as a grouped skills family containing `xuan-master`, `archon`, `prism`, and `init`, rather than flattening the system into one long instruction file.

The installer should detect an existing grouped SynapseOS payload and update it in place when the payload markers are present. If `~/.hermes/skills/synapseos` exists but does not look like SynapseOS, the dry-run must report a conflict instead of copying over it.

## Consequences

### Positive

- Hermes users get a native paste-link installation mode.
- The installer skill is readable Markdown and uses Hermes' own skill install path.
- The local baseline remains inspectable and reusable.
- Repeat paste-link installs can safely update an existing SynapseOS payload.
- Future registry publication has a stable bootstrap design.

### Negative

- The repository gains a Hermes-specific installer skill and guide to maintain.
- Full host verification depends on Hermes being installed and able to reload skills.
- Grouped family layout may need future category/package tuning for ideal Hermes UX.

## Follow-Up

- Maintain `install/hermes-chat-install/SKILL.md`.
- Maintain `docs/HERMES_INSTALL.md`.
- Add Hermes-native verification to `synapse-cli verify --agent hermes` in a future coding slice.
- Evaluate Hermes registry/native package publication after the direct-link path stabilizes.
