#!/usr/bin/env python3
"""
Builder script for agent-docs-harness installer.
Compiles templates, graph.json, and kb_lint.py into self-contained payload inside install.py.
Zero external dependencies (Python 3 stdlib: base64, zlib, json, pathlib).
"""

import os
import sys
import json
import zlib
import base64
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
SCRIPTS_DIR = REPO_ROOT / "scripts"
INSTALL_PY = REPO_ROOT / "install.py"
DIST_DIR = REPO_ROOT / "dist"
DIST_INSTALL_PY = DIST_DIR / "install.py"
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"


def bundle_assets() -> dict:
    assets = {}

    # 1. Collect all 14 templates
    template_files = sorted(list(TEMPLATES_DIR.glob("*.md")))
    if not template_files:
        raise RuntimeError(f"No templates found in {TEMPLATES_DIR}")

    for tf in template_files:
        content = tf.read_text(encoding="utf-8")
        assets[f"00_Templates/{tf.name}"] = content
        print(f"  • Bundled template: {tf.name} ({len(content)} chars)")

    # 2. Collect graph.json
    graph_json = TEMPLATES_DIR / "graph.json"
    if graph_json.is_file():
        assets[".obsidian/graph.json"] = graph_json.read_text(encoding="utf-8")
        print(f"  • Bundled: .obsidian/graph.json")

    # 3. Collect scripts (kb_lint.py, kb_release.py, kb_ingest.py)
    for sname in ["kb_lint.py", "kb_release.py", "kb_ingest.py"]:
        sfile = SCRIPTS_DIR / sname
        if sfile.is_file():
            assets[f"scripts/{sname}"] = sfile.read_text(encoding="utf-8")
            print(f"  • Bundled: scripts/{sname} ({len(assets[f'scripts/{sname}'])} chars)")

    # 4. Collect AI agent skills from .agents/skills/
    if SKILLS_DIR.is_dir():
        skill_dirs = sorted([d for d in SKILLS_DIR.iterdir() if d.is_dir()])
        for sdir in skill_dirs:
            skill_md = sdir / "SKILL.md"
            if skill_md.is_file():
                rel_key = f".agents/skills/{sdir.name}/SKILL.md"
                assets[rel_key] = skill_md.read_text(encoding="utf-8")
                print(f"  • Bundled skill: {sdir.name}/SKILL.md ({len(assets[rel_key])} chars)")

    # 5. Collect CI workflows and issue templates
    workflows_dir = REPO_ROOT / ".github" / "workflows"
    if workflows_dir.is_dir():
        for wf in sorted(list(workflows_dir.glob("*.yml"))):
            rel_key = f".github/workflows/{wf.name}"
            assets[rel_key] = wf.read_text(encoding="utf-8")
            print(f"  • Bundled workflow: {wf.name} ({len(assets[rel_key])} chars)")

    issue_tpl_dir = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"
    if issue_tpl_dir.is_dir():
        for itf in sorted(list(issue_tpl_dir.glob("*.yml"))):
            if itf.name == "config.yml":
                continue
            rel_key = f".github/ISSUE_TEMPLATE/{itf.name}"
            assets[rel_key] = itf.read_text(encoding="utf-8")
            print(f"  • Bundled issue template: {itf.name} ({len(assets[rel_key])} chars)")


    # 6. Collect Zero_To_Hero_Guide.md
    zth_guide = REPO_ROOT / "docs" / "Zero_To_Hero_Guide.md"
    if zth_guide.is_file():
        assets["docs/Zero_To_Hero_Guide.md"] = zth_guide.read_text(encoding="utf-8")
        print(f"  • Bundled guide: Zero_To_Hero_Guide.md ({len(assets['docs/Zero_To_Hero_Guide.md'])} chars)")

    # 7. Collect procedural memory patterns.md
    memory_patterns = REPO_ROOT / "docs" / "06_Memory" / "patterns.md"
    if memory_patterns.is_file():
        assets["docs/06_Memory/patterns.md"] = memory_patterns.read_text(encoding="utf-8")
        print(f"  • Bundled memory patterns: patterns.md ({len(assets['docs/06_Memory/patterns.md'])} chars)")

    # 8. Collect single-source rules corpus (TASK-085)
    rules_corpus = REPO_ROOT / "rules" / "AGENTS_CORE.md"
    if not rules_corpus.is_file():
        raise RuntimeError(f"Rules corpus not found: {rules_corpus}")
    assets["rules/AGENTS_CORE.md"] = rules_corpus.read_text(encoding="utf-8")
    print(f"  • Bundled rules corpus: rules/AGENTS_CORE.md ({len(assets['rules/AGENTS_CORE.md'])} chars)")

    return assets


def compress_bundle(assets: dict) -> str:
    raw_json = json.dumps(assets, ensure_ascii=False)
    compressed = zlib.compress(raw_json.encode("utf-8"), level=9)
    b64 = base64.b64encode(compressed).decode("ascii")
    print(f"\n📦 Bundle stats: raw {len(raw_json)} bytes -> compressed {len(b64)} b64 chars (ratio: {len(b64)/len(raw_json):.1%})")
    return b64


def build():
    print("🚀 Compiling agent-docs-harness assets into install.py and dist/install.py...")
    assets = bundle_assets()
    bundle_b64 = compress_bundle(assets)

    if not INSTALL_PY.exists():
        print(f"⚠️ {INSTALL_PY} does not exist yet. It will be generated from template.")
        return bundle_b64

    content = INSTALL_PY.read_text(encoding="utf-8")
    marker_start = "# --- BEGIN_EMBEDDED_ASSETS ---"
    marker_end = "# --- END_EMBEDDED_ASSETS ---"

    if marker_start in content and marker_end in content:
        before = content.split(marker_start)[0]
        after = content.split(marker_end)[1]
        new_content = f"{before}{marker_start}\nEMBEDDED_ASSETS_B64 = \"{bundle_b64}\"\n{marker_end}{after}"
        with open(INSTALL_PY, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        size_kb = INSTALL_PY.stat().st_size / 1024
        print(f"✅ Successfully updated embedded payload in {INSTALL_PY.name}! (Size: {size_kb:.1f} KB / {INSTALL_PY.stat().st_size} bytes)")

        # Also emit to dist/install.py
        DIST_DIR.mkdir(parents=True, exist_ok=True)
        with open(DIST_INSTALL_PY, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        dist_size_kb = DIST_INSTALL_PY.stat().st_size / 1024
        print(f"✅ Successfully mirrored compiled installer into {DIST_INSTALL_PY.relative_to(REPO_ROOT)}! (Size: {dist_size_kb:.1f} KB / {DIST_INSTALL_PY.stat().st_size} bytes)")
    else:
        print("⚠️ Markers not found in install.py. Please insert markers or re-run generator.")

    return bundle_b64


if __name__ == "__main__":
    build()
