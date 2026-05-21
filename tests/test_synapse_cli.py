from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "synapse-cli"


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result


class SynapseCliTests(unittest.TestCase):
    def test_help_lists_commands(self) -> None:
        result = run_cli("--help")

        self.assertIn("doctor", result.stdout)
        self.assertIn("install", result.stdout)
        self.assertIn("verify", result.stdout)

    def test_doctor_json_reports_prerequisites(self) -> None:
        result = run_cli("doctor", "--json", check=False)
        payload = json.loads(result.stdout)

        self.assertIn(payload["status"], {"pass", "fail"})
        self.assertTrue(any(check["id"] == "python" for check in payload["checks"]))
        self.assertTrue(all("installable" in check for check in payload["checks"]))
        self.assertIn("missing_required", payload)
        self.assertIn("installable_missing", payload)
        self.assertTrue(any(host["adapter_id"] == "generic" for host in payload["hosts"]))

    def test_list_agents_json_includes_supported_hosts(self) -> None:
        result = run_cli("list-agents", "--json")
        payload = json.loads(result.stdout)
        adapter_ids = {agent["adapter_id"] for agent in payload["agents"]}

        self.assertEqual(
            {"claude-code", "codex", "cursor", "opencode", "openclaw", "hermes", "generic"},
            adapter_ids,
        )

    def test_init_writes_metadata_to_selected_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            metadata_dir = Path(temp_dir) / "state"
            result = run_cli("init", "--json", "--metadata-dir", str(metadata_dir))
            payload = json.loads(result.stdout)

            self.assertEqual("initialized", payload["status"])
            self.assertTrue((metadata_dir / "state.json").exists())

    def test_generic_install_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "host"
            result = run_cli("install", "--agent", "generic", "--target", str(target), "--dry-run", "--json")
            payload = json.loads(result.stdout)

            self.assertEqual("planned", payload["status"])
            self.assertFalse((target / "synapseos").exists())
            self.assertTrue(any(operation["action"] == "copy" for operation in payload["operations"]))

    def test_generic_install_and_verify_are_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "host"

            first = run_cli("install", "--agent", "generic", "--target", str(target), "--yes", "--json")
            second = run_cli("install", "--agent", "generic", "--target", str(target), "--yes", "--json")
            verify = run_cli("verify", "--agent", "generic", "--target", str(target), "--json")

            first_payload = json.loads(first.stdout)
            second_payload = json.loads(second.stdout)
            verify_payload = json.loads(verify.stdout)

            self.assertEqual("installed", first_payload["status"])
            self.assertEqual("installed", second_payload["status"])
            self.assertEqual("pass", verify_payload["status"])
            self.assertTrue((target / "synapseos" / "synapse-cli").exists())
            self.assertTrue((target / "synapseos" / "xuan-master" / "SKILL.md").exists())
            self.assertTrue((target / "synapseos" / "synapseos-install-manifest.json").exists())

    def test_install_requires_yes_without_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_cli(
                "install",
                "--agent",
                "generic",
                "--target",
                str(Path(temp_dir) / "host"),
                "--json",
                check=False,
            )
            payload = json.loads(result.stdout)

            self.assertEqual(2, result.returncode)
            self.assertEqual("blocked", payload["status"])


if __name__ == "__main__":
    unittest.main()
