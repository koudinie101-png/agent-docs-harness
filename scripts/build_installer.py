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
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"


def bundle_assets() -> dict:
    assets = {}

    # 1. Collect all 12 templates
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

    # 3. Collect kb_lint.py
    kb_lint = SCRIPTS_DIR / "kb_lint.py"
    if kb_lint.is_file():
        assets["scripts/kb_lint.py"] = kb_lint.read_text(encoding="utf-8")
        print(f"  • Bundled: scripts/kb_lint.py ({len(assets['scripts/kb_lint.py'])} chars)")

    # 4. Collect AI agent skills from .agents/skills/
    if SKILLS_DIR.is_dir():
        skill_dirs = sorted([d for d in SKILLS_DIR.iterdir() if d.is_dir()])
        for sdir in skill_dirs:
            skill_md = sdir / "SKILL.md"
            if skill_md.is_file():
                rel_key = f".agents/skills/{sdir.name}/SKILL.md"
                assets[rel_key] = skill_md.read_text(encoding="utf-8")
                print(f"  • Bundled skill: {sdir.name}/SKILL.md ({len(assets[rel_key])} chars)")

    return assets


def compress_bundle(assets: dict) -> str:
    raw_json = json.dumps(assets, ensure_ascii=False)
    compressed = zlib.compress(raw_json.encode("utf-8"), level=9)
    b64 = base64.b64encode(compressed).decode("ascii")
    print(f"\n📦 Bundle stats: raw {len(raw_json)} bytes -> compressed {len(b64)} b64 chars (ratio: {len(b64)/len(raw_json):.1%})")
    return b64


def build():
    print("🚀 Compiling agent-docs-harness assets into install.py...")
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
    else:
        print("⚠️ Markers not found in install.py. Please insert markers or re-run generator.")

    return bundle_b64


if __name__ == "__main__":
    build()
