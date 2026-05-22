#!/usr/bin/env sh
set -eu

DEFAULT_REPO="https://github.com/agilewayai/SynapseOS.git"
DEFAULT_REF="main"
DEFAULT_INSTALL_DIR="$HOME/.synapseos/SynapseOS"
DEFAULT_BIN_DIR="$HOME/.local/bin"

repo="${SYNAPSEOS_REPO:-$DEFAULT_REPO}"
ref="${SYNAPSEOS_REF:-$DEFAULT_REF}"
install_dir="${SYNAPSEOS_INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
bin_dir="${SYNAPSEOS_BIN_DIR:-$DEFAULT_BIN_DIR}"
agent="${SYNAPSEOS_AGENT:-}"
target="${SYNAPSEOS_TARGET:-}"
strategy="${SYNAPSEOS_STRATEGY:-copy}"
yes="${SYNAPSEOS_YES:-0}"
dry_run="${SYNAPSEOS_DRY_RUN:-0}"
skip_doctor="${SYNAPSEOS_SKIP_DOCTOR:-0}"
verbose="${SYNAPSEOS_VERBOSE:-0}"

usage() {
    cat <<'EOF'
SynapseOS one-line installer

Usage:
  curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash
  curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash -s -- --agent codex --yes
  curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash -s -- --agent generic --target /path/to/host --yes

Options:
  --agent <id>          Also install the skills stack into this agent host.
  --target <path>      Host base directory for adapters that need an explicit target.
  --strategy <mode>    synapse-cli install strategy: copy or symlink. Default: copy.
  --yes                Apply the agent install after showing the dry-run plan.
  --dry-run            Only show the agent install plan.
  --repo <url-or-path> Repository to clone. Default: official GitHub repository.
  --ref <ref>          Git ref to install. Default: main.
  --install-dir <path> Managed checkout path. Default: ~/.synapseos/SynapseOS.
  --bin-dir <path>     Directory for the synapse-cli launcher. Default: ~/.local/bin.
  --skip-doctor        Skip the post-install doctor check.
  --verbose            Show full doctor JSON and command details.
  -h, --help           Show this help.

Environment variables mirror the option names:
  SYNAPSEOS_AGENT, SYNAPSEOS_TARGET, SYNAPSEOS_YES, SYNAPSEOS_REPO,
  SYNAPSEOS_REF, SYNAPSEOS_INSTALL_DIR, SYNAPSEOS_BIN_DIR, SYNAPSEOS_VERBOSE.
EOF
}

log() {
    printf '%s\n' "synapseos-install: $*"
}

agent_label() {
    case "$1" in
        claude-code) printf '%s\n' "Claude Code" ;;
        codex) printf '%s\n' "Codex" ;;
        cursor) printf '%s\n' "Cursor" ;;
        opencode) printf '%s\n' "OpenCode" ;;
        gemini) printf '%s\n' "Gemini CLI" ;;
        antigravity) printf '%s\n' "Google Antigravity" ;;
        antigravity-cli) printf '%s\n' "Antigravity CLI" ;;
        openclaw) printf '%s\n' "OpenClaw" ;;
        hermes) printf '%s\n' "Hermes" ;;
        generic) printf '%s\n' "Generic Agent Host" ;;
        *) printf '%s\n' "$1" ;;
    esac
}

die() {
    printf '%s\n' "synapseos-install: error: $*" >&2
    exit 1
}

need_arg() {
    [ "$#" -ge 2 ] || die "missing value for $1"
}

