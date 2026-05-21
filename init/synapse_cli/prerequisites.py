from __future__ import annotations

from pathlib import Path
import os
import platform
import shutil
import sys

from .adapters import ADAPTERS


def _check(
    check_id: str,
    required: bool,
    status: str,
    detected: str | None,
    hint: str,
    installable: bool = False,
    category: str = "runtime",
) -> dict:
    return {
        "id": check_id,
        "category": category,
        "required": required,
        "status": status,
        "detected": detected,
        "missing": status == "fail",
        "installable": installable,
        "hint": hint,
    }


def check_prerequisites(repo_root: Path) -> dict:
    checks = []

    checks.append(_check(
        check_id="python",
        required=True,
        status="pass" if sys.version_info >= (3, 9) else "fail",
        detected=platform.python_version(),
        hint="Use Python 3.9 or newer.",
        installable=False,
    ))

    git_path = shutil.which("git")
    checks.append(_check(
        check_id="git",
        required=True,
        status="pass" if git_path else "fail",
        detected=git_path,
        hint="Install Git and ensure it is available on PATH.",
        installable=False,
    ))

    checks.append(_check(
        check_id="repo-root",
        required=True,
        status="pass" if (repo_root / "AGENTS.md").exists() else "fail",
        detected=str(repo_root),
        hint="Run synapse-cli from the SynapseOS repository or use the bundled launcher.",
        installable=False,
        category="repository",
    ))

    required_payload = ["xuan-master/SKILL.md", "archon/SKILL.md", "prism/SKILL.md", "init/SKILL.md"]
    missing_payload = [relative for relative in required_payload if not (repo_root / relative).exists()]
    checks.append(_check(
        check_id="synapse-payload",
        required=True,
        status="pass" if not missing_payload else "fail",
        detected="complete" if not missing_payload else f"missing: {', '.join(missing_payload)}",
        hint="Restore the missing SynapseOS entrypoint files before installation.",
        installable=False,
        category="repository",
    ))

    checks.append(_check(
        check_id="repo-writable",
        required=False,
        status="pass" if os.access(repo_root, os.W_OK) else "warn",
        detected=str(repo_root),
        hint="Repo-local init metadata requires write access to this checkout.",
        installable=False,
        category="filesystem",
    ))

    host_results = [adapter.detect().__dict__ for adapter in ADAPTERS.values()]
    missing_required = [check["id"] for check in checks if check["required"] and check["status"] == "fail"]
    missing_optional = [check["id"] for check in checks if not check["required"] and check["status"] in {"fail", "warn"}]
    installable_missing = [check["id"] for check in checks if check["missing"] and check["installable"]]
    status = "pass" if all(check["status"] == "pass" for check in checks if check["required"]) else "fail"
    return {
        "status": status,
        "checks": checks,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
        "installable_missing": installable_missing,
        "hosts": host_results,
        "install_missing_supported": False,
        "install_missing_hint": "Automatic prerequisite installation is intentionally not implemented in the local baseline; install missing tools manually, then rerun doctor.",
    }
