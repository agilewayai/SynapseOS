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
- Default OpenClaw target: `~/.openclaw/skills/synapseos`

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

### Success Response

After successful verification, explain:

- where SynapseOS was installed
- whether `synapse-cli verify` passed
- whether `openclaw skills check --json` passed
- how to start using the skill family

Then tell the user to try:

```text
Load SynapseOS. Explain when I should use Xuan Master, Archon, Prism, and Init, then recommend the first skill for my current task.
```

### Failure Response

If any step fails, stop and report:

- the command that failed
- the relevant error message
- whether the failure is prerequisite, checkout, SynapseOS payload verification, or OpenClaw native skill visibility
- the safest next command to retry
