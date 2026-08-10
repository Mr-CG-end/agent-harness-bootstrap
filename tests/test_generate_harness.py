from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = (
    ROOT
    / "skills"
    / "bootstrap-project-harness"
    / "scripts"
    / "generate_harness.py"
)


def run_generator(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GENERATOR), str(repository), *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class GenerateHarnessTests(unittest.TestCase):
    def test_preview_reports_creation_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_generator(root)

            self.assertIn("`AGENTS.md`: create", result.stdout)
            self.assertIn("preview only", result.stdout)
            self.assertFalse((root / "AGENTS.md").exists())

    def test_apply_creates_agents_file_with_detected_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text(
                json.dumps({"scripts": {"test": "vitest run"}}),
                encoding="utf-8",
            )
            (root / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (root / "src.ts").write_text("export {};\n", encoding="utf-8")

            result = run_generator(root, "--apply")
            content = (root / "AGENTS.md").read_text(encoding="utf-8")

        self.assertIn("Operation: apply", result.stdout)
        self.assertIn("Repository mode: brownfield", content)
        self.assertIn("Ecosystems: javascript-typescript", content)
        self.assertIn("`test`: `vitest run`", content)

    def test_apply_never_overwrites_existing_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agents = root / "AGENTS.md"
            agents.write_text("keep me\n", encoding="utf-8")

            result = run_generator(root, "--apply", "--json")
            output = json.loads(result.stdout)

            self.assertEqual(agents.read_text(encoding="utf-8"), "keep me\n")

        self.assertEqual(output["created"], [])
        self.assertEqual(output["artifacts"][0]["action"], "skip")
        self.assertEqual(output["artifacts"][0]["reason"], "already exists")

    def test_second_apply_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = json.loads(run_generator(root, "--apply", "--json").stdout)
            original = (root / "AGENTS.md").read_bytes()
            second = json.loads(run_generator(root, "--apply", "--json").stdout)

            self.assertEqual((root / "AGENTS.md").read_bytes(), original)

        self.assertEqual(first["created"], ["AGENTS.md"])
        self.assertEqual(second["created"], [])
        self.assertEqual(second["artifacts"][0]["action"], "skip")


if __name__ == "__main__":
    unittest.main()
