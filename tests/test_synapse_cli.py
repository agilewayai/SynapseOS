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
            {
                "antigravity",
                "antigravity-cli",
                "claude-code",
                "codex",
                "cursor",
                "gemini",
                "opencode",
                "openclaw",
                "hermes",
                "generic",
            },
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

    def test_grouped_adapter_reports_older_payload_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "host"
            run_cli("install", "--agent", "generic", "--target", str(target), "--yes", "--json")

            manifest_path = target / "synapseos" / "synapseos-install-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["payload_version"] = "0.0.1"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            result = run_cli("install", "--agent", "generic", "--target", str(target), "--dry-run", "--json")
            payload = json.loads(result.stdout)
            previous = payload["previous_installation"]

            self.assertEqual("update", payload["install_mode"])
            self.assertEqual("existing_grouped_payload", previous["status"])
            self.assertTrue(previous["update_required"])
            self.assertEqual("0.0.1", previous["payload"]["installed_payload_version"])
            self.assertEqual("older", previous["payload"]["version_status"])

    def test_grouped_adapters_support_update_mode_and_conflict_blocking(self) -> None:
        grouped_adapters = (
            "antigravity",
            "antigravity-cli",
            "claude-code",
            "codex",
            "cursor",
            "gemini",
            "generic",
            "hermes",
            "opencode",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for adapter_id in grouped_adapters:
                target = root / adapter_id

                fresh = run_cli("install", "--agent", adapter_id, "--target", str(target), "--dry-run", "--json")
                install = run_cli("install", "--agent", adapter_id, "--target", str(target), "--yes", "--json")
                update = run_cli("install", "--agent", adapter_id, "--target", str(target), "--dry-run", "--json")
                verify = run_cli("verify", "--agent", adapter_id, "--target", str(target), "--json")

                fresh_payload = json.loads(fresh.stdout)
                install_payload = json.loads(install.stdout)
                update_payload = json.loads(update.stdout)
                verify_payload = json.loads(verify.stdout)

                self.assertEqual("install", fresh_payload["install_mode"], adapter_id)
                self.assertEqual("fresh", fresh_payload["previous_installation"]["status"], adapter_id)
                self.assertEqual("installed", install_payload["status"], adapter_id)
                self.assertEqual("update", update_payload["install_mode"], adapter_id)
                self.assertEqual("existing_grouped_payload", update_payload["previous_installation"]["status"], adapter_id)
                self.assertTrue(update_payload["previous_installation"]["update_required"], adapter_id)
                self.assertEqual("pass", verify_payload["status"], adapter_id)
                self.assertTrue((target / "synapseos" / "xuan-master" / "SKILL.md").exists(), adapter_id)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for adapter_id in grouped_adapters:
                target = root / adapter_id
                unknown_payload = target / "synapseos"
                unknown_payload.mkdir(parents=True)
                (unknown_payload / "README.txt").write_text("not a SynapseOS install\n", encoding="utf-8")

                result = run_cli(
                    "install",
                    "--agent",
                    adapter_id,
                    "--target",
                    str(target),
                    "--dry-run",
                    "--json",
                    check=False,
                )
                payload = json.loads(result.stdout)

                self.assertEqual(1, result.returncode, adapter_id)
                self.assertEqual("error", payload["status"], adapter_id)
                self.assertEqual("existing_unrecognized_payload", payload["previous_installation"]["status"], adapter_id)
                self.assertTrue(
                    any(operation["action"] == "conflict_existing_payload" for operation in payload["operations"]),
                    adapter_id,
                )

    def test_openclaw_install_adds_native_skill_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "openclaw-skills"

            dry_run = run_cli("install", "--agent", "openclaw", "--target", str(target), "--dry-run", "--json")
            install = run_cli("install", "--agent", "openclaw", "--target", str(target), "--yes", "--json")
            verify = run_cli("verify", "--agent", "openclaw", "--target", str(target), "--json")
            second_dry_run = run_cli("install", "--agent", "openclaw", "--target", str(target), "--dry-run", "--json")

            dry_run_payload = json.loads(dry_run.stdout)
            install_payload = json.loads(install.stdout)
            verify_payload = json.loads(verify.stdout)
            second_dry_run_payload = json.loads(second_dry_run.stdout)
            planned_destinations = {operation["destination"] for operation in dry_run_payload["operations"]}

            self.assertEqual("planned", dry_run_payload["status"])
            self.assertEqual(str(target / "synapseos"), dry_run_payload["install_root"])
            self.assertEqual(str(target), dry_run_payload["native_skill_root"])
            self.assertEqual("xuan_master", dry_run_payload["native_skill_names"]["xuan-master"])
            self.assertEqual("synapse_init", dry_run_payload["native_skill_names"]["init"])
            self.assertIn(str(target / "xuan-master"), planned_destinations)
            self.assertIn(str(target / "archon"), planned_destinations)
            self.assertIn(str(target / "prism"), planned_destinations)
            self.assertIn(str(target / "init"), planned_destinations)
            self.assertIn(str(target / "optimization"), planned_destinations)

            self.assertEqual("installed", install_payload["status"])
            self.assertEqual("pass", verify_payload["status"])
            self.assertTrue((target / "synapseos" / "synapse-cli").exists())
            self.assertTrue((target / "xuan-master" / "SKILL.md").exists())
            self.assertTrue((target / "archon" / "SKILL.md").exists())
            self.assertTrue((target / "prism" / "SKILL.md").exists())
            self.assertTrue((target / "init" / "SKILL.md").exists())
            self.assertTrue((target / "optimization" / "SKILL.md").exists())
            self.assertTrue((target / "xuan-master" / "00-entry" / "SKILL.md").exists())
            self.assertIn("name: xuan_master", (target / "xuan-master" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertIn("name: synapse_init", (target / "init" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertTrue(any(check["id"] == "openclaw-native/xuan-master/SKILL.md" for check in verify_payload["checks"]))
            self.assertEqual("current", second_dry_run_payload["previous_installation"]["status"])
            self.assertFalse(second_dry_run_payload["previous_installation"]["update_required"])

    def test_openclaw_current_layout_reports_update_when_payload_version_is_old(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "openclaw-skills"
            run_cli("install", "--agent", "openclaw", "--target", str(target), "--yes", "--json")

            manifest_path = target / "synapseos" / "synapseos-install-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["payload_version"] = "0.0.1"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            dry_run = run_cli("install", "--agent", "openclaw", "--target", str(target), "--dry-run", "--json")
            dry_run_payload = json.loads(dry_run.stdout)
            previous = dry_run_payload["previous_installation"]

            self.assertEqual("update", dry_run_payload["install_mode"])
            self.assertEqual("update_required", previous["status"])
            self.assertTrue(previous["update_required"])
            self.assertEqual("older", previous["payload"]["version_status"])

    def test_openclaw_current_entries_report_update_when_manifest_is_not_openclaw_current(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "openclaw-skills"
            run_cli("install", "--agent", "openclaw", "--target", str(target), "--yes", "--json")

            manifest_path = target / "synapseos" / "synapseos-install-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["adapter"] = "generic"
            manifest.pop("native_skill_paths", None)
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            dry_run = run_cli("install", "--agent", "openclaw", "--target", str(target), "--dry-run", "--json")
            previous = json.loads(dry_run.stdout)["previous_installation"]

            self.assertEqual("update_required", previous["status"])
            self.assertTrue(previous["update_required"])
            self.assertEqual("generic", previous["payload"]["manifest_adapter"])

    def test_openclaw_install_blocks_non_synapseos_native_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "openclaw-skills"
            conflicting_skill = target / "xuan-master"
            conflicting_skill.mkdir(parents=True)
            (conflicting_skill / "SKILL.md").write_text("---\nname: other-skill\n---\n", encoding="utf-8")

            result = run_cli(
                "install",
                "--agent",
                "openclaw",
                "--target",
                str(target),
                "--dry-run",
                "--json",
                check=False,
            )
            payload = json.loads(result.stdout)

            self.assertEqual(1, result.returncode)
            self.assertEqual("error", payload["status"])
            self.assertTrue(any(operation["action"] == "conflict_existing_path" for operation in payload["operations"]))

    def test_openclaw_install_updates_legacy_grouped_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "openclaw-skills"
            run_cli("install", "--agent", "generic", "--target", str(target), "--yes", "--json")
            manifest_path = target / "synapseos" / "synapseos-install-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["adapter"] = "openclaw"
            manifest.pop("native_skill_paths", None)
            manifest.pop("native_skill_names", None)
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            dry_run = run_cli("install", "--agent", "openclaw", "--target", str(target), "--dry-run", "--json")
            install = run_cli("install", "--agent", "openclaw", "--target", str(target), "--yes", "--json")
            verify = run_cli("verify", "--agent", "openclaw", "--target", str(target), "--json")

            dry_run_payload = json.loads(dry_run.stdout)
            install_payload = json.loads(install.stdout)
            verify_payload = json.loads(verify.stdout)

            self.assertEqual("planned", dry_run_payload["status"])
            self.assertEqual("update", dry_run_payload["install_mode"])
            self.assertEqual("legacy_grouped_only", dry_run_payload["previous_installation"]["status"])
            self.assertTrue(dry_run_payload["previous_installation"]["update_required"])
            self.assertEqual("update", install_payload["install_mode"])
            self.assertEqual("pass", verify_payload["status"])
            self.assertTrue((target / "xuan-master" / "SKILL.md").exists())
            self.assertIn("name: xuan_master", (target / "xuan-master" / "SKILL.md").read_text(encoding="utf-8"))

    def test_openclaw_install_blocks_unrecognized_existing_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "openclaw-skills"
            unknown_payload = target / "synapseos"
            unknown_payload.mkdir(parents=True)
            (unknown_payload / "README.txt").write_text("not a SynapseOS install\n", encoding="utf-8")

            result = run_cli(
                "install",
                "--agent",
                "openclaw",
                "--target",
                str(target),
                "--dry-run",
                "--json",
                check=False,
            )
            payload = json.loads(result.stdout)

            self.assertEqual(1, result.returncode)
            self.assertEqual("error", payload["status"])
            self.assertEqual("existing_unrecognized_payload", payload["previous_installation"]["status"])
            self.assertTrue(any(operation["action"] == "conflict_existing_payload" for operation in payload["operations"]))

    def test_hermes_install_updates_existing_grouped_install(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "hermes-skills"

            first = run_cli("install", "--agent", "hermes", "--target", str(target), "--yes", "--json")
            dry_run = run_cli("install", "--agent", "hermes", "--target", str(target), "--dry-run", "--json")
            update = run_cli("install", "--agent", "hermes", "--target", str(target), "--yes", "--json")
            verify = run_cli("verify", "--agent", "hermes", "--target", str(target), "--json")

            first_payload = json.loads(first.stdout)
            dry_run_payload = json.loads(dry_run.stdout)
            update_payload = json.loads(update.stdout)
            verify_payload = json.loads(verify.stdout)

            self.assertEqual("installed", first_payload["status"])
            self.assertEqual("planned", dry_run_payload["status"])
            self.assertEqual("update", dry_run_payload["install_mode"])
            self.assertEqual("existing_grouped_payload", dry_run_payload["previous_installation"]["status"])
            self.assertTrue(dry_run_payload["previous_installation"]["update_required"])
            self.assertEqual("update", update_payload["install_mode"])
            self.assertEqual("pass", verify_payload["status"])
            self.assertEqual("existing_grouped_payload", verify_payload["previous_installation"]["status"])
            self.assertTrue((target / "synapseos" / "xuan-master" / "SKILL.md").exists())

    def test_hermes_install_blocks_unrecognized_existing_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "hermes-skills"
            unknown_payload = target / "synapseos"
            unknown_payload.mkdir(parents=True)
            (unknown_payload / "README.txt").write_text("not a SynapseOS install\n", encoding="utf-8")

            result = run_cli(
                "install",
                "--agent",
                "hermes",
                "--target",
                str(target),
                "--dry-run",
                "--json",
                check=False,
            )
            payload = json.loads(result.stdout)

            self.assertEqual(1, result.returncode)
            self.assertEqual("error", payload["status"])
            self.assertEqual("existing_unrecognized_payload", payload["previous_installation"]["status"])
            self.assertTrue(any(operation["action"] == "conflict_existing_payload" for operation in payload["operations"]))

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
