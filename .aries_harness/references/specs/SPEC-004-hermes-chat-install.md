# Spec Package

## Document Control

- Spec ID: `SPEC-004`
- Artifact type: `spec`
- Objective mode: `functional_capability`
- Title: `Hermes direct-SKILL installer and chatbox installation mode`
- Status: `active`
- Owner: `Arthur`
- Parent request: `REQ-004`
- Child refs: `STORY-004`, `ARCH-004`, `ADR-0006`, `TRACE-001`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Interface Evidence

This spec is grounded in local Hermes Agent v0.14.0 behavior available in this workspace:

- `hermes --version` reports `Hermes Agent v0.14.0 (2026.5.16)`
- `hermes skills install --help` accepts an identifier or direct HTTP(S) URL to a `SKILL.md` file
- `hermes skills install --help` exposes `--category`, `--name`, `--force`, and `--yes`
- `hermes skills list` lists installed builtin, local, and category-scoped skills
- Installed Hermes skills use YAML frontmatter fields such as `name`, `description`, `version`, `platforms`, and `metadata.hermes`
- Public Hermes docs also describe working with skills and the skills feature surface:
  - `https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md`
  - `https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md`

## Belongs Here

- Objective: define what must be true for SynapseOS to support a Hermes-specific chatbox installer that starts from a direct `SKILL.md` link
- In scope:
  - Hermes installer skill at `install/hermes-chat-install/SKILL.md`
  - Hermes-specific installation guide
  - chatbox prompt that tells Hermes to install and run the installer skill
  - current safe baseline using `synapse-cli install --agent hermes`
  - detection and update of existing grouped SynapseOS Hermes installs
  - Hermes-native verification through `hermes skills list` and `hermes skills check`
  - first-use learning prompt after installation
- Out of scope:
  - publishing to a Hermes registry
  - mutating Hermes configuration automatically
  - installing Hermes itself
  - destructive uninstall
  - guaranteeing live skill visibility without Hermes-native checks
- Primary actors:
  - Hermes user installing SynapseOS from a chat session
  - Hermes support operator diagnosing install drift
  - SynapseOS maintainer validating Hermes compatibility

## Required User Flows

### Flow 1: Chatbox Installer Skill

User pastes into Hermes:

```text
Install this Hermes skill and use it to install the SynapseOS skills family:
https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/hermes-chat-install/SKILL.md

After installing it as synapseos-installer, run it. Show me the target directory and dry-run plan first, then complete the install and verification if the plan is safe.
```

If Hermes asks for an explicit command:

```text
/skills install https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/hermes-chat-install/SKILL.md --name synapseos-installer
/synapseos-installer install the SynapseOS skills family. Show the dry-run plan first, then install and verify if safe.
```

Required behavior:

- install the direct `SKILL.md` as `synapseos-installer`
- clone or update SynapseOS over HTTPS
- run `./synapse-cli doctor --json`
- show `./synapse-cli install --agent hermes --dry-run --json`
- if a previous grouped SynapseOS install exists, report `install_mode: update`, `payload_version`, and `previous_installation.status: existing_grouped_payload`
- apply `./synapse-cli install --agent hermes --yes --json` only after the target is safe
- run `./synapse-cli verify --agent hermes --json`
- run `hermes skills list` and `hermes skills check`
- print the quick learning prompt

### Flow 2: Safe Local Install

```sh
./synapse-cli install --agent hermes --dry-run --json
./synapse-cli install --agent hermes --yes --json
./synapse-cli verify --agent hermes --json
hermes skills list
hermes skills check
```

Required behavior:

- dry-run renders writes before applying them
- dry-run reports `install_mode`, `payload_version`, and `previous_installation` when an existing SynapseOS install is present
- approved install writes into the Hermes adapter target, defaulting to `~/.hermes/skills/synapseos`
- approved install updates an existing grouped SynapseOS payload in place
- SynapseOS verification checks files and manifest
- Hermes verification checks host skill visibility

### Flow 3: Quick Learning After Install

After verification, the guide should instruct the user to ask Hermes:

```text
Use SynapseOS. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first skill for my current task.
```

## Acceptance Conditions

- `install/hermes-chat-install/SKILL.md` exists with Hermes-compatible frontmatter and installation workflow.
- `docs/HERMES_INSTALL.md` exists and includes prerequisites, chatbox install mode, safe local install, verification, update, troubleshooting, and first-use learning prompt.
- The guide uses Hermes-native commands instead of relying only on SynapseOS self-verification.
- The chatbox flow avoids opaque remote shell and delegates filesystem writes to `synapse-cli` dry-run and approved install.
- `synapse-cli install --agent hermes --dry-run --json` produces a valid plan.
- Existing grouped installs are treated as update plans, while unrecognized existing `synapseos/` directories are blocked.
- `synapse-cli verify --agent hermes --json` remains the payload integrity check.
- Hermes-native verification includes `hermes skills list` and `hermes skills check`.
- Failures must distinguish prerequisite, checkout, payload verification, and Hermes skill visibility issues.

## NFRs

- Hermes users should be able to start installation from one pasted link and one simple prompt.
- Operators must be able to inspect the installer skill before running it.
- The local checkout path must work without network access after the repository is already present.
- The installer skill must be readable as plain Markdown.
- The approach must not require SSH keys.

## Regression Guardrails

- Do not make Hermes the only supported host.
- Do not silently modify Hermes configuration.
- Do not replace the repo-local `synapse-cli` contract with a Hermes-only path.
- Do not bypass dry-run and target display.
- Do not rename canonical SynapseOS layers.
- Do not overwrite an unrecognized existing `synapseos/` directory without explicit operator action outside the installer.

## Slice Candidates

| Slice ID | User value | Acceptance anchor | Priority | Notes |
| --- | --- | --- | --- | --- |
| `STORY-004A` | Hermes users get a governed install mode and detailed guide | `REQ-004`, `SPEC-004`, `STORY-004`, `ARCH-004`, `ADR-0006`, guide, and installer skill exist | `now` | This pass |
| `STORY-004B` | Hermes users get deeper native verification | `synapse-cli verify --agent hermes` can optionally run or summarize Hermes-native checks | `next` | Requires coding slice |
| `STORY-004C` | Hermes users get registry/native package installation | SynapseOS is available through a Hermes-supported registry or package source | `later` | Deferred |
| `STORY-004D` | Maintainers get Hermes compatibility checks | Checklist or test validates payload plus Hermes skill visibility where Hermes is installed | `later` | Environment-dependent |

## Linked Artifacts

- Request brief: `.aries_harness/references/requests/REQ-004-hermes-chat-install.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-004-hermes-chat-install.md`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-004-hermes-chat-install.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0006-hermes-chat-install.md`
- User guide: `docs/HERMES_INSTALL.md`
- Installer skill: `install/hermes-chat-install/SKILL.md`
- Traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Open Questions And Risks

- Open question: should a future Hermes package install each SynapseOS layer as category-scoped skills instead of grouped under `synapseos/`?
- Open question: should `synapse-cli verify --agent hermes` run `hermes skills check` directly or report the exact command for the user?
- Risk: Hermes session skill lists may need reload/new session after installation.
- Risk: Hermes skill metadata expectations may evolve.
- Refresh trigger: Hermes CLI, skill metadata, install target, or verification behavior changes.
- Audit log entry: `AUDIT-001`
