#!/usr/bin/env python3
"""
Knowledge Base Linter for Docs-as-Code Vaults.
Validates wikilinks, file existence, and YAML frontmatter integrity.
Zero external dependencies (uses standard Python 3 library only).
"""

import sys
import os
import re
import json
import argparse
import urllib.parse
import difflib
import tempfile
import subprocess
from dataclasses import dataclass
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

RULESET_VERSION = 1  # Ð²ÐµÑ€ÑÐ¸Ñ Ð½Ð°Ð±Ð¾Ñ€Ð° Ð¿Ñ€Ð°Ð²Ð¸Ð»/ÑÑ…ÐµÐ¼Ñ‹ Ð²Ñ‹Ð²Ð¾Ð´Ð°; Ð½Ðµ Ñ€ÐµÐ»Ð¸Ð·Ð½Ð°Ñ Ð²ÐµÑ€ÑÐ¸Ñ Ñ…Ð°Ñ€Ð½ÐµÑÑÐ°

# Ð ÐµÐµÑÑ‚Ñ€ ÑÑ‚Ð°Ð±Ð¸Ð»ÑŒÐ½Ñ‹Ñ… Ð¸Ð´ÐµÐ½Ñ‚Ð¸Ñ„Ð¸ÐºÐ°Ñ‚Ð¾Ñ€Ð¾Ð² Ð¿Ñ€Ð°Ð²Ð¸Ð» (SSOT Ð´Ð»Ñ --format json/sarif).
RULES: Dict[str, str] = {
    "KB-001": "Broken or unresolved wikilink or markdown link",
    "KB-002": "Missing or invalid YAML frontmatter",
    "KB-003": "Procedural memory limit exceeded",
    "KB-004": "Tech debt registry integrity",
    "KB-005": "Asset layout violation",
    "KB-006": "Phase consistency mismatch",
    "KB-007": "Missing research basis for a plan",
    "KB-008": "Devlog next-step semantics",
    "KB-009": "Untracked TODO/FIXME without backlog reference",
    "KB-010": "Task dependency cycle or unknown dependency",
    "KB-011": "Living Spec drift",
    "KB-012": "Fast-track scope or budget violation",
    "KB-013": "Memory index consistency",
    "KB-014": "Symbolic scope contract violation",
    "KB-015": "Asset weight budget exceeded",
    "KB-016": "Spec quality marker or checklist violation",
    "KB-017": "Scenario-to-test traceability gap",
    "KB-018": "Review contract or convergence deviation",
    "KB-019": "Delta-spec convention violation",
    "KB-020": "Deep-risk tag requires parent plan or research basis",
}

# KB-010 Ð·Ð°Ñ€ÐµÐ·ÐµÑ€Ð²Ð¸Ñ€Ð¾Ð²Ð°Ð½ Ð¿Ð¾Ð´ depends_on (Ð¤Ð°Ð·Ð° 28+): Ð² Ñ€ÐµÐµÑÑ‚Ñ€Ðµ ÐµÑÑ‚ÑŒ, severity Ð½ÐµÑ‚ â€”
# Ð¿Ð¾Ð¿Ñ‹Ñ‚ÐºÐ° ÑÐ¼Ð¸ÑÑÐ¸Ð¸ Ð´Ð°Ñ‘Ñ‚ ValueError, Ð¿Ð¾ÑÑ‚Ð¾Ð¼Ñƒ Ð¿Ñ€Ð°Ð²Ð¸Ð»Ð¾ Ð½Ðµ Ð¼Ð¾Ð¶ÐµÑ‚ Â«Ð¿Ñ€Ð¾ÑÐ¾Ñ‡Ð¸Ñ‚ÑŒÑÑÂ» Ð·Ð°Ñ€Ð°Ð½ÐµÐµ.
RULE_SEVERITY: Dict[str, str] = {
    "KB-001": "error",
    "KB-002": "error",
    "KB-003": "error",
    "KB-004": "error",
    "KB-005": "warning",
    "KB-006": "warning",
    "KB-007": "warning",
    "KB-008": "warning",
    "KB-009": "warning",
    "KB-010": "error",
    "KB-011": "warning",
    "KB-012": "warning",
    "KB-013": "warning",
    "KB-014": "warning",
    "KB-015": "warning",
    "KB-016": "error",
    "KB-017": "warning",
    "KB-018": "warning",
    "KB-019": "warning",
    "KB-020": "warning",
}

VALID_SEVERITIES = ("error", "warning")


class Finding(str):
    """ÐžÐ´Ð½Ð° Ð½Ð°Ñ…Ð¾Ð´ÐºÐ° Ð»Ð¸Ð½Ñ‚ÐµÑ€Ð°: Ñ‚ÐµÐºÑÑ‚ ÑÐ¾Ð¾Ð±Ñ‰ÐµÐ½Ð¸Ñ + ÑÑ‚Ñ€ÑƒÐºÑ‚ÑƒÑ€Ð¸Ñ€Ð¾Ð²Ð°Ð½Ð½Ñ‹Ðµ Ð¼ÐµÑ‚Ð°Ð´Ð°Ð½Ð½Ñ‹Ðµ.

    ÐÐ°ÑÐ»ÐµÐ´ÑƒÐµÑ‚ÑÑ Ð¾Ñ‚ ``str`` Ð½Ð°Ð¼ÐµÑ€ÐµÐ½Ð½Ð¾: ``check_*`` Ð¸ÑÑ‚Ð¾Ñ€Ð¸Ñ‡ÐµÑÐºÐ¸ Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°Ð»Ð¸ ÑÐ¿Ð¸ÑÐºÐ¸
    ÑÐ¾Ð¾Ð±Ñ‰ÐµÐ½Ð¸Ð¹, Ð¸ Ð¿Ð¾Ñ‚Ñ€ÐµÐ±Ð¸Ñ‚ÐµÐ»Ð¸ (Ñ‚ÐµÑÑ‚Ñ‹, ÐºÐ»Ð¸ÐµÐ½Ñ‚ÑÐºÐ¸Ðµ ÑÐºÑ€Ð¸Ð¿Ñ‚Ñ‹) ÑÑ€Ð°Ð²Ð½Ð¸Ð²Ð°ÑŽÑ‚ Ð¸Ñ… ÐºÐ°Ðº ÑÑ‚Ñ€Ð¾ÐºÐ¸.
    JSON/SARIF-Ñ€ÐµÐ½Ð´ÐµÑ€ÐµÑ€Ñ‹ Ñ‡Ð¸Ñ‚Ð°ÑŽÑ‚ Ð°Ñ‚Ñ€Ð¸Ð±ÑƒÑ‚Ñ‹, text-Ñ€ÐµÐ½Ð´ÐµÑ€ÐµÑ€ Ð¿ÐµÑ‡Ð°Ñ‚Ð°ÐµÑ‚ ``str(finding)``.
    """

    __slots__ = ("rule_id", "severity", "file", "location", "fixable")

    def __new__(cls, rule_id: str, message: str, severity: str, file: str = "", location: str = "", fixable: bool = False):
        obj = super().__new__(cls, message)
        obj.rule_id = rule_id
        obj.severity = severity
        obj.file = file or ""
        obj.location = location or ""
        obj.fixable = bool(fixable)
        return obj

    @property
    def message(self) -> str:
        return str(self)


