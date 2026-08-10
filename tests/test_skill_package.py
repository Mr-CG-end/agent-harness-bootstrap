from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "bootstrap-project-harness"


class SkillPackageTests(unittest.TestCase):
    def test_required_files_are_present(self) -> None:
        required = [
            SKILL / "SKILL.md",
            SKILL / "agents" / "openai.yaml",
            SKILL / "scripts" / "audit_repo.py",
            SKILL / "scripts" / "generate_harness.py",
            SKILL / "references" / "open-source-patterns.md",
            SKILL / "references" / "stack-patterns.md",
        ]
        self.assertEqual([str(path) for path in required if not path.is_file()], [])

    def test_frontmatter_name_matches_directory(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        _, frontmatter, _ = content.split("---", 2)
        name = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)

        self.assertIsNotNone(name)
        self.assertIsNotNone(description)
        self.assertEqual(name.group(1).strip(), SKILL.name)
        self.assertGreater(len(description.group(1).strip()), 40)

    def test_skill_package_contains_no_repository_documentation(self) -> None:
        forbidden = {
            "README.md",
            "README.zh-CN.md",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            "SECURITY.md",
        }
        present = {path.name for path in SKILL.iterdir()}
        self.assertEqual(present & forbidden, set())

    def test_ui_metadata_has_required_fields(self) -> None:
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        for field in ("display_name:", "short_description:", "default_prompt:"):
            self.assertIn(field, metadata)
        self.assertIn("$bootstrap-project-harness", metadata)

    def test_readmes_link_to_each_other(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("README.zh-CN.md", english)
        self.assertIn("README.md", chinese)


if __name__ == "__main__":
    unittest.main()
