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
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".canvas", ".excalidraw"}
VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}
TASK_NAMESPACE_PATTERN = re.compile(r"^(?:TASK|BUG)-\d{3,}(?:-[a-zA-Z0-9_-]+)?$")
CODE_FILE_EXTENSIONS = {".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".swift", ".cs", ".go", ".rs", ".java", ".kt", ".rb", ".php", ".c", ".h", ".cpp", ".hpp", ".m", ".mm"}
LINE_ANCHOR_RE = re.compile(
    r"(?:\b[\w./\\-]+\.\w+:L\d{1,5}\b|\bL\d{1,5}\s*[-–]\s*L?\d{1,5}\b)"
)
FILE_CONTRACT_RE = re.compile(r"^\s*[\*\-]\s*`?\[(NEW|MODIFY|DELETE)\]`?\s*`([^`]+)`")
NESTED_SYMBOL_RE = re.compile(r"^\s{2,}[\*\-]\s+\S")
HARNESS_META_TECHDEBT_IDS = {
    "PLAN-019",
    "PLAN-021",
    "TASK-075",
    "TASK-076",
    "TASK-077",
    "TASK-078",
    "TASK-082",
    "TASK-083",
    "TASK-084",
}


def find_vault_root(start_dir: Path) -> Path:
    cur = start_dir.resolve()
    while cur != cur.parent:
        if (cur / "docs").is_dir() or (cur / "00_Index.md").is_file():
            if (cur / "docs").is_dir():
                return cur / "docs"
            return cur
        cur = cur.parent
    return start_dir.resolve()


def _is_relative_to(p: Path, base: Path) -> bool:
    """Check if path p is relative to base directory (Python 3.8+ compatible)."""
    try:
        p_res = str(p.resolve())
        base_res = str(base.resolve())
        return os.path.normcase(os.path.commonpath([p_res, base_res])) == os.path.normcase(base_res)
    except (ValueError, TypeError):
        return False


def _relative_to(p: Path, base: Path) -> Path:
    """Return relative path, compatible with Python 3.8+."""
    try:
        return p.resolve().relative_to(base.resolve())
    except (AttributeError, ValueError):
        return Path(os.path.relpath(p.resolve(), base.resolve()))


def parse_wikilinks(content: str) -> List[str]:
    # 1. Strip code blocks ```...``` and inline code `...`
    stripped = re.sub(r'```[\s\S]*?```', '', content)
    stripped = re.sub(r'`[^`\n]*`', '', stripped)

    # 2. Match wikilinks: [[target|label]], [[target#heading|label]], [[target]] with optional escaped pipes \|
    # and embed prefix: ![[target|size]], ![[target]]
    pattern = re.compile(r'!?\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\\?\|[^\]]*)?\]\]')
    matches = pattern.findall(stripped)

    # 3. Clean up escaping backslashes from targets and strip size/alias parameters
    cleaned = []
    for m in matches:
        target = m.rstrip("\\").strip()
        if target.startswith("!"):
            target = target[1:].strip()
        if "|" in target:
            target = target.split("|", 1)[0].strip()
        if target:
            cleaned.append(target)
    return cleaned


def parse_markdown_images(content: str) -> List[str]:
    # 1. Strip code blocks ```...``` and inline code `...`
    stripped = re.sub(r'```[\s\S]*?```', '', content)
    stripped = re.sub(r'`[^`\n]*`', '', stripped)

    # 2. Match standard markdown images: ![alt](path)
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    matches = pattern.findall(stripped)

    cleaned = []
    for _alt, path_str in matches:
        target = path_str.strip()
        if " " in target:
            target = target.split()[0].strip()
        if target.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        cleaned_target = urllib.parse.unquote(target)
        if cleaned_target:
            cleaned.append(cleaned_target)
    return cleaned


def check_file_frontmatter(file_path: Path):
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read file: {e}"

    if not text.startswith("---"):
        return False, "Missing or malformed YAML frontmatter (starts without ---)"

    parts = text.split("---", 2)
    if len(parts) < 3:
        return False, "Malformed YAML frontmatter (missing closing ---)"

    fm_raw = parts[1]
    rel_posix = file_path.as_posix()

    schemas = {
        "02_Tasks/Inbox": ["id", "title", "status", "type", "channel", "created"],
        "06_Memory/Incidents": ["id", "title", "status", "created"],
        "02_Tasks/Specs": ["id", "title", "status", "type", "phase", "parent_plan", "created"],
        "02_Tasks/Bugs": ["id", "title", "status", "severity", "type", "created"],
        "03_Decisions_ADR": ["id", "title", "status"],
    }

    for path_prefix, required_fields in schemas.items():
        if path_prefix in rel_posix:
            missing = []
            for field in required_fields:
                if not re.search(rf'^{field}:\s*.+', fm_raw, re.MULTILINE):
                    missing.append(field)
            if path_prefix == "03_Decisions_ADR":
                if not re.search(r'^(date|created):\s*.+', fm_raw, re.MULTILINE):
                    missing.append("date/created")
            if missing:
                return False, f"Missing required frontmatter fields: {', '.join(missing)}"
            break

    if "02_Tasks/Inbox" in rel_posix:
        status_match = re.search(r'^status:\s*([^\s#]+)', fm_raw, re.MULTILINE)
        if status_match:
            val = status_match.group(1).lower()
            allowed_statuses = ["new", "triaged", "processed", "rejected"]
            if val not in allowed_statuses:
                return False, f"Invalid status '{val}' in Inbox item. Expected one of: {allowed_statuses}"

    return True, "Valid YAML frontmatter"


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


def check_fast_track_specs(docs_dir: Path) -> list:
    """
    Audits Fast-Track task specifications (type: fast-track) for adherence to scope limits:
    - Maximum 2 files touched in file contracts ([NEW], [MODIFY], [DELETE]).
    - Mandatory Verification Plan section or automated verification command.
    Returns a list of warning strings.
    """
    warnings = []
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if not specs_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Specs").is_dir():
        specs_dir = docs_dir / "docs" / "02_Tasks" / "Specs"
    if not specs_dir.is_dir():
        return warnings

    for spec_file in specs_dir.rglob("*.md"):
        if spec_file.name.startswith("TEMPLATE_"):
            continue
        try:
            content = spec_file.read_text(encoding="utf-8")
        except Exception:
            continue

        if not content.startswith("---"):
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        fm = parts[1]
        type_match = re.search(r"^type:\s*([^\s#]+)", fm, re.MULTILINE)
        if not type_match or type_match.group(1).strip().lower() != "fast-track":
            continue

        rel_name = spec_file.name

        # 1. Count files in file contract
        contract_section = ""
        m_contract = re.search(r"##\s+2\.\s+Контракт файлов([\s\S]*?)(?=\n##|\n---|$)", content, re.IGNORECASE)
        if m_contract:
            contract_section = m_contract.group(1)
        else:
            # Fallback to general section 2
            m_sec2 = re.search(r"##\s+(?:2\.|Затрагиваемые файлы)([\s\S]*?)(?=\n##|\n---|$)", content, re.IGNORECASE)
            if m_sec2:
                contract_section = m_sec2.group(1)

        file_items = re.findall(r"^\s*[\*\-]\s*`?\[(?:NEW|MODIFY|DELETE)\]`?", contract_section, re.MULTILINE | re.IGNORECASE)
        if len(file_items) > 2:
            warnings.append(
                f"Fast-Track spec '{rel_name}' touches {len(file_items)} files (limit: <= 2). Consider full RFC."
            )

        # 2. Check Verification Plan
        has_verif = bool(
            re.search(r"##\s+.*(?:План верификации|Verification Plan)", content, re.IGNORECASE) or
            re.search(r"(?:python|pytest|dotnet|npm|cargo)\s+.*", content, re.IGNORECASE)
        )
        if not has_verif:
            warnings.append(
                f"Fast-Track spec '{rel_name}' is missing a Verification Plan."
            )

    return warnings


def check_phase_consistency(docs_dir: Path) -> list:
    """
    Scans docs/02_Tasks/Specs/ for task specifications and validates:
    1. Folder Phase vs Frontmatter Phase:
       e.g., Specs/15_LatencyAndChannels/TASK-*.md must have phase: 15.
    2. Frontmatter Phase vs Tags:
       if tags contains 'phase15', frontmatter phase must be 15.
    Returns a list of non-blocking warning strings.
    """
    warnings = []
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if not specs_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Specs").is_dir():
        specs_dir = docs_dir / "docs" / "02_Tasks" / "Specs"
    if not specs_dir.is_dir():
        return warnings

    for folder in sorted(specs_dir.iterdir()):
        if not folder.is_dir():
            continue
        m_folder = re.match(r"^(\d+)_", folder.name)
        if not m_folder:
            continue
        folder_phase = int(m_folder.group(1))

        for spec_file in sorted(folder.glob("*.md")):
            if spec_file.name.startswith("TEMPLATE_"):
                continue
            try:
                content = spec_file.read_text(encoding="utf-8")
            except Exception:
                continue

            if not content.startswith("---"):
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                continue

            fm = parts[1]
            m_phase = re.search(r"^phase:\s*(\d+)", fm, re.MULTILINE)
            if not m_phase:
                continue

            fm_phase = int(m_phase.group(1))
            rel_path = spec_file.name

            # 1. Folder Phase vs Frontmatter Phase
            if fm_phase != folder_phase:
                warnings.append(
                    f"Spec '{rel_path}' declares phase {fm_phase}, but is located in folder '{folder.name}' (expected phase {folder_phase})."
                )

            # 2. Frontmatter Phase vs Tags
            tags_block = ""
            m_tags = re.search(r"^tags:\s*([\s\S]*?)(?=\n[a-zA-Z_-]+:|\n---|$)", fm, re.MULTILINE)
            if m_tags:
                tags_block = m_tags.group(1)
            tag_matches = re.findall(r"\bphase(\d+)\b", tags_block, re.IGNORECASE)
            for tag_phase_str in tag_matches:
                tag_phase = int(tag_phase_str)
                if tag_phase != fm_phase:
                    warnings.append(
                        f"Spec '{rel_path}' declares phase {fm_phase}, but contains mismatched tag 'phase{tag_phase}'."
                    )

    return warnings


def check_memory_limits(docs_dir: Path) -> list:
    """
    Tier 1 Quality Gate: validates procedural memory limits and formats in docs/06_Memory/:
    1. Maximum 15 active patterns in docs/06_Memory/patterns.md (- [TRG-XX] ...)
    Returns a list of error strings that block the linter (Exit code 1).
    """
    errors = []
    memory_dir = docs_dir / "06_Memory"
    if not memory_dir.is_dir() and (docs_dir / "docs" / "06_Memory").is_dir():
        memory_dir = docs_dir / "docs" / "06_Memory"
    if not memory_dir.is_dir():
        return errors

    patterns_file = memory_dir / "patterns.md"
    if patterns_file.is_file():
        try:
            content = patterns_file.read_text(encoding="utf-8")
            pattern_matches = re.findall(r"^\s*-\s*\[TRG-\d+\].*", content, flags=re.MULTILINE)
            if len(pattern_matches) > 15:
                try:
                    rel_p = patterns_file.relative_to(docs_dir).as_posix()
                except ValueError:
                    rel_p = patterns_file.name
                errors.append(
                    f"Memory patterns limit exceeded: {len(pattern_matches)} active patterns found in "
                    f"'{rel_p}' (maximum allowed: 15). "
                    f"Archive or consolidate patterns to preserve token economy!"
                )
        except Exception:
            pass

    return errors


MEMORY_SEEDED_MARKER = "seeded pattern (no archived report)"


def _parse_memory_frontmatter(text: str) -> Dict[str, str]:
    """Extract scalar YAML frontmatter fields used by procedural-memory reports."""
    fields: Dict[str, str] = {}
    if not text.startswith("---"):
        return fields
    parts = text.split("---", 2)
    if len(parts) < 3:
        return fields
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, raw_value = match.group(1), match.group(2).strip()
        if not raw_value or raw_value.startswith("#"):
            continue
        if len(raw_value) >= 2 and raw_value[0] == raw_value[-1] and raw_value[0] in "\"'":
            raw_value = raw_value[1:-1]
        fields[key] = raw_value
    return fields


def check_memory_consistency(docs_dir: Path) -> List[str]:
    """
    Tier 1 Quality Gate (Non-blocking, advisory):
    Validates referential integrity of the procedural memory contour docs/06_Memory/:
    1. Every INC-XXX referenced from patterns.md has an incident report file.
    2. Incident frontmatter `id` matches the INC-XXX filename prefix.
    3. Incident `target_pattern` exists in patterns.md as [TRG-XX].
    4. A pattern [TRG-XX] linking INC-YYY agrees with that incident's target_pattern.

    Seeded patterns marked 'seeded pattern (no archived report)' keep their place in
    the index but are not treated as incident references.
    Returns a list of non-blocking 'WARN:' strings (never blocks the linter).
    """
    warnings: List[str] = []
    memory_dir = docs_dir / "06_Memory"
    if not memory_dir.is_dir() and (docs_dir / "docs" / "06_Memory").is_dir():
        memory_dir = docs_dir / "docs" / "06_Memory"
    if not memory_dir.is_dir():
        return warnings

    patterns_file = memory_dir / "patterns.md"
    if not patterns_file.is_file():
        return warnings

    try:
        patterns_content = patterns_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return warnings

    pattern_entries: List[tuple] = []
    for line in patterns_content.splitlines():
        match = re.match(r"^\s*-\s*\[(TRG-\d{2,})\]\s*(.*)$", line)
        if match:
            pattern_entries.append((match.group(1), line))
    pattern_tags = {tag for tag, _ in pattern_entries}

    incidents_dir = memory_dir / "Incidents"
    incident_reports_by_prefix: Dict[str, Dict[str, str]] = {}
    incident_warnings: List[str] = []
    if incidents_dir.is_dir():
        for incident_file in sorted(incidents_dir.glob("*.md")):
            if incident_file.name.startswith("TEMPLATE_"):
                continue
            try:
                incident_text = incident_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            frontmatter = _parse_memory_frontmatter(incident_text)
            incident_id = frontmatter.get("id", "").strip()
            prefix_match = re.match(r"^(INC-\d{3})", incident_file.stem)
            filename_prefix = prefix_match.group(1) if prefix_match else ""
            if not incident_id:
                incident_warnings.append(
                    f"WARN: incident '{incident_file.name}' has no 'id' in frontmatter"
                )
            elif not filename_prefix or incident_id != filename_prefix:
                incident_warnings.append(
                    f"WARN: incident '{incident_id}' id does not match filename '{incident_file.name}'"
                )
            lookup_prefix = filename_prefix or incident_id
            if lookup_prefix:
                incident_reports_by_prefix[lookup_prefix] = {
                    "target_pattern": frontmatter.get("target_pattern", "").strip(),
                }

    for tag, line in pattern_entries:
        if MEMORY_SEEDED_MARKER in line:
            continue
        for incident_id in sorted(set(re.findall(r"INC-\d{3}", line))):
            if incident_id not in incident_reports_by_prefix:
                warnings.append(
                    f"WARN: patterns.md references missing incident report '{incident_id}'"
                )
                continue
            target_pattern = incident_reports_by_prefix[incident_id]["target_pattern"]
            if target_pattern and target_pattern != tag:
                warnings.append(
                    f"WARN: pattern '{tag}' links '{incident_id}' whose target_pattern is '{target_pattern}'"
                )

    for incident_id, report in sorted(incident_reports_by_prefix.items()):
        target_pattern = report["target_pattern"]
        if not target_pattern:
            incident_warnings.append(
                f"WARN: incident '{incident_id}' is missing required 'target_pattern'"
            )
        elif target_pattern not in pattern_tags:
            incident_warnings.append(
                f"WARN: incident '{incident_id}' targets '{target_pattern}' which is absent from patterns.md"
            )

    warnings.extend(incident_warnings)
    return warnings


RESEARCH_BASIS_RE = re.compile(r"^research_basis:\s*(.*)$", re.MULTILINE)
BASIS_NOTE_RE = re.compile(r"^basis_note:\s*(.*)$", re.MULTILINE)


def _normalize_plan_value(raw: str) -> str:
    """Strip quotes, inline comments and surrounding whitespace from a scalar."""
    value = raw.strip().split("#", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def check_research_basis(docs_dir: Path) -> List[str]:
    """
    Tier 1 Quality Gate (Non-blocking): audit plan provenance.

    A plan that declares `research_basis: none` must explain why research was not
    needed via a non-empty `basis_note`. Plans without the field are silently
    accepted (backward compatible with plans created before ADR-0031).
    Returns a list of warning strings (never blocks the linter).
    """
    warnings = []
    plans_dir = docs_dir / "02_Tasks" / "Plans"
    if not plans_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Plans").is_dir():
        plans_dir = docs_dir / "docs" / "02_Tasks" / "Plans"
    if not plans_dir.is_dir():
        return warnings

    for plan_file in sorted(plans_dir.rglob("*.md")):
        if plan_file.name.startswith("TEMPLATE_"):
            continue
        try:
            text = plan_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        frontmatter = parts[1]

        basis_match = RESEARCH_BASIS_RE.search(frontmatter)
        if not basis_match:
            continue
        if _normalize_plan_value(basis_match.group(1)).lower() != "none":
            continue

        note_match = BASIS_NOTE_RE.search(frontmatter)
        note = _normalize_plan_value(note_match.group(1)) if note_match else ""
        if not note:
            warnings.append(
                "WARN: plan '%s' sets research_basis: none without basis_note" % plan_file.name
            )
    return warnings


def check_symbolic_scope(docs_dir: Path) -> List[str]:
    """ADR-0029: active task specs must name nested code symbols."""
    warnings = []
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if not specs_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Specs").is_dir():
        specs_dir = docs_dir / "docs" / "02_Tasks" / "Specs"
    if not specs_dir.is_dir():
        return warnings

    for spec_file in specs_dir.rglob("*.md"):
        try:
            text = spec_file.read_text(encoding="utf-8")
        except OSError:
            continue

        parts = text.split("---", 2)
        if not text.startswith("---") or len(parts) < 3:
            continue
        frontmatter = parts[1]

        if "type: task" not in frontmatter or not re.search(
            r"^status:\s*(?:planned|in-progress|in_progress)\b", frontmatter, re.MULTILINE
        ):
            continue

        section = re.search(r"^##\s+2\.[^\n]*\n([\s\S]*?)(?=^##\s|\Z)", text, re.MULTILINE)
        if not section:
            continue
        section = section.group(1)

        if LINE_ANCHOR_RE.search(section):
            warnings.append("WARN: task '%s' uses line-number anchors (ADR-0029)" % spec_file.name)

        lines = section.splitlines()
        for idx, line in enumerate(lines):
            item = FILE_CONTRACT_RE.match(line)
            if not item:
                continue
            marker, raw_path = item.group(1), item.group(2).strip()
            if marker not in ("NEW", "MODIFY"):
                continue
            if Path(raw_path).suffix not in CODE_FILE_EXTENSIONS:
                continue

            has_symbol = False
            for follow in lines[idx + 1:]:
                if FILE_CONTRACT_RE.match(follow) or follow.startswith("## "):
                    break
                if NESTED_SYMBOL_RE.match(follow):
                    has_symbol = True
                    break
            if not has_symbol:
                warnings.append(
                    "WARN: task '%s' modifies code '%s' without a nested symbol (ADR-0029)"
                    % (spec_file.name, raw_path)
                )
    return warnings


def check_asset_weights(docs_dir: Path, max_bytes: int = 2 * 1024 * 1024) -> List[str]:
    """
    Tier 1 Quality Gate (Non-blocking):
    Audits docs/assets/ for media files exceeding size threshold (default 2 MB).
    Returns a list of warning strings.
    """
    warnings = []
    assets_dir = docs_dir / "assets"
    if not assets_dir.is_dir() and (docs_dir / "docs" / "assets").is_dir():
        assets_dir = docs_dir / "docs" / "assets"
    if not assets_dir.is_dir():
        return warnings

    for p in sorted(assets_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in MEDIA_EXTENSIONS:
            try:
                size = p.stat().st_size
                if size > max_bytes:
                    mb = size / (1024 * 1024)
                    rel_p = p.relative_to(docs_dir).as_posix() if _is_relative_to(p, docs_dir) else p.name
                    warnings.append(f"WARN: Asset '{rel_p}' exceeds size limit ({mb:.1f} MB > 2.0 MB)")
            except Exception:
                pass
    return warnings


def check_asset_layout(docs_dir: Path) -> List[str]:
    """
    Tier 1 Quality Gate (Non-blocking):
    Validates docs/assets/ directory topology:
    - Root subdirectories must be in VALID_ASSET_ROOTS ("mockups", "screenshots", "diagrams", "design").
    - No unorganized loose files in root docs/assets/.
    - Subdirectories inside docs/assets/mockups/<target>/ must be task-scoped (TASK-XXX or BUG-XXX).
    Returns a list of warning strings.
    """
    warnings: List[str] = []
    assets_dir = docs_dir / "assets"
    if not assets_dir.is_dir() and (docs_dir / "docs" / "assets").is_dir():
        assets_dir = docs_dir / "docs" / "assets"
    if not assets_dir.is_dir():
        return warnings

    allowed_str = ", ".join(sorted(VALID_ASSET_ROOTS))
    for item in sorted(assets_dir.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            if item.name not in VALID_ASSET_ROOTS:
                warnings.append(
                    f"WARN: Disallowed asset category directory 'assets/{item.name}'. "
                    f"Allowed root categories: {allowed_str}. "
                    f"Move platform folders inside 'assets/mockups/{item.name}/' or 'assets/screenshots/{item.name}/'."
                )
        elif item.is_file():
            warnings.append(
                f"WARN: Unorganized file 'assets/{item.name}' in root of docs/assets/. "
                f"Place assets inside mockups/, screenshots/, diagrams/, or design/."
            )

    mockups_dir = assets_dir / "mockups"
    if mockups_dir.is_dir():
        for target_dir in sorted(mockups_dir.iterdir()):
            if not target_dir.is_dir() or target_dir.name.startswith("."):
                continue
            for entry in sorted(target_dir.iterdir()):
                if entry.name.startswith("."):
                    continue
                if not entry.is_dir() or not TASK_NAMESPACE_PATTERN.match(entry.name):
                    rel_entry = f"assets/mockups/{target_dir.name}/{entry.name}"
                    warnings.append(
                        f"WARN: Non-task mockup entry '{rel_entry}'. "
                        f"Expected task-scoped directory 'assets/mockups/{target_dir.name}/TASK-XXX/' (ADR-0027)."
                    )
    return warnings


def check_tech_debt_integrity(docs_dir: Path, file_map: Optional[Dict[str, Path]] = None) -> List[str]:
    """
    Tier 1 / Tier 2 Quality Gate: validates tech debt registry docs/02_Tasks/TechDebt.md.
    Checks:
    1. Existence of docs/02_Tasks/TechDebt.md.
    2. Format of active debt IDs in table (must match ^DEBT-\\d{3,}$, e.g. DEBT-001).
    3. Wikilinks validity inside the table.
    Returns a list of error/warning strings.
    """
    errors = []
    recorded_debt_ids: Set[str] = set()
    debt_path = docs_dir / "02_Tasks" / "TechDebt.md"
    if not debt_path.is_file() and (docs_dir / "docs" / "02_Tasks" / "TechDebt.md").is_file():
        debt_path = docs_dir / "docs" / "02_Tasks" / "TechDebt.md"

    if not debt_path.is_file():
        errors.append("Tech debt registry not found: expected 'TechDebt.md' in '02_Tasks'")
        return errors

    try:
        content = debt_path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"Could not read TechDebt.md: {e}")
        return errors

    if not content.startswith("---"):
        errors.append("Malformed YAML frontmatter in TechDebt.md (starts without ---)")

    if file_map is None:
        file_map = build_file_map(docs_dir)

    repo_root = docs_dir.parent if docs_dir.name == "docs" else docs_dir
    in_debt_section = False

    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if "##" in stripped and ("долг" in stripped.lower() or "debt" in stripped.lower()):
            in_debt_section = True
            continue
        elif stripped.startswith("## ") and in_debt_section:
            in_debt_section = False

        if in_debt_section and stripped.startswith("|") and stripped.endswith("|"):
            parts = [p.strip() for p in stripped.split("|")[1:-1]]
            if not parts:
                continue
            first_cell = parts[0]
            if first_cell.lower() in ["id", "идентификатор"] or re.match(r"^:?-+:?$", first_cell):
                continue
            if not first_cell:
                continue

            # Validate DEBT-XXX format
            if re.match(r"^DEBT-\d{3,}$", first_cell):
                recorded_debt_ids.add(first_cell)
            else:
                errors.append(
                    f"In 'TechDebt.md' line {line_no}: invalid tech debt ID '{first_cell}'. "
                    f"Expected format DEBT-XXX (e.g. DEBT-001)."
                )

            # Validate wikilinks in this row
            row_links = parse_wikilinks(stripped)
            for link in row_links:
                link_clean = link.strip()
                if not link_clean or "XXX" in link_clean:
                    continue
                direct_target = (debt_path.parent / link_clean).resolve()
                direct_target_md = (debt_path.parent / f"{link_clean}.md").resolve()
                vault_target = (docs_dir / link_clean).resolve()
                vault_target_md = (docs_dir / f"{link_clean}.md").resolve()
                repo_target = (repo_root / link_clean).resolve()
                repo_target_md = (repo_root / f"{link_clean}.md").resolve()
                link_stem = Path(link_clean).stem.lower()
                link_name = Path(link_clean).name.lower()

                found = (
                    direct_target.exists()
                    or direct_target_md.exists()
                    or vault_target.exists()
                    or vault_target_md.exists()
                    or repo_target.exists()
                    or repo_target_md.exists()
                    or link_clean in file_map
                    or link_clean.lower() in file_map
                    or link_name in file_map
                    or link_stem in file_map
                )
                if not found:
                    errors.append(f"In 'TechDebt.md' line {line_no}: broken wikilink [[{link_clean}]]")

    # Semantic cross-check: plans/specs tagged #techdebt must reference a registered DEBT-XXX
    for base_dir in (docs_dir / "02_Tasks" / "Plans", docs_dir / "02_Tasks" / "Specs"):
        if not base_dir.is_dir():
            continue
        for md_file in sorted(base_dir.rglob("*.md")):
            if md_file.name.startswith("TEMPLATE_"):
                continue
            try:
                doc_content = md_file.read_text(encoding="utf-8")
            except Exception:
                continue
            if not doc_content.startswith("---"):
                continue
            parts = doc_content.split("---", 2)
            if len(parts) < 3:
                continue

            fm = parts[1]
            body = parts[2]
            id_match = re.search(r"^id:\s*([^\s#]+)", fm, re.MULTILINE)
            doc_id = id_match.group(1).strip() if id_match else ""
            if doc_id in HARNESS_META_TECHDEBT_IDS:
                continue

            if not re.search(r"\b(?:techdebt|tech-debt)\b", fm, re.IGNORECASE):
                continue

            rel_name = md_file.name
            has_debt_ref = bool(re.search(r"DEBT-\d{3,}", body))
            if not has_debt_ref:
                errors.append(
                    f"WARN: '{rel_name}' is tagged #techdebt but has no DEBT-XXX reference. "
                    f"Register the debt in TechDebt.md and link it from this document."
                )
            elif not recorded_debt_ids:
                errors.append(
                    f"WARN: '{rel_name}' references DEBT-XXX but TechDebt.md registry is empty. "
                    f"Register the referenced DEBT-XXX in the Active P3 Debt table."
                )

    return errors


def check_untracked_todos(docs_dir: Path) -> List[str]:
    """
    Tier 1 / Tier 2 Non-blocking Quality Gate:
    Audits documentation files and scripts for untracked TODO/FIXME comments
    that are not associated with a // ROADMAP-<ID> or // DEBT-XXX
    (or # ROADMAP-<ID> / <!-- ROADMAP-<ID> / <!-- DEBT-XXX).
    Returns a list of warning strings.
    """
    warnings = []
    repo_root = docs_dir.parent if docs_dir.name == "docs" else docs_dir

    files_to_scan: List[Path] = []
    if docs_dir.is_dir():
        for md_file in docs_dir.rglob("*.md"):
            if "00_Templates" in md_file.parts or md_file.name.startswith("TEMPLATE_"):
                continue
            files_to_scan.append(md_file)

    scripts_dir = repo_root / "scripts"
    if scripts_dir.is_dir():
        for py_file in scripts_dir.glob("*.py"):
            files_to_scan.append(py_file)

    md_comment_pattern = re.compile(r'<!--\s*(?:TODO|FIXME)\b', re.IGNORECASE)
    code_comment_pattern = re.compile(r'(?:#|//|/\*)\s*(?:TODO|FIXME)\b', re.IGNORECASE)

    for file_path in sorted(set(files_to_scan)):
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        rel_name = file_path.name
        try:
            if _is_relative_to(file_path, docs_dir):
                rel_name = _relative_to(file_path, docs_dir).as_posix()
            elif _is_relative_to(file_path, repo_root):
                rel_name = _relative_to(file_path, repo_root).as_posix()
        except Exception:
            pass

        is_markdown = file_path.suffix.lower() == ".md"
        active_pattern = md_comment_pattern if is_markdown else code_comment_pattern

        for line_no, line in enumerate(content.splitlines(), start=1):
            line_to_check = re.sub(r'`[^`]*`', '', line)
            if active_pattern.search(line_to_check):
                if not re.search(r'(?:ROADMAP-[A-Za-z0-9_-]+|DEBT-\d{3,})', line, re.IGNORECASE):
                    warnings.append(
                        f"Untracked TODO without ROADMAP-<ID> or DEBT-XXX reference in {rel_name}:{line_no}"
                    )

    return warnings


def build_file_map(docs_dir: Path, repo_root: Optional[Path] = None) -> Dict[str, Path]:
    if repo_root is None:
        repo_root = docs_dir.parent if docs_dir.name == "docs" else docs_dir
    file_map: Dict[str, Path] = {}

    all_md_files = list(docs_dir.rglob("*.md"))
    for root_doc in ["SPEC.md", "README.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"]:
        r_file = repo_root / root_doc
        if r_file.is_file():
            all_md_files.append(r_file)

    for f in all_md_files:
        if _is_relative_to(f, docs_dir):
            rel_posix = _relative_to(f, docs_dir).as_posix()
            file_map[rel_posix] = f
            file_map[rel_posix.lower()] = f
        name_no_ext = f.stem
        file_map[name_no_ext] = f
        file_map[name_no_ext.lower()] = f
        file_map[f.name] = f
        file_map[f.name.lower()] = f

    # Register media files from docs_dir (strictly with extension, NEVER by stem!)
    for p in docs_dir.rglob("*"):
        if not p.is_file() or p.name.startswith("."):
            continue
        ext = p.suffix.lower()
        if ext in MEDIA_EXTENSIONS:
            file_map[p.name] = p
            file_map[p.name.lower()] = p
            if _is_relative_to(p, docs_dir):
                rel_posix = _relative_to(p, docs_dir).as_posix()
                file_map[rel_posix] = p
                file_map[rel_posix.lower()] = p

    return file_map


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

    # Collect map of base names and relative paths
    file_map = build_file_map(docs_dir, repo_root)

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

        if _is_relative_to(f, docs_dir):
            rel = _relative_to(f, docs_dir).as_posix()
        else:
            rel = f.name

        # Check frontmatter for task/spec/bug/adr/plan/inbox/incident
        if any(prefix in rel for prefix in ["02_Tasks/Specs", "02_Tasks/Plans", "02_Tasks/Bugs", "03_Decisions_ADR", "02_Tasks/Inbox", "06_Memory/Incidents"]):
            if not f.name.startswith("TEMPLATE_"):
                has_fm, msg = check_file_frontmatter(f)
                if not has_fm:
                    frontmatter_warnings.append((rel, msg))

        # Check wikilinks & markdown images (skip template files containing placeholder links)
        if "TEMPLATE" in f.name or "00_Templates" in rel:
            continue

        links = parse_wikilinks(content)
        md_images = parse_markdown_images(content)
        all_targets = links + [img for img in md_images if img not in links]

        for link in all_targets:
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

            # Check relative to parent directory (e.g. 02_Tasks sibling directories)
            sibling_target = (file_dir.parent / link).resolve()
            sibling_target_md = (file_dir.parent / f"{link}.md").resolve()

            # Check stripped leading relative dots against docs_dir and repo_root
            stripped_link = re.sub(r'^(?:\.\./|\./)+', '', link)
            stripped_vault_target = (docs_dir / stripped_link).resolve()
            stripped_vault_target_md = (docs_dir / f"{stripped_link}.md").resolve()
            stripped_repo_target = (repo_root / stripped_link).resolve()
            stripped_repo_target_md = (repo_root / f"{stripped_link}.md").resolve()

            link_name = Path(link).name
            link_name_lower = link_name.lower()
            link_stem = Path(link).stem
            link_stem_lower = link_stem.lower()
            link_ext = Path(link).suffix.lower()

            found = False
            candidates = [
                direct_target, direct_target_md,
                vault_target, vault_target_md,
                repo_target, repo_target_md,
                sibling_target, sibling_target_md,
                stripped_vault_target, stripped_vault_target_md,
                stripped_repo_target, stripped_repo_target_md,
            ]
            for cand in candidates:
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
                has_path_sep = ("/" in link or "\\" in link)
                if link_ext in MEDIA_EXTENSIONS or "." in link_name:
                    if not has_path_sep and (link_name in file_map or link_name_lower in file_map):
                        found = True
                    elif (
                        link in file_map
                        or link.lower() in file_map
                        or stripped_link in file_map
                        or stripped_link.lower() in file_map
                    ):
                        found = True
                else:
                    if not has_path_sep and (link_stem in file_map or link_stem_lower in file_map):
                        found = True

            if not found:
                broken_links.append((rel, link))

    drift_warnings = check_spec_drift(docs_dir)
    devlog_warnings = check_devlog_semantic_guard(docs_dir)
    fast_track_warnings = check_fast_track_specs(docs_dir)
    phase_warnings = check_phase_consistency(docs_dir)
    research_warnings = check_research_basis(docs_dir)
    symbolic_warnings = check_symbolic_scope(docs_dir)
    memory_errors = check_memory_limits(docs_dir)
    memory_warnings = check_memory_consistency(docs_dir)
    asset_warnings = check_asset_weights(docs_dir)
    asset_layout_warnings = check_asset_layout(docs_dir)
    debt_results = check_tech_debt_integrity(docs_dir, file_map=file_map)
    debt_errors = [
        e for e in debt_results
        if not e.startswith("WARN:") and not e.startswith("Tech debt registry not found")
    ]
    has_tasks_harness = (
        (docs_dir / "02_Tasks" / "Kanban.md").is_file()
        or (docs_dir / "02_Tasks" / "Roadmap.md").is_file()
        or (docs_dir / "docs" / "02_Tasks" / "Kanban.md").is_file()
        or (docs_dir / "docs" / "02_Tasks" / "Roadmap.md").is_file()
    )
    debt_warnings = [
        e for e in debt_results
        if e.startswith("WARN:")
        or (e.startswith("Tech debt registry not found") and has_tasks_harness)
    ]
    todo_warnings = check_untracked_todos(docs_dir)
    has_errors = bool(broken_links or frontmatter_warnings or memory_errors or debt_errors)

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

        if memory_errors:
            print(f"❌ Memory Limit Errors ({len(memory_errors)}):")
            for me in memory_errors:
                print(f"   • {me}")
            print()

        if memory_warnings:
            print(f"⚠️ Memory Consistency Warnings ({len(memory_warnings)}):")
            for mw in memory_warnings:
                print(f"   • {mw}")
            print()

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

        if fast_track_warnings:
            print(f"⚠️ Fast-Track Guard Warnings ({len(fast_track_warnings)}):")
            for ftw in fast_track_warnings:
                print(f"   • {ftw}")
            print()

        if phase_warnings:
            print(f"⚠️ Phase Consistency Warnings ({len(phase_warnings)}):")
            for pw in phase_warnings:
                print(f"   • {pw}")
            print()

        if research_warnings:
            print(f"⚠️ Research Basis Warnings ({len(research_warnings)}):")
            for rw in research_warnings:
                print(f"   • {rw}")
            print()

        if symbolic_warnings:
            print("⚠️ Symbolic Scope Warnings (%d):" % len(symbolic_warnings))
            print("\n".join("   • " + sw for sw in symbolic_warnings))
            print()

        if asset_warnings:
            print(f"⚠️ Asset Weight Warnings ({len(asset_warnings)}):")
            for aw in asset_warnings:
                print(f"   • {aw}")
            print()

        if asset_layout_warnings:
            print(f"⚠️ Asset Layout Warnings ({len(asset_layout_warnings)}):")
            for alw in asset_layout_warnings:
                print(f"   • {alw}")
            print()

        if debt_warnings:
            print(f"⚠️ Tech Debt Warnings ({len(debt_warnings)}):")
            for dw in debt_warnings:
                print(f"   • {dw}")
            print()

        if debt_errors:
            print(f"❌ Tech Debt Integrity Errors ({len(debt_errors)}):")
            for de in debt_errors:
                print(f"   • {de}")
            print()

        if todo_warnings:
            print(f"⚠️ Untracked TODO Warnings ({len(todo_warnings)}):")
            for tw in todo_warnings:
                print(f"   • {tw}")
            print()

        if has_errors:
            print("❌ Linter failed: please resolve errors.")
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
        for ftw in fast_track_warnings:
            print(f"⚠️  WARN: {ftw}")
        for pw in phase_warnings:
            print(f"⚠️  WARN: {pw}")
        for rw in research_warnings:
            if rw.startswith("WARN:"):
                print(f"⚠️  {rw}")
            else:
                print(f"⚠️  WARN: {rw}")
        for sw in symbolic_warnings:
            print(f"⚠️  {sw}" if sw.startswith("WARN:") else f"⚠️  WARN: {sw}")
        for aw in asset_warnings:
            print(f"⚠️  {aw}")
        for alw in asset_layout_warnings:
            print(f"⚠️  {alw}")
        for dw in debt_warnings:
            if dw.startswith("WARN:"):
                print(f"⚠️  {dw}")
            else:
                print(f"⚠️  WARN: {dw}")
        for mw in memory_warnings:
            if mw.startswith("WARN:"):
                print(f"⚠️  {mw}")
            else:
                print(f"⚠️  WARN: {mw}")
        for tw in todo_warnings:
            print(f"⚠️  WARN: {tw}")
        if not has_errors:
            print(f"OK: {len(all_md_files)} files scanned, {checked_links_count} wikilinks verified (0 broken).")
            return 0
        else:
            error_count = len(broken_links) + len(frontmatter_warnings) + len(memory_errors) + len(debt_errors)
            print(f"ERROR: {len(broken_links)} broken links, {len(frontmatter_warnings)} frontmatter warnings, {len(memory_errors)} memory errors, {len(debt_errors)} tech debt errors.")
            if broken_links:
                for src, target in broken_links:
                    print(f"   • In '{src}' -> target not found: [[{target}]]")
            if frontmatter_warnings:
                for src, msg in frontmatter_warnings:
                    print(f"   • {src}: {msg}")
            if memory_errors:
                for me in memory_errors:
                    print(f"   • {me}")
            if debt_errors:
                for de in debt_errors:
                    print(f"   • {de}")
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