expand_path() {
    case "$1" in
        "~")
            printf '%s\n' "$HOME"
            ;;
        "~/"*)
            printf '%s/%s\n' "$HOME" "${1#~/}"
            ;;
        *)
            printf '%s\n' "$1"
            ;;
    esac
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --agent)
            need_arg "$@"
            agent="$2"
            shift 2
            ;;
        --target)
            need_arg "$@"
            target="$2"
            shift 2
            ;;
        --strategy)
            need_arg "$@"
            strategy="$2"
            shift 2
            ;;
        --yes)
            yes="1"
            shift
            ;;
        --dry-run)
            dry_run="1"
            shift
            ;;
        --repo)
            need_arg "$@"
            repo="$2"
            shift 2
            ;;
        --ref)
            need_arg "$@"
            ref="$2"
            shift 2
            ;;
        --install-dir)
            need_arg "$@"
            install_dir="$2"
            shift 2
            ;;
        --bin-dir)
            need_arg "$@"
            bin_dir="$2"
            shift 2
            ;;
        --skip-doctor)
            skip_doctor="1"
            shift
            ;;
        --verbose)
            verbose="1"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "unknown option: $1"
            ;;
    esac
done

install_dir="$(expand_path "$install_dir")"
bin_dir="$(expand_path "$bin_dir")"

command -v git >/dev/null 2>&1 || die "git is required"
command -v python3 >/dev/null 2>&1 || die "python3 is required"

case "$strategy" in
    copy|symlink)
        ;;
    *)
        die "--strategy must be copy or symlink"
        ;;
esac

install_parent="$(dirname "$install_dir")"
mkdir -p "$install_parent"

if [ -d "$install_dir/.git" ]; then
    log "Updating managed checkout at $install_dir"
    if [ -n "$(git -C "$install_dir" status --porcelain)" ]; then
        die "$install_dir has local changes; refusing to overwrite them"
    fi
    git -C "$install_dir" fetch --quiet --depth 1 origin "$ref"
    git -C "$install_dir" checkout --quiet --detach FETCH_HEAD >/dev/null
elif [ -e "$install_dir" ]; then
    die "$install_dir exists but is not a git checkout; choose another --install-dir"
else
    log "Installing managed checkout at $install_dir"
    if [ -d "$repo/.git" ]; then
        git clone --quiet --no-local --depth 1 "$repo" "$install_dir"
    else
        git clone --quiet --depth 1 "$repo" "$install_dir"
    fi
    if [ -n "$ref" ]; then
        git -C "$install_dir" fetch --quiet --depth 1 origin "$ref" >/dev/null 2>&1 || true
        git -C "$install_dir" checkout --quiet --detach FETCH_HEAD >/dev/null 2>&1 || git -C "$install_dir" checkout --quiet "$ref" >/dev/null
    fi
fi

[ -x "$install_dir/synapse-cli" ] || die "synapse-cli was not found in $install_dir"
log "Skills stack fetched at $install_dir"

mkdir -p "$bin_dir"
launcher="$bin_dir/synapse-cli"
cat > "$launcher" <<EOF
#!/usr/bin/env sh
exec python3 "$install_dir/synapse-cli" "\$@"
EOF
chmod +x "$launcher"

log "Installed launcher at $launcher"

case ":$PATH:" in
    *":$bin_dir:"*)
        ;;
    *)
        log "Add $bin_dir to PATH to run synapse-cli directly"
        ;;
esac

