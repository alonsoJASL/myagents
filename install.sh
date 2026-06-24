#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
COMMANDS_DIR="$CLAUDE_DIR/commands"
SKILLS_DIR="$CLAUDE_DIR/skills"

# Parse arguments for agy/gemini installation
INSTALL_AGY=false
FORCE_FLAG=""

for arg in "$@"; do
  case "$arg" in
    --agy|--gemini)
      INSTALL_AGY=true
      ;;
    --force|-f)
      FORCE_FLAG="--force"
      ;;
  esac
done

if [ "$INSTALL_AGY" = true ]; then
  python3 "$REPO_DIR/install_agy.py" $FORCE_FLAG
  exit 0
fi

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

link() {
  local src="$1"
  local dst="$2"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    echo -e "  ${YELLOW}skipped${NC}  $dst (file already exists and is not a symlink)"
    return
  fi
  ln -sf "$src" "$dst"
  echo -e "  ${GREEN}linked${NC}   $dst"
}

# Like link(), but for a directory target. Uses -n so an existing symlink is
# replaced rather than dereferenced (on macOS `ln -sf` into a symlinked dir nests
# the new link inside it instead of replacing it).
link_dir() {
  local src="$1"
  local dst="$2"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    echo -e "  ${YELLOW}skipped${NC}  $dst (directory exists and is not a symlink)"
    return
  fi
  ln -sfn "$src" "$dst"
  echo -e "  ${GREEN}linked${NC}   $dst"
}

echo ""
echo "Installing myagents into $CLAUDE_DIR"
echo ""

mkdir -p "$COMMANDS_DIR"

link "$REPO_DIR/CLAUDE.md"      "$CLAUDE_DIR/CLAUDE.md"
link "$REPO_DIR/settings.json"  "$CLAUDE_DIR/settings.json"
link "$REPO_DIR/statusline.sh"  "$CLAUDE_DIR/statusline.sh"

for cmd in "$REPO_DIR/commands/"*.md; do
  name="$(basename "$cmd")"
  link "$cmd" "$COMMANDS_DIR/$name"
done

# Skills (each is a directory containing SKILL.md). The skills dir is created on
# demand; any repo dir holding a SKILL.md is linked, the rest are skipped.
mkdir -p "$SKILLS_DIR"
for skill in "$REPO_DIR"/*/; do
  skill="${skill%/}"                      # strip trailing slash from glob
  [ -f "$skill/SKILL.md" ] || continue    # not a skill dir; skip
  name="$(basename "$skill")"
  link_dir "$skill" "$SKILLS_DIR/$name"
done

echo ""
echo "Done. Start a new Claude Code session to pick up the changes."
echo ""
