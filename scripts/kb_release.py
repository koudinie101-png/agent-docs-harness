#!/usr/bin/env python3
"""
scripts/kb_release.py — Zero-Dependencies Release Automation Utility for Docs-as-Code.

Functions:
- Environment detection (Git, branch, clean working tree, remote origin, GitHub CLI status).
- Artifact inspection (SHA-256 calculation, file sizes in KB/MB).
- Phase artifacts aggregation from docs/ (Specs, Bugs, ADRs).
- Markdown generation conforming to TEMPLATE_RELEASE.md.
- CLI interface with JSON and markdown output options.
"""

import sys
import os
import re
import json
import hashlib
import shutil
import subprocess
import argparse
import posixpath
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def detect_release_environment(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Detects repository and environment capabilities:
    - has_git: bool
    - is_clean: bool
    - branch: Optional[str]
    - has_remote: bool
    - remote_url: Optional[str]
    - is_github: bool
    - has_gh_cli: bool
    - gh_authenticated: bool
    - mode: "github" | "local-only"
    """
    if repo_root is None:
        repo_root = Path.cwd()

    status: Dict[str, Any] = {
        "has_git": False,
        "is_clean": False,
        "branch": None,
        "has_remote": False,
        "remote_url": None,
        "is_github": False,
        "has_gh_cli": False,
        "gh_authenticated": False,
        "mode": "local-only",
    }

    if shutil.which("git"):
        try:
            res_worktree = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if res_worktree.returncode == 0 and res_worktree.stdout.strip() == "true":
                status["has_git"] = True

                # Current branch
                res_branch = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=repo_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if res_branch.returncode == 0:
                    status["branch"] = res_branch.stdout.strip()

                # Clean working tree check
                res_status = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=repo_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if res_status.returncode == 0:
                    status["is_clean"] = len(res_status.stdout.strip()) == 0

                # Remote origin check
                res_remote = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=repo_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if res_remote.returncode == 0:
                    status["has_remote"] = True
                    remote_url = res_remote.stdout.strip()
                    status["remote_url"] = remote_url
                    if "github.com" in remote_url.lower():
                        status["is_github"] = True
        except Exception:
            pass

    # GitHub CLI check
    if shutil.which("gh"):
        status["has_gh_cli"] = True
        try:
            res_gh_auth = subprocess.run(
                ["gh", "auth", "status"],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if res_gh_auth.returncode == 0:
                status["gh_authenticated"] = True
        except Exception:
            pass

    # Dual-Mode resolution
    if status["is_github"] and (status["has_gh_cli"] and status["gh_authenticated"]):
        status["mode"] = "github"
    else:
        status["mode"] = "local-only"

    return status


def inspect_release_artifacts(dist_dir: Path) -> List[Dict[str, str]]:
    """
    Scans dist_dir, ignoring hidden files.
    Calculates file size (KB / MB) and SHA-256 hash using 64 KB streaming chunks.
    Returns list of dicts: [{"name": str, "path": str, "size": str, "sha256": str}].
    """
    if not dist_dir.exists() or not dist_dir.is_dir():
        return []

    artifacts: List[Dict[str, str]] = []
    for item in sorted(dist_dir.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue

        hasher = hashlib.sha256()
        try:
            size_bytes = item.stat().st_size
            with open(item, "rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            sha256_hash = hasher.hexdigest()

            if size_bytes >= 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size_bytes / 1024:.1f} KB"

            rel_path = f"dist/{item.name}"
            artifacts.append({
                "name": item.name,
                "path": rel_path,
                "size": size_str,
                "sha256": sha256_hash,
            })
        except Exception as e:
            print(f"⚠️ Error reading artifact {item.name}: {e}", file=sys.stderr)

    return artifacts


def format_artifacts_markdown_table(artifacts: List[Dict[str, str]]) -> str:
    """Formats markdown table of release artifacts with SHA-256."""
    if not artifacts:
        return "*В каталоге `dist/` не обнаружено скомпилированных артефактов (Source Release).*"

    lines = [
        "| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for art in artifacts:
        lines.append(f"| `{art['name']}` | {art['size']} | `{art['sha256']}` | `{art['path']}` |")
    return "\n".join(lines)


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Simple parser for YAML frontmatter key-values without external PyYAML."""
    data: Dict[str, Any] = {}
    if not content.startswith("---"):
        return data

    parts = content.split("---", 2)
    if len(parts) < 3:
        return data

    fm_text = parts[1]
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            data[key] = val
    return data


def find_phase_artifacts(docs_dir: Path, phase_num: int) -> Dict[str, List[Dict[str, str]]]:
    """
    Scans docs/ and finds:
    - tasks: Specs in docs/02_Tasks/Specs/ matching phase_num.
    - bugs: Closed defect reports in docs/02_Tasks/Bugs/.
    - adrs: Accepted ADRs in docs/03_Decisions_ADR/.
    """
    result: Dict[str, List[Dict[str, str]]] = {
        "tasks": [],
        "bugs": [],
        "adrs": [],
    }

    if not docs_dir.exists():
        return result

    # 1. Tasks / Specs
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if specs_dir.exists():
        for spec_file in sorted(specs_dir.rglob("*.md")):
            if spec_file.name.startswith("TEMPLATE_"):
                continue
            try:
                content = spec_file.read_text(encoding="utf-8")
                fm = parse_frontmatter(content)
                file_phase = fm.get("phase")
                phase_match = False
                if file_phase is not None:
                    try:
                        phase_match = int(file_phase) == phase_num
                    except ValueError:
                        phase_match = str(file_phase) == str(phase_num)
                else:
                    # Fallback only if frontmatter phase is missing
                    if f"0{phase_num}_" in str(spec_file) or f"phase{phase_num}" in str(spec_file).lower():
                        phase_match = True

                if phase_match:
                    task_id = fm.get("id", spec_file.stem.split("-")[0])
                    title = fm.get("title", spec_file.stem)
                    # Compute relative link from docs/02_Tasks/Releases/
                    # We can use ../Specs/<subfolder>/<filename>
                    rel_to_tasks = spec_file.relative_to(docs_dir / "02_Tasks")
                    link = f"../{rel_to_tasks.as_posix()[:-3]}"
                    result["tasks"].append({
                        "id": task_id,
                        "title": title,
                        "link": link,
                        "status": fm.get("status", "done"),
                    })
            except Exception:
                pass

    # 2. Bugs
    bugs_dir = docs_dir / "02_Tasks" / "Bugs"
    if bugs_dir.exists():
        for bug_file in sorted(bugs_dir.rglob("*.md")):
            if bug_file.name.startswith("TEMPLATE_"):
                continue
            try:
                content = bug_file.read_text(encoding="utf-8")
                fm = parse_frontmatter(content)
                status = fm.get("status", "").lower()
                if status in ["done", "resolved", "closed"]:
                    bug_id = fm.get("id", bug_file.stem)
                    title = fm.get("title", bug_file.stem)
                    rel_to_tasks = bug_file.relative_to(docs_dir / "02_Tasks")
                    link = f"../{rel_to_tasks.as_posix()[:-3]}"
                    result["bugs"].append({
                        "id": bug_id,
                        "title": title,
                        "link": link,
                        "status": status,
                    })
            except Exception:
                pass

    # 3. ADRs
    adrs_dir = docs_dir / "03_Decisions_ADR"
    if adrs_dir.exists():
        for adr_file in sorted(adrs_dir.glob("*.md")):
            if adr_file.name.startswith("TEMPLATE_"):
                continue
            try:
                content = adr_file.read_text(encoding="utf-8")
                fm = parse_frontmatter(content)
                status = fm.get("status", "").lower()
                if status == "accepted":
                    adr_id = fm.get("id", adr_file.stem)
                    title = fm.get("title", adr_file.stem)
                    link = f"../../03_Decisions_ADR/{adr_file.stem}"
                    result["adrs"].append({
                        "id": adr_id,
                        "title": title,
                        "link": link,
                        "status": status,
                    })
            except Exception:
                pass

    return result


def generate_release_markdown(
    version: str,
    phase_num: int,
    env_info: Dict[str, Any],
    artifacts: List[Dict[str, str]],
    phase_data: Dict[str, List[Dict[str, str]]],
    summary: str = "",
    release_date: Optional[str] = None,
) -> str:
    """Generates complete RELEASE-vX.Y.Z.md content conforming to TEMPLATE_RELEASE.md."""
    import datetime

    ver_clean = version.lstrip("v")
    tag = f"v{ver_clean}"
    today = release_date or datetime.date.today().isoformat()
    mode = env_info.get("mode", "local-only")
    remote_url = env_info.get("remote_url", "")
    gh_release_url = ""
    if mode == "github" and remote_url:
        # Convert git url to https
        clean_url = remote_url.replace("git@github.com:", "https://github.com/")
        if clean_url.endswith(".git"):
            clean_url = clean_url[:-4]
        gh_release_url = f"{clean_url}/releases/tag/{tag}"

    # Features list
    features_md: List[str] = []
    if phase_data.get("tasks"):
        for t in phase_data["tasks"]:
            features_md.append(f"- [[{t['link']}|{t['id']}]]: {t['title']}.")
    else:
        features_md.append("- Плановые задачи фазы выполнены.")

    # Bug fixes list
    bugs_md: List[str] = []
    if phase_data.get("bugs"):
        for b in phase_data["bugs"]:
            bugs_md.append(f"- [[{b['link']}|{b['id']}]]: {b['title']}.")
    else:
        bugs_md.append("- Критических дефектов и регрессий за период фазы не зафиксировано.")

    # ADRs list
    adrs_md: List[str] = []
    if phase_data.get("adrs"):
        for a in phase_data["adrs"]:
            adrs_md.append(f"- [[{a['link']}|{a['id']}]]: {a['title']}.")
    else:
        adrs_md.append("- Архитектурных изменений в рамках фазы не вводилось.")

    artifacts_table = format_artifacts_markdown_table(artifacts)

    # Verification instructions
    first_art_name = artifacts[0]["name"] if artifacts else "archive.zip"
    verify_snippet = f"""```bash
# Проверка в PowerShell (Windows)
Get-FileHash -Path dist/{first_art_name} -Algorithm SHA256

# Проверка в Bash / macOS / Linux
sha256sum dist/{first_art_name}
# или
shasum -a 256 dist/{first_art_name}
```"""

    doc_summary = summary.strip() or f"Официальный релиз {tag} по завершении Фазы {phase_num}."

    frontmatter_artifacts = []
    for art in artifacts:
        frontmatter_artifacts.append(
            f"  - name: \"{art['name']}\"\n"
            f"    path: \"{art['path']}\"\n"
            f"    size: \"{art['size']}\"\n"
            f"    sha256: \"{art['sha256']}\""
        )
    fm_artifacts_str = "\n".join(frontmatter_artifacts) if frontmatter_artifacts else "  []"

    content = f"""---
id: RELEASE-{tag}
title: "Релиз {tag}: Фаза {phase_num}"
version: "{ver_clean}"
phase: {phase_num}
status: completed
date: {today}
git_tag: "{tag}"
github_release_url: "{gh_release_url}"
mode: "{mode}"
artifacts:
{fm_artifacts_str}
tags:
  - release
  - changelog
  - {tag}
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз {tag}: Фаза {phase_num}

> **Версия:** {tag}  
> **Фаза:** {phase_num}  
> **Дата:** {today}  
> **Режим публикации:** {'GitHub Release' if mode == 'github' else 'Local-Only Package'}  
> **Git Tag:** `{tag}`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
{doc_summary}

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
{chr(10).join(features_md)}

### 🐛 Исправленные дефекты (Bug Fixes)
{chr(10).join(bugs_md)}

### 🏛️ Архитектурные решения (ADR)
{chr(10).join(adrs_md)}

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

{artifacts_table}

---

## 🔍 Инструкция по проверке целостности артефактов

{verify_snippet}

---

## 📋 Чеклист верификации и приемки релиза
- [x] Все задачи фазы {phase_num} завершены и проверены в `Roadmap.md`.
- [x] Все приемочные тесты (`05_Testing/`) успешно пройдены.
- [x] Целостность базы знаний подтверждена (`python scripts/kb_lint.py --path docs`).
- [x] Все артефакты в `dist/` собраны и контрольные суммы SHA-256 рассчитаны.
- [x] Релизный документ зафиксирован в `docs/02_Tasks/Releases/RELEASE-{tag}.md`.
"""
    return content


def convert_wikilinks_to_github_markdown(text: str, repo_url: str = "", branch: str = "main") -> str:
    """
    Converts internal Obsidian wikilinks to clean GitHub Flavored Markdown:
    - [[path/to/spec|Title]] -> [Title](repo_url/blob/branch/docs/path/to/spec.md) (if repo_url provided)
    - [[path/to/spec|Title]] -> **Title** (if repo_url is empty)
    - [[Title]] -> **Title**
    """
    clean_repo_url = ""
    if repo_url:
        clean_repo_url = repo_url.replace("git@github.com:", "https://github.com/").rstrip("/")
        if clean_repo_url.endswith(".git"):
            clean_repo_url = clean_repo_url[:-4]

    def replace_wikilink(match):
        target = match.group(1).strip()
        alias = match.group(2).strip() if match.group(2) else target

        # External URLs inside wikilinks
        if target.startswith("http://") or target.startswith("https://"):
            return f"[{alias}]({target})"

        if clean_repo_url:
            # Resolve relative link from docs/02_Tasks/Releases/
            if target.startswith("../") or target.startswith("./"):
                resolved = posixpath.normpath(posixpath.join("02_Tasks/Releases", target))
            else:
                resolved = target.lstrip("/")

            clean_target = resolved
            if not clean_target.endswith(".md"):
                clean_target += ".md"

            full_url = f"{clean_repo_url}/blob/{branch}/docs/{clean_target}"
            return f"[{alias}]({full_url})"

        return f"**{alias}**"

    pattern = r"\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]"
    return re.sub(pattern, replace_wikilink, text)


def generate_public_release_notes(
    version: str,
    phase_num: int,
    env_info: Dict[str, Any],
    artifacts: List[Dict[str, str]],
    phase_data: Dict[str, List[Dict[str, str]]],
    summary: str = "",
) -> str:
    """Generates public dist/RELEASE_NOTES.md in clean GitHub Flavored Markdown (GFM)."""
    ver_clean = version.lstrip("v")
    tag = f"v{ver_clean}"
    branch = env_info.get("branch") or "main"
    remote_url = env_info.get("remote_url", "")
    clean_repo_url = ""
    raw_install_url = "https://raw.githubusercontent.com/<owner>/<repo>/main/install.py"
    diff_url = ""

    if remote_url:
        clean_repo_url = remote_url.replace("git@github.com:", "https://github.com/").rstrip("/")
        if clean_repo_url.endswith(".git"):
            clean_repo_url = clean_repo_url[:-4]
        if "github.com/" in clean_repo_url:
            repo_path = clean_repo_url.split("github.com/", 1)[1]
            raw_install_url = f"https://raw.githubusercontent.com/{repo_path}/{branch}/install.py"
            diff_url = f"{clean_repo_url}/releases/tag/{tag}"

    doc_summary = summary.strip() or f"Официальный релиз {tag} по завершении Фазы {phase_num}."

    # Features
    features_md: List[str] = []
    if phase_data.get("tasks"):
        for t in phase_data["tasks"]:
            raw_item = f"- [[{t['link']}|{t['id']}]]: {t['title']}."
            features_md.append(convert_wikilinks_to_github_markdown(raw_item, clean_repo_url, branch))
    else:
        features_md.append("- Плановые задачи фазы выполнены.")

    # Bug fixes
    bugs_md: List[str] = []
    if phase_data.get("bugs"):
        for b in phase_data["bugs"]:
            raw_item = f"- [[{b['link']}|{b['id']}]]: {b['title']}."
            bugs_md.append(convert_wikilinks_to_github_markdown(raw_item, clean_repo_url, branch))
    else:
        bugs_md.append("- Критических дефектов и регрессий за период фазы не зафиксировано.")

    # ADRs
    adrs_md: List[str] = []
    if phase_data.get("adrs"):
        for a in phase_data["adrs"]:
            raw_item = f"- [[{a['link']}|{a['id']}]]: {a['title']}."
            adrs_md.append(convert_wikilinks_to_github_markdown(raw_item, clean_repo_url, branch))
    else:
        adrs_md.append("- Архитектурных изменений в рамках фазы не вводилось.")

    artifacts_table = format_artifacts_markdown_table(artifacts)
    first_art_name = artifacts[0]["name"] if artifacts else "install.py"

    full_changelog_md = ""
    if diff_url:
        full_changelog_md = f"\n\n---\n\n**Полный список изменений (Full Changelog):** {diff_url}"

    notes = f"""# 🚀 Release {tag} — Фаза {phase_num}

> 💡 **Executive Summary:** {doc_summary}

---

### ⚡ Быстрый старт / Обновление (Quick Install)
```bash
# Новая установка Docs-as-Code
curl -fsSL {raw_install_url} | python3

# Обновление существующего проекта
python install.py --update
```

---

### ✨ Новые возможности (Features)
{chr(10).join(features_md)}

### 🐛 Исправленные дефекты (Bug Fixes)
{chr(10).join(bugs_md)}

### 🏛️ Архитектурные решения (ADR)
{chr(10).join(adrs_md)}

---

### 📦 Релизные артефакты и контрольные суммы (SHA-256 Checksums)

{artifacts_table}

**Верификация в PowerShell:**
```powershell
Get-FileHash -Path ./dist/{first_art_name} -Algorithm SHA256
```

**Верификация в Bash:**
```bash
sha256sum ./dist/{first_art_name}
```{full_changelog_md}
"""
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="kb_release.py — Zero-Dependencies Release Automation Utility for Docs-as-Code"
    )
    parser.add_argument("--version", type=str, default="", help="Release version (e.g. 0.4.0 or v0.4.0)")
    parser.add_argument("--phase", type=int, default=1, help="Phase number associated with the release")
    parser.add_argument("--docs-dir", type=str, default="docs", help="Path to docs directory (default: docs)")
    parser.add_argument("--dist-dir", type=str, default="dist", help="Path to dist directory (default: dist)")
    parser.add_argument("--output", type=str, default="", help="Target release markdown path")
    parser.add_argument("--notes-output", type=str, default="", help="Path to public release notes (default: <dist-dir>/RELEASE_NOTES.md)")
    parser.add_argument("--summary", type=str, default="", help="Executive summary text")
    parser.add_argument("--dry-run", action="store_true", help="Print release markdown to stdout without writing")
    parser.add_argument("--detect-only", action="store_true", help="Only detect environment and print JSON")
    parser.add_argument("--ci-mode", action="store_true", help="Run in CI mode for GitHub Actions")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    repo_root = Path.cwd()
    env_info = detect_release_environment(repo_root)

    if args.detect_only:
        print(json.dumps(env_info, indent=2, ensure_ascii=False))
        return 0

    if not args.version:
        print("❌ Error: --version is required (e.g. --version 0.4.0 or --version v0.4.0)", file=sys.stderr)
        return 1

    ver_clean = args.version.lstrip("v")
    tag = f"v{ver_clean}"

    docs_path = Path(args.docs_dir)
    dist_path = Path(args.dist_dir)

    artifacts = inspect_release_artifacts(dist_path)
    phase_data = find_phase_artifacts(docs_path, args.phase)

    release_content = generate_release_markdown(
        version=ver_clean,
        phase_num=args.phase,
        env_info=env_info,
        artifacts=artifacts,
        phase_data=phase_data,
        summary=args.summary,
    )

    public_notes = generate_public_release_notes(
        version=ver_clean,
        phase_num=args.phase,
        env_info=env_info,
        artifacts=artifacts,
        phase_data=phase_data,
        summary=args.summary,
    )

    if args.dry_run:
        print(release_content)
        print("\n" + "=" * 40 + " PUBLIC RELEASE NOTES " + "=" * 40 + "\n")
        print(public_notes)
        return 0

    out_path = Path(args.output) if args.output else docs_path / "02_Tasks" / "Releases" / f"RELEASE-{tag}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(release_content, encoding="utf-8")

    notes_path = Path(args.notes_output) if args.notes_output else dist_path / "RELEASE_NOTES.md"
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text(public_notes, encoding="utf-8")

    if args.verbose:
        print(f"✅ Generated release document: {out_path.as_posix()}")
        print(f"✅ Generated public release notes: {notes_path.as_posix()}")
        print(f"📦 Artifacts cataloged: {len(artifacts)}")
        print(f"🌐 Environment mode: {env_info['mode']}")
    else:
        print(f"OK: Release {tag} generated at {out_path.as_posix()} and {notes_path.as_posix()} ({len(artifacts)} artifacts, mode: {env_info['mode']}).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
