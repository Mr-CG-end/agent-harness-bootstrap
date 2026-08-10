#!/usr/bin/env python3
"""Preview or create a minimal, non-overwriting repository harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from audit_repo import audit


def render_agents(report: dict[str, Any]) -> str:
    ecosystems = ", ".join(report["ecosystems"]) or "not detected"
    managers = ", ".join(report["package_managers"]) or "not detected"
    commands: list[str] = []
    commands.extend(
        f"- `{name}`: `{command}`"
        for name, command in report["verification_scripts"].items()
    )
    commands.extend(f"- `{path}`" for path in report["verification_entrypoints"])
    if not commands:
        commands.append(
            "- No executable verification entry point is detected. Establish one before broad changes."
        )

    return "\n".join(
        [
            "# Repository Guidelines",
            "",
            "## Working Agreement",
            "",
            "- Inspect existing instructions, manifests, documentation, and tests before changing code.",
            "- Make the smallest change that satisfies the request and preserve established conventions.",
            "- Keep generated artifacts, dependencies, credentials, and unrelated cleanup out of changes.",
            "- Add or update deterministic tests when behavior changes.",
            "",
            "## Detected Context",
            "",
            f"- Repository mode: {report['mode']}",
            f"- Ecosystems: {ecosystems}",
            f"- Package managers: {managers}",
            "",
            "## Verification",
            "",
            *commands,
            "",
            "Run the narrowest relevant checks during development and the complete verification path before handoff.",
            "",
            "## Safety and Approval",
            "",
            "- Do not weaken tests, checks, permissions, or safety boundaries to obtain a green result.",
            "- Ask before destructive operations, dependency migrations, secret handling, deployment, commits, pushes, or remote repository changes.",
            "- Report automated verification, skipped checks, environment blockers, and manual acceptance separately.",
            "",
        ]
    )


def build_plan(root: Path) -> dict[str, Any]:
    report = audit(root)
    target = root.resolve() / "AGENTS.md"
    if target.exists():
        artifacts: list[dict[str, str]] = [
            {"path": "AGENTS.md", "action": "skip", "reason": "already exists"}
        ]
    else:
        artifacts = [
            {
                "path": "AGENTS.md",
                "action": "create",
                "content": render_agents(report),
            }
        ]
    return {
        "root": str(root.resolve()),
        "mode": report["mode"],
        "artifacts": artifacts,
    }


def apply_plan(plan: dict[str, Any]) -> list[str]:
    root = Path(plan["root"])
    created: list[str] = []
    for artifact in plan["artifacts"]:
        if artifact["action"] != "create":
            continue
        target = root / artifact["path"]
        try:
            with target.open("x", encoding="utf-8", newline="\n") as file:
                file.write(artifact["content"])
        except FileExistsError:
            continue
        created.append(artifact["path"])
    return created


def printable_plan(plan: dict[str, Any], applied: bool) -> str:
    lines = [
        "# Repository harness generation plan",
        "",
        f"- Root: `{plan['root']}`",
        f"- Mode: **{plan['mode']}**",
        f"- Operation: {'apply' if applied else 'preview only'}",
        "",
        "## Artifacts",
        "",
    ]
    for artifact in plan["artifacts"]:
        reason = f" ({artifact['reason']})" if "reason" in artifact else ""
        lines.append(f"- `{artifact['path']}`: {artifact['action']}{reason}")
    if not applied:
        lines.extend(
            [
                "",
                "No files were changed. Run again with `--apply` to create missing artifacts.",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create missing artifacts; existing files are never overwritten",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = Path(args.repository).resolve()
    try:
        plan = build_plan(root)
    except ValueError as error:
        parser.error(str(error))

    created = apply_plan(plan) if args.apply else []
    if args.json:
        output = dict(plan)
        for artifact in output["artifacts"]:
            artifact.pop("content", None)
        output["applied"] = args.apply
        output["created"] = created
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(printable_plan(plan, args.apply))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
