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
from typing import Dict, List, Any, Optional, Tuple, Set, Iterable

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_env_local(repo_root: Optional[Path] = None):
    """Loads key-value pairs from .env.local if present, without overwriting existing env."""
    root = repo_root or Path.cwd()
    env_file = root / ".env.local"
    if not env_file.is_file():
        return
    try:
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'\"")
            if k and k not in os.environ:
                os.environ[k] = v
    except Exception:
        pass


def detect_release_environment(repo_root: Optional[Path] = None, explicit_mode: str = "auto") -> Dict[str, Any]:
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
    - has_github_token: bool
    - publish_provider: "gh_cli" | "rest_api" | "none"
    - mode: "github" | "local-only"
    - warning: Optional[str]
    """
    if repo_root is None:
        repo_root = Path.cwd()

    load_env_local(repo_root)
    github_token = os.environ.get("GITHUB_TOKEN", "").strip()

    status: Dict[str, Any] = {
        "has_git": False,
        "is_clean": False,
        "branch": None,
        "has_remote": False,
        "remote_url": None,
        "is_github": False,
        "has_gh_cli": False,
        "gh_authenticated": False,
        "has_github_token": bool(github_token),
        "publish_provider": "none",
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
    if explicit_mode == "local-only":
        status["mode"] = "local-only"
        status["publish_provider"] = "none"
    elif explicit_mode == "github":
        if status["has_gh_cli"] and status["gh_authenticated"]:
            status["mode"] = "github"
            status["publish_provider"] = "gh_cli"
        elif status["has_github_token"]:
            status["mode"] = "github"
            status["publish_provider"] = "rest_api"
        else:
            status["mode"] = "local-only"
            status["publish_provider"] = "none"
            reason = "gh_cli_not_installed" if not status["has_gh_cli"] else "gh_not_authenticated"
            status["gh_missing_reason"] = reason
            status["warning"] = (
                "Запрошен режим GitHub, но GitHub CLI ('gh') не установлен/не авторизован, и GITHUB_TOKEN не задан. "
                "Релиз переведен в режим Local-Only. Для публикации на GitHub Releases установите gh "
                "('winget install GitHub.cli' на Windows, 'brew install gh' на macOS) или укажите GITHUB_TOKEN."
            )
    else:  # "auto"
        if status["is_github"]:
            if status["has_gh_cli"] and status["gh_authenticated"]:
                status["mode"] = "github"
                status["publish_provider"] = "gh_cli"
            elif status["has_github_token"]:
                status["mode"] = "github"
                status["publish_provider"] = "rest_api"
            else:
                status["mode"] = "local-only"
                status["publish_provider"] = "none"
                reason = "gh_cli_not_installed" if not status["has_gh_cli"] else "gh_not_authenticated"
                status["gh_missing_reason"] = reason
                status["warning"] = (
                    "Репозиторий размещен на GitHub, но GitHub CLI ('gh') не найден/не авторизован, и GITHUB_TOKEN не задан. "
                    "Релиз переведен в режим Local-Only. Для публикации на GitHub Releases установите gh "
                    "('winget install GitHub.cli' на Windows, 'brew install gh' на macOS) или задайте GITHUB_TOKEN."
                )
        else:
            status["mode"] = "local-only"

    return status


def inspect_release_artifacts(dist_dir: Path, excluded_names: Optional[Iterable[str]] = None) -> List[Dict[str, str]]:
    """
    Scans dist_dir, ignoring hidden files and release notes documents.
    Calculates file size (KB / MB) and SHA-256 hash using 64 KB streaming chunks.
    Returns list of dicts: [{"name": str, "path": str, "size": str, "sha256": str}].
    """
    if not dist_dir.exists() or not dist_dir.is_dir():
        return []

    ignore_set: Set[str] = {"RELEASE_NOTES.md"}
    if excluded_names:
        ignore_set.update(excluded_names)

    artifacts: List[Dict[str, str]] = []
    for item in sorted(dist_dir.iterdir()):
        if not item.is_file() or item.name.startswith(".") or item.name in ignore_set:
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


def normalize_version(ver: Optional[str]) -> str:
    """Normalizes version string for reliable comparison (strips leading 'v', trims, lowercases)."""
    if not ver:
        return ""
    ver = str(ver).strip().lower()
    if ver.startswith("v"):
        ver = ver[1:]
    return ver


def is_release_blocker(val: Any) -> bool:
    """Checks if a frontmatter release_blocker value evaluates to True."""
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() in ["true", "1", "yes"]
    if isinstance(val, (int, float)):
        return bool(val)
    return False


def collect_fixed_bugs(
    bugs_dir: Path,
    target_version: Optional[str] = None,
    current_phase: Optional[int] = None,
    target_phases: Optional[List[int]] = None,
) -> List[Dict[str, str]]:
    """
    Collects closed defect reports targeted strictly for the release version or phase.

    Inclusion criteria:
    1. status in ['done', 'resolved', 'closed', 'fixed']
    2. If target_version is provided:
       - If bug specifies fixed_in: include if normalize_version(fixed_in) == normalize_version(target_version), else exclude.
       - Else if bug specifies target_release: include if normalize_version(target_release) == normalize_version(target_version), else exclude.
       - Else if bug specifies target_phase: include if (current_phase is not None and bug_phase == current_phase) or (target_phases and bug_phase in target_phases), else exclude.
       - Else (no fixed_in, no target_release, no target_phase): include for backward compatibility with legacy unannotated reports.
    3. If target_version is not provided:
       - If current_phase or target_phases provided:
         * If bug specifies target_phase: include if bug_phase in active_phases, else exclude.
         * Else: include.
       - Else: include all closed bugs.
    """
    bugs: List[Dict[str, str]] = []
    if not bugs_dir.exists():
        return bugs

    active_phases = list(target_phases) if target_phases else ([current_phase] if current_phase is not None else [])
    norm_target_ver = normalize_version(target_version)

    for bug_file in sorted(bugs_dir.rglob("*.md")):
        if bug_file.name.startswith("TEMPLATE_"):
            continue
        try:
            content = bug_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            status = fm.get("status", "").strip().lower()
            if status not in ["done", "resolved", "closed", "fixed"]:
                continue

            bug_id = fm.get("id", bug_file.stem)
            title = fm.get("title", bug_file.stem)
            fixed_in = fm.get("fixed_in", "")
            target_release = fm.get("target_release", "")
            target_phase_raw = fm.get("target_phase")
            bug_phase: Optional[int] = None
            if target_phase_raw is not None and str(target_phase_raw).strip() != "" and str(target_phase_raw).strip().lower() != "null":
                try:
                    bug_phase = int(str(target_phase_raw).strip())
                except ValueError:
                    pass

            include = False
            if norm_target_ver:
                if fixed_in and fixed_in.lower() != "null":
                    include = (normalize_version(fixed_in) == norm_target_ver)
                elif target_release and target_release.lower() != "null":
                    include = (normalize_version(target_release) == norm_target_ver)
                elif bug_phase is not None:
                    include = (bug_phase in active_phases)
                else:
                    # Legacy fallback: bug has no version and no phase metadata
                    include = True
            elif active_phases:
                if bug_phase is not None:
                    include = (bug_phase in active_phases)
                else:
                    include = True
            else:
                include = True

            if include:
                try:
                    if bugs_dir.name == "Bugs" and bugs_dir.parent.name == "02_Tasks":
                        rel_to_tasks = bug_file.relative_to(bugs_dir.parent)
                        link = f"../{rel_to_tasks.as_posix()[:-3]}"
                    else:
                        link = f"../Bugs/{bug_file.stem}"
                except Exception:
                    link = f"../Bugs/{bug_file.stem}"

                bugs.append({
                    "id": bug_id,
                    "title": title,
                    "link": link,
                    "status": status,
                })
        except Exception:
            pass

    return bugs


def check_release_blockers(
    bugs_dir: Path,
    target_version: Optional[str] = None,
    current_phase: Optional[int] = None,
    target_phases: Optional[List[int]] = None,
) -> List[str]:
    """
    Checks for open defects with release_blocker == True targeting the release version or phase.
    Returns a list of error messages. If non-empty, release pipeline must abort with Exit Code 1.
    """
    errors: List[str] = []
    if not bugs_dir.exists():
        return errors

    active_phases = list(target_phases) if target_phases else ([current_phase] if current_phase is not None else [])
    norm_target_ver = normalize_version(target_version)

    for bug_file in sorted(bugs_dir.rglob("*.md")):
        if bug_file.name.startswith("TEMPLATE_"):
            continue
        try:
            content = bug_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            status = fm.get("status", "").strip().lower()
            if status in ["done", "resolved", "closed", "fixed"]:
                continue

            if not is_release_blocker(fm.get("release_blocker")):
                continue

            bug_id = fm.get("id", bug_file.stem)
            title = fm.get("title", bug_file.stem)
            target_rel = fm.get("target_release", "")
            target_ph_raw = fm.get("target_phase")
            bug_phase: Optional[int] = None
            if target_ph_raw is not None and str(target_ph_raw).strip() != "" and str(target_ph_raw).strip().lower() != "null":
                try:
                    bug_phase = int(str(target_ph_raw).strip())
                except ValueError:
                    pass

            applies = False
            if norm_target_ver:
                if target_rel and target_rel.lower() != "null":
                    applies = (normalize_version(target_rel) == norm_target_ver)
                elif bug_phase is not None:
                    applies = (bug_phase in active_phases)
                else:
                    # Unspecified open blocker applies to current active release
                    applies = True
            elif active_phases:
                if bug_phase is not None:
                    applies = (bug_phase in active_phases)
                elif not target_rel or target_rel.lower() == "null":
                    applies = True
            else:
                applies = True

            if applies:
                ver_display = target_version if target_version else (f"Phase {current_phase}" if current_phase else "target")
                errors.append(f"Release {ver_display} is blocked by open defect {bug_id}: {title} (release_blocker=true)")
        except Exception:
            pass

    return errors


def extract_release_meta_from_doc(doc_path: Path) -> Dict[str, Any]:
    """
    Extracts phase and executive summary from an existing RELEASE-vX.Y.Z.md file.
    Preserves ground-truth metadata generated during release cut.
    """
    meta: Dict[str, Any] = {"phase": None, "summary": ""}
    if not doc_path.exists() or not doc_path.is_file():
        return meta

    try:
        content = doc_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if "phase" in fm:
            try:
                meta["phase"] = int(fm["phase"])
            except ValueError:
                pass
        if "phases" in fm:
            raw_phases = str(fm["phases"]).strip("[] ")
            phases_list = [int(p.strip()) for p in raw_phases.split(",") if p.strip().isdigit()]
            if phases_list:
                meta["phases"] = phases_list

        # Extract Executive Summary section
        pattern = r"##\s+.*?Executive Summary.*?\n([\s\S]*?)(?=\n##|\n---|$(?![\r\n]))"
        match = re.search(pattern, content)
        if match:
            raw_summary = match.group(1).strip()
            clean_lines = []
            for line in raw_summary.splitlines():
                stripped = line.strip()
                if stripped.startswith(">"):
                    stripped = stripped.lstrip(">").strip()
                if stripped:
                    clean_lines.append(stripped)
            summary_candidate = " ".join(clean_lines).strip()
            summary_candidate = re.sub(r"^(?:💡\s*)?(?:\*\*Executive Summary:\*\*\s*)?", "", summary_candidate).strip()
            meta["summary"] = summary_candidate
    except Exception:
        pass

    return meta


def detect_latest_phase(docs_dir: Path) -> int:
    """
    Scans docs/02_Tasks/Specs/ to detect the highest phase number.
    Falls back to 1 if no phases are found.
    """
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if not specs_dir.exists():
        return 1

    highest_phase = 1
    for item in specs_dir.iterdir():
        if item.is_dir():
            match = re.match(r"^(\d+)_", item.name)
            if match:
                try:
                    highest_phase = max(highest_phase, int(match.group(1)))
                except ValueError:
                    pass

    for spec_file in specs_dir.rglob("*.md"):
        if spec_file.name.startswith("TEMPLATE_"):
            continue
        try:
            fm = parse_frontmatter(spec_file.read_text(encoding="utf-8"))
            if "phase" in fm:
                highest_phase = max(highest_phase, int(fm["phase"]))
        except Exception:
            pass

    return highest_phase


def is_adr_for_phase(
    adr_path: Path,
    adr_content: str,
    phase_num: int,
    phase_context_text: str,
) -> bool:
    """
    Determines if an accepted ADR belongs to the specified phase_num:
    1. Explicit 'phase: N' in ADR frontmatter.
    2. Tag 'phaseN', 'phase-N', or '#phaseN' in ADR content.
    3. ADR id (e.g. 'ADR-0017') or filename stem referenced in phase tasks, plans, or roadmap.
    """
    fm = parse_frontmatter(adr_content)
    if "phase" in fm:
        try:
            return int(fm["phase"]) == phase_num
        except ValueError:
            return str(fm["phase"]).strip() == str(phase_num).strip()

    # Check phase tags in ADR content
    if re.search(rf"(?:#|\b)phase[-_]?{phase_num}\b", adr_content, re.IGNORECASE):
        return True

    # Check if ADR ID or stem is mentioned in phase context (tasks, plan, roadmap)
    adr_id = fm.get("id", adr_path.stem)
    adr_stem = adr_path.stem
    if re.search(rf"\b{re.escape(adr_id)}\b", phase_context_text, re.IGNORECASE) or \
       re.search(rf"\b{re.escape(adr_stem)}\b", phase_context_text, re.IGNORECASE):
        return True

    return False


def find_phase_artifacts(
    docs_dir: Path,
    phase_num: int,
    phases: Optional[List[int]] = None,
    target_version: Optional[str] = None,
) -> Dict[str, List[Dict[str, str]]]:
    """
    Scans docs/ and finds:
    - tasks: Specs in docs/02_Tasks/Specs/ matching phase_num (or phases list).
    - bugs: Closed defect reports in docs/02_Tasks/Bugs/.
    - adrs: Accepted ADRs in docs/03_Decisions_ADR/ relevant to phase_num (or phases list).
    """
    result: Dict[str, List[Dict[str, str]]] = {
        "tasks": [],
        "bugs": [],
        "adrs": [],
    }

    if not docs_dir.exists():
        return result

    target_phases = phases if phases else [phase_num]
    phase_tasks_text_parts: List[str] = []

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
                        phase_match = int(file_phase) in target_phases
                    except ValueError:
                        phase_match = str(file_phase) in [str(p) for p in target_phases]
                else:
                    # Fallback only if frontmatter phase is missing
                    for p in target_phases:
                        if f"0{p}_" in str(spec_file) or f"phase{p}" in str(spec_file).lower():
                            phase_match = True
                            break

                if phase_match:
                    phase_tasks_text_parts.append(content)
                    task_id = fm.get("id", spec_file.stem.split("-")[0])
                    title = fm.get("title", spec_file.stem)
                    rel_to_tasks = spec_file.relative_to(docs_dir / "02_Tasks")
                    link = f"../{rel_to_tasks.as_posix()[:-3]}"
                    result["tasks"].append({
                        "id": task_id,
                        "title": title,
                        "link": link,
                        "status": fm.get("status", "done"),
                        "type": fm.get("type", "task"),
                    })
            except Exception:
                pass

    # Collect phase context from plans and roadmap
    phase_context_parts: List[str] = list(phase_tasks_text_parts)
    plans_dir = docs_dir / "02_Tasks" / "Plans"
    if plans_dir.exists():
        for plan_file in sorted(plans_dir.glob("*.md")):
            if plan_file.name.startswith("TEMPLATE_"):
                continue
            try:
                plan_content = plan_file.read_text(encoding="utf-8")
                plan_fm = parse_frontmatter(plan_content)
                plan_phase = plan_fm.get("phase")
                match_plan = False
                if plan_phase is not None:
                    try:
                        match_plan = int(plan_phase) in target_phases
                    except ValueError:
                        match_plan = str(plan_phase) in [str(p) for p in target_phases]
                else:
                    for p in target_phases:
                        if f"PLAN-{p:03d}" in plan_file.name or f"phase{p}" in plan_file.name.lower():
                            match_plan = True
                            break

                if match_plan:
                    phase_context_parts.append(plan_content)
            except Exception:
                pass

    roadmap_file = docs_dir / "02_Tasks" / "Roadmap.md"
    if roadmap_file.is_file():
        try:
            rm_content = roadmap_file.read_text(encoding="utf-8")
            for p in target_phases:
                m = re.search(
                    rf"(?:##\s+Фаза\s+{p}:|##\s+Phase\s+{p}:)([\s\S]*?)(?=\n##|\n---|$)",
                    rm_content,
                    re.IGNORECASE,
                )
                if m:
                    phase_context_parts.append(m.group(0))
        except Exception:
            pass

    phase_context_text = "\n".join(phase_context_parts)

    # 2. Bugs
    bugs_dir = docs_dir / "02_Tasks" / "Bugs"
    result["bugs"] = collect_fixed_bugs(
        bugs_dir=bugs_dir,
        target_version=target_version,
        current_phase=phase_num,
        target_phases=target_phases,
    )

    # 3. ADRs (filtered by target phases)
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
                    if any(is_adr_for_phase(adr_file, content, p, phase_context_text) for p in target_phases):
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
    phases: Optional[List[int]] = None,
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

    is_cumulative = phases is not None and len(phases) > 1
    if is_cumulative:
        phases_title = " и ".join(str(p) for p in phases) if len(phases) == 2 else ", ".join(str(p) for p in phases)
        title_str = f"Релиз {tag}: Фазы {phases_title} (Кумулятивный)"
        phases_fm_str = f"phases: [{', '.join(str(p) for p in phases)}]\n"
        meta_phase_line = f"> **Фазы:** {phases_title} (Кумулятивный)  "
        checklist_phase_line = f"- [x] Все задачи фаз {phases_title} завершены и проверены в `Roadmap.md`."
        default_summary = f"Официальный кумулятивный релиз {tag} по завершении Фаз {phases_title}."
        tags_cumulative = "\n  - cumulative"
    else:
        title_str = f"Релиз {tag}: Фаза {phase_num}"
        phases_fm_str = ""
        meta_phase_line = f"> **Фаза:** {phase_num}  "
        checklist_phase_line = f"- [x] Все задачи фазы {phase_num} завершены и проверены в `Roadmap.md`."
        default_summary = f"Официальный релиз {tag} по завершении Фазы {phase_num}."
        tags_cumulative = ""

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

    doc_summary = summary.strip() or default_summary

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
title: "{title_str}"
version: "{ver_clean}"
phase: {phase_num}
{phases_fm_str}status: completed
date: {today}
git_tag: "{tag}"
github_release_url: "{gh_release_url}"
mode: "{mode}"
artifacts:
{fm_artifacts_str}
tags:
  - release
  - changelog{tags_cumulative}
  - {tag}
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 {title_str}

> **Версия:** {tag}  
{meta_phase_line}
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
{checklist_phase_line}
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


def parse_version_tuple(v_str: str) -> Tuple[int, ...]:
    """Extracts integer components from version string for semantic sorting."""
    nums = re.findall(r"\d+", v_str)
    return tuple(int(n) for n in nums) if nums else (0,)


def detect_previous_tag(
    target_version: str,
    repo_root: Optional[Path] = None,
    docs_path: Optional[Path] = None,
) -> Optional[str]:
    """
    Detects the immediately preceding release tag via Git tags or docs/02_Tasks/Releases.
    Returns tag string like 'v0.10.0' or None if no prior release exists.
    """
    target_clean = target_version.lstrip("v")
    target_tuple = parse_version_tuple(target_clean)

    found_tags: List[str] = []

    # 1. Inspect git tags if inside git worktree
    root = repo_root or Path.cwd()
    if shutil.which("git"):
        try:
            res = subprocess.run(
                ["git", "tag", "--list", "v*"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0 and res.stdout.strip():
                for line in res.stdout.splitlines():
                    t = line.strip()
                    if t:
                        found_tags.append(t)
        except Exception:
            pass

    # 2. Inspect docs/02_Tasks/Releases/ if docs_path is available or can be inferred
    d_path = docs_path or (root / "docs")
    releases_dir = d_path / "02_Tasks" / "Releases"
    if releases_dir.is_dir():
        for f in releases_dir.glob("RELEASE-v*.md"):
            m = re.search(r"RELEASE-(v[\d\.]+)\.md", f.name)
            if m:
                found_tags.append(m.group(1))

    unique_tags = set(found_tags)
    older_candidates = []
    for t in unique_tags:
        clean_t = t.lstrip("v")
        t_tuple = parse_version_tuple(clean_t)
        if t_tuple < target_tuple:
            older_candidates.append((t_tuple, f"v{clean_t}"))

    if older_candidates:
        older_candidates.sort(key=lambda x: x[0], reverse=True)
        return older_candidates[0][1]

    return None


def generate_public_release_notes(
    version: str,
    phase_num: int,
    env_info: Dict[str, Any],
    artifacts: List[Dict[str, str]],
    phase_data: Dict[str, List[Dict[str, str]]],
    summary: str = "",
    phases: Optional[List[int]] = None,
    quick_install: Optional[str] = None,
    repo_root: Optional[Path] = None,
    prev_tag: Optional[str] = None,
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
            resolved_prev = prev_tag
            if not resolved_prev:
                effective_root_for_tag = repo_root or Path.cwd()
                resolved_prev = detect_previous_tag(target_version=ver_clean, repo_root=effective_root_for_tag)
            if resolved_prev:
                diff_url = f"{clean_repo_url}/compare/{resolved_prev}...{tag}"
            else:
                diff_url = f"{clean_repo_url}/commits/{tag}"

    is_cumulative = phases is not None and len(phases) > 1
    if is_cumulative:
        phases_title = " и ".join(str(p) for p in phases) if len(phases) == 2 else ", ".join(str(p) for p in phases)
        header_title = f"# 🚀 Release {tag} — Фазы {phases_title} (Кумулятивный)"
        default_summary = f"Официальный кумулятивный релиз {tag} по завершении Фаз {phases_title}."
    else:
        header_title = f"# 🚀 Release {tag} — Фаза {phase_num}"
        default_summary = f"Официальный релиз {tag} по завершении Фазы {phase_num}."

    doc_summary = summary.strip() or default_summary

    # Features / Highlights
    features_md: List[str] = []
    highlights_md: List[str] = []
    if phase_data.get("tasks"):
        for t in phase_data["tasks"]:
            t_type = t.get("type", "task")
            if t_type == "fast-track":
                marker = "⚡ Fast-Track:"
            else:
                marker = "✨ Фича:"
            raw_item = f"- {marker} [[{t['link']}|{t['id']}]]: {t['title']}."
            converted = convert_wikilinks_to_github_markdown(raw_item, clean_repo_url, branch)
            features_md.append(converted)
            # Add top features to highlights
            highlights_md.append(f"- **{t['title']}** ({t['id']})")
    else:
        features_md.append("- Плановые задачи фазы выполнены.")

    # Bug fixes
    bugs_md: List[str] = []
    if phase_data.get("bugs"):
        for b in phase_data["bugs"]:
            raw_item = f"- 🐛 Исправление: [[{b['link']}|{b['id']}]]: {b['title']}."
            bugs_md.append(convert_wikilinks_to_github_markdown(raw_item, clean_repo_url, branch))
    else:
        bugs_md.append("- Критических дефектов и регрессий за период фазы не зафиксировано.")

    highlights_block = ""
    if highlights_md:
        highlights_preview = "\n".join(highlights_md[:4])
        highlights_block = f"""### 🌟 Главное в этом релизе (Highlights)
{highlights_preview}

