import unittest
from datetime import datetime, timedelta, timezone
from nuclear_news_indexer import matches_keywords, is_entry_recent

class TestNuclearNewsIndexer(unittest.TestCase):
    def test_matches_keywords_true(self):
        text = "This article discusses nuclear fusion and reactors."
        self.assertTrue(matches_keywords(text))

    def test_matches_keywords_false(self):
        text = "This article is about gardening and plants."
        self.assertFalse(matches_keywords(text))

    def test_is_entry_recent_true(self):
        entry = {
            "published": datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z"),
            "published_parsed": datetime.now(timezone.utc).timetuple(),
            "title": "Recent Article"
        }
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        # Should be recent
        self.assertTrue(is_entry_recent(entry, one_week_ago, logger=DummyLogger()))

    def test_is_entry_recent_false(self):
        old_date = datetime.now(timezone.utc) - timedelta(days=10)
        entry = {
            "published": old_date.strftime("%a, %d %b %Y %H:%M:%S %z"),
            "published_parsed": old_date.timetuple(),
            "title": "Old Article"
        }
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        # Should not be recent
        self.assertFalse(is_entry_recent(entry, one_week_ago, logger=DummyLogger()))

class DummyLogger:
    def info(self, msg):
        # Dummy logger for testing: does nothing
        pass
    def warning(self, msg):
        # Dummy logger for testing: does nothing
        pass
    def error(self, msg):
        # Dummy logger for testing: does nothing
        pass

if __name__ == '__main__':
    unittest.main()
