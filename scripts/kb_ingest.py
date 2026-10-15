#!/usr/bin/env python3
"""
scripts/kb_ingest.py — Multi-Channel Feedback Ingestion Engine for Docs-as-Code.
Imports external feedback (GitHub Issues, Email IMAP, Quick Paste) into docs/02_Tasks/Inbox/.
Zero external dependencies (uses standard Python 3 library only).
"""

import sys
import os
import re
import json
import hashlib
import datetime
import argparse
import subprocess
import urllib.request
import urllib.error
import imaplib
import email
from email.header import decode_header
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def detect_github_repo(repo_root: Optional[Path] = None) -> Optional[str]:
    """
    Zero-dependencies detection of GitHub owner/repo from git config remote.origin.url.
    Supports HTTPS, SSH, and personal access token URL schemes:
      - https://github.com/owner/repo.git
      - https://github.com/owner/repo
      - git@github.com:owner/repo.git
      - https://x-access-token:...@github.com/owner/repo.git
    Returns 'owner/repo' or None.
    """
    env_repo = os.environ.get("GITHUB_REPOSITORY")
    if env_repo:
        return env_repo.strip()

    try:
        cmd = ["git", "config", "--get", "remote.origin.url"]
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            cwd=str(repo_root) if repo_root else None
        )
        if res.returncode != 0 or not res.stdout:
            return None
        url = res.stdout.strip()
        pattern = r'(?:git@github\.com:|https://(?:[^@]+@)?github\.com/)([\w.-]+)/([\w.-]+?)(?:\.git)?$'
        m = re.search(pattern, url)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
        return None
    except Exception:
        return None


def find_inbox_dir(start_dir: Path) -> Path:
    """Finds or resolves the docs/02_Tasks/Inbox directory."""
    cur = start_dir.resolve()
    while cur != cur.parent:
        candidate = cur / "docs" / "02_Tasks" / "Inbox"
        if candidate.is_dir():
            return candidate
        candidate2 = cur / "02_Tasks" / "Inbox"
        if candidate2.is_dir():
            return candidate2
        cur = cur.parent
    # Fallback to local relative
    return (start_dir / "docs" / "02_Tasks" / "Inbox").resolve()


def load_env_local(repo_root: Path):
    """Loads key-value pairs from .env.local if present, without overwriting existing env."""
    env_file = repo_root / ".env.local"
    if not env_file.is_file():
        return
    try:
        lines = env_file.read_text(encoding="utf-8").splitlines()
        for line in lines:
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


class InboxStateManager:
    """Manages offset cursor and deduplication in .inbox_state.json."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.data = {
            "version": 1,
            "github": {"last_issue_number": 0, "processed_ids": []},
            "email": {"last_uid": 0, "processed_message_ids": []},
            "paste": {"processed_hashes": []}
        }
        self.load()

    def load(self):
        if self.state_file.is_file():
            try:
                loaded = json.loads(self.state_file.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    self.data.update(loaded)
            except Exception:
                pass

    def save(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def is_github_processed(self, issue_num: int) -> bool:
        gh_data = self.data.setdefault("github", {})
        processed_ids = gh_data.setdefault("processed_ids", [])
        return issue_num in processed_ids

    def mark_github_processed(self, issue_num: int):
        gh_data = self.data.setdefault("github", {})
        processed_ids = gh_data.setdefault("processed_ids", [])
        if issue_num not in processed_ids:
            processed_ids.append(issue_num)
        if issue_num > gh_data.get("last_issue_number", 0):
            gh_data["last_issue_number"] = issue_num

    def is_email_processed(self, message_id: str, uid: int = 0) -> bool:
        em_data = self.data.setdefault("email", {})
        processed_mids = em_data.setdefault("processed_message_ids", [])
        if message_id and message_id in processed_mids:
            return True
        last_uid = em_data.get("last_uid", 0)
        if uid > 0 and uid <= last_uid:
            return True
        return False

    def mark_email_processed(self, message_id: str, uid: int = 0):
        em_data = self.data.setdefault("email", {})
        processed_mids = em_data.setdefault("processed_message_ids", [])
        if message_id and message_id not in processed_mids:
            processed_mids.append(message_id)
        if uid > em_data.get("last_uid", 0):
            em_data["last_uid"] = uid

    def is_content_processed(self, content_hash: str) -> bool:
        p_data = self.data.setdefault("paste", {})
        hashes = p_data.setdefault("processed_hashes", [])
        return content_hash in hashes

    def mark_content_processed(self, content_hash: str):
        p_data = self.data.setdefault("paste", {})
        hashes = p_data.setdefault("processed_hashes", [])
        if content_hash not in hashes:
            hashes.append(content_hash)


def clean_markdown_text(text: str) -> str:
    """Sanitizes text for markdown inclusion."""
    if not text:
        return ""
    # Normalize line endings
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def build_feedback_markdown(
    fb_id: str,
    title: str,
    channel: str,
    body: str,
    author: str = "",
    source_ref: str = "",
    created_date: str = "",
    perceived_severity: str = "s2"
) -> str:
    today = created_date or datetime.date.today().isoformat()
    return f"""---
