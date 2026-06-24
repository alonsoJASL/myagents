#!/usr/bin/env python3
"""
install_agy.py - Installer helper for Google Antigravity (agy) custom rules and skills.

This script parses existing Claude command markdown files, wraps them with valid
YAML frontmatter for agy, and installs them along with global developer manifest
rules (CLAUDE.md verbatim as GEMINI.md and AGENTS.md) and skills like scaffold-docs.

Strictly follows the CLAUDE.md architectural guidelines:
- Separation of orchestration (file I/O, logging, path construction) from logic.
- Explicit data contracts via dataclasses.
- Stateless logic components.
- Dependency injection (no globals or singletons, I/O streams are injected).
"""

import argparse
import dataclasses
import os
from pathlib import Path
import shutil
import sys
from typing import List, Optional, TextIO


# ==============================================================================
# 1. Data Contracts
# ==============================================================================

@dataclasses.dataclass(frozen=True)
class CommandSource:
    """Represents a legacy Claude command file."""
    name: str
    content: str


@dataclasses.dataclass(frozen=True)
class TranslatedSkill:
    """Represents a translated skill with YAML frontmatter."""
    name: str
    skill_md_content: str


@dataclasses.dataclass(frozen=True)
class LinkTarget:
    """Represents a path symlink configuration."""
    src: Path
    dst: Path
    is_dir: bool


@dataclasses.dataclass(frozen=True)
class SkillTarget:
    """Represents a translated skill target to be written."""
    name: str
    skill_md_content: str
    parent_dirs: List[Path]


@dataclasses.dataclass(frozen=True)
class InstallationConfig:
    """Injection configuration containing directory paths and behavior options."""
    repo_dir: Path
    home_dir: Path
    use_symlink: bool
    force: bool


# ==============================================================================
# 2. Stateless Logic Layer (Library)
# ==============================================================================

def translate_command_to_skill(source: CommandSource) -> TranslatedSkill:
    """
    Stateless data transformation logic.
    Takes a command name and content, extracts the first paragraph before the 
    first empty line to use as the YAML description, and returns the wrapped SKILL.md content.
    """
    lines = source.content.splitlines()
    description_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            break
        description_lines.append(stripped)
        
    description = " ".join(description_lines)
    if not description:
        description = f"Custom command /{source.name} migrated for agy."
        
    # Standard YAML frontmatter format for agy skills
    frontmatter = [
        "---",
        f"name: {source.name}",
        f"description: {description}",
        "---",
        "",
        ""
    ]
    
    skill_md_content = "\n".join(frontmatter) + source.content
    return TranslatedSkill(name=source.name, skill_md_content=skill_md_content)


# ==============================================================================
# 3. Orchestration Layer (File I/O and System State)
# ==============================================================================

