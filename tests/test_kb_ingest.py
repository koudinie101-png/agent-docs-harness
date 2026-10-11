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


if __name__ == "__main__":
    unittest.main()