id: {fb_id}
title: "{title}"
status: new
type: feedback
channel: {channel}
perceived_severity: {perceived_severity}
target: ""
created: {today}
updated: {today}
author: "{author}"
source_ref: "{source_ref}"
tags:
  - feedback
  - inbox
---

# 📥 Обращение: {fb_id} — {title}

> **Источник:** {channel.capitalize()} ({source_ref or 'Direct'}) | **Статус:** new  
> **Целевой артефакт:**   

---

## 1. Исходное сообщение
{body}

## 2. Анализ и предварительный скрининг
<!-- Тип: Дефект / Идея / Вопрос / Спам -->
<!-- Воспринимаемая тяжесть и контекст окружения -->

## 3. Решение по триажу
<!-- Итог разбора: Конвертировано в BUG-XXX / Добавлено в Roadmap Icebox / Ответ пользователю / Отклонено -->
"""


class GitHubIngestDriver:
    """Fetches GitHub Issues via REST API v3 using urllib.request."""

    def __init__(self, repo: str = None, token: str = None, repo_root: Path = None):
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY", "") or (detect_github_repo(repo_root) or "")
        self.token = token or os.environ.get("GITHUB_TOKEN", "")

    def fetch_issues(self, label: str = "needs-triage", all_open: bool = False) -> list:
        if not self.repo:
            return []
        if all_open:
            url = f"https://api.github.com/repos/{self.repo}/issues?state=open&per_page=100"
        else:
            url = f"https://api.github.com/repos/{self.repo}/issues?state=open&labels={label}&per_page=100"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "agent-docs-harness/kb_ingest")
        req.add_header("Accept", "application/vnd.github.v3+json")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                # Filter out PRs if returned by issues API
                return [i for i in data if "pull_request" not in i]
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("❌ Ошибка GitHub API: Неверный или просроченный GITHUB_TOKEN (HTTP 401 Unauthorized).", file=sys.stderr)
            elif e.code == 403:
                print("❌ Ошибка GitHub API: Превышен лимит запросов API (HTTP 403 Forbidden). Используйте GITHUB_TOKEN или дождитесь сброса лимита.", file=sys.stderr)
            elif e.code == 404:
                print(f"❌ Ошибка GitHub API: Репозиторий '{self.repo}' не найден или является приватным (HTTP 404 Not Found).", file=sys.stderr)
            else:
                print(f"❌ Ошибка GitHub API: HTTP {e.code} ({e.reason}).", file=sys.stderr)
            return []
        except Exception as e:
            print(f"⚠️ GitHub Ingest Error ({self.repo}): {e}", file=sys.stderr)
            return []


def render_status_dashboard(inbox_dir: Path, repo_root: Path) -> int:
    """Renders the diagnostic status dashboard for feedback ingestion channels."""
    state_file = inbox_dir / ".inbox_state.json"
    state = InboxStateManager(state_file)

    # 1. GitHub
    env_repo = os.environ.get("GITHUB_REPOSITORY")
    if env_repo:
        repo_val = env_repo.strip()
        source_val = "env"
    else:
        detected = detect_github_repo(repo_root)
        if detected:
            repo_val = detected
            source_val = "auto-detect"
        else:
            repo_val = "None"
            source_val = "not-found"

    token = os.environ.get("GITHUB_TOKEN", "")
    auth_val = "Token configured" if token else "Anonymous (rate-limited)"

    # Rate limit check
    quota_str = "unknown/unknown req/h (Сброс: N/A)"
    try:
        req = urllib.request.Request("https://api.github.com/rate_limit")
        req.add_header("User-Agent", "agent-docs-harness/kb_ingest")
        req.add_header("Accept", "application/vnd.github.v3+json")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            rl_data = json.loads(resp.read().decode("utf-8"))
            rate = rl_data.get("rate") or rl_data.get("resources", {}).get("core", {})
            rem = rate.get("remaining", "unknown")
            lim = rate.get("limit", "unknown")
            reset_ts = rate.get("reset")
            if reset_ts:
                reset_time = datetime.datetime.fromtimestamp(reset_ts).strftime("%Y-%m-%d %H:%M:%S")
            else:
                reset_time = "N/A"
            quota_str = f"{rem}/{lim} req/h (Сброс: {reset_time})"
    except Exception:
        pass

    default_label = "needs-triage"
    gh_state = state.data.get("github", {})
    last_issue = gh_state.get("last_issue_number", 0)
    gh_count = len(gh_state.get("processed_ids", []))

    # 2. Email
    imap_host = os.environ.get("FEEDBACK_IMAP_HOST", "")
    imap_user = os.environ.get("FEEDBACK_IMAP_USER", "")
    if imap_host and imap_user:
        email_cfg = "configured"
        host_val = imap_host
        user_val = imap_user
    else:
        email_cfg = "not-configured"
        host_val = imap_host or "None"
        user_val = imap_user or "None"

    email_state = state.data.get("email", {})
    last_uid = email_state.get("last_uid", 0)
    email_count = len(email_state.get("processed_message_ids", []))

    # 3. Inbox
    total_tickets = 0
    new_count = 0
    proc_count = 0
    rej_count = 0

    if inbox_dir.is_dir():
        for f in inbox_dir.glob("FB-*.md"):
            total_tickets += 1
            try:
                text = f.read_text(encoding="utf-8")
                m = re.search(r"^status:\s*([a-zA-Z_-]+)", text, re.MULTILINE)
                if m:
                    st = m.group(1).lower()
                    if st == "new":
                        new_count += 1
                    elif st == "processed":
                        proc_count += 1
                    elif st == "rejected":
                        rej_count += 1
            except Exception:
                pass

    print("======================================================================")
    print("📊 Docs-as-Code Feedback Ingestion Status Dashboard")
    print("======================================================================")
    print("[Канал: GitHub Issues]")
    print(f"  • Репозиторий:        {repo_val} ({source_val})")
    print(f"  • Авторизация:        {auth_val}")
    print(f"  • Квота API:          {quota_str}")
    print(f"  • Фильтр по умолчанию: --label {default_label}")
    print(f"  • Курсор смещения:    last_issue_number={last_issue}, processed={gh_count}")
    print()
    print("[Канал: Email (IMAP)]")
    print(f"  • Хост / Пользователь: {host_val} / {user_val} ({email_cfg})")
    print(f"  • Курсор смещения:    last_uid={last_uid}, processed={email_count}")
    print()
    print("[Буфер обращений: docs/02_Tasks/Inbox/]")
    print(f"  • Всего тикетов:      {total_tickets}")
    print(f"  • Статусы:            new: {new_count} | processed: {proc_count} | rejected: {rej_count}")
    print("======================================================================")
    return 0


class EmailIngestDriver:
    """Fetches incoming feedback emails over IMAP SSL using imaplib & email."""

    def __init__(self, host: str, user: str, password: str, folder: str = "INBOX"):
        self.host = host
        self.user = user
        self.password = password
        self.folder = folder

    def decode_mime_header(self, val: str) -> str:
        if not val:
            return ""
        decoded_parts = decode_header(val)
        res = []
        for part, enc in decoded_parts:
            if isinstance(part, bytes):
                res.append(part.decode(enc or "utf-8", errors="replace"))
            else:
                res.append(str(part))
        return "".join(res)

    def extract_body(self, msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdisp = str(part.get("Content-Disposition", ""))
                if ctype == "text/plain" and "attachment" not in cdisp:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        return payload.decode(charset, errors="replace")
            # Fallback to any text part
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        return payload.decode(charset, errors="replace")
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
        return ""

    def fetch_emails(self) -> list:
        if not self.host or not self.user or not self.password:
            return []

        results = []
        try:
            client = imaplib.IMAP4_SSL(self.host, timeout=10)
            client.login(self.user, self.password)
            client.select(self.folder)

            typ, data = client.search(None, "UNSEEN")
            if typ != "OK" or not data or not data[0]:
                client.logout()
                return []

            msg_ids = data[0].split()
            for mid in msg_ids:
                typ, fetch_data = client.fetch(mid, "(RFC822)")
                if typ != "OK":
                    continue
                raw_email = fetch_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = self.decode_mime_header(msg.get("Subject", "No Subject"))
                sender = self.decode_mime_header(msg.get("From", "Unknown"))
                date_str = msg.get("Date", "")
                message_id = msg.get("Message-ID", f"{mid.decode()}-{hashlib.sha256(raw_email).hexdigest()[:8]}")
                body = self.extract_body(msg)

                try:
                    uid_val = int(mid)
                except Exception:
                    uid_val = 0

                results.append({
                    "uid": uid_val,
                    "message_id": message_id.strip(),
                    "subject": subject.strip(),
                    "sender": sender.strip(),
                    "date": date_str,
                    "body": clean_markdown_text(body)
                })

            client.logout()
        except Exception as e:
            print(f"⚠️ Email Ingest Error ({self.host}): {e}", file=sys.stderr)

        return results


def ingest_quick_paste(
    text: str,
    title: str,
    author: str,
    inbox_dir: Path,
    state: InboxStateManager,
    dry_run: bool = False
) -> tuple:
    """Ingests a direct snippet/paste with hash deduplication."""
    clean_body = clean_markdown_text(text)
    if not clean_body:
        return False, "Empty content, skipping."

    content_hash = hashlib.sha256(f"{title}\n{clean_body}".encode("utf-8")).hexdigest()
    if state.is_content_processed(content_hash):
        return False, f"Duplicate content detected (hash: {content_hash[:8]}), skipped."

    today_str = datetime.date.today().strftime("%Y%m%d")
    short_hash = content_hash[:8]
    filename = f"FB-PASTE-{today_str}-{short_hash}.md"
    file_path = inbox_dir / filename

    content = build_feedback_markdown(
        fb_id=f"FB-PASTE-{today_str}-{short_hash}",
        title=title or f"Snippet {short_hash}",
        channel="paste",
        body=clean_body,
        author=author or "User",
        source_ref=f"hash:{short_hash}"
    )

    if not dry_run:
        file_path.write_text(content, encoding="utf-8")
        state.mark_content_processed(content_hash)
        state.save()

    return True, filename


def run_ingest(
    inbox_dir: Path,
    github: bool = False,
    email_mode: bool = False,
    paste_data: dict = None,
    dry_run: bool = False,
    verbose: bool = False,
    github_repo: str = None,
    github_token: str = None,
    label: str = "needs-triage",
    all_open: bool = False,
    repo_root: Path = None
) -> int:
    """Main orchestration entry point."""
    inbox_dir.mkdir(parents=True, exist_ok=True)
    state_file = inbox_dir / ".inbox_state.json"
    state = InboxStateManager(state_file)

    created_count = 0
    skipped_count = 0

    # 1. Quick Paste
    if paste_data and paste_data.get("text"):
        ok, msg = ingest_quick_paste(
            text=paste_data.get("text"),
            title=paste_data.get("title", "Quick Feedback"),
            author=paste_data.get("author", "User"),
            inbox_dir=inbox_dir,
            state=state,
            dry_run=dry_run
        )
        if ok:
            created_count += 1
            if verbose:
                print(f"✅ Ingested Paste: {msg}")
        else:
            skipped_count += 1
            if verbose:
                print(f"ℹ️ {msg}")

    # 2. GitHub Issues
    if github:
        repo = github_repo or os.environ.get("GITHUB_REPOSITORY") or detect_github_repo(repo_root)
        if not repo:
            print("⚠️ Warning: Канал GitHub пропущен: репозиторий не найден. Убедитесь, что настроен git remote origin или задана переменная GITHUB_REPOSITORY.")
        else:
            token = github_token or os.environ.get("GITHUB_TOKEN", "")
            if not token:
                print("ℹ️ Info: GitHub опрашивается анонимно (лимит 60 req/h). Для лимита 5000 req/h настройте GITHUB_TOKEN в .env.local или переменных среды.")
            driver = GitHubIngestDriver(repo=repo, token=token)
            issues = driver.fetch_issues(label=label, all_open=all_open)
            for issue in issues:
                num = issue.get("number")
                if not num:
                    continue
                if state.is_github_processed(num):
                    skipped_count += 1
                    continue

                title = issue.get("title", f"Issue #{num}")
                body = issue.get("body", "")
                user = issue.get("user", {}).get("login", "")
                html_url = issue.get("html_url", "")
                created_at = issue.get("created_at", "")[:10]

                fb_id = f"FB-GH-{num}"
                filename = f"{fb_id}.md"
                file_path = inbox_dir / filename

                md_content = build_feedback_markdown(
                    fb_id=fb_id,
                    title=title,
                    channel="github",
                    body=clean_markdown_text(body),
                    author=user,
                    source_ref=html_url or f"#{num}",
                    created_date=created_at
                )

                if not dry_run:
                    file_path.write_text(md_content, encoding="utf-8")
                    state.mark_github_processed(num)
                    state.save()

                created_count += 1
                if verbose:
                    print(f"✅ Ingested GitHub Issue: {filename}")

    # 3. Email (IMAP)
    if email_mode:
        imap_host = os.environ.get("FEEDBACK_IMAP_HOST", "")
        imap_user = os.environ.get("FEEDBACK_IMAP_USER", "")
        imap_pass = os.environ.get("FEEDBACK_IMAP_PASS", "")
        if not imap_host or not imap_user:
            print("⚠️ Warning: Канал Email пропущен: не настроены переменные FEEDBACK_IMAP_HOST / FEEDBACK_IMAP_USER.")
        elif not imap_pass:
            print("⚠️ Warning: Канал Email пропущен: не настроена переменная FEEDBACK_IMAP_PASS.")
        else:
            driver = EmailIngestDriver(host=imap_host, user=imap_user, password=imap_pass)
            messages = driver.fetch_emails()
            for msg in messages:
                mid = msg.get("message_id")
                uid = msg.get("uid", 0)
                if state.is_email_processed(mid, uid):
                    skipped_count += 1
                    continue

                today_str = datetime.date.today().strftime("%Y%m%d")
                short_hash = hashlib.sha256(mid.encode("utf-8")).hexdigest()[:8]
                fb_id = f"FB-MAIL-{today_str}-{short_hash}"
                filename = f"{fb_id}.md"
                file_path = inbox_dir / filename

                md_content = build_feedback_markdown(
                    fb_id=fb_id,
                    title=msg.get("subject") or "Feedback Email",
                    channel="email",
                    body=msg.get("body") or "",
                    author=msg.get("sender") or "",
                    source_ref=mid
                )

                if not dry_run:
                    file_path.write_text(md_content, encoding="utf-8")
                    state.mark_email_processed(mid, uid)
                    state.save()

                created_count += 1
                if verbose:
                    print(f"✅ Ingested Email: {filename}")

    if not dry_run:
        state.save()

    if verbose or created_count > 0:
        print(f"OK: Ingest completed. Created: {created_count}, Skipped (deduplicated): {skipped_count}.")
    else:
        print(f"OK: Ingest checked (0 new items, {skipped_count} skipped).")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Multi-Channel Feedback Ingestion Engine (Zero-Dependencies)")
    parser.add_argument("--github", action="store_true", help="Ingest issues from GitHub repository")
    parser.add_argument("--email", action="store_true", help="Ingest incoming feedback via IMAP")
    parser.add_argument("--paste", nargs="?", const=True, default=None, help="Ingest quick snippet/paste from arguments or stdin")
    parser.add_argument("--all", action="store_true", help="Run all available channels (GitHub + Email)")
    parser.add_argument("--title", type=str, default="", help="Title for pasted feedback")
    parser.add_argument("--text", type=str, default="", help="Text content for pasted feedback")
    parser.add_argument("--author", type=str, default="", help="Author identifier for feedback")
    parser.add_argument("--inbox-dir", type=str, default="", help="Explicit path to Inbox directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate ingestion without writing files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging output")
    parser.add_argument("--status", action="store_true", help="Display feedback ingestion status dashboard")
    parser.add_argument("--label", type=str, default="needs-triage", help="GitHub label filter (default: needs-triage)")
    parser.add_argument("--all-open", action="store_true", help="Fetch all open GitHub issues (ignoring labels)")

    args = parser.parse_args()

    # Load local env if present
    repo_root = Path.cwd()
    load_env_local(repo_root)

    inbox_dir = Path(args.inbox_dir) if args.inbox_dir else find_inbox_dir(repo_root)

    if args.status:
        sys.exit(render_status_dashboard(inbox_dir=inbox_dir, repo_root=repo_root))

    paste_data = None
    if args.paste is not None or args.text:
        text_content = args.text
        if not text_content and isinstance(args.paste, str):
            text_content = args.paste
        if not text_content and not sys.stdin.isatty():
            try:
                text_content = sys.stdin.read()
            except Exception:
                pass
        paste_data = {
            "text": text_content,
            "title": args.title,
            "author": args.author
        }

    do_github = args.github or args.all
    do_email = args.email or args.all

    if not do_github and not do_email and not paste_data:
        # Default behavior: run quick check or report status
        do_github = bool(os.environ.get("GITHUB_REPOSITORY") or detect_github_repo(repo_root))
        do_email = bool(os.environ.get("FEEDBACK_IMAP_HOST"))

    sys.exit(run_ingest(
        inbox_dir=inbox_dir,
        github=do_github,
        email_mode=do_email,
        paste_data=paste_data,
        dry_run=args.dry_run,
        verbose=args.verbose,
        label=args.label,
        all_open=args.all_open,
        repo_root=repo_root
    ))


if __name__ == "__main__":
    main()
