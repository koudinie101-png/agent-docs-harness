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


def check_spec_drift(docs_dir: Path) -> list:
    """
    Heuristic audit for living spec drift.
    Checks if multiple phases in Roadmap.md are completed while SPEC.md remains un-updated.
    Returns a list of non-blocking warning strings.
    """
    warnings = []
    repo_root = docs_dir.parent if docs_dir.name == "docs" else docs_dir

    roadmap_path = docs_dir / "02_Tasks" / "Roadmap.md"
    if not roadmap_path.is_file() and (docs_dir / "docs" / "02_Tasks" / "Roadmap.md").is_file():
        roadmap_path = docs_dir / "docs" / "02_Tasks" / "Roadmap.md"

    spec_path = repo_root / "SPEC.md"
    if not spec_path.is_file():
        spec_path = docs_dir / "SPEC.md"
    if not spec_path.is_file() and (docs_dir / "docs" / "SPEC.md").is_file():
        spec_path = docs_dir / "docs" / "SPEC.md"

    if not roadmap_path.is_file() or not spec_path.is_file():
        return warnings

    roadmap_content = roadmap_path.read_text(encoding="utf-8")
    phase_blocks = re.split(r'\n(?=##\s+(?:Фаза|Phase)\s+\d+:)', roadmap_content, flags=re.IGNORECASE)
    completed_phases = 0
    for block in phase_blocks:
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if not lines:
            continue
        first_line = lines[0]
        if re.search(r'##\s+(?:Фаза|Phase)\s+\d+:', first_line, re.IGNORECASE):
            if re.search(r'Завершена|Completed|Done', first_line, re.IGNORECASE):
                completed_phases += 1
            elif "- [x]" in block and "- [ ]" not in block:
                completed_phases += 1

    spec_content = spec_path.read_text(encoding="utf-8")
    updated_match = re.search(r'^updated:\s*(\d{4}-\d{2}-\d{2})', spec_content, re.MULTILINE)
    created_match = re.search(r'^created:\s*(\d{4}-\d{2}-\d{2})', spec_content, re.MULTILINE)

    if completed_phases >= 2 and updated_match:
        updated_date = updated_match.group(1)
        created_date = created_match.group(1) if created_match else None
        if created_date and updated_date == created_date:
            warnings.append(
                f"Living Spec Drift: SPEC.md was never updated since creation ({created_date}), "
                f"despite {completed_phases} completed phases in Roadmap.md. Consider syncing Master Spec."
            )

    return warnings


def check_devlog_semantic_guard(docs_dir: Path) -> list:
    """
    Scans Devlog.md for bare 'Следующий шаг:' or 'Next Step:' triggers
    that lack explicit human-waiting markers, provoking eager auto-chaining.
    Returns a list of non-blocking warning strings.
    """
    warnings = []
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.is_file():
        devlog_path = docs_dir.parent / "Devlog.md" if docs_dir.name == "docs" else devlog_path
    if not devlog_path.is_file() and (docs_dir / "docs" / "Devlog.md").is_file():
        devlog_path = docs_dir / "docs" / "Devlog.md"
    if not devlog_path.is_file():
        return warnings

    try:
        content = devlog_path.read_text(encoding="utf-8")
    except Exception:
        return warnings

    # Matches bare trigger without awaiting user confirmation guard
    pattern = re.compile(
        r'^\s*-\s*\*\*(?:Следующий шаг|Next Step):?\*\*:?\s*(?!.*(?:ожидает команды пользователя|awaits user command|awaiting user input))',
        re.IGNORECASE
    )

    rel_name = devlog_path.name
    for i, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            warnings.append(
                f"In '{rel_name}' line {i}: bare step trigger detected without user guardrail. "
                f"Prefer '- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**' to prevent auto-chaining."
            )
    return warnings


def run_linter(docs_dir: Path, verbose: bool = False) -> int:
    if verbose:
        print(f"🔍 Auditing Knowledge Base at: {docs_dir.resolve()}\n")
    if not docs_dir.exists():
        print(f"❌ Directory does not exist: {docs_dir}", file=sys.stderr)
        return 1

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
            if verbose:
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
            if not link or "XXX" in link or "Название" in link or "Имя" in link or link.lower() in ["wikilinks", "...", "target", "заметка", "документ", "файл", "slug"]:
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

    drift_warnings = check_spec_drift(docs_dir)
    devlog_warnings = check_devlog_semantic_guard(docs_dir)
    has_errors = bool(broken_links or frontmatter_warnings)

    if verbose:
        print(f"📊 Total Markdown Files Scanned: {len(all_md_files)}")
        print(f"🔗 Total Wikilinks Validated: {checked_links_count}\n")

        if broken_links:
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

        if drift_warnings:
            print(f"⚠️ Spec Drift Warnings ({len(drift_warnings)}):")
            for dw in drift_warnings:
                print(f"   • {dw}")
            print()

        if devlog_warnings:
            print(f"⚠️ Devlog Semantic Guard Warnings ({len(devlog_warnings)}):")
            for dw in devlog_warnings:
                print(f"   • {dw}")
            print()

        if has_errors:
            print("❌ Linter failed: please resolve broken links.")
            return 1
        else:
            print("🎉 Knowledge base is healthy and consistent!")
            return 0
    else:
        # Silent-on-Success mode
        for dw in drift_warnings:
            print(f"⚠️  WARN: {dw}")
        for dw in devlog_warnings:
            print(f"⚠️  WARN: {dw}")
        if not has_errors:
            print(f"OK: {len(all_md_files)} files scanned, {checked_links_count} wikilinks verified (0 broken).")
            return 0
        else:
            print(f"ERROR: {len(broken_links)} broken links, {len(frontmatter_warnings)} frontmatter warnings.")
            if broken_links:
                for src, target in broken_links:
                    print(f"   • In '{src}' -> target not found: [[{target}]]")
            if frontmatter_warnings:
                for src, msg in frontmatter_warnings:
                    print(f"   • {src}: {msg}")
            return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docs-as-Code Knowledge Base Linter")
    parser.add_argument("--path", "-p", type=str, default=".", help="Path to docs directory or project root")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose audit output")
    args = parser.parse_args()

    start = Path(args.path).resolve()
    if (start / "docs").is_dir():
        vault = start / "docs"
    elif start.name == "docs" and start.is_dir():
        vault = start
    else:
        vault = find_vault_root(start)

    exit_code = run_linter(vault, verbose=args.verbose)
    sys.exit(exit_code)
