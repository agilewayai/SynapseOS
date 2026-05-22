from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from . import __version__
from .adapters import ADAPTERS, get_adapter
from .installer import apply_plan, build_plan, verify_install
from .prerequisites import check_prerequisites


REPO_ROOT = Path(__file__).resolve().parents[2]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def emit(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    status = result.get("status", "unknown")
    print(f"status: {status}")
    if "message" in result:
        print(f"message: {result['message']}")
    if "install_root" in result:
        print(f"install_root: {result['install_root']}")
    if "install_mode" in result:
        print(f"install_mode: {result['install_mode']}")
    if "native_skill_root" in result and result.get("native_skill_root"):
        print(f"native_skill_root: {result['native_skill_root']}")
    if result.get("previous_installation"):
        previous = result["previous_installation"]
        print(f"previous_installation: {previous.get('status')} update_required={previous.get('update_required')}")
    if "manifest" in result:
        print(f"manifest: {result['manifest']}")
    for check in result.get("checks", []):
        print(f"- {check.get('id')}: {check.get('status')} ({check.get('detected') or check.get('path')})")
    for host in result.get("hosts", []):
        detected = "detected" if host.get("detected") else "not detected"
        target = host.get("target_base") or "no target"
        print(f"- {host.get('adapter_id')}: {detected}; target={target}")
    for operation in result.get("operations", []):
        source = operation.get("source") or "-"
        print(f"- {operation.get('action')}: {source} -> {operation.get('destination')} [{operation.get('status')}]")


def command_doctor(args: argparse.Namespace) -> int:
    result = check_prerequisites(REPO_ROOT)
    if args.install_missing:
        result["requested_install_missing"] = True
        result["install_missing_approved"] = bool(args.yes)
        result["message"] = result["install_missing_hint"]
    emit(result, args.json)
    return 0 if result["status"] == "pass" else 1


def command_init(args: argparse.Namespace) -> int:
    metadata_dir = Path(args.metadata_dir).expanduser()
    if not metadata_dir.is_absolute():
        metadata_dir = REPO_ROOT / metadata_dir
    state_path = metadata_dir / "state.json"
    result = {
        "status": "planned" if args.dry_run else "initialized",
        "metadata_dir": str(metadata_dir),
        "state_path": str(state_path),
        "dry_run": args.dry_run,
    }

    if not args.dry_run:
        metadata_dir.mkdir(parents=True, exist_ok=True)
        state = {
            "schema_version": 1,
            "initialized_at": now_utc(),
            "repo_root": str(REPO_ROOT),
            "synapse_cli_version": __version__,
        }
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    emit(result, args.json)
    return 0


def command_list_agents(args: argparse.Namespace) -> int:
    result = {
        "status": "pass",
        "agents": [adapter.detect().__dict__ for adapter in ADAPTERS.values()],
    }
    emit(result, args.json)
    return 0


def command_install(args: argparse.Namespace) -> int:
    try:
        adapter = get_adapter(args.agent)
    except ValueError as exc:
        emit({"status": "error", "message": str(exc)}, args.json)
        return 2

    plan = build_plan(REPO_ROOT, adapter, args.target, args.strategy)
    if args.dry_run:
        plan["dry_run"] = True
        emit(plan, args.json)
        return 0 if plan.get("status") == "planned" else 1

    if not args.yes:
        result = {
            "status": "blocked",
            "message": "install writes outside the source tree require --yes; rerun with --dry-run to inspect the plan first",
            "plan": plan,
        }
        emit(result, args.json)
        return 2

    result = apply_plan(REPO_ROOT, plan)
    emit(result, args.json)
    return 0 if result["status"] == "installed" else 1


def command_verify(args: argparse.Namespace) -> int:
    try:
        adapter = get_adapter(args.agent)
    except ValueError as exc:
        emit({"status": "error", "message": str(exc)}, args.json)
        return 2

    result = verify_install(adapter, args.target)
    emit(result, args.json)
    return 0 if result["status"] == "pass" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="synapse-cli", description="SynapseOS initialization and installation CLI")
    parser.add_argument("--version", action="version", version=f"synapse-cli {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser("doctor", help="check prerequisites, permissions, and known agent hosts")
    doctor.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    doctor.add_argument("--install-missing", action="store_true", help="request prerequisite installation planning")
    doctor.add_argument("--yes", action="store_true", help="approve supported remediation actions")
    doctor.set_defaults(func=command_doctor)

    init_cmd = subcommands.add_parser("init", help="create or refresh repo-local SynapseOS initialization metadata")
    init_cmd.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    init_cmd.add_argument("--dry-run", action="store_true", help="show planned metadata writes without applying them")
    init_cmd.add_argument("--metadata-dir", default=".synapseos", help="metadata directory, relative to repo root unless absolute")
    init_cmd.set_defaults(func=command_init)

    list_agents = subcommands.add_parser("list-agents", help="list supported agent host adapters and detection status")
    list_agents.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    list_agents.set_defaults(func=command_list_agents)

    install = subcommands.add_parser("install", help="plan or apply installation into an agent host")
    install.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    install.add_argument("--agent", required=True, choices=sorted(ADAPTERS), help="agent host adapter id")
    install.add_argument("--target", help="host base directory; final managed install root is <target>/synapseos unless target already ends with synapseos")
    install.add_argument("--strategy", choices=("copy", "symlink"), default="copy", help="installation strategy")
    install.add_argument("--dry-run", action="store_true", help="show planned writes without applying them")
    install.add_argument("--yes", action="store_true", help="approve applying the install plan")
    install.set_defaults(func=command_install)

    verify = subcommands.add_parser("verify", help="verify installed SynapseOS entrypoints for an agent host")
    verify.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    verify.add_argument("--agent", required=True, choices=sorted(ADAPTERS), help="agent host adapter id")
    verify.add_argument("--target", help="host base directory used during installation")
    verify.set_defaults(func=command_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
