#!/usr/bin/env python3
"""
Knowledge Base State & Deterministic Navigation Utility for Docs-as-Code Vaults.
Resolves project state, task dependencies, and single next action for developers and AI agents.
Zero external dependencies (uses standard Python 3 library only).
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

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


def _clean_id(raw: str) -> str:
    cleaned = raw.strip().strip("'\"")
    if cleaned.startswith("[[") and cleaned.endswith("]]"):
        cleaned = cleaned[2:-2].strip()
        if "|" in cleaned:
            cleaned = cleaned.split("|", 1)[0].strip()
    if "/" in cleaned or "\\" in cleaned:
        cleaned = Path(cleaned).stem
    m = re.match(r"^((?:TASK|BUG)-[0-9A-Za-z_-]+)", cleaned)
    if m:
        return m.group(1)
    return cleaned.strip()


def _normalize_status(raw: str) -> str:
    cleaned = raw.strip().lower()
    cleaned = re.sub(r"\s*#.*$", "", cleaned).strip().strip("'\"")
    if cleaned in ("done", "completed", "resolved", "fixed", "closed", "выполнено"):
        return "done"
    if cleaned in ("in-progress", "in_progress", "in progress", "wip", "в работе"):
        return "in-progress"
    if cleaned in ("planned", "todo", "backlog", "к реализации", "запланировано"):
        return "planned"
    if cleaned in ("cancelled", "canceled", "rejected", "отменено"):
        return "cancelled"
    return cleaned


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Extracts metadata dictionary from document YAML frontmatter."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = parts[1]

    data: Dict[str, Any] = {}

    # id
    m_id = re.search(r"^id:\s*([^\s#]+)", fm, re.MULTILINE)
    if m_id:
        data["id"] = _clean_id(m_id.group(1))

    # title
    m_title = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
    if m_title:
        title_raw = m_title.group(1).strip()
        title_raw = re.sub(r"\s*#.*$", "", title_raw)  # remove trailing comment
        title_raw = title_raw.strip().strip("'\"")
        data["title"] = title_raw
    else:
        data["title"] = data.get("id", "")

    # status
    m_status = re.search(r"^status:\s*(.+)$", fm, re.MULTILINE)
    if m_status:
        data["status"] = _normalize_status(m_status.group(1))
    else:
        data["status"] = "unknown"

    # type
    m_type = re.search(r"^type:\s*([^\s#]+)", fm, re.MULTILINE)
    if m_type:
        data["type"] = m_type.group(1).strip().lower()
    else:
        data["type"] = "task" if data.get("id", "").startswith("TASK-") else "bug"

    # phase / target_phase
    m_phase = re.search(r"^(?:phase|target_phase):\s*([^\s#]+)", fm, re.MULTILINE)
    if m_phase:
        val = m_phase.group(1).strip().strip("'\"")
        try:
            data["phase"] = int(val)
        except ValueError:
            data["phase"] = val
    else:
        data["phase"] = None

    # release_blocker
    m_blocker = re.search(r"^release_blocker:\s*([^\s#]+)", fm, re.MULTILINE)
    if m_blocker:
        val_blocker = m_blocker.group(1).strip().lower()
        data["release_blocker"] = val_blocker in ("true", "yes", "1")
    else:
        data["release_blocker"] = False

    # target_release
    m_rel = re.search(r"^target_release:\s*([^\s#]+)", fm, re.MULTILINE)
    if m_rel:
        data["target_release"] = m_rel.group(1).strip().strip("'\"")

    # depends_on
    deps: List[str] = []
    m_inline = re.search(r"^\s*depends_on:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    if m_inline:
        raw_items = m_inline.group(1).split(",")
        for item in raw_items:
            clean = _clean_id(item)
            if clean:
                deps.append(clean)
    else:
        m_block = re.search(r"^\s*depends_on:\s*\n((?:\s*-\s*[^\n]+\n?)+)", fm, re.MULTILINE)
        if m_block:
            for line in m_block.group(1).splitlines():
                m_item = re.match(r"^\s*-\s*(.+)$", line)
                if m_item:
                    clean = _clean_id(m_item.group(1))
                    if clean:
                        deps.append(clean)
    data["depends_on"] = deps

    return data


def _find_docs_root(specified_path: Optional[str] = None) -> Path:
    """Locates the docs root directory based on user input or auto-detection."""
    if specified_path:
        p = Path(specified_path).resolve()
        if p.is_dir():
            if (p / "02_Tasks").is_dir():
                return p
            if (p / "docs" / "02_Tasks").is_dir():
                return p / "docs"
            return p
        raise FileNotFoundError(f"Specified docs path not found: {specified_path}")

    cwd = Path.cwd().resolve()
    candidates = [
        cwd / "docs",
        cwd,
        cwd.parent / "docs",
    ]
    for c in candidates:
        if c.is_dir() and (c / "02_Tasks").is_dir():
            return c

    # Fallback to cwd / "docs"
    return cwd / "docs"


def _normalize_rel_path(p: Path, base_dir: Path) -> str:
    """Creates a normalized forward-slash path relative to repo or base dir."""
    repo_root = base_dir.parent if base_dir.name == "docs" else base_dir
    try:
        rel = p.relative_to(repo_root)
        return str(rel).replace("\\", "/")
    except ValueError:
        try:
            rel = p.relative_to(base_dir)
            return ("docs/" + str(rel)).replace("\\", "/")
        except ValueError:
            return str(p).replace("\\", "/")


def scan_tasks_and_bugs(docs_root: Path) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    Scans docs_root for all task specifications and defect reports.
    Returns:
        (tasks_dict, bugs_dict) mapped by canonical ID.
    """
    tasks: Dict[str, Dict[str, Any]] = {}
    bugs: Dict[str, Dict[str, Any]] = {}

    specs_dir = docs_root / "02_Tasks" / "Specs"
    if specs_dir.is_dir():
        for f in sorted(specs_dir.rglob("*.md")):
            if f.name.startswith("TEMPLATE_") or "00_Templates" in f.parts:
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except Exception:
                continue
            fm = parse_frontmatter(content)
            if not fm:
                continue
            task_id = fm.get("id") or f.stem
            fm["file_path"] = f
            fm["rel_path"] = _normalize_rel_path(f, docs_root)
            tasks[task_id] = fm

    bugs_dir = docs_root / "02_Tasks" / "Bugs"
    if bugs_dir.is_dir():
        for f in sorted(bugs_dir.rglob("*.md")):
            if f.name.startswith("TEMPLATE_") or "00_Templates" in f.parts:
                continue
            try:
                content = f.read_text(encoding="utf-8")
            except Exception:
                continue
            fm = parse_frontmatter(content)
            if not fm:
                continue
            bug_id = fm.get("id") or f.stem
            fm["file_path"] = f
            fm["rel_path"] = _normalize_rel_path(f, docs_root)
            bugs[bug_id] = fm

    return tasks, bugs