class AgyInstallerOrchestrator:
    """
    Orchestrator handling path resolution, file I/O operations, logging,
    and target creation. Injects dependencies for configuration and I/O streams.
    """
    def __init__(
        self,
        config: InstallationConfig,
        stdout: TextIO = sys.stdout,
        stderr: TextIO = sys.stderr
    ):
        self.config = config
        self.stdout = stdout
        self.stderr = stderr

        # Color codes matching the legacy shell script
        self.green = "\033[0;32m"
        self.yellow = "\033[1;33m"
        self.nc = "\033[0m"

    def log_linked(self, path: Path):
        self.stdout.write(f"  {self.green}linked{self.nc}   {path}\n")

    def log_copied(self, path: Path):
        self.stdout.write(f"  {self.green}copied{self.nc}   {path}\n")

    def log_skipped(self, path: Path, reason: str):
        self.stdout.write(f"  {self.yellow}skipped{self.nc}  {path} ({reason})\n")

    def log_info(self, message: str):
        self.stdout.write(message + "\n")

    def install_link(self, target: LinkTarget) -> None:
        """
        Safely creates a symlink or copy for files and directories.
        Mimics install.sh: skips target if it exists and is NOT a symlink.
        """
        # Ensure parent directory exists
        target.dst.parent.mkdir(parents=True, exist_ok=True)

        # Check existing target path
        if target.dst.exists() or target.dst.is_symlink():
            if not target.dst.is_symlink() and not self.config.force:
                reason = "directory exists and is not a symlink" if target.is_dir else "file already exists and is not a symlink"
                self.log_skipped(target.dst, reason)
                return
            
            # Clean up existing symlink (or file if force is active)
            if target.dst.is_dir() and not target.dst.is_symlink():
                shutil.rmtree(target.dst)
            else:
                target.dst.unlink(missing_ok=True)

        # Perform installation
        if self.config.use_symlink:
            try:
                target.dst.symlink_to(target.src, target_is_directory=target.is_dir)
                self.log_linked(target.dst)
            except OSError as e:
                # Fallback to copy if symlinking fails (e.g. permission issues or Windows without elevation)
                self.log_info(f"Symlinking failed: {e}. Falling back to copy.")
                self._copy_target(target)
        else:
            self._copy_target(target)

    def _copy_target(self, target: LinkTarget) -> None:
        if target.is_dir:
            shutil.copytree(target.src, target.dst)
        else:
            shutil.copy2(target.src, target.dst)
        self.log_copied(target.dst)

    def install_translated_skill(self, target: SkillTarget) -> None:
        """
        Creates skill directories and writes dynamically translated SKILL.md.
        Ensures safety check (doesn't overwrite user file/dir where folder or SKILL.md should be).
        """
        for parent_dir in target.parent_dirs:
            skill_dir = parent_dir / target.name
            skill_md_path = skill_dir / "SKILL.md"

            # Check if skill directory conflicts with a regular file
            if skill_dir.exists() and not skill_dir.is_dir():
                if not self.config.force:
                    self.log_skipped(skill_dir, "path exists and is a regular file")
                    continue
                skill_dir.unlink()

            skill_dir.mkdir(parents=True, exist_ok=True)

            # Check if SKILL.md conflicts with a directory or symlink
            if skill_md_path.exists():
                if skill_md_path.is_dir() or (skill_md_path.is_symlink() and not self.config.force):
                    self.log_skipped(skill_md_path, "path exists and is a directory or symlink")
                    continue
                # If it's a regular file, it's safe to overwrite since it is dynamically managed by the installer

            # Write the generated skill content
            with open(skill_md_path, "w", encoding="utf-8") as f:
                f.write(target.skill_md_content)
            
            self.log_copied(skill_md_path)

    def execute(self) -> None:
        """Drives the entire installation process using injected configuration."""
        gemini_dir = self.config.home_dir / ".gemini"
        config_dir = gemini_dir / "config"
        agy_cli_dir = gemini_dir / "antigravity-cli"

        self.log_info("")
        self.log_info(f"Installing myagents rules and skills for Antigravity into {gemini_dir}")
        self.log_info("")

        # 1. Rules
        claude_md = self.config.repo_dir / "CLAUDE.md"
        gemini_rules = gemini_dir / "GEMINI.md"
        config_agents_rules = config_dir / "agents" / "AGENTS.md"

        self.install_link(LinkTarget(src=claude_md, dst=gemini_rules, is_dir=False))
        self.install_link(LinkTarget(src=claude_md, dst=config_agents_rules, is_dir=False))

        # 2. Shared Skills (scaffold-docs)
        scaffold_docs_src = self.config.repo_dir / "scaffold-docs"
        if scaffold_docs_src.exists():
            cli_scaffold_docs_dst = agy_cli_dir / "skills" / "scaffold-docs"
            config_scaffold_docs_dst = config_dir / "skills" / "scaffold-docs"

            self.install_link(LinkTarget(src=scaffold_docs_src, dst=cli_scaffold_docs_dst, is_dir=True))
            self.install_link(LinkTarget(src=scaffold_docs_src, dst=config_scaffold_docs_dst, is_dir=True))

        # 3. Commands translation
        commands_src_dir = self.config.repo_dir / "commands"
        if commands_src_dir.exists():
            for cmd_file in commands_src_dir.glob("*.md"):
                name = cmd_file.stem
                
                try:
                    with open(cmd_file, "r", encoding="utf-8") as f:
                        content = f.read()
                except OSError as e:
                    self.stderr.write(f"Error reading command file {cmd_file}: {e}\n")
                    continue

                # Translate legacy command structure to agy skill
                source = CommandSource(name=name, content=content)
                translated = translate_command_to_skill(source)

                # Write translated skill to both skills destinations
                skill_target = SkillTarget(
                    name=translated.name,
                    skill_md_content=translated.skill_md_content,
                    parent_dirs=[
                        agy_cli_dir / "skills",
                        config_dir / "skills"
                    ]
                )
                self.install_translated_skill(skill_target)

        self.log_info("")
        self.log_info("Antigravity installation complete.")
        self.log_info("")


# ==============================================================================
# 4. Entry Point & CLI Argument Parsing
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="Helper to install myagents rules and skills for Google Antigravity.")
    parser.add_argument("--repo-dir", type=Path, default=Path.cwd(), help="Repository root directory")
    parser.add_argument("--home-dir", type=Path, default=Path.home(), help="User home directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing non-symlink targets")
    args = parser.parse_args()

    repo_dir = args.repo_dir.resolve()
    home_dir = args.home_dir.resolve()
    use_symlink = True

    # Standardize symlink option: Windows cannot symlink reliably without elevation, so fallback to copies
    if use_symlink and os.name == "nt":
        use_symlink = False

    config = InstallationConfig(
        repo_dir=repo_dir,
        home_dir=home_dir,
        use_symlink=use_symlink,
        force=args.force
    )

    orchestrator = AgyInstallerOrchestrator(config)
    try:
        orchestrator.execute()
        return 0
    except Exception as e:
        sys.stderr.write(f"Installation failed: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
