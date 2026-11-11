#!/usr/bin/env bash
# Install the research-writing skill for Claude Code and/or Codex.
# Usage: scripts/install.sh [--claude] [--codex] [--project DIR] [--copy]
#   --claude        install for Claude Code (user scope: ~/.claude/skills)
#   --codex         install for Codex (user scope: ~/.agents/skills)
#   --project DIR   install into a project instead (DIR/.claude/skills and/or DIR/.agents/skills)
#   --copy          copy files instead of creating a symlink (default: symlink, so `git pull` updates it)
# With no target flag, installs for both Claude Code and Codex.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_DIR/skills/research-writing"
NAME="research-writing"
CLAUDE=0; CODEX=0; PROJECT=""; MODE="link"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude) CLAUDE=1 ;;
    --codex) CODEX=1 ;;
    --project) PROJECT="${2:?--project needs a directory}"; shift ;;
    --copy) MODE="copy" ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done
[[ $CLAUDE -eq 0 && $CODEX -eq 0 ]] && { CLAUDE=1; CODEX=1; }

install_to() {
  local dest_root="$1" dest="$1/$NAME"
  mkdir -p "$dest_root"
  if [[ -e "$dest" || -L "$dest" ]]; then
    echo "Replacing existing $dest"
    rm -rf "$dest"
  fi
  if [[ "$MODE" == "copy" ]]; then
    cp -R "$SRC" "$dest"
  else
    ln -s "$SRC" "$dest"
  fi
  echo "Installed ($MODE): $dest"
}

if [[ -n "$PROJECT" ]]; then
  [[ $CLAUDE -eq 1 ]] && install_to "$PROJECT/.claude/skills"
  [[ $CODEX -eq 1 ]] && install_to "$PROJECT/.agents/skills"
else
  [[ $CLAUDE -eq 1 ]] && install_to "$HOME/.claude/skills"
  [[ $CODEX -eq 1 ]] && install_to "$HOME/.agents/skills"
fi
echo "Done. Restart Claude Code / Codex to load the skill."
