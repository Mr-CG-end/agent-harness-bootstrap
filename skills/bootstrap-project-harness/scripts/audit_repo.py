#!/usr/bin/env python3
"""Read-only, dependency-free repository harness audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ECOSYSTEM_MARKERS = {
    "javascript-typescript": ["package.json", "tsconfig.json", "jsconfig.json"],
    "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
    "jvm": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "dotnet": ["global.json", "Directory.Build.props"],
    "ruby": ["Gemfile"],
    "php": ["composer.json"],
}

PACKAGE_MANAGERS = {
    "npm": ["package-lock.json"],
    "pnpm": ["pnpm-lock.yaml"],
    "yarn": ["yarn.lock"],
    "bun": ["bun.lock", "bun.lockb"],
    "uv": ["uv.lock"],
    "poetry": ["poetry.lock"],
    "cargo": ["Cargo.lock"],
    "go-modules": ["go.sum"],
    "maven": ["mvnw", "pom.xml"],
    "gradle": ["gradlew", "build.gradle", "build.gradle.kts"],
}

INSTRUCTION_FILES = [
    "AGENTS.md",
    "AGENTS.override.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
]

QUALITY_FILES = [
    ".editorconfig",
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.ts",
    ".eslintrc",
    ".prettierrc",
    "biome.json",
    "biome.jsonc",
    "vitest.config.ts",
    "vitest.config.js",
    "jest.config.ts",
    "jest.config.js",
    "pytest.ini",
    "mypy.ini",
    "ruff.toml",
    "rustfmt.toml",
    "clippy.toml",
]

HOOK_FILES = [
    ".pre-commit-config.yaml",
    ".husky",
    "lefthook.yml",
    "lefthook.yaml",
    ".githooks",
]

CI_FILES = [
    ".gitlab-ci.yml",
    "azure-pipelines.yml",
    "Jenkinsfile",
    ".circleci/config.yml",
]

VERIFICATION_ENTRYPOINT_FILES = [
    "scripts/verify.py",
    "scripts/verify.sh",
    "scripts/verify.ps1",
    "Makefile",
    "justfile",
    "Justfile",
    "Taskfile.yml",
    "Taskfile.yaml",
]

SOURCE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt",
    ".kts", ".php", ".py", ".rb", ".rs", ".swift", ".ts", ".tsx",
}

IGNORED_DIRECTORIES = {
    ".git", ".idea", ".next", ".output", ".turbo", ".venv", ".vscode",
    "build", "coverage", "dist", "node_modules", "target", "vendor",
}


def existing(root: Path, candidates: list[str]) -> list[str]:
    return [candidate for candidate in candidates if (root / candidate).exists()]


def glob_relative(root: Path, pattern: str) -> list[str]:
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.glob(pattern)
        if path.is_file()
    )


def package_scripts(root: Path) -> dict[str, str]:
    package_json = root / "package.json"
    if not package_json.is_file():
        return {}
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {"<parse-error>": "package.json could not be parsed"}
    scripts = data.get("scripts", {})
    return scripts if isinstance(scripts, dict) else {}


def count_sources(root: Path, limit: int = 10_000) -> int:
    count = 0
    pending = [root]
    while pending and count < limit:
        directory = pending.pop()
        try:
            entries = list(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_dir() and entry.name not in IGNORED_DIRECTORIES:
                pending.append(entry)
            elif entry.is_file() and entry.suffix.lower() in SOURCE_EXTENSIONS:
                count += 1
                if count >= limit:
                    break
    return count


def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Repository path is not a directory: {root}")

    ecosystems = [
        name
        for name, markers in ECOSYSTEM_MARKERS.items()
        if existing(root, markers)
    ]
    package_managers = [
        name
        for name, markers in PACKAGE_MANAGERS.items()
        if existing(root, markers)
    ]
    workflows = glob_relative(root, ".github/workflows/*.yml")
    workflows += glob_relative(root, ".github/workflows/*.yaml")
    workflows += existing(root, CI_FILES)
    source_count = count_sources(root)
    scripts = package_scripts(root)
    verification_entrypoints = existing(root, VERIFICATION_ENTRYPOINT_FILES)

    verification_names = {
        "verify", "check", "ci", "lint", "format", "format:check", "typecheck",
        "test", "build",
    }
    verification_scripts = {
        name: command
        for name, command in scripts.items()
        if name in verification_names
    }

    findings: list[str] = []
    if not existing(root, INSTRUCTION_FILES):
        findings.append("No repository AI instruction entry point detected.")
    if not verification_scripts and not verification_entrypoints:
        findings.append("No common verification entry point detected.")
    elif "verify" not in verification_scripts and not verification_entrypoints:
        findings.append("Checks exist, but no single verification entry point was detected.")
    if not workflows:
        findings.append("No common CI configuration detected.")
    if not package_managers and ecosystems:
        findings.append("An ecosystem was detected without a recognized dependency lockfile.")
    if source_count == 0:
        findings.append("No source files detected; treat as a greenfield repository.")

    return {
        "root": str(root),
        "mode": "greenfield" if source_count == 0 else "brownfield",
        "git_repository": (root / ".git").exists(),
        "source_file_count_capped": source_count,
        "ecosystems": ecosystems,
        "package_managers": package_managers,
        "instruction_files": existing(root, INSTRUCTION_FILES),
        "ci_files": sorted(set(workflows)),
        "quality_configs": existing(root, QUALITY_FILES),
        "hook_configs": existing(root, HOOK_FILES),
        "verification_scripts": verification_scripts,
        "verification_entrypoints": verification_entrypoints,
        "docs_present": (root / "docs").is_dir(),
        "findings": findings,
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Repository harness audit",
        "",
        f"- Root: `{report['root']}`",
        f"- Mode: **{report['mode']}**",
        f"- Git repository: {report['git_repository']}",
        f"- Source files (capped): {report['source_file_count_capped']}",
        f"- Ecosystems: {', '.join(report['ecosystems']) or 'none detected'}",
        f"- Package managers: {', '.join(report['package_managers']) or 'none detected'}",
        "",
        "## Detected harness surfaces",
        "",
    ]
    for key in (
        "instruction_files",
        "ci_files",
        "quality_configs",
        "hook_configs",
        "verification_scripts",
        "verification_entrypoints",
    ):
        value = report[key]
        rendered = json.dumps(value, ensure_ascii=False) if value else "none"
        lines.append(f"- {key}: {rendered}")
    lines.extend(["", "## Findings", ""])
    lines.extend(f"- {item}" for item in report["findings"])
    if not report["findings"]:
        lines.append(
            "- No obvious bootstrap gaps detected; inspect semantics and remote settings manually."
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root (default: current directory)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    try:
        report = audit(Path(args.repository))
    except ValueError as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