def make_finding(rule_id: str, message: str, file: str = "", severity: Optional[str] = None,
                 location: str = "", fixable: Optional[bool] = None) -> Finding:
    """Creates a finding after validating rule id and severity against the registry."""
    if rule_id not in RULES:
        raise ValueError("Unknown lint rule: %s" % rule_id)
    resolved = severity or RULE_SEVERITY.get(rule_id)
    if resolved not in VALID_SEVERITIES:
        raise ValueError("Rule %s is reserved and cannot be emitted yet" % rule_id)
    if fixable is None:
        msg_l = message.lower()
        fixable = False
        if rule_id == "KB-002" and ("missing closing ---" in msg_l or "starts without ---" in msg_l or "delimiter" in msg_l or "invalid date format" in msg_l or "missing '#'" in msg_l):
            fixable = True
        elif rule_id in ("KB-004", "KB-005", "KB-006", "KB-007") and ("date format" in msg_l or "delimiter" in msg_l or "trailing whitespace" in msg_l or "tag format" in msg_l):
            fixable = True
    return Finding(rule_id, message, resolved, file, location, fixable=bool(fixable))


class LintReport(object):
    """Ð ÐµÐ·ÑƒÐ»ÑŒÑ‚Ð°Ñ‚ Ð¿Ñ€Ð¾Ð³Ð¾Ð½Ð° Ð»Ð¸Ð½Ñ‚ÐµÑ€Ð°: ÑÑ‡Ñ‘Ñ‚Ñ‡Ð¸ÐºÐ¸ Ð¸ Ð½Ð°Ñ…Ð¾Ð´ÐºÐ¸ (ÐµÐ´Ð¸Ð½Ñ‹Ð¹ Ð¸ÑÑ‚Ð¾Ñ‡Ð½Ð¸Ðº Ð´Ð»Ñ Ñ€ÐµÐ½Ð´ÐµÑ€ÐµÑ€Ð¾Ð²)."""

    __slots__ = ("files", "wikilinks", "findings")

    def __init__(self, files: int, wikilinks: int, findings: List[Finding]):
        self.files = files
        self.wikilinks = wikilinks
        self.findings = findings

    def by_rule(self, rule_id: str, severity: Optional[str] = None) -> List[Finding]:
        return [
            f for f in self.findings
            if f.rule_id == rule_id and (severity is None or f.severity == severity)
        ]

    def by_rule_severity(self, severity: str) -> List[Finding]:
        return [f for f in self.findings if f.severity == severity]

    def has_errors(self) -> bool:
        return any(f.severity == "error" for f in self.findings)


@dataclass
class Fix:
    rule_id: str
    description: str
    file_path: Path
    line_number: int  # 1-based (0 if whole-file / EOF)
    original_text: str
    replacement_text: str


@dataclass
class FixResult:
    file_path: Path
    original_content: str
    modified_content: str
    diff_lines: List[str]
    fixes: List[Fix]

    @property
    def has_changes(self) -> bool:
        return self.original_content != self.modified_content


COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_RESET = "\033[0m"


def render_diff(diff_lines: List[str], use_color: bool = False) -> str:
    """Renders unified diff lines with optional ANSI color highlighting."""
    if not diff_lines:
        return ""
    if not use_color:
        return "".join(diff_lines)
    colored: List[str] = []
    for line in diff_lines:
        if line.startswith("+++") or line.startswith("---"):
            colored.append(line)
        elif line.startswith("+"):
            colored.append(f"{COLOR_GREEN}{line}{COLOR_RESET}")
        elif line.startswith("-"):
            colored.append(f"{COLOR_RED}{line}{COLOR_RESET}")
        elif line.startswith("@@"):
            colored.append(f"{COLOR_CYAN}{line}{COLOR_RESET}")
        else:
            colored.append(line)
    return "".join(colored)


