# Set IDEA AIAssistant Commit Prompt

Small CLI that updates the prompt for the JetBrains AIAssistant for all projects recursively from
current folder.

The JetBrains AIAssistant prompt is stored in the `AIAssistant.VCS.GenerateCommitMessage` action
inside `.idea/workspace.xml` files. This tool walks the directory tree (default: current working
directory), finds all `.idea/workspace.xml`, and rewrites the `<option name="content" ...>` value to
the prompt you provide.

## Quick start

- Requires Python 3.12+ (repo uses uv tooling).
- From the project root:
    - `uv run set-prompt --prompt "Your new prompt" --root ./projets`
    - You can omit `--root` to search from the current directory.

## Example

```bash
set-prompt --prompt "Avoid overly verbose descriptions or unnecessary details. Do not use markdown. Don't add dot (.) at the end of the commit message. Use conventional-commit format"
```

## Install as a CLI

Option 1: run in-place (no install)

- `uv run set-prompt --prompt "…"`

Option 2: editable install in your environment

- `uv pip install -e .`
- Afterwards run `set-prompt --prompt "…" --root ./projets`

Legacy wrapper

- You can also run `python set-prompt.py --prompt "…" --root ./projets` if you prefer calling the
  top-level script directly.

## What the tool does

- Recursively finds `.idea/workspace.xml` files under `--root`.
- For each `<AIAssistantStoredInstruction>` block where
  `<option name="actionId" value="AIAssistant.VCS.GenerateCommitMessage" />`
  is present, it sets the sibling `<option name="content" value="…" />` to the provided prompt.
- Prints which files changed; leaves files untouched if already up to date.
- Invalid XML files are skipped with an error message.

## Notes

- The XML is rewritten via `xml.etree.ElementTree`; minor formatting differences
  (e.g., quote style) may occur, but structure and content are preserved.
