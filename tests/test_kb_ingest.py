#!/usr/bin/env python3
"""
Unit tests for scripts/kb_ingest.py (Feedback Ingestion Engine).
Tests deduplication, state persistence, Quick Paste, GitHub Driver, and Email Driver.
"""

import sys
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import kb_ingest


class TestKbIngest(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.inbox_dir = self.temp_dir / "docs" / "02_Tasks" / "Inbox"
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.inbox_dir / ".inbox_state.json"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_inbox_state_manager_deduplication(self):
        """Test cursor tracking and deduplication for github, email, and paste."""
        state = kb_ingest.InboxStateManager(self.state_file)

        # 1. GitHub
        self.assertFalse(state.is_github_processed(101))
        state.mark_github_processed(101)
        self.assertTrue(state.is_github_processed(101))
        self.assertEqual(state.data["github"]["last_issue_number"], 101)

        # 2. Email
        self.assertFalse(state.is_email_processed("msg-001@example.com", uid=5))
        state.mark_email_processed("msg-001@example.com", uid=5)
        self.assertTrue(state.is_email_processed("msg-001@example.com", uid=5))
        self.assertTrue(state.is_email_processed("other@example.com", uid=4))  # uid <= last_uid

        # 3. Paste
        content_hash = "abc12345"
        self.assertFalse(state.is_content_processed(content_hash))
        state.mark_content_processed(content_hash)
        self.assertTrue(state.is_content_processed(content_hash))

        # Save and reload in new instance
        state.save()
        new_state = kb_ingest.InboxStateManager(self.state_file)
        self.assertTrue(new_state.is_github_processed(101))
        self.assertTrue(new_state.is_email_processed("msg-001@example.com"))
        self.assertTrue(new_state.is_content_processed(content_hash))

    def test_quick_paste_ingestion(self):
        """Test ingestion of pasted text snippet and hash deduplication."""
        state = kb_ingest.InboxStateManager(self.state_file)

        ok, filename = kb_ingest.ingest_quick_paste(
            text="App crashes on button click.",
            title="Crash bug",
            author="UserAlice",
            inbox_dir=self.inbox_dir,
            state=state,
            dry_run=False
        )
        self.assertTrue(ok)
        created_file = self.inbox_dir / filename
        self.assertTrue(created_file.is_file())

        content = created_file.read_text(encoding="utf-8")
        self.assertIn("title: \"Crash bug\"", content)
        self.assertIn("channel: paste", content)
        self.assertIn("author: \"UserAlice\"", content)
        self.assertIn("App crashes on button click.", content)

        # Second attempt with exact same content must be skipped
        ok2, msg2 = kb_ingest.ingest_quick_paste(
            text="App crashes on button click.",
            title="Crash bug",
            author="UserAlice",
            inbox_dir=self.inbox_dir,
            state=state,
            dry_run=False
        )
        self.assertFalse(ok2)
        self.assertIn("Duplicate content detected", msg2)

    def test_quick_paste_dry_run(self):
        """Dry-run should return success but create no files on disk."""
        state = kb_ingest.InboxStateManager(self.state_file)

        ok, filename = kb_ingest.ingest_quick_paste(
            text="Temporary notice.",
            title="Notice",
            author="Bob",
            inbox_dir=self.inbox_dir,
            state=state,
            dry_run=True
        )
        self.assertTrue(ok)
        created_file = self.inbox_dir / filename
        self.assertFalse(created_file.exists())

    @patch("urllib.request.urlopen")
    def test_github_driver_ingestion(self, mock_urlopen):
        """Test GitHub issues ingestion with REST API mock."""
        mock_response_data = [
            {
                "number": 42,
                "title": "Bug in installer wizard",
                "body": "When choosing Swift, it prompts twice.",
                "user": {"login": "dev_contributor"},
                "html_url": "https://github.com/org/repo/issues/42",
                "created_at": "2026-10-11T12:00:00Z"
            }
        ]
        mock_cm = MagicMock()
        mock_cm.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_cm

        driver = kb_ingest.GitHubIngestDriver(repo="org/repo", token="ghp_dummy")
        issues = driver.fetch_issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["number"], 42)

        # Run ingest orchestration
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            exit_code = kb_ingest.run_ingest(
                inbox_dir=self.inbox_dir,
                github=True,
                verbose=True,
                github_repo="org/repo",
                github_token="ghp_dummy"
            )
        self.assertEqual(exit_code, 0)
        expected_file = self.inbox_dir / "FB-GH-42.md"
        self.assertTrue(expected_file.is_file())
        file_text = expected_file.read_text(encoding="utf-8")
        self.assertIn("id: FB-GH-42", file_text)
        self.assertIn("channel: github", file_text)
        self.assertIn("When choosing Swift, it prompts twice.", file_text)

    @patch("imaplib.IMAP4_SSL")
    def test_email_driver_ingestion(self, mock_imap_ssl):
        """Test Email IMAP driver with mocked imaplib connection."""
        mock_client = MagicMock()
        mock_imap_ssl.return_value = mock_client
        mock_client.search.return_value = ("OK", [b"1"])

        raw_email = (
            b"From: user@test.com\r\n"
            b"Subject: Feedback on CLI\r\n"
            b"Message-ID: <unique-123@test.com>\r\n"
            b"Date: Sun, 11 Oct 2026 12:00:00 +0000\r\n"
            b"Content-Type: text/plain; charset=utf-8\r\n"
            b"\r\n"
            b"Great tool! Would love dark mode support.\r\n"
        )
        mock_client.fetch.return_value = ("OK", [(b"1 (RFC822)", raw_email)])

        driver = kb_ingest.EmailIngestDriver(
            host="imap.example.com",
            user="user@test.com",
            password="secret_password"
        )
        emails = driver.fetch_emails()
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0]["subject"], "Feedback on CLI")
        self.assertIn("dark mode support", emails[0]["body"])

    def test_detect_github_repo(self):
        """Test zero-deps git remote URL parsing and env override."""
        # 1. Environment variable override
        with patch.dict("os.environ", {"GITHUB_REPOSITORY": "override-org/override-repo"}):
            self.assertEqual(kb_ingest.detect_github_repo(), "override-org/override-repo")

        # 2. Subprocess git URL schemes
        cases = [
            ("https://github.com/alice/cool-app.git", "alice/cool-app"),
            ("https://github.com/bob/other-tool", "bob/other-tool"),
            ("git@github.com:team/project.git", "team/project"),
            ("git@github.com:team/project", "team/project"),
            ("https://x-access-token:ghp_secret@github.com/org/secured.git", "org/secured"),
            ("https://gitlab.com/external/repo.git", None),
            ("invalid-url", None),
        ]

        with patch.dict("os.environ", {}, clear=True):
            for remote_url, expected in cases:
                mock_proc = MagicMock()
                mock_proc.returncode = 0
                mock_proc.stdout = f"{remote_url}\n"
                with patch("subprocess.run", return_value=mock_proc):
                    res = kb_ingest.detect_github_repo()
                    self.assertEqual(res, expected, f"Failed for {remote_url}")

            # Git command failure
            mock_proc_fail = MagicMock()
            mock_proc_fail.returncode = 1
            mock_proc_fail.stdout = ""
            with patch("subprocess.run", return_value=mock_proc_fail):
                self.assertIsNone(kb_ingest.detect_github_repo())

            # Git not installed (FileNotFoundError)
            with patch("subprocess.run", side_effect=FileNotFoundError):
                self.assertIsNone(kb_ingest.detect_github_repo())

    @patch("urllib.request.urlopen")
    def test_github_driver_filters(self, mock_urlopen):
        """Test GitHub issues filtering with custom label and --all-open."""
        mock_cm = MagicMock()
        mock_cm.read.return_value = json.dumps([
            {"number": 1, "title": "Regular Issue"},
            {"number": 2, "title": "PR", "pull_request": {}}
        ]).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_cm

        driver = kb_ingest.GitHubIngestDriver(repo="test/repo", token="dummy")

        # 1. Default label
        issues = driver.fetch_issues(label="needs-triage", all_open=False)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["number"], 1)
        req1 = mock_urlopen.call_args[0][0]
        self.assertIn("labels=needs-triage", req1.full_url)
        self.assertIn("per_page=100", req1.full_url)

        # 2. Custom label
        driver.fetch_issues(label="user-feedback", all_open=False)
        req2 = mock_urlopen.call_args[0][0]
        self.assertIn("labels=user-feedback", req2.full_url)

        # 3. All open
        driver.fetch_issues(all_open=True)
        req3 = mock_urlopen.call_args[0][0]
        self.assertNotIn("labels=", req3.full_url)
        self.assertIn("state=open&per_page=100", req3.full_url)

    @patch("urllib.request.urlopen")
    def test_github_driver_http_errors(self, mock_urlopen):
        """Test HTTP error handling (401, 403, 404, 500)."""
        import urllib.error

        driver = kb_ingest.GitHubIngestDriver(repo="test/repo", token="dummy")

        error_cases = [
            (401, "Неверный или просроченный GITHUB_TOKEN"),
            (403, "Превышен лимит запросов API"),
            (404, "Репозиторий 'test/repo' не найден или является приватным"),
            (500, "HTTP 500"),
        ]

        for code, expected_text in error_cases:
            err = urllib.error.HTTPError(
                url="https://api.github.com",
                code=code,
                msg="Error",
                hdrs={},
                fp=io.BytesIO(b"")
            )
            mock_urlopen.side_effect = err
            stderr_cap = io.StringIO()
            with patch("sys.stderr", stderr_cap):
                res = driver.fetch_issues()
                self.assertEqual(res, [])
                self.assertIn(expected_text, stderr_cap.getvalue())

    def test_channel_transparency_warnings(self):
        """Test warning outputs when channels are unconfigured or anonymous."""
        # 1. GitHub without repository
        stdout_cap = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), patch("sys.stdout", stdout_cap), patch("kb_ingest.detect_github_repo", return_value=None):
            kb_ingest.run_ingest(inbox_dir=self.inbox_dir, github=True)
            self.assertIn("⚠️ Warning: Канал GitHub пропущен: репозиторий не найден", stdout_cap.getvalue())

        # 2. GitHub anonymous warning
        stdout_cap2 = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), patch("sys.stdout", stdout_cap2), patch("kb_ingest.detect_github_repo", return_value="org/repo"), patch.object(kb_ingest.GitHubIngestDriver, "fetch_issues", return_value=[]):
            kb_ingest.run_ingest(inbox_dir=self.inbox_dir, github=True)
            self.assertIn("ℹ️ Info: GitHub опрашивается анонимно", stdout_cap2.getvalue())

        # 3. Email without configuration
        stdout_cap3 = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), patch("sys.stdout", stdout_cap3):
            kb_ingest.run_ingest(inbox_dir=self.inbox_dir, email_mode=True)
            self.assertIn("⚠️ Warning: Канал Email пропущен: не настроены переменные FEEDBACK_IMAP_HOST", stdout_cap3.getvalue())

    def test_render_status_dashboard(self):
        """Test status dashboard rendering with Inbox state."""
        # Create some sample inbox items
        (self.inbox_dir / "FB-001.md").write_text("---\nstatus: new\n---\nBody", encoding="utf-8")
        (self.inbox_dir / "FB-002.md").write_text("---\nstatus: processed\n---\nBody", encoding="utf-8")
        (self.inbox_dir / "FB-003.md").write_text("---\nstatus: rejected\n---\nBody", encoding="utf-8")

        stdout_cap = io.StringIO()
        with patch("sys.stdout", stdout_cap), patch("kb_ingest.detect_github_repo", return_value="my-org/my-project"):
            code = kb_ingest.render_status_dashboard(self.inbox_dir, self.temp_dir)
            self.assertEqual(code, 0)

        output = stdout_cap.getvalue()
        self.assertIn("📊 Docs-as-Code Feedback Ingestion Status Dashboard", output)
        self.assertIn("[Канал: GitHub Issues]", output)
        self.assertIn("my-org/my-project (auto-detect)", output)
        self.assertIn("[Канал: Email (IMAP)]", output)
        self.assertIn("[Буфер обращений: docs/02_Tasks/Inbox/]", output)
        self.assertIn("Всего тикетов:      3", output)
        self.assertIn("new: 1 | processed: 1 | rejected: 1", output)


if __name__ == "__main__":
    unittest.main()
