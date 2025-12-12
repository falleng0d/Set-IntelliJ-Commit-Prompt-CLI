"""Update JetBrains AIAssistant commit message prompt across projects.

Usage:
  python set-commit-prompt.py --prompt "NEW VALUE"

It searches recursively from the given root (default: current directory)
for `.idea/workspace.xml` and updates the `content` option inside
`AIAssistantStoredInstruction` where `actionId` matches
`AIAssistant.VCS.GenerateCommitMessage`.
"""

from set_prompt.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
