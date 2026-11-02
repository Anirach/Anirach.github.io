"""Regression checks for imported-draft publication dates. No site writes."""
import pathlib
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import gen_feed


class PublicationDateTests(unittest.TestCase):
    def check_stamp(self, git_stamp):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            (root/'post.html').write_text('<meta property="article:published_time" content="2026-10-23">')
            with patch.object(gen_feed, 'ROOT', root), patch.object(gen_feed.subprocess, 'run', return_value=SimpleNamespace(stdout=git_stamp)):
                return gen_feed.first_commit_date('post.html')

    def test_imported_draft_keeps_declared_day(self):
        self.assertEqual(self.check_stamp('Tue, 27 Oct 2026 14:12:03 +0700'), 'Fri, 23 Oct 2026 09:00:00 +0700')

    def test_matching_history_keeps_original_time(self):
        self.assertEqual(self.check_stamp('Fri, 23 Oct 2026 14:12:03 +0700'), 'Fri, 23 Oct 2026 14:12:03 +0700')

    def test_uncommitted_draft_keeps_declared_day(self):
        self.assertEqual(self.check_stamp(''), 'Fri, 23 Oct 2026 09:00:00 +0700')


if __name__ == '__main__': unittest.main()
