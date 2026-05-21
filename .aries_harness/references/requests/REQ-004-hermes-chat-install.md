# Request Brief

## Document Control

- Request ID: `REQ-004`
- Artifact type: `request`
- Objective mode: `functional_capability`
- Title: `Hermes chatbox installation for SynapseOS skills family`
- Status: `active`
- Owner: `Arthur`
- Review date: `2026-05-21`
- Parent refs: `REQ-002`, `SPEC-002`, `ARCH-002`
- Child refs: `SPEC-004`, `STORY-004`, `ARCH-004`, `ADR-0006`, `TRACE-001`
- Source of truth: `this file`

## Belongs Here

- Request source: operator request to support Hermes-specific skills installation and enable a Hermes channel chatbox install mode
- Problem statement: the baseline `synapse-cli` can install into a Hermes target, but Hermes users need a native chatbox workflow that starts from a direct `SKILL.md` link and lets Hermes finish the full SynapseOS skills-family installation
- Intended user outcome: a Hermes user can paste one installer-skill link and one simple prompt into Hermes, have Hermes install the installer skill, then have that skill clone SynapseOS, run dry-run, install, verify, and teach first use
- Business value:
  - reduces Hermes onboarding friction
  - uses Hermes' native direct-URL `SKILL.md` install path
  - gives support and docs a stable paste-link install mode
  - keeps the safe local `synapse-cli install --agent hermes` path as the inspectable baseline
- Interface references:
  - Hermes skills are `SKILL.md` files with YAML frontmatter and Markdown instructions
  - Hermes CLI supports `hermes skills install <identifier-or-http-url-to-SKILL.md>`
  - Hermes CLI supports `--name`, `--category`, `--force`, and `--yes` on install
  - Hermes CLI exposes `hermes skills list` and `hermes skills check`
- Success signals:
  - `install/hermes-chat-install/SKILL.md` exists as a direct-link Hermes installer skill
  - `docs/HERMES_INSTALL.md` documents the chatbox prompt, safe local path, verification, update, and troubleshooting
  - `synapse-cli install --agent hermes --dry-run --json` works
  - harness artifacts trace the Hermes mode and follow-on hardening slices
- Target quality attributes: `Hermes-native`, `safe-by-default`, `low-friction`, `inspectable`, `agent-readable`
- Scope boundary: add the Hermes installer skill, guide, and governed artifact package now; deeper Hermes-native verification or registry publication can follow later
- Constraints:
  - do not run opaque remote shell
  - do not silently overwrite existing non-SynapseOS skill folders
  - do not require SSH keys for installation
  - do not make Hermes the only supported host
  - preserve canonical SynapseOS layer names and content
- Non-goals:
  - publishing to a Hermes registry during this pass
  - changing Hermes global configuration automatically
  - adding destructive uninstall behavior
  - guaranteeing live Hermes skill visibility without running Hermes-native checks

## Keep Out

- Non-Hermes host behavior
- Full release packaging beyond the direct `SKILL.md` installer skill
- Claims that Hermes loaded the family unless `hermes skills list` or equivalent evidence supports it

## Delivery Links

- Spec package: `.aries_harness/references/specs/SPEC-004-hermes-chat-install.md`
- Story-slice pack: `.aries_harness/references/stories/STORY-004-hermes-chat-install.md`
- Architecture design pack: `.aries_harness/decisions/architecture/ARCH-004-hermes-chat-install.md`
- ADR: `.aries_harness/decisions/adrs/ADR-0006-hermes-chat-install.md`
- Installation guide: `docs/HERMES_INSTALL.md`
- Installer skill: `install/hermes-chat-install/SKILL.md`
- Value traceability matrix: `.aries_harness/references/VALUE-TRACEABILITY-MATRIX.md`

## Refresh Triggers

- Hermes changes skill frontmatter requirements, install command behavior, skill roots, or verification commands
- SynapseOS changes Hermes adapter paths, payload layout, or install manifest behavior
- A Hermes registry publication path is added
- Audit log entry: `AUDIT-001`