---

"""

    # Adaptive Quick Install / Start block
    effective_root = repo_root or Path.cwd()
    is_harness_repo = False
    if clean_repo_url:
        is_harness_repo = "agent-docs-harness" in clean_repo_url
    elif effective_root:
        is_harness_repo = (effective_root / "install.py").is_file() and (effective_root / "build_installer.py").is_file()


    quick_install_block = ""
    if quick_install and quick_install.strip():
        quick_install_block = f"""### ⚡ Быстрый старт / Установка (Quick Install)
```bash
{quick_install.strip()}
```

---

"""
    elif is_harness_repo:
        quick_install_block = f"""### ⚡ Быстрый старт / Обновление (Quick Install)
```bash
# Новая установка Docs-as-Code
curl -fsSL {raw_install_url} | python3

# Обновление существующего проекта
python install.py --update
```

---

"""
    elif artifacts and clean_repo_url:
        first_art = artifacts[0]["name"]
        quick_install_block = f"""### ⚡ Быстрый старт (Quick Start)
```bash
# Скачать {first_art}
curl -LO {clean_repo_url}/releases/download/{tag}/{first_art}
```

---

"""

    artifacts_table = format_artifacts_markdown_table(artifacts)
    verification_block = ""
    if artifacts:
        first_art_name = artifacts[0]["name"]
        verification_block = f"""