summarize_doctor() {
    python3 - "$1" "$2" "$3" <<'PY'
import json
import sys

doctor_path, err_path, launcher = sys.argv[1:4]

def log(message):
    print(f"synapseos-install: {message}")

try:
    with open(doctor_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
except Exception:
    log("Readiness: failed")
    log("Reason: doctor output could not be parsed")
    try:
        with open(err_path, "r", encoding="utf-8") as handle:
            first_error = handle.read().strip().splitlines()[0]
    except Exception:
        first_error = ""
    if first_error:
        log(f"Detail: {first_error}")
    log(f"Next: run {launcher} doctor --json for details")
    sys.exit(0)

status = payload.get("status", "unknown")
checks = payload.get("checks", [])
hosts = payload.get("hosts", [])

if status == "pass":
    detected_hosts = [host.get("adapter_id") for host in hosts if host.get("detected")]
    log("Readiness: pass")
    if detected_hosts:
        log("Detected hosts: " + ", ".join(detected_hosts))
    sys.exit(0)

log("Readiness: failed")

required_failures = [
    check for check in checks
    if check.get("required") and check.get("status") == "fail"
]

if not required_failures:
    log(f"Reason: doctor status is {status}")
else:
    for check in required_failures:
        check_id = check.get("id", "unknown")
        detected = check.get("detected")
        hint = check.get("hint")
        if check_id == "python":
            if detected:
                log(f"Required action: install Python 3.8 or newer (detected {detected})")
            else:
                log("Required action: install Python 3.8 or newer")
        elif hint:
            log(f"Required action: {hint}")
        else:
            log(f"Required action: fix failed check '{check_id}'")

log(f"Next: run {launcher} doctor --json for details after fixing prerequisites")
PY
}

summarize_agent_result() {
    python3 - "$1" "$2" <<'PY'
import json
import sys

result_path, stage = sys.argv[1:3]

def log(message):
    print(f"synapseos-install: {message}")

try:
    with open(result_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
except Exception:
    log(f"{stage}: output could not be parsed")
    sys.exit(0)

DISPLAY_NAMES = {
    "claude-code": "Claude Code",
    "codex": "Codex",
    "cursor": "Cursor",
    "opencode": "OpenCode",
    "gemini": "Gemini CLI",
    "antigravity": "Google Antigravity",
    "antigravity-cli": "Antigravity CLI",
    "openclaw": "OpenClaw",
    "hermes": "Hermes",
    "generic": "Generic Agent Host",
}

adapter = payload.get("adapter", "agent")
name = payload.get("display_name") or DISPLAY_NAMES.get(adapter, adapter)
status = payload.get("status", "unknown")
target = payload.get("install_root")
version = payload.get("payload_version")
previous = payload.get("previous_installation") or {}
previous_status = previous.get("status")
payload_state = previous.get("payload") or {}
version_status = payload_state.get("version_status")

if stage == "plan":
    if status != "planned":
        log(f"Plan: blocked for {name}")
        errors = [op for op in payload.get("operations", []) if op.get("status") == "error"]
        for operation in errors[:3]:
            action = operation.get("action", "error")
            destination = operation.get("destination")
            if destination:
                log(f"Reason: {action} at {destination}")
            else:
                log(f"Reason: {action}")
    else:
        mode = payload.get("install_mode", "install")
        if previous_status in {"existing_grouped_payload", "legacy_grouped_only", "update_required", "current"}:
            description = "refresh"
        elif previous_status == "native_entries_without_payload":
            description = "repair"
        else:
            description = "fresh install" if mode == "install" else "refresh"
        log(f"Plan: {description} for {name}")
        if target:
            log(f"Target: {target}")
        if version:
            log(f"Version: {version}")
        if version_status == "older":
            installed_version = payload_state.get("installed_payload_version")
            if installed_version:
                log(f"Existing version: {installed_version} -> {version}")
        if payload.get("native_skill_root"):
            log(f"Native skill entries: {payload.get('native_skill_root')}")
        actions = {op.get("action") for op in payload.get("operations", []) if op.get("status") == "planned"}
        changes = []
        if "copy" in actions:
            changes.append("copy SynapseOS payload")
        if "symlink" in actions:
            changes.append("link SynapseOS payload")
        if "copy_openclaw_skill" in actions:
            changes.append("refresh OpenClaw-native skill entries")
        if "write_manifest" in actions:
            changes.append("write install manifest")
        if changes:
            log("Planned changes: " + ", ".join(changes))
    sys.exit(0)

if stage == "apply":
    if status == "installed":
        log(f"Install: complete for {name}")
        if target:
            log(f"Target: {target}")
        manifest = payload.get("manifest")
        if manifest:
            log(f"Manifest: {manifest}")
    else:
        log(f"Install: failed for {name}")
        message = payload.get("message")
        if message:
            log(f"Reason: {message}")
    sys.exit(0)

if stage == "verify":
    checks = payload.get("checks", [])
    failed = [check for check in checks if check.get("status") != "pass"]
    if status == "pass":
        log(f"Verify: pass for {name} ({len(checks)} checks)")
        if target:
            log(f"Installed at: {target}")
    else:
        log(f"Verify: failed for {name}")
        for check in failed[:5]:
            check_id = check.get("id", "unknown")
            log(f"Failed check: {check_id}")
    sys.exit(0)

log(f"{stage}: {status}")
PY
}

show_json_if_verbose() {
    if [ "$verbose" = "1" ] && [ -s "$1" ]; then
        cat "$1"
    fi
}

doctor_status="skipped"
if [ "$skip_doctor" != "1" ]; then
    doctor_out="${TMPDIR:-/tmp}/synapseos-doctor-$$.json"
    doctor_err="${TMPDIR:-/tmp}/synapseos-doctor-$$.err"

    log "Checking readiness"
    if "$launcher" doctor --json >"$doctor_out" 2>"$doctor_err"; then
        doctor_status="pass"
    else
        doctor_status="fail"
    fi

    if [ "$verbose" = "1" ]; then
        [ ! -s "$doctor_out" ] || cat "$doctor_out"
        [ ! -s "$doctor_err" ] || cat "$doctor_err" >&2
    fi

    summarize_doctor "$doctor_out" "$doctor_err" "$launcher"
    rm -f "$doctor_out" "$doctor_err"
fi

run_install_plan() {
    if [ -n "$target" ]; then
        "$launcher" install --agent "$agent" --target "$target" --strategy "$strategy" --dry-run --json
    else
        "$launcher" install --agent "$agent" --strategy "$strategy" --dry-run --json
    fi
}

run_install_apply() {
    if [ -n "$target" ]; then
        "$launcher" install --agent "$agent" --target "$target" --strategy "$strategy" --yes --json
    else
        "$launcher" install --agent "$agent" --strategy "$strategy" --yes --json
    fi
}

run_verify() {
    if [ -n "$target" ]; then
        "$launcher" verify --agent "$agent" --target "$target" --json
    else
        "$launcher" verify --agent "$agent" --json
    fi
}

if [ -n "$agent" ]; then
    agent_name="$(agent_label "$agent")"

    if [ "$doctor_status" = "fail" ]; then
        log "Result: CLI installed, skills install not started"
        die "fix readiness issues first, then rerun with --agent $agent --yes"
    fi

    log "Planning skills install for $agent_name"
    plan_out="${TMPDIR:-/tmp}/synapseos-plan-$$.json"
    if run_install_plan >"$plan_out"; then
        plan_status="pass"
    else
        plan_status="fail"
    fi
    show_json_if_verbose "$plan_out"
    summarize_agent_result "$plan_out" "plan"
    if [ "$plan_status" != "pass" ]; then
        rm -f "$plan_out"
        die "skills install plan failed"
    fi

    if [ "$dry_run" = "1" ] || [ "$yes" != "1" ]; then
        rm -f "$plan_out"
        log "Dry-run complete. Re-run with --yes to apply the skills install."
        exit 0
    fi
    rm -f "$plan_out"

    log "Applying skills install for $agent_name"
    apply_out="${TMPDIR:-/tmp}/synapseos-apply-$$.json"
    if run_install_apply >"$apply_out"; then
        apply_status="pass"
    else
        apply_status="fail"
    fi
    show_json_if_verbose "$apply_out"
    summarize_agent_result "$apply_out" "apply"
    if [ "$apply_status" != "pass" ]; then
        rm -f "$apply_out"
        die "skills install failed"
    fi
    rm -f "$apply_out"

    log "Verifying skills install for $agent_name"
    verify_out="${TMPDIR:-/tmp}/synapseos-verify-$$.json"
    if run_verify >"$verify_out"; then
        verify_status="pass"
    else
        verify_status="fail"
    fi
    show_json_if_verbose "$verify_out"
    summarize_agent_result "$verify_out" "verify"
    if [ "$verify_status" != "pass" ]; then
        rm -f "$verify_out"
        die "skills verification failed"
    fi
    rm -f "$verify_out"
    log "Result: SynapseOS skills installed for $agent_name"
else
    if [ "$doctor_status" = "fail" ]; then
        log "Result: CLI installed with readiness issues"
    else
        log "Result: CLI installed"
    fi
    log "Install skills with: curl -fsSL https://raw.githubusercontent.com/agilewayai/SynapseOS/main/install/synapseos.sh | bash -s -- --agent codex --yes"
fi
