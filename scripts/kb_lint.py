#!/usr/bin/env python3
"""
Knowledge Base Linter for Docs-as-Code Vaults.
Validates wikilinks, file existence, and YAML frontmatter integrity.
Zero external dependencies (uses standard Python 3 library only).
"""

import sys
import os
import re
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def find_vault_root(start_dir: Path) -> Path:
    cur = start_dir.resolve()
    while cur != cur.parent:
        if (cur / "docs").is_dir() or (cur / "00_Index.md").is_file():
            if (cur / "docs").is_dir():
                return cur / "docs"
            return cur
        cur = cur.parent
    return start_dir.resolve()


def parse_wikilinks(content: str):
    # Matches [[target|label]], [[target#heading|label]], or [[target]]
    pattern = re.compile(r'\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]')
    return pattern.findall(content)


def check_file_frontmatter(file_path: Path):
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read file: {e}"

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return True, "Valid YAML frontmatter"
    return False, "Missing or malformed YAML frontmatter (starts without ---)"


def run_linter(docs_dir: Path):
    print(f"🔍 Auditing Knowledge Base at: {docs_dir.resolve()}\n")
    if not docs_dir.exists():
        print(f"❌ Directory does not exist: {docs_dir}")
        sys.exit(1)

    all_md_files = list(docs_dir.rglob("*.md"))
    repo_root = docs_dir.parent

    # Also collect root markdown files (SPEC.md, README.md, AGENTS.md, CLAUDE.md)
    for root_doc in ["SPEC.md", "README.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"]:
        if (repo_root / root_doc).is_file():
            all_md_files.append(repo_root / root_doc)

    # Collect map of base names without extension and relative paths
    file_map = {}
    for f in all_md_files:
        if f.is_relative_to(docs_dir):
            rel_posix = f.relative_to(docs_dir).as_posix()
            file_map[rel_posix] = f
            file_map[rel_posix.lower()] = f
        name_no_ext = f.stem
        file_map[name_no_ext] = f
        file_map[name_no_ext.lower()] = f

    broken_links = []
    frontmatter_warnings = []
    checked_links_count = 0

    for f in all_md_files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️ Error reading {f}: {e}")
            continue

        if f.is_relative_to(docs_dir):
            rel = f.relative_to(docs_dir).as_posix()
        else:
            rel = f.name

        # Check frontmatter for task/spec/bug/adr/plan
        if any(prefix in rel for prefix in ["02_Tasks/Specs", "02_Tasks/Plans", "02_Tasks/Bugs", "03_Decisions_ADR"]):
            if not f.name.startswith("TEMPLATE_"):
                has_fm, msg = check_file_frontmatter(f)
                if not has_fm:
                    frontmatter_warnings.append((rel, msg))

        # Check wikilinks (skip template files containing placeholder links)
        if "TEMPLATE" in f.name or "00_Templates" in rel:
            continue

        links = parse_wikilinks(content)
        for link in links:
            link = link.strip()
            # Ignore placeholder links in documentation
            if not link or "XXX" in link or "Название" in link or "Имя" in link or link.lower() in ["wikilinks", "...", "target"]:
                continue
            checked_links_count += 1

            # Check relative to current file's dir
            file_dir = f.parent
            direct_target = (file_dir / link).resolve()
            direct_target_md = (file_dir / f"{link}.md").resolve()

            # Check relative to docs_dir
            vault_target = (docs_dir / link).resolve()
            vault_target_md = (docs_dir / f"{link}.md").resolve()

            # Check relative to repo root (for [[../SPEC]], [[../../SPEC]], etc.)
            repo_target = (repo_root / link).resolve()
            repo_target_md = (repo_root / f"{link}.md").resolve()

            link_name_no_ext = Path(link).name
            link_name_lower = link_name_no_ext.lower()

            found = False
            for cand in [direct_target, direct_target_md, vault_target, vault_target_md, repo_target, repo_target_md]:
                if cand.exists():
                    found = True
                    break

            if not found:
                try:
                    norm_path = (file_dir / link).resolve()
                    if norm_path.exists() or (file_dir / f"{link}.md").resolve().exists():
                        found = True
                except Exception:
                    pass

            if not found:
                if link_name_no_ext in file_map or link_name_lower in file_map:
                    found = True

            if not found:
                broken_links.append((rel, link))

    print(f"📊 Total Markdown Files Scanned: {len(all_md_files)}")
    print(f"🔗 Total Wikilinks Validated: {checked_links_count}\n")

    has_errors = False

    if broken_links:
        has_errors = True
        print(f"❌ Broken Wikilinks Detected ({len(broken_links)}):")
        for src, target in broken_links:
            print(f"   • In '{src}' -> target not found: [[{target}]]")
        print()
    else:
        print("✅ No broken wikilinks found!\n")

    if frontmatter_warnings:
        print(f"⚠️ Frontmatter / Property Warnings ({len(frontmatter_warnings)}):")
        for src, msg in frontmatter_warnings:
            print(f"   • {src}: {msg}")
        print()
    else:
        print("✅ All inspected task/spec/plan files have valid YAML frontmatter!\n")

    if has_errors:
        print("❌ Linter failed: please resolve broken links.")
        sys.exit(1)
    else:
        print("🎉 Knowledge base is healthy and consistent!")
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docs-as-Code Knowledge Base Linter")
    parser.add_argument("--path", "-p", type=str, default=".", help="Path to docs directory or project root")
    args = parser.parse_args()

    start = Path(args.path).resolve()
    if (start / "docs").is_dir():
        vault = start / "docs"
    elif start.name == "docs" and start.is_dir():
        vault = start
    else:
        vault = find_vault_root(start)

    run_linter(vault)
