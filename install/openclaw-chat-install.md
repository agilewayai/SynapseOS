# SynapseOS OpenClaw Chatbox Install Prompt

Use this prompt inside an OpenClaw channel chatbox to install the SynapseOS skills family.

## Simple Prompt To Paste

```text
Install the SynapseOS skills family for OpenClaw from this installation prompt:
https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw-chat-install.md

Follow the prompt exactly. Show me the target directory and dry-run plan first, then complete the install and verification if the plan is safe.
```

## Instructions For OpenClaw

You are OpenClaw. Install SynapseOS as an OpenClaw skill family.

### Source

- Repository: `https://github.com/agilewayai/SynapseOS.git`
- Raw prompt: `https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/openclaw-chat-install.md`
- Default OpenClaw skill root: `~/.openclaw/skills`
- Managed SynapseOS payload root: `~/.openclaw/skills/synapseos`
- OpenClaw-native skill entries:
  - `~/.openclaw/skills/xuan-master/SKILL.md` with skill name `xuan_master`
  - `~/.openclaw/skills/archon/SKILL.md` with skill name `archon`
  - `~/.openclaw/skills/prism/SKILL.md` with skill name `prism`
  - `~/.openclaw/skills/init/SKILL.md` with skill name `synapse_init`
  - `~/.openclaw/skills/optimization/SKILL.md` with skill name `optimization`

### Safety Policy

- Do not run opaque remote shell.
- Do not overwrite a non-SynapseOS folder without explicit user confirmation.
- Always show the resolved target and dry-run plan before applying writes.
- Prefer HTTPS clone so the install does not require SSH key setup.
- If a command needs approval in this OpenClaw environment, ask for approval with the exact command and reason.
- If OpenClaw is not available on `PATH`, stop after explaining that OpenClaw must be installed first.

### Install Steps

1. Check prerequisites:

```sh
openclaw --version
openclaw doctor
git --version
python3 --version
```

2. Prepare a local checkout:

```sh
INSTALL_ROOT="${TMPDIR:-/tmp}/synapseos-openclaw-install"
if [ -d "$INSTALL_ROOT/.git" ]; then
  git -C "$INSTALL_ROOT" pull --ff-only
else
  git clone https://github.com/agilewayai/SynapseOS.git "$INSTALL_ROOT"
fi
```

3. Inspect SynapseOS readiness:

```sh
cd "$INSTALL_ROOT"
./synapse-cli doctor --json
```

4. Show the OpenClaw install plan:

```sh
./synapse-cli install --agent openclaw --dry-run --json
```

Confirm the plan includes:

- `install_root`: `~/.openclaw/skills/synapseos`
- `install_mode`: `install` for a fresh target or `update` when a previous SynapseOS install exists
- `payload_version` and `previous_installation.payload.version_status`: use these to identify old installed payloads before refresh
- `previous_installation.status`: `fresh`, `legacy_grouped_only`, `update_required`, `native_entries_without_payload`, or `current`
- `native_skill_root`: `~/.openclaw/skills`
- native skill paths for `xuan-master`, `archon`, `prism`, `init`, and `optimization`
- native skill names `xuan_master`, `archon`, `prism`, `synapse_init`, and `optimization`

If `previous_installation.status` is `legacy_grouped_only`, this is the old OpenClaw layout where only `~/.openclaw/skills/synapseos` exists. Treat it as a safe SynapseOS update path if the payload markers are present and there are no direct skill conflicts.

5. If the dry-run target is safe, install:

```sh
./synapse-cli install --agent openclaw --yes --json
```

6. Verify the SynapseOS payload:

```sh
./synapse-cli verify --agent openclaw --json
```

7. Verify OpenClaw's native skill view:

```sh
openclaw skills check --json
openclaw skills list --json
```

The native list should include the SynapseOS layer skills by frontmatter name, including `xuan_master`, `archon`, `prism`, `synapse_init`, and `optimization`. If the grouped payload verifies but these names are missing, rerun the installer from the latest checkout so the direct OpenClaw entries are written.

Use the OpenClaw-safe skill names from the list output when invoking a skill.

### Success Response

After successful verification, explain:

- where the managed SynapseOS payload was installed
- where the OpenClaw-native skill entries were installed
- whether this was a fresh install or an update of a previous install
- whether `synapse-cli verify` passed
- whether `openclaw skills check --json` passed
- whether `openclaw skills list --json` showed the native skill names
- how to start using the skill family

Then tell the user to try:

```text
Use xuan_master. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first SynapseOS skill for my current task.
```

### Failure Response

If any step fails, stop and report:

- the command that failed
- the relevant error message
- whether the failure is prerequisite, checkout, SynapseOS payload verification, or OpenClaw native skill visibility
- whether the dry-run reported `conflict_existing_payload` or `conflict_existing_path`
- the safest next command to retry
