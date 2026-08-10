import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / '.codex-plugin' / 'plugin.json'


class PluginPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))

    def test_manifest_identifies_release(self) -> None:
        self.assertEqual(self.manifest['name'], 'agent-harness-bootstrap')
        self.assertRegex(self.manifest['version'], re.compile(r'^\d+\.\d+\.\d+$'))
        self.assertEqual(self.manifest['version'], '0.1.0')
        self.assertEqual(self.manifest['license'], 'Apache-2.0')
        self.assertEqual(self.manifest['author']['name'], 'Mr-CG-end')

    def test_manifest_points_to_packaged_skill(self) -> None:
        skills_path = ROOT / self.manifest['skills']
        self.assertTrue(skills_path.is_dir())
        self.assertTrue((skills_path / 'bootstrap-project-harness' / 'SKILL.md').is_file())

    def test_manifest_has_required_interface_metadata(self) -> None:
        interface = self.manifest['interface']
        for field in (
            'displayName',
            'shortDescription',
            'longDescription',
            'developerName',
            'category',
            'capabilities',
            'defaultPrompt',
        ):
            self.assertTrue(interface[field])

    def test_manifest_does_not_advertise_unbundled_components(self) -> None:
        for field in ('apps', 'mcpServers', 'hooks'):
            self.assertNotIn(field, self.manifest)

    def test_readmes_document_installer_and_skill_path(self) -> None:
        for filename in ('README.md', 'README.en.md'):
            content = (ROOT / filename).read_text(encoding='utf-8')
            self.assertIn('$skill-installer', content)
            self.assertIn(
                'github.com/Mr-CG-end/agent-harness-bootstrap/tree/main/'
                'skills/bootstrap-project-harness',
                content,
            )


if __name__ == '__main__':
    unittest.main()
