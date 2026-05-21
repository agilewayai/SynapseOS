# Architecture Design Pack

## Document Control

- Architecture ID: `ARCH-003`
- Artifact type: `architecture`
- Title: `OpenClaw one-link quick learning-and-installation architecture`
- Status: `active`
- Owner: `Arthur`
- Related request: `REQ-003`
- Related spec: `SPEC-003`
- Child refs: `ADR-0005`
- Last reviewed: `2026-05-21`
- Source of truth: `this file`

## Design Drivers

- Primary outcome: make SynapseOS installable and learnable inside OpenClaw with minimal friction and clear verification
- Quality attributes:
  - OpenClaw-native
  - safe by default
  - one-command friendly
  - auditable
  - reversible by operator action
  - inspectable without remote shell
- Constraints:
  - SynapseOS remains a multi-skill stack, not one flattened skill
  - existing `synapse-cli` install behavior remains the stable local baseline
  - OpenClaw config and allowlists are not silently mutated
  - hosted one-link automation must not bypass dry-run and target display

## Current And Target Shape

- Current state:
  - `synapse-cli` has an `openclaw` adapter that resolves a default target under `~/.openclaw/skills`
  - `install --agent openclaw` can copy the SynapseOS payload into an OpenClaw-managed skill root group
  - `verify --agent openclaw` checks SynapseOS payload files and manifest, but does not yet run OpenClaw-native visibility checks
  - public docs do not yet have a dedicated OpenClaw install guide
- Target state:
  - public docs expose a copy-paste OpenClaw installation guide
  - OpenClaw chatbox install mode provides one stable raw prompt link plus a simple instruction
  - local baseline install remains `./synapse-cli install --agent openclaw --dry-run` followed by `--yes`
  - OpenClaw-native verification is part of the acceptance path through `openclaw skills check --json`
  - future one-link installer wraps clone/install/verify/learning prompt behind one safe command
  - future packaging can add an OpenClaw-native source install without breaking the local baseline

## OpenClaw Interface Mapping

| OpenClaw concept | SynapseOS mapping | Design note |
| --- | --- | --- |
| Skill folder containing `SKILL.md` | `xuan-master/`, `archon/`, `prism/`, `init/` | SynapseOS remains a grouped multi-skill install |
| Required skill metadata | `SKILL.md` frontmatter | Future OpenClaw package surfaces may need OpenClaw-safe aliases while preserving canonical layer names |
| Shared managed skill root | `~/.openclaw/skills` by default | Adapter target can be overridden |
| Skill groups or nested local skill directories | `~/.openclaw/skills/synapseos/<layer>/SKILL.md` | Keeps SynapseOS layers together |
| `openclaw skills check --json` | Host-native verification gate | Confirms OpenClaw visibility beyond file presence |
| `openclaw skills install` | Future native package path | May require an OpenClaw-specific package surface |

## Proposed Installation Modes

| Mode | User command shape | Status | Tradeoff |
| --- | --- | --- | --- |
| Local safe baseline | `./synapse-cli install --agent openclaw --dry-run`; then `--yes` | available baseline | Inspectable and safe, but requires checkout |
| Chatbox prompt installer | Paste `https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw-chat-install.md` plus a simple install prompt into OpenClaw chat | available baseline | Lowest friction inside OpenClaw, depends on OpenClaw tool permissions |
| Shell one-link installer | `curl -fsSL .../install/openclaw.sh | bash` | specified future slice | Useful outside chat, but requires stronger safety and trust messaging |
| OpenClaw-native package | `openclaw skills install <source>` | future packaging slice | Feels native, may need package reshaping |
| Development checkout | OpenClaw `skills.load.extraDirs` points at a local repo/package path | documented fallback | Good for maintainers, more config ceremony |

## Component Boundaries

- `OpenClaw install guide`: public operator instructions, troubleshooting, and first-use prompt
- `Chatbox install prompt`: `install/openclaw-chat-install.md`, a self-contained instruction link for OpenClaw to fetch, install, verify, and teach SynapseOS
- `OpenClaw adapter`: target resolution, dry-run/install plan, and payload verification for OpenClaw
- `OpenClaw-native verifier`: optional integration that runs or summarizes `openclaw skills check --json`
- `One-link installer`: future shell entrypoint that clones or updates SynapseOS, delegates to `synapse-cli`, and prints learning guidance
- `Package surface`: future OpenClaw-native package shape if direct `openclaw skills install` becomes the preferred path; it may include metadata aliases that satisfy OpenClaw's active `SKILL.md` rules

## Decisions

| Decision | Why | Tradeoff | Linked ADR |
| --- | --- | --- | --- |
| Treat OpenClaw as a grouped multi-skill install target | SynapseOS has multiple loadable layers and should preserve them | Direct single-skill Git install may require an extra package surface | `ADR-0005` |
| Keep `synapse-cli` as the safe local baseline | It already owns dry-run, manifest, and verification behavior | One-link mode is a wrapper, not the source of truth | `ADR-0005` |
| Require OpenClaw-native check in guide and future adapter hardening | File presence does not prove OpenClaw skill visibility | Requires OpenClaw binary for full validation | `ADR-0005` |
| Provide chatbox link UX before shell one-link UX | It uses OpenClaw itself to perform visible steps instead of immediately running opaque remote shell | Depends on OpenClaw chat/tool permissions and web access | `ADR-0005` |
| Provide shell one-link UX only with explicit safety rules | Low friction is valuable but remote shell is trust-sensitive | Slightly more implementation ceremony | `ADR-0005` |

## Delivery Impact

- Affected stories: `STORY-003A`, `STORY-003B`, `STORY-003C`, `STORY-003D`, `STORY-003E`, `STORY-003F`
- Verification impact: combine SynapseOS payload checks with OpenClaw-native skill checks where available
- Documentation impact: add `docs/OPENCLAW_INSTALL.md` and link it from public onboarding docs
- Future code impact: likely changes to `init/synapse_cli/installer.py`, `init/synapse_cli/adapters.py`, and optionally a new `install/openclaw.sh`

## Risks And Open Questions

- Risk: OpenClaw root precedence or skill command semantics may change.
- Risk: OpenClaw metadata validation may reject source-layer frontmatter, requiring an adapter package or generated aliases.
- Risk: chatbox install depends on OpenClaw being allowed to fetch links and run shell commands.
- Risk: shell one-link scripts can feel unsafe if users cannot inspect them first.
- Risk: direct OpenClaw-native Git install may not fit SynapseOS's multi-skill repository shape without an adapter package.
- Open question: should one-link installation clone the full repo, use a release tarball, or use `synapse-cli` from a package later?
- Open question: should OpenClaw verification be part of `verify` by default or behind `--host-check`?
- Refresh trigger: OpenClaw docs, adapter behavior, one-link script, or package layout changes.
- Audit log entry: `AUDIT-001`