def is_task_ready(
    task: Dict[str, Any],
    all_tasks: Dict[str, Dict[str, Any]],
    all_bugs: Dict[str, Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    """
    Checks if a planned task has all dependencies satisfied.
    Returns:
        (is_ready, list_of_unmet_dependencies)
    """
    if task.get("status") != "planned":
        return False, []

    missing: List[str] = []
    deps = task.get("depends_on", [])
    for dep in deps:
        if dep in all_tasks:
            dep_status = all_tasks[dep].get("status")
            if dep_status != "done":
                missing.append(dep)
        elif dep in all_bugs:
            dep_status = all_bugs[dep].get("status")
            if dep_status not in ("fixed", "closed", "done"):
                missing.append(dep)
        else:
            missing.append(dep)

    return len(missing) == 0, missing


def resolve_next_action(docs_root: Path) -> Dict[str, Any]:
    """
    Deterministically computes the single next action according to ADR-0035:
    Priority 1: Task with status 'in-progress'.
    Priority 2: Defect with 'release_blocker: true' and unresolved status.
    Priority 3: First planned task whose dependencies are all satisfied.
    Priority 4: Recommendation to release if all tasks are complete.
    Priority 5: Deadlock notification if remaining planned tasks are all blocked.
    Priority 6: Empty state if no tasks exist.
    """
    tasks, bugs = scan_tasks_and_bugs(docs_root)

    if not tasks and not bugs:
        return {
            "status": "empty",
            "action": "no_tasks",
            "target": None,
            "blocked_by": [],
            "message": "Задачи не найдены в каталоге Specs. Создайте первую задачу через /kb-plan или /kb-task.",
        }

    # Helper sort key: (phase or 9999, id)
    def _sort_key(item: Dict[str, Any]) -> Tuple[int, str]:
        p = item.get("phase")
        phase_num = p if isinstance(p, int) else 9999
        return phase_num, item.get("id", "")

    # Priority 1: in-progress tasks
    in_progress_tasks = [t for t in tasks.values() if t.get("status") == "in-progress"]
    if in_progress_tasks:
        in_progress_tasks.sort(key=_sort_key)
        top = in_progress_tasks[0]
        return {
            "status": "in-progress",
            "action": "continue_task",
            "target": {
                "id": top["id"],
                "title": top["title"],
                "path": top["rel_path"],
                "command": f"/kb-implement {top['id']}",
                "phase": top.get("phase"),
            },
            "blocked_by": [],
            "message": f"Текущая задача в работе: {top['id']} — {top['title']}. Продолжите выполнение: /kb-implement {top['id']}",
        }

    # Priority 2: release blocker bugs
    open_blocker_bugs = [
        b for b in bugs.values()
        if b.get("release_blocker") is True and b.get("status") not in ("fixed", "closed", "done")
    ]
    if open_blocker_bugs:
        open_blocker_bugs.sort(key=lambda b: (b.get("phase") if isinstance(b.get("phase"), int) else 9999, b.get("id", "")))
        top_bug = open_blocker_bugs[0]
        return {
            "status": "blocked_by_bug",
            "action": "fix_blocker_bug",
            "target": {
                "id": top_bug["id"],
                "title": top_bug["title"],
                "path": top_bug["rel_path"],
                "command": f"/kb-implement {top_bug['id']}",
                "phase": top_bug.get("phase"),
            },
            "blocked_by": [],
            "message": f"Критический дефект блокирует релиз: {top_bug['id']} — {top_bug['title']}. Устраните дефект: /kb-implement {top_bug['id']}",
        }

    # Priority 3: Ready planned tasks
    planned_tasks = [t for t in tasks.values() if t.get("status") == "planned"]
    ready_tasks: List[Dict[str, Any]] = []
    blocked_tasks_info: List[Dict[str, Any]] = []

    for t in planned_tasks:
        ready, missing = is_task_ready(t, tasks, bugs)
        if ready:
            ready_tasks.append(t)
        else:
            blocked_tasks_info.append({
                "task_id": t["id"],
                "missing_dependencies": missing,
            })

    if ready_tasks:
        ready_tasks.sort(key=_sort_key)
        top_ready = ready_tasks[0]
        return {
            "status": "ready",
            "action": "start_task",
            "target": {
                "id": top_ready["id"],
                "title": top_ready["title"],
                "path": top_ready["rel_path"],
                "command": f"/kb-implement {top_ready['id']}",
                "phase": top_ready.get("phase"),
            },
            "blocked_by": [],
            "message": f"Следующая готовая задача: {top_ready['id']} — {top_ready['title']}. Запустите: /kb-implement {top_ready['id']}",
        }

    # Priority 4: All tasks completed (and no blocker bugs)
    if tasks and all(t.get("status") in ("done", "cancelled") for t in tasks.values()):
        return {
            "status": "all_done",
            "action": "release",
            "target": None,
            "blocked_by": [],
            "message": "Все плановые задачи завершены! Рекомендуется провести релиз: /kb-release",
        }

    # Priority 5: Deadlock / Blocked
    if planned_tasks and not ready_tasks:
        return {
            "status": "deadlock",
            "action": "deadlock_blocked",
            "target": None,
            "blocked_by": blocked_tasks_info,
            "message": "Все оставшиеся плановые задачи заблокированы невыполненными зависимостями.",
        }

    # Fallback default
    return {
        "status": "idle",
        "action": "none",
        "target": None,
        "blocked_by": [],
        "message": "Нет активных или готовых задач для выполнения.",
    }


def compute_status_summary(docs_root: Path) -> Dict[str, Any]:
    """Aggregates a complete overview of project tasks, phases, and health."""
    tasks, bugs = scan_tasks_and_bugs(docs_root)

    status_counts: Dict[str, int] = {"done": 0, "in-progress": 0, "planned": 0, "cancelled": 0, "other": 0}
    for t in tasks.values():
        st = t.get("status", "other")
        if st in status_counts:
            status_counts[st] += 1
        else:
            status_counts["other"] += 1

    bug_counts: Dict[str, int] = {"open": 0, "in-progress": 0, "fixed": 0, "closed": 0, "other": 0}
    blocker_bugs_open = 0
    for b in bugs.values():
        st = b.get("status", "other")
        if st in ("done", "fixed"):
            bug_counts["fixed"] += 1
        elif st in bug_counts:
            bug_counts[st] += 1
        else:
            bug_counts["other"] += 1
        if b.get("release_blocker") is True and st not in ("fixed", "closed", "done"):
            blocker_bugs_open += 1

    next_act = resolve_next_action(docs_root)

    # Detect current phase
    current_phase = None
    if next_act.get("target") and next_act["target"].get("phase") is not None:
        current_phase = next_act["target"]["phase"]
    elif tasks:
        # Find highest phase that is in-progress or planned, else highest done
        phases = [t.get("phase") for t in tasks.values() if isinstance(t.get("phase"), int)]
        if phases:
            current_phase = max(phases)

    # Collect ready and blocked lists
    ready_list: List[Dict[str, Any]] = []
    blocked_list: List[Dict[str, Any]] = []
    for t in tasks.values():
        if t.get("status") == "planned":
            ready, missing = is_task_ready(t, tasks, bugs)
            if ready:
                ready_list.append({
                    "id": t["id"],
                    "title": t["title"],
                    "phase": t.get("phase"),
                    "command": f"/kb-implement {t['id']}",
                })
            else:
                blocked_list.append({
                    "id": t["id"],
                    "title": t["title"],
                    "phase": t.get("phase"),
                    "blocked_by": missing,
                })

    ready_list.sort(key=lambda x: (x.get("phase") if isinstance(x.get("phase"), int) else 9999, x["id"]))
    blocked_list.sort(key=lambda x: (x.get("phase") if isinstance(x.get("phase"), int) else 9999, x["id"]))

    return {
        "current_phase": current_phase,
        "total_tasks": len(tasks),
        "tasks_by_status": status_counts,
        "total_bugs": len(bugs),
        "bugs_by_status": bug_counts,
        "open_blocker_bugs": blocker_bugs_open,
        "ready_tasks": ready_list,
        "blocked_tasks": blocked_list,
        "next_action": next_act,
    }


def render_text_next(action_data: Dict[str, Any]) -> str:
    """Formats single next action as human-readable text."""
    status = action_data.get("status")
    target = action_data.get("target")
    message = action_data.get("message", "")

    lines: List[str] = []
    if status == "in-progress" and target:
        lines.append("⏳ ТЕКУЩАЯ ЗАДАЧА В РАБОТЕ:")
        lines.append(f"  • {target['id']}: {target['title']}" + (f" (Фаза {target['phase']})" if target.get('phase') else ""))
        lines.append(f"  ▶ Продолжить: {target['command']}")
    elif status == "blocked_by_bug" and target:
        lines.append("🚨 КРИТИЧЕСКИЙ БЛОКЕР РЕЛИЗА:")
        lines.append(f"  • {target['id']}: {target['title']}")
        lines.append(f"  ▶ Устранить: {target['command']}")
    elif status == "ready" and target:
        lines.append("🎯 СЛЕДУЮЩАЯ ГОТОВАЯ ЗАДАЧА:")
        lines.append(f"  • {target['id']}: {target['title']}" + (f" (Фаза {target['phase']})" if target.get('phase') else ""))
        lines.append(f"  ▶ Запустить: {target['command']}")
    elif status == "all_done":
        lines.append("🎉 ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")
        lines.append("  ▶ Рекомендуется выпустить релиз: /kb-release")
    elif status == "deadlock":
        lines.append("⚠️ ОБНАРУЖЕНА БЛОКИРОВКА ЗАДАЧ (DEADLOCK):")
        lines.append("  Все оставшиеся плановые задачи ожидают невыполненных зависимостей:")
        for b in action_data.get("blocked_by", []):
            lines.append(f"  • {b['task_id']} ожидает: {', '.join(b['missing_dependencies'])}")
    else:
        lines.append(message)

    return "\n".join(lines)


def render_text_status(summary: Dict[str, Any]) -> str:
    """Formats full status overview as human-readable text."""
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("📊 СТАТУС ПРОЕКТА (Docs-as-Code State)")
    lines.append("=" * 60)

    cur_phase = summary.get("current_phase")
    lines.append(f"Текущая фаза: {cur_phase if cur_phase is not None else 'Не определена'}")

    ts = summary.get("tasks_by_status", {})
    lines.append(
        f"Задачи (всего {summary.get('total_tasks', 0)}): "
        f"Готово: {ts.get('done', 0)} | "
        f"В работе: {ts.get('in-progress', 0)} | "
        f"Планируется: {ts.get('planned', 0)} | "
        f"Отменено: {ts.get('cancelled', 0)}"
    )

    bs = summary.get("bugs_by_status", {})
    blockers = summary.get("open_blocker_bugs", 0)
    lines.append(
        f"Дефекты (всего {summary.get('total_bugs', 0)}): "
        f"Открыто: {bs.get('open', 0)} | "
        f"В работе: {bs.get('in-progress', 0)} | "
        f"Исправлено: {bs.get('fixed', 0)} "
        f"(Критических блокеров: {blockers})"
    )

    ready = summary.get("ready_tasks", [])
    if ready:
        lines.append("\nГотовы к реализации:")
        for r in ready[:5]:
            p_str = f" (Фаза {r['phase']})" if r.get('phase') is not None else ""
            lines.append(f"  • {r['id']}: {r['title']}{p_str}")
        if len(ready) > 5:
            lines.append(f"  ... и еще {len(ready) - 5} готовых задач")

    blocked = summary.get("blocked_tasks", [])
    if blocked:
        lines.append("\nЗаблокированы зависимостями:")
        for b in blocked[:5]:
            lines.append(f"  • {b['id']}: ожидает [{', '.join(b['blocked_by'])}]")
        if len(blocked) > 5:
            lines.append(f"  ... и еще {len(blocked) - 5} заблокированных задач")

    lines.append("\n" + "-" * 60)
    next_action = summary.get("next_action", {})
    lines.append(render_text_next(next_action))
    lines.append("=" * 60)

    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI Entry point for kb_state."""
    parser = argparse.ArgumentParser(
        prog="kb_state",
        description="Docs-as-Code State & Deterministic Navigation Utility",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="next",
        choices=["next", "status"],
        help="Navigation command: 'next' (single next action) or 'status' (project overview). Default: next",
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Path to docs vault (auto-detected if omitted)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' (default) or 'json'",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Shortcut for --format json",
    )

    args = parser.parse_args(argv)

    try:
        docs_root = _find_docs_root(args.path)
    except Exception as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 1

    output_format = "json" if args.json else args.format

    if args.command == "next":
        res = resolve_next_action(docs_root)
        if output_format == "json":
            sys.stdout.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
        else:
            sys.stdout.write(render_text_next(res) + "\n")
        return 0

    elif args.command == "status":
        summary = compute_status_summary(docs_root)
        if output_format == "json":
            sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
        else:
            sys.stdout.write(render_text_status(summary) + "\n")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