**Верификация в PowerShell:**
```powershell
Get-FileHash -Path ./dist/{first_art_name} -Algorithm SHA256
```

**Верификация в Bash:**
```bash
sha256sum ./dist/{first_art_name}
```"""

    full_changelog_md = ""
    if diff_url:
        full_changelog_md = f"\n\n---\n\n**Полный список изменений (Full Changelog):** {diff_url}"

    notes = f"""{header_title}

> 💡 **Executive Summary:** {doc_summary}

---

{highlights_block}{quick_install_block}### ✨ Новые возможности (Features)
{chr(10).join(features_md)}

### 🐛 Исправленные дефекты (Bug Fixes)
{chr(10).join(bugs_md)}

---

### 📦 Релизные артефакты и контрольные суммы (SHA-256 Checksums)

{artifacts_table}{verification_block}{full_changelog_md}
"""
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="kb_release.py — Zero-Dependencies Release Automation Utility for Docs-as-Code"
    )
    parser.add_argument("--version", type=str, default="", help="Release version (e.g. 0.4.0 or v0.4.0)")
    parser.add_argument("--phase", type=int, default=None, help="Phase number associated with the release (default: auto-detected)")
    parser.add_argument("--phases", type=str, default="", help="Comma-separated list of phase numbers for cumulative release (e.g. '9,10')")
    parser.add_argument("--docs-dir", type=str, default="docs", help="Path to docs directory (default: docs)")
    parser.add_argument("--dist-dir", type=str, default="dist", help="Path to dist directory (default: dist)")
    parser.add_argument("--output", type=str, default="", help="Target release markdown path")
    parser.add_argument("--notes-output", type=str, default="", help="Path to public release notes (default: <dist-dir>/RELEASE_NOTES.md)")
    parser.add_argument("--summary", type=str, default="", help="Executive summary text")
    parser.add_argument("--quick-install", type=str, default=None, help="Custom instructions or command for Quick Install block")
    parser.add_argument("--prev-tag", type=str, default=None, help="Previous release tag for Full Changelog diff URL (default: auto-detected)")
    parser.add_argument("--mode", choices=["auto", "github", "local-only"], default="auto", help="Release publication mode (default: auto)")
    parser.add_argument("--require-github", action="store_true", help="Fail if GitHub Release mode cannot be used for a GitHub-hosted repository")
    parser.add_argument("--dry-run", action="store_true", help="Print release markdown to stdout without writing")
    parser.add_argument("--detect-only", action="store_true", help="Only detect environment and print JSON")
    parser.add_argument("--ci-mode", action="store_true", help="Run in CI mode for GitHub Actions")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    repo_root = Path.cwd()
    env_info = detect_release_environment(repo_root, explicit_mode=args.mode)

    if args.detect_only:
        print(json.dumps(env_info, indent=2, ensure_ascii=False))
        return 0

    if args.require_github and env_info["is_github"] and env_info["mode"] != "github":
        warning_msg = env_info.get("warning", "GitHub Release mode is required, but unavailable.")
        print(f"❌ ERROR: {warning_msg}", file=sys.stderr)
        return 1

    if env_info.get("warning") and not args.ci_mode and args.mode != "local-only":
        print(f"⚠️ Warning: {env_info['warning']}", file=sys.stderr)

    if not args.version:
        print("❌ Error: --version is required (e.g. --version 0.4.0 or --version v0.4.0)", file=sys.stderr)
        return 1

    ver_clean = args.version.lstrip("v")
    tag = f"v{ver_clean}"

    docs_path = Path(args.docs_dir)
    dist_path = Path(args.dist_dir)

    out_path = Path(args.output) if args.output else docs_path / "02_Tasks" / "Releases" / f"RELEASE-{tag}.md"

    # Resolve phase, phases and summary (Single Source of Truth)
    phase_num = args.phase
    summary_text = args.summary.strip() if args.summary else ""
    phases_list: Optional[List[int]] = None
    if args.phases.strip():
        try:
            phases_list = [int(p.strip()) for p in args.phases.split(",") if p.strip()]
        except ValueError:
            print("❌ Error: --phases must be comma-separated integers, e.g. '9,10'", file=sys.stderr)
            return 1

    # If release doc already exists, infer ground truth metadata unless explicitly overridden
    if out_path.exists():
        existing_meta = extract_release_meta_from_doc(out_path)
        if phase_num is None and existing_meta.get("phase") is not None:
            phase_num = existing_meta["phase"]
        if phases_list is None and existing_meta.get("phases"):
            phases_list = existing_meta["phases"]
        if not summary_text and existing_meta.get("summary"):
            summary_text = existing_meta["summary"]

    if phases_list:
        if phase_num is None:
            phase_num = max(phases_list)
        elif phase_num not in phases_list:
            phases_list.append(phase_num)
            phases_list.sort()

    # Fallback phase detection if still None
    if phase_num is None:
        phase_num = detect_latest_phase(docs_path)

    # Pre-flight check: Release Blockers
    bugs_dir = docs_path / "02_Tasks" / "Bugs"
    blockers = check_release_blockers(
        bugs_dir=bugs_dir,
        target_version=ver_clean,
        current_phase=phase_num,
        target_phases=phases_list,
    )
    if blockers:
        for b_msg in blockers:
            print(f"❌ ERROR: {b_msg}", file=sys.stderr)
        return 1

    custom_notes_name = Path(args.notes_output).name if args.notes_output else None
    excluded = {custom_notes_name} if custom_notes_name else None
    artifacts = inspect_release_artifacts(dist_path, excluded_names=excluded)
    phase_data = find_phase_artifacts(
        docs_path,
        phase_num,
        phases=phases_list,
        target_version=ver_clean,
    )

    release_content = generate_release_markdown(
        version=ver_clean,
        phase_num=phase_num,
        env_info=env_info,
        artifacts=artifacts,
        phase_data=phase_data,
        summary=summary_text,
        phases=phases_list,
    )

    public_notes = generate_public_release_notes(
        version=ver_clean,
        phase_num=phase_num,
        env_info=env_info,
        artifacts=artifacts,
        phase_data=phase_data,
        summary=summary_text,
        phases=phases_list,
        quick_install=args.quick_install,
        repo_root=repo_root,
        prev_tag=args.prev_tag,
    )

    if args.dry_run:
        print(release_content)
        print("\n" + "=" * 40 + " PUBLIC RELEASE NOTES " + "=" * 40 + "\n")
        print(public_notes)
        return 0

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
