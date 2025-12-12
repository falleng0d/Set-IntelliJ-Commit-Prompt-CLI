"""CLI entrypoint for updating JetBrains AIAssistant commit prompts."""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET


TARGET_ACTION_ID = "AIAssistant.VCS.GenerateCommitMessage"


def find_workspace_files(root: str) -> list[str]:
    """Return paths to workspace.xml files living directly under .idea/."""
    matches: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        if os.path.basename(dirpath) == ".idea" and "workspace.xml" in filenames:
            matches.append(os.path.join(dirpath, "workspace.xml"))
            dirnames[:] = []
    return matches


def update_workspace(path: str, prompt: str) -> bool:
    """Set the content option value to prompt. Return True if changed."""
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False

    for instruction in root.findall(".//AIAssistantStoredInstruction"):
        options = {opt.get("name"): opt for opt in instruction.findall("option")}
        action = options.get("actionId")
        content = options.get("content")

        if action is None or content is None:
            continue
        if action.get("value") != TARGET_ACTION_ID:
            continue
        if content.get("value") != prompt:
            content.set("value", prompt)
            changed = True

    if changed:
        tree.write(path, encoding="UTF-8", xml_declaration=True)
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Set AIAssistant commit message prompt in JetBrains workspaces."
    )
    parser.add_argument("--prompt", required=True, help="New prompt text to store.")
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to search (defaults to current directory).",
    )

    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)

    workspaces = find_workspace_files(root)
    if not workspaces:
        print("No .idea/workspace.xml files found.")
        return 1

    updated = []
    unchanged = []

    for path in workspaces:
        try:
            if update_workspace(path, args.prompt):
                updated.append(path)
            else:
                unchanged.append(path)
        except ET.ParseError as exc:
            print(f"Skipping invalid XML: {path} ({exc})", file=sys.stderr)

    if updated:
        print("Updated:")
        for path in updated:
            print(f"  {path}")
    if unchanged:
        print("No change (already up to date):")
        for path in unchanged:
            print(f"  {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