def git_check_clean(file_path: Path) -> bool:
    """Returns True if the file has no uncommitted git changes, or if git is unavailable."""
    try:
        resolved = file_path.resolve()
        proc = subprocess.run(
            ["git", "status", "--porcelain", "--", str(resolved)],
            cwd=str(resolved.parent),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if proc.returncode != 0:
            return True
        return len(proc.stdout.strip()) == 0
    except Exception:
        return True


def atomic_write_file(file_path: Path, content: str) -> None:
    """Writes content atomically using a temporary file in the same directory and os.replace."""
    resolved = file_path.resolve()
    target_dir = resolved.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile("w", dir=str(target_dir), delete=False, encoding="utf-8", newline="")
    temp_name = temp_file.name
    try:
        temp_file.write(content)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()
        os.replace(temp_name, str(resolved))
    except Exception:
        try:
            temp_file.close()
            if os.path.exists(temp_name):
                os.remove(temp_name)
        except Exception:
            pass
        raise


def generate_file_fixes(content: str, file_path: Path) -> FixResult:
    """Generates surgical deterministic fixes for safe rules (KB-004, KB-005, KB-006, KB-007, KB-010)."""
    fixes: List[Fix] = []
    if not content:
        return FixResult(file_path=file_path, original_content=content, modified_content=content, diff_lines=[], fixes=[])

    raw_lines = content.splitlines(keepends=True)
    lines = list(raw_lines)

    # 1. Frontmatter delimiter check (KB-004) & detection
    fm_start = -1
    fm_end = -1
    if lines and re.match(r"^---\s*$", lines[0]):
        fm_start = 0
        if lines[0] != "---\n":
            old_line = lines[0]
            lines[0] = "---\n"
            fixes.append(Fix(
                rule_id="KB-004",
                description="Normalize frontmatter opening delimiter",
                file_path=file_path,
                line_number=1,
                original_text=old_line,
                replacement_text="---\n",
            ))
        for idx in range(1, len(lines)):
            if re.match(r"^---\s*$", lines[idx]):
                fm_end = idx
                if lines[idx] != "---\n":
                    old_line = lines[idx]
                    lines[idx] = "---\n"
                    fixes.append(Fix(
                        rule_id="KB-004",
                        description="Normalize frontmatter closing delimiter",
                        file_path=file_path,
                        line_number=idx + 1,
                        original_text=old_line,
                        replacement_text="---\n",
                    ))
                break

    # 2. Date format normalization inside frontmatter (KB-005)
    if fm_start != -1 and fm_end != -1:
        for idx in range(fm_start + 1, fm_end):
            line = lines[idx]
            clean = line.rstrip("\r\n")
            m = re.match(r"^(\s*(?:created|updated|date):\s*)(['\"]?)(\d{4})[./](\d{2})[./](\d{2})\2(\s*(?:#.*)?)$", clean)
            if m:
                prefix, quote, y, m_month, d, comment = m.groups()
                norm_date = f"{prefix}{quote}{y}-{m_month}-{d}{quote}{comment}\n"
                if norm_date != line:
                    old_line = line
                    lines[idx] = norm_date
                    fixes.append(Fix(
                        rule_id="KB-005",
                        description=f"Normalize date to ISO-8601 YYYY-MM-DD ({y}-{m_month}-{d})",
                        file_path=file_path,
                        line_number=idx + 1,
                        original_text=old_line,
                        replacement_text=norm_date,
                    ))

    # 3. Default depends_on: [] injection in task specs (KB-010)
    posix_path = file_path.as_posix()
    is_task_spec = (
        ("02_Tasks/Specs/" in posix_path or bool(re.match(r"^TASK-\d{3,}", file_path.name)))
        and not file_path.name.startswith("TEMPLATE_")
    )
    if is_task_spec and fm_start != -1 and fm_end != -1:
        has_depends_on = any(re.match(r"^\s*depends_on\s*:", lines[i]) for i in range(fm_start + 1, fm_end))
        if not has_depends_on:
            lines.insert(fm_end, "depends_on: []\n")
            fixes.append(Fix(
                rule_id="KB-010",
                description="Inject default 'depends_on: []' in task specification frontmatter",
                file_path=file_path,
                line_number=fm_end + 1,
                original_text="",
                replacement_text="depends_on: []\n",
            ))
            fm_end += 1

    # 4. Trailing whitespace removal (KB-006)
    for idx in range(len(lines)):
        line = lines[idx]
        clean_nl = line.rstrip("\r\n")
        in_fm = (fm_start != -1 and idx > fm_start and (fm_end == -1 or idx < fm_end))
        if in_fm:
            stripped = clean_nl.rstrip(" \t")
        else:
            # In Markdown body, exactly two spaces at the end of a non-empty line indicates a hard line break (<br>)
            if clean_nl.endswith("  ") and not clean_nl.endswith("   ") and clean_nl.strip() != "":
                stripped = clean_nl
            else:
                stripped = clean_nl.rstrip(" \t")

        if stripped != clean_nl:
            new_line = stripped + "\n"
            old_line = line
            lines[idx] = new_line
            fixes.append(Fix(
                rule_id="KB-006",
                description="Remove trailing whitespace",
                file_path=file_path,
                line_number=idx + 1,
                original_text=old_line,
                replacement_text=new_line,
            ))

    # 5. Ensure single EOF newline (KB-007)
    intermediate = "".join(lines)
    ensured = intermediate.rstrip("\r\n") + "\n"
    if ensured != intermediate:
        fixes.append(Fix(
            rule_id="KB-007",
            description="Ensure single trailing newline at EOF",
            file_path=file_path,
            line_number=len(lines),
            original_text=intermediate[len(ensured.rstrip("\r\n")):],
            replacement_text="\n",
        ))
        intermediate = ensured

    diff_lines = list(difflib.unified_diff(
        content.splitlines(keepends=True),
        intermediate.splitlines(keepends=True),
        fromfile=f"a/{file_path.name}",
        tofile=f"b/{file_path.name}",
    ))

    return FixResult(
        file_path=file_path,
        original_content=content,
        modified_content=intermediate,
        diff_lines=diff_lines,
        fixes=fixes,
    )



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


def _docs_rel(file_path: Path, docs_dir: Path) -> str:
    """Path relative to the knowledge base root (kept for text/JSON ``file``)."""
    try:
        return _relative_to(file_path, docs_dir).as_posix()
    except Exception:
        return file_path.name


def _repo_rel(file_path: Path, docs_dir: Path) -> str:
    """Path relative to the repository root (BUG-013: required by SARIF / Code Scanning)."""
    repo_root = docs_dir.parent if docs_dir.name == "docs" else docs_dir
    try:
        return _relative_to(file_path, repo_root).as_posix()
    except Exception:
        return file_path.name


def resolve_location(file_value: str, docs_dir: Path) -> str:
    """Repo-relative location for a finding whose ``file`` is knowledge-base relative."""
    if not file_value:
        return ""
    candidate = docs_dir / file_value
    if candidate.is_file():
        return _repo_rel(candidate, docs_dir)
    return file_value


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


def check_spec_drift(docs_dir: Path) -> List[Finding]:
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
            warnings.append(make_finding("KB-011", f"Living Spec Drift: SPEC.md was never updated since creation ({created_date}), "
                f"despite {completed_phases} completed phases in Roadmap.md. Consider syncing Master Spec.", file="02_Tasks/Roadmap.md"))

    return warnings


def check_devlog_semantic_guard(docs_dir: Path) -> List[Finding]:
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
            warnings.append(make_finding("KB-008", f"In '{rel_name}' line {i}: bare step trigger detected without user guardrail. "
                f"Prefer '- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**' to prevent auto-chaining.", file=_docs_rel(devlog_path, docs_dir)))
    return warnings


def check_fast_track_specs(docs_dir: Path) -> List[Finding]:
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
            warnings.append(make_finding("KB-012", f"Fast-Track spec '{rel_name}' touches {len(file_items)} files (limit: <= 2). Consider full RFC.", file=_docs_rel(spec_file, docs_dir)))

        # 2. Check Verification Plan
        has_verif = bool(
            re.search(r"##\s+.*(?:План верификации|Verification Plan)", content, re.IGNORECASE) or
            re.search(r"(?:python|pytest|dotnet|npm|cargo)\s+.*", content, re.IGNORECASE)
        )
        if not has_verif:
            warnings.append(make_finding("KB-012", f"Fast-Track spec '{rel_name}' is missing a Verification Plan.", file=_docs_rel(spec_file, docs_dir)))

    return warnings


def check_phase_consistency(docs_dir: Path) -> List[Finding]:
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
                warnings.append(make_finding("KB-006", f"Spec '{rel_path}' declares phase {fm_phase}, but is located in folder '{folder.name}' (expected phase {folder_phase}).", file=_docs_rel(spec_file, docs_dir)))

            # 2. Frontmatter Phase vs Tags
            tags_block = ""
            m_tags = re.search(r"^tags:\s*([\s\S]*?)(?=\n[a-zA-Z_-]+:|\n---|$)", fm, re.MULTILINE)
            if m_tags:
                tags_block = m_tags.group(1)
            tag_matches = re.findall(r"\bphase(\d+)\b", tags_block, re.IGNORECASE)
            for tag_phase_str in tag_matches:
                tag_phase = int(tag_phase_str)
                if tag_phase != fm_phase:
                    warnings.append(make_finding("KB-006", f"Spec '{rel_path}' declares phase {fm_phase}, but contains mismatched tag 'phase{tag_phase}'.", file=_docs_rel(spec_file, docs_dir)))

    return warnings


def check_memory_limits(docs_dir: Path) -> List[Finding]:
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
                errors.append(make_finding("KB-003", f"Memory patterns limit exceeded: {len(pattern_matches)} active patterns found in "
                    f"'{rel_p}' (maximum allowed: 15). "
                    f"Archive or consolidate patterns to preserve token economy!", file=rel_p))
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


def check_memory_consistency(docs_dir: Path) -> List[Finding]:
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
                incident_warnings.append(make_finding("KB-013", f"WARN: incident '{incident_file.name}' has no 'id' in frontmatter", file=_docs_rel(incident_file, docs_dir)))
            elif not filename_prefix or incident_id != filename_prefix:
                incident_warnings.append(make_finding("KB-013", f"WARN: incident '{incident_id}' id does not match filename '{incident_file.name}'", file=_docs_rel(incident_file, docs_dir)))
            lookup_prefix = filename_prefix or incident_id
            if lookup_prefix:
                incident_reports_by_prefix[lookup_prefix] = {
                    "target_pattern": frontmatter.get("target_pattern", "").strip(),
                    "file": _docs_rel(incident_file, docs_dir),
                }

    for tag, line in pattern_entries:
        if MEMORY_SEEDED_MARKER in line:
            continue
        for incident_id in sorted(set(re.findall(r"INC-\d{3}", line))):
            if incident_id not in incident_reports_by_prefix:
                warnings.append(make_finding("KB-013", f"WARN: patterns.md references missing incident report '{incident_id}'", file="06_Memory/patterns.md"))
                continue
            target_pattern = incident_reports_by_prefix[incident_id]["target_pattern"]
            if target_pattern and target_pattern != tag:
                warnings.append(make_finding("KB-013", f"WARN: pattern '{tag}' links '{incident_id}' whose target_pattern is '{target_pattern}'", file="06_Memory/patterns.md"))

    for incident_id, report in sorted(incident_reports_by_prefix.items()):
        target_pattern = report["target_pattern"]
        if not target_pattern:
            incident_warnings.append(make_finding("KB-013", f"WARN: incident '{incident_id}' is missing required 'target_pattern'", file=report.get("file", "")))
        elif target_pattern not in pattern_tags:
            incident_warnings.append(make_finding("KB-013", f"WARN: incident '{incident_id}' targets '{target_pattern}' which is absent from patterns.md", file=report.get("file", "")))

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


def check_research_basis(docs_dir: Path) -> List[Finding]:
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
            warnings.append(make_finding("KB-007", "WARN: plan '%s' sets research_basis: none without basis_note" % plan_file.name, file=_docs_rel(plan_file, docs_dir)))
    return warnings


DEEP_RISK_TAGS: Set[str] = {"architecture", "security", "migration", "public-api"}


def _extract_frontmatter_tags(frontmatter_raw: str) -> Set[str]:
    """Extracts tag identifiers from frontmatter block."""
    tags: Set[str] = set()
    list_match = re.search(r"^tags:\s*\n((?:\s*-\s*[^\n]+\n?)+)", frontmatter_raw, re.MULTILINE)
    if list_match:
        for line in list_match.group(1).splitlines():
            clean = line.strip().lstrip("-").strip().lower().lstrip("#")
            if clean:
                tags.add(clean)
    else:
        inline_match = re.search(r"^tags:\s*\[(.*?)\]", frontmatter_raw, re.MULTILINE)
        if inline_match:
            for item in inline_match.group(1).split(","):
                clean = item.strip().strip("'\"").strip().lower().lstrip("#")
                if clean:
                    tags.add(clean)
    return tags


def check_deep_risk_tags(docs_dir: Path) -> List[Finding]:
    """
    Tier 1 Quality Gate (Non-blocking): audit deep-risk tasks and plans.

    Rule KB-020 (SEVERITY_WARNING):
    Tasks or plans tagged with deep-risk identifiers (architecture, security, migration, public-api)
    should be backed by a parent plan or research basis to ensure architectural due diligence.
    """
    warnings: List[Finding] = []

    # 1. Audit Specs
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if not specs_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Specs").is_dir():
        specs_dir = docs_dir / "docs" / "02_Tasks" / "Specs"

    if specs_dir.is_dir():
        for spec_file in sorted(specs_dir.rglob("*.md")):
            if spec_file.name.startswith("TEMPLATE_"):
                continue
            try:
                text = spec_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if not text.startswith("---"):
                continue
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            frontmatter = parts[1]
            tags = _extract_frontmatter_tags(frontmatter)
            matched = tags & DEEP_RISK_TAGS
            if not matched:
                continue

            plan_match = re.search(r"^parent_plan:\s*(.*)", frontmatter, re.MULTILINE)
            plan_val = plan_match.group(1).strip().strip("'\"") if plan_match else ""
            if not plan_val or plan_val.lower() in ("none", "null", "[]"):
                tag_str = ", ".join(sorted(matched))
                warnings.append(make_finding(
                    "KB-020",
                    f"WARN: task '{spec_file.name}' has deep-risk tag(s) [{tag_str}] but lacks parent_plan reference",
                    file=_docs_rel(spec_file, docs_dir),
                ))

    # 2. Audit Plans
    plans_dir = docs_dir / "02_Tasks" / "Plans"
    if not plans_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Plans").is_dir():
        plans_dir = docs_dir / "docs" / "02_Tasks" / "Plans"

    if plans_dir.is_dir():
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
            tags = _extract_frontmatter_tags(frontmatter)
            matched = tags & DEEP_RISK_TAGS
            if not matched:
                continue

            phase_match = re.search(r"^phase:\s*(\d+)", frontmatter, re.MULTILINE)
            if phase_match and int(phase_match.group(1)) < 24:
                # Backward compatibility: ADR-0031 research basis requirement adopted in Phase 24
                continue

            basis_match = RESEARCH_BASIS_RE.search(frontmatter)
            basis_val = _normalize_plan_value(basis_match.group(1)).lower() if basis_match else ""
            note_match = BASIS_NOTE_RE.search(frontmatter)
            note_val = _normalize_plan_value(note_match.group(1)) if note_match else ""

            if not basis_val or (basis_val == "none" and not note_val):
                tag_str = ", ".join(sorted(matched))
                warnings.append(make_finding(
                    "KB-020",
                    f"WARN: plan '{plan_file.name}' has deep-risk tag(s) [{tag_str}] but lacks verified research_basis or basis_note",
                    file=_docs_rel(plan_file, docs_dir),
                ))

    return warnings


def check_symbolic_scope(docs_dir: Path) -> List[Finding]:
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
            warnings.append(make_finding("KB-014", "WARN: task '%s' uses line-number anchors (ADR-0029)" % spec_file.name, file=_docs_rel(spec_file, docs_dir)))

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
                warnings.append(make_finding("KB-014", "WARN: task '%s' modifies code '%s' without a nested symbol (ADR-0029)"
                    % (spec_file.name, raw_path), file=_docs_rel(spec_file, docs_dir)))
    return warnings


def check_asset_weights(docs_dir: Path, max_bytes: int = 2 * 1024 * 1024) -> List[Finding]:
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
                    warnings.append(make_finding("KB-015", f"WARN: Asset '{rel_p}' exceeds size limit ({mb:.1f} MB > 2.0 MB)", file=rel_p))
            except Exception:
                pass
    return warnings


def check_asset_layout(docs_dir: Path) -> List[Finding]:
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
                warnings.append(make_finding("KB-005", f"WARN: Disallowed asset category directory 'assets/{item.name}'. "
                    f"Allowed root categories: {allowed_str}. "
                    f"Move platform folders inside 'assets/mockups/{item.name}/' or 'assets/screenshots/{item.name}/'.", file="assets/" + item.name))
        elif item.is_file():
            warnings.append(make_finding("KB-005", f"WARN: Unorganized file 'assets/{item.name}' in root of docs/assets/. "
                f"Place assets inside mockups/, screenshots/, diagrams/, or design/.", file="assets/" + item.name))

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
                    warnings.append(make_finding("KB-005", f"WARN: Non-task mockup entry '{rel_entry}'. "
                        f"Expected task-scoped directory 'assets/mockups/{target_dir.name}/TASK-XXX/' (ADR-0027).", file=rel_entry))
    return warnings


def check_tech_debt_integrity(docs_dir: Path, file_map: Optional[Dict[str, Path]] = None) -> List[Finding]:
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
        errors.append(make_finding("KB-004", "Tech debt registry not found: expected 'TechDebt.md' in '02_Tasks'", file="02_Tasks/TechDebt.md", severity="warning"))
        return errors

    try:
        content = debt_path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(make_finding("KB-004", f"Could not read TechDebt.md: {e}", file="02_Tasks/TechDebt.md"))
        return errors

    if not content.startswith("---"):
        errors.append(make_finding("KB-004", "Malformed YAML frontmatter in TechDebt.md (starts without ---)", file="02_Tasks/TechDebt.md"))

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
                errors.append(make_finding("KB-004", f"In 'TechDebt.md' line {line_no}: invalid tech debt ID '{first_cell}'. "
                    f"Expected format DEBT-XXX (e.g. DEBT-001).", file="02_Tasks/TechDebt.md"))

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
                    errors.append(make_finding("KB-004", f"In 'TechDebt.md' line {line_no}: broken wikilink [[{link_clean}]]", file="02_Tasks/TechDebt.md"))

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
                errors.append(make_finding("KB-004", f"WARN: '{rel_name}' is tagged #techdebt but has no DEBT-XXX reference. "
                    f"Register the debt in TechDebt.md and link it from this document.", file=_docs_rel(md_file, docs_dir), severity="warning"))
            elif not recorded_debt_ids:
                errors.append(make_finding("KB-004", f"WARN: '{rel_name}' references DEBT-XXX but TechDebt.md registry is empty. "
                    f"Register the referenced DEBT-XXX in the Active P3 Debt table.", file=_docs_rel(md_file, docs_dir), severity="warning"))

    return errors


def check_untracked_todos(docs_dir: Path) -> List[Finding]:
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
                    warnings.append(make_finding("KB-009", f"Untracked TODO without ROADMAP-<ID> or DEBT-XXX reference in {rel_name}:{line_no}", file=_docs_rel(file_path, docs_dir)))

    return warnings


def parse_task_dependencies(content: str) -> List[str]:
    """Extracts a list of task/bug IDs from YAML frontmatter 'depends_on' field."""
    if not content.startswith("---"):
        return []
    parts = content.split("---", 2)
    if len(parts) < 3:
        return []
    fm = parts[1]

    m_inline = re.search(r"^\s*depends_on:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    deps: List[str] = []
    if m_inline:
        raw_items = m_inline.group(1).split(",")
        for item in raw_items:
            clean = _clean_task_dep_id(item)
            if clean:
                deps.append(clean)
        return deps

    m_block = re.search(r"^\s*depends_on:\s*\n((?:\s*-\s*[^\n]+\n?)+)", fm, re.MULTILINE)
    if m_block:
        for line in m_block.group(1).splitlines():
            m_item = re.match(r"^\s*-\s*(.+)$", line)
            if m_item:
                clean = _clean_task_dep_id(m_item.group(1))
                if clean:
                    deps.append(clean)
        return deps

    return []


def _clean_task_dep_id(raw: str) -> str:
    cleaned = raw.strip().strip("'\"")
    if cleaned.startswith("[[") and cleaned.endswith("]]"):
        cleaned = cleaned[2:-2].strip()
        if "|" in cleaned:
            cleaned = cleaned.split("|", 1)[0].strip()
    if "/" in cleaned or "\\" in cleaned:
        cleaned = Path(cleaned).stem
    m_id = re.match(r"^((?:TASK|BUG)-[0-9A-Za-z_-]+)", cleaned)
    if m_id:
        return m_id.group(1)
    return cleaned.strip()


def find_dependency_cycles(graph: Dict[str, List[str]]) -> Optional[List[str]]:
    """Detects cycles in directed dependency graph using DFS coloring. Returns cycle path or None."""
    color: Dict[str, int] = {}

    def dfs(node: str, path: List[str]) -> Optional[List[str]]:
        color[node] = 1
        for dep in graph.get(node, []):
            if color.get(dep, 0) == 1:
                idx = path.index(dep) if dep in path else 0
                return path[idx:] + [dep]
            if color.get(dep, 0) == 0:
                cycle = dfs(dep, path + [dep])
                if cycle:
                    return cycle
        color[node] = 2
        return None

    for n in sorted(graph.keys()):
        if color.get(n, 0) == 0:
            c = dfs(n, [n])
            if c:
                return c
    return None


def check_task_dependencies(docs_dir: Path) -> List[Finding]:
    """
    Tier 1 Blocking Quality Gate (KB-010):
    Audits task dependencies (depends_on):
    - Validates that every dependency targets a known TASK-XXX or BUG-XXX.
    - Validates absence of dependency cycles (DFS cycle detection).
    """
    findings: List[Finding] = []
    specs_dir = docs_dir / "02_Tasks" / "Specs"
    if not specs_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Specs").is_dir():
        specs_dir = docs_dir / "docs" / "02_Tasks" / "Specs"
    if not specs_dir.is_dir():
        return findings

    known_ids: Set[str] = set()
    spec_files: List[Tuple[str, Path, str]] = []

    for sf in sorted(specs_dir.rglob("*.md")):
        if sf.name.startswith("TEMPLATE_") or "00_Templates" in sf.parts:
            continue
        try:
            content = sf.read_text(encoding="utf-8")
        except Exception:
            continue

        m = re.search(r"^id:\s*([^\s#]+)", content, re.MULTILINE)
        task_id = m.group(1).strip() if m else sf.stem
        m_canonical = re.match(r"^((?:TASK|BUG)-[0-9A-Za-z_-]+)", task_id)
        canon_id = m_canonical.group(1) if m_canonical else task_id
        known_ids.add(canon_id)
        spec_files.append((canon_id, sf, content))

    bugs_dir = docs_dir / "02_Tasks" / "Bugs"
    if not bugs_dir.is_dir() and (docs_dir / "docs" / "02_Tasks" / "Bugs").is_dir():
        bugs_dir = docs_dir / "docs" / "02_Tasks" / "Bugs"
    if bugs_dir.is_dir():
        for bf in bugs_dir.rglob("*.md"):
            if not bf.name.startswith("TEMPLATE_") and "00_Templates" not in bf.parts:
                m_bug = re.match(r"^(BUG-[0-9A-Za-z_-]+)", bf.stem)
                if m_bug:
                    known_ids.add(m_bug.group(1))

    graph: Dict[str, List[str]] = {}
    task_file_map: Dict[str, str] = {}

    for task_id, sf, content in spec_files:
        rel_path = _docs_rel(sf, docs_dir)
        task_file_map[task_id] = rel_path

        deps = parse_task_dependencies(content)
        valid_deps: List[str] = []
        for dep in deps:
            if dep not in known_ids:
                findings.append(
                    make_finding(
                        "KB-010",
                        f"Task '{task_id}' depends on unknown task '{dep}'",
                        file=rel_path,
                    )
                )
            else:
                valid_deps.append(dep)
        graph[task_id] = valid_deps

    cycle = find_dependency_cycles(graph)
    if cycle:
        cycle_head = cycle[0]
        file_loc = task_file_map.get(cycle_head, "02_Tasks/Specs")
        cycle_str = " -> ".join(cycle)
        findings.append(
            make_finding(
                "KB-010",
                f"Task dependency cycle detected: {cycle_str}",
                file=file_loc,
            )
        )

    return findings


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


# Порядок секций silent-вывода (легаси-контракт: совпадает с допереходным выводом).
_TEXT_WARNING_ORDER = (
    "KB-011", "KB-008", "KB-012", "KB-006", "KB-007",
    "KB-014", "KB-015", "KB-005", "KB-004", "KB-013", "KB-009",
)
# Правила, чей silent-вывод исторически печатался без префикса "WARN:".
_TEXT_SILENT_PLAIN = ("KB-015", "KB-005")
# Правила, чьё сообщение само может начинаться с "WARN:" (легаси-формат сохранён дословно).
_TEXT_WARN_INSIDE = ("KB-007", "KB-014", "KB-004", "KB-013")


def _silent_warning_line(finding: Finding) -> str:
    if finding.rule_id in _TEXT_SILENT_PLAIN:
        return "⚠️  %s" % finding.message
    if finding.rule_id in _TEXT_WARN_INSIDE and finding.message.startswith("WARN:"):
        return "⚠️  %s" % finding.message
    return "⚠️  WARN: %s" % finding.message


def render_text(report: LintReport, verbose: bool) -> str:
    """Воспроизводит прежний человекочитаемый вывод байт-в-байт."""
    lines: List[str] = []
    broken = report.by_rule("KB-001")
    frontmatter = report.by_rule("KB-002")
    memory_errors = report.by_rule("KB-003")
    debt_errors = report.by_rule("KB-004", "error")

    if verbose:
        lines.append("📊 Total Markdown Files Scanned: %d" % report.files)
        lines.append("🔗 Total Wikilinks Validated: %d" % report.wikilinks)
        lines.append("")
        if broken:
            lines.append("❌ Broken Wikilinks Detected (%d):" % len(broken))
            lines.extend("   • " + f.message for f in broken)
            lines.append("")
        else:
            lines.append("✅ No broken wikilinks found!")
            lines.append("")
        if frontmatter:
            lines.append("⚠️ Frontmatter / Property Warnings (%d):" % len(frontmatter))
            lines.extend("   • " + f.file + ": " + f.message for f in frontmatter)
            lines.append("")
        else:
            lines.append("✅ All inspected task/spec/plan files have valid YAML frontmatter!")
            lines.append("")
        sections = (
            ("❌ Memory Limit Errors", memory_errors),
            ("⚠️ Memory Consistency Warnings", report.by_rule("KB-013")),
            ("⚠️ Spec Drift Warnings", report.by_rule("KB-011")),
            ("⚠️ Devlog Semantic Guard Warnings", report.by_rule("KB-008")),
            ("⚠️ Fast-Track Guard Warnings", report.by_rule("KB-012")),
            ("⚠️ Phase Consistency Warnings", report.by_rule("KB-006")),
            ("⚠️ Research Basis Warnings", report.by_rule("KB-007")),
            ("⚠️ Symbolic Scope Warnings", report.by_rule("KB-014")),
            ("⚠️ Asset Weight Warnings", report.by_rule("KB-015")),
            ("⚠️ Asset Layout Warnings", report.by_rule("KB-005")),
            ("⚠️ Tech Debt Warnings", report.by_rule("KB-004", "warning")),
            ("❌ Tech Debt Integrity Errors", debt_errors),
            ("⚠️ Untracked TODO Warnings", report.by_rule("KB-009")),
        )
        for title, items in sections:
            if not items:
                continue
            lines.append("%s (%d):" % (title, len(items)))
            lines.extend("   • " + f.message for f in items)
            lines.append("")
        if report.has_errors():
            lines.append("❌ Linter failed: please resolve errors.")
        else:
            lines.append("🎉 Knowledge base is healthy and consistent!")
        return "\n".join(lines) + "\n"

    for rule_id in _TEXT_WARNING_ORDER:
        for finding in report.by_rule(rule_id, "warning"):
            lines.append(_silent_warning_line(finding))
    if not report.has_errors():
        lines.append(
            "OK: %d files scanned, %d wikilinks verified (0 broken)." % (report.files, report.wikilinks)
        )
        return "\n".join(lines) + "\n"
    lines.append(
        "ERROR: %d broken links, %d frontmatter warnings, %d memory errors, %d tech debt errors."
        % (len(broken), len(frontmatter), len(memory_errors), len(debt_errors))
    )
    lines.extend("   • " + f.message for f in broken)
    lines.extend("   • " + f.file + ": " + f.message for f in frontmatter)
    lines.extend("   • " + f.message for f in memory_errors)
    lines.extend("   • " + f.message for f in debt_errors)
    return "\n".join(lines) + "\n"


def _finding_payload(finding: Finding, include_fix: bool = False) -> dict:
    payload = {
        "rule_id": finding.rule_id,
        "severity": finding.severity,
        "file": finding.file or None,
        "location": finding.location or None,
        "message": finding.message,
    }
    if include_fix:
        payload["fixable"] = getattr(finding, "fixable", False)
    return payload


def render_json(
    report: LintReport,
    fix_results: Optional[List[FixResult]] = None,
    include_fix: bool = False,
) -> str:
    """Machine-readable contract: schema version, summary counters, findings by severity."""
    errors = sorted(report.by_rule_severity("error"), key=lambda f: (f.rule_id, f.file, f.message))
    warnings = sorted(report.by_rule_severity("warning"), key=lambda f: (f.rule_id, f.file, f.message))
    with_fix = include_fix or (fix_results is not None)

    summary = {
        "files": report.files,
        "wikilinks": report.wikilinks,
        "errors": len(errors),
        "warnings": len(warnings),
    }
    if with_fix:
        summary["fixable"] = sum(1 for f in report.findings if getattr(f, "fixable", False))

    payload = {
        "version": RULESET_VERSION,
        "summary": summary,
        "errors": [_finding_payload(f, include_fix=with_fix) for f in errors],
        "warnings": [_finding_payload(f, include_fix=with_fix) for f in warnings],
    }

    if with_fix and fix_results is not None:
        all_fixes = []
        for r in fix_results:
            for fix in r.fixes:
                all_fixes.append({
                    "rule_id": fix.rule_id,
                    "file": str(fix.file_path.as_posix() if hasattr(fix.file_path, "as_posix") else fix.file_path),
                    "line": fix.line_number,
                    "description": fix.description,
                    "original": fix.original_text,
                    "replacement": fix.replacement_text,
                })
        payload["fixes"] = all_fixes

    return json.dumps(payload, indent=2, ensure_ascii=False)


def render_sarif(
    report: LintReport,
    fix_results: Optional[List[FixResult]] = None,
    include_fix: bool = False,
) -> str:
    """Minimal valid SARIF 2.1.0 document (no line regions, no project-origin metadata)."""
    with_fix = include_fix or (fix_results is not None)
    used_rules: List[str] = []
    for finding in report.findings:
        if finding.rule_id not in used_rules:
            used_rules.append(finding.rule_id)
    rules = [{"id": rid, "shortDescription": {"text": RULES[rid]}} for rid in sorted(used_rules)]

    ordered = sorted(report.findings, key=lambda f: (f.severity != "error", f.rule_id, f.file, f.message))
    results = []
    for finding in ordered:
        result = {
            "ruleId": finding.rule_id,
            "level": "error" if finding.severity == "error" else "warning",
            "message": {"text": finding.message},
        }
        if finding.file:
            result["locations"] = [{"physicalLocation": {"artifactLocation": {"uri": finding.location or finding.file}}}]
        if with_fix and getattr(finding, "fixable", False):
            result["fixes"] = [
                {
                    "description": {
                        "text": "Deterministic autofix available via 'kb_lint.py --fix --write'"
                    }
                }
            ]
        results.append(result)

    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "kb_lint",
                        "version": str(RULESET_VERSION),
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def run_linter(
    docs_dir: Path,
    verbose: bool = False,
    output_format: str = "text",
    fix: bool = False,
    write: bool = False,
    allow_dirty: bool = False,
) -> int:
    if verbose and output_format == "text":
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

    fix_results: Optional[List[FixResult]] = None
    if fix:
        fix_results = []
        for f in all_md_files:
            try:
                content = f.read_text(encoding="utf-8")
            except Exception:
                continue
            res = generate_file_fixes(content, f)
            if res.has_changes:
                fix_results.append(res)

        applied_files = 0
        applied_fixes = 0
        skipped_files = 0

        if write:
            for res in fix_results:
                if not allow_dirty and not git_check_clean(res.file_path):
                    if output_format == "text":
                        sys.stdout.write(
                            "WARNING: Skipping %s (has uncommitted changes in git. Use --allow-dirty to overwrite).\n"
                            % res.file_path.name
                        )
                    skipped_files += 1
                    continue
                atomic_write_file(res.file_path, res.modified_content)
                applied_files += 1
                applied_fixes += len(res.fixes)

        if output_format == "text":
            use_color = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
            for res in fix_results:
                diff_str = render_diff(res.diff_lines, use_color=use_color)
                if diff_str:
                    sys.stdout.write(diff_str + "\n")

            total_fixes = sum(len(r.fixes) for r in fix_results)
            if not write:
                if fix_results:
                    sys.stdout.write(
                        "[DRY-RUN] Found %d fixable issue(s) in %d file(s). Run with '--fix --write' to apply.\n"
                        % (total_fixes, len(fix_results))
                    )
                else:
                    sys.stdout.write("[DRY-RUN] No fixable issues found.\n")
            else:
                if applied_files > 0:
                    sys.stdout.write(
                        "[FIXED] Successfully applied %d fix(es) in %d file(s).\n"
                        % (applied_fixes, applied_files)
                    )
                elif skipped_files > 0:
                    sys.stdout.write(
                        "[FIXED] All %d fixable file(s) were skipped due to uncommitted git changes.\n"
                        % skipped_files
                    )
                else:
                    sys.stdout.write("[FIXED] No fixable issues found.\n")

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

    findings: List[Finding] = []
    findings.extend(
        make_finding("KB-001", "In '%s' -> target not found: [[%s]]" % (src, target), file=src)
        for src, target in broken_links
    )
    findings.extend(make_finding("KB-002", msg, file=src) for src, msg in frontmatter_warnings)
    findings.extend(check_spec_drift(docs_dir))
    findings.extend(check_devlog_semantic_guard(docs_dir))
    findings.extend(check_fast_track_specs(docs_dir))
    findings.extend(check_phase_consistency(docs_dir))
    findings.extend(check_research_basis(docs_dir))
    findings.extend(check_symbolic_scope(docs_dir))
    findings.extend(check_memory_limits(docs_dir))
    findings.extend(check_memory_consistency(docs_dir))
    findings.extend(check_asset_weights(docs_dir))
    findings.extend(check_asset_layout(docs_dir))

    debt_results = check_tech_debt_integrity(docs_dir, file_map=file_map)
    has_tasks_harness = (
        (docs_dir / "02_Tasks" / "Kanban.md").is_file()
        or (docs_dir / "02_Tasks" / "Roadmap.md").is_file()
        or (docs_dir / "docs" / "02_Tasks" / "Kanban.md").is_file()
        or (docs_dir / "docs" / "02_Tasks" / "Roadmap.md").is_file()
    )
    findings.extend(f for f in debt_results if f.severity == "error")
    findings.extend(
        f for f in debt_results
        if f.severity == "warning"
        and (not f.message.startswith("Tech debt registry not found") or has_tasks_harness)
    )
    findings.extend(check_untracked_todos(docs_dir))
    findings.extend(check_task_dependencies(docs_dir))
    findings.extend(check_deep_risk_tags(docs_dir))

    for finding in findings:
        finding.location = resolve_location(finding.file, docs_dir)

    report = LintReport(files=len(all_md_files), wikilinks=checked_links_count, findings=findings)

    if output_format == "json":
        sys.stdout.write(render_json(report, fix_results=fix_results if fix else None, include_fix=fix) + "\n")
    elif output_format == "sarif":
        sys.stdout.write(render_sarif(report, fix_results=fix_results if fix else None, include_fix=fix) + "\n")
    else:
        sys.stdout.write(render_text(report, verbose))
    return 1 if report.has_errors() else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docs-as-Code Knowledge Base Linter")
    parser.add_argument("--path", "-p", type=str, default=".", help="Path to docs directory or project root")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose audit output")
    parser.add_argument(
        "--format", "-f",
        dest="output_format",
        choices=["text", "json", "sarif"],
        default="text",
        help="Output format: text (default), json (machine-readable), sarif (SARIF 2.1.0)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Analyze and preview safe autofixes (dry-run by default)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply autofixes to files on disk (use with --fix)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly run in dry-run preview mode (default behavior of --fix)",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow autofixing files with uncommitted git modifications",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="kb_lint %d" % RULESET_VERSION,
        help="Print the rule-set version and exit",
    )
    args = parser.parse_args()

    start = Path(args.path).resolve()
    if (start / "docs").is_dir():
        vault = start / "docs"
    elif start.name == "docs" and start.is_dir():
        vault = start
    else:
        vault = find_vault_root(start)

    effective_write = bool(args.write and not args.dry_run)
    exit_code = run_linter(
        vault,
        verbose=args.verbose,
        output_format=args.output_format,
        fix=args.fix,
        write=effective_write,
        allow_dirty=args.allow_dirty,
    )
    sys.exit(exit_code)
