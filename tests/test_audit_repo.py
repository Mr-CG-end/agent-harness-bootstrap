from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = (
    ROOT
    / "skills"
    / "bootstrap-project-harness"
    / "scripts"
    / "audit_repo.py"
)
SPEC = importlib.util.spec_from_file_location("audit_repo", AUDIT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {AUDIT_PATH}")
AUDIT_REPO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT_REPO)


class AuditRepositoryTests(unittest.TestCase):
    def test_empty_directory_is_greenfield(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = AUDIT_REPO.audit(Path(directory))

        self.assertEqual(report["mode"], "greenfield")
        self.assertEqual(report["source_file_count_capped"], 0)
        self.assertIn(
            "No source files detected; treat as a greenfield repository.",
            report["findings"],
        )

    def test_typescript_repository_surfaces_are_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "index.ts").write_text("export {};\n", encoding="utf-8")
            (root / "package.json").write_text(
                json.dumps({"scripts": {"verify": "npm test", "custom": "echo ok"}}),
                encoding="utf-8",
            )
            (root / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (root / "tsconfig.json").write_text("{}\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
            workflow = root / ".github" / "workflows"
            workflow.mkdir(parents=True)
            (workflow / "ci.yml").write_text("name: CI\n", encoding="utf-8")

            report = AUDIT_REPO.audit(root)

        self.assertEqual(report["mode"], "brownfield")
        self.assertEqual(report["ecosystems"], ["javascript-typescript"])
        self.assertEqual(report["package_managers"], ["npm"])
        self.assertEqual(report["instruction_files"], ["AGENTS.md"])
        self.assertEqual(report["ci_files"], [".github/workflows/ci.yml"])
        self.assertEqual(report["verification_scripts"], {"verify": "npm test"})
        self.assertEqual(report["verification_entrypoints"], [])
        self.assertNotIn("custom", report["verification_scripts"])

    def test_malformed_package_manifest_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text("{", encoding="utf-8")

            self.assertEqual(
                AUDIT_REPO.package_scripts(root),
                {"<parse-error>": "package.json could not be parsed"},
            )
            report = AUDIT_REPO.audit(root)

        self.assertEqual(report["verification_scripts"], {})
        self.assertIn(
            "No common verification entry point detected.",
            report["findings"],
        )

    def test_repository_verify_script_is_a_verification_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "verify.py").write_text("print('ok')\n", encoding="utf-8")

            report = AUDIT_REPO.audit(root)

        self.assertEqual(report["verification_entrypoints"], ["scripts/verify.py"])
        self.assertNotIn(
            "No common verification entry point detected.",
            report["findings"],
        )

    def test_generated_and_dependency_directories_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dependency = root / "node_modules" / "example"
            dependency.mkdir(parents=True)
            (dependency / "index.js").write_text("module.exports = {};\n", encoding="utf-8")

            report = AUDIT_REPO.audit(root)

        self.assertEqual(report["source_file_count_capped"], 0)
        self.assertEqual(report["mode"], "greenfield")

    def test_cli_emits_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(AUDIT_PATH), directory, "--json"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        report = json.loads(result.stdout)
        self.assertEqual(report["mode"], "greenfield")


if __name__ == "__main__":
    unittest.main()
