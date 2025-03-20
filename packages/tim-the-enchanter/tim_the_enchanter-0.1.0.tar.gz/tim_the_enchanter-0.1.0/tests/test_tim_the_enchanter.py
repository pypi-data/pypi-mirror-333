"""Tests for Tim The Enchanter package."""

import time
import unittest
from tim_the_enchanter import TimTheEnchanter, TimTheEnchanterReportFormat


class TestTimTheEnchanter(unittest.TestCase):
    """Test cases for the TimTheEnchanter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.tracker = TimTheEnchanter.create(enabled=True)
        self.tracker.start_session("test_session")

    def tearDown(self):
        """Tear down test fixtures."""
        self.tracker.end_session()

    def test_record(self):
        """Test that recording events works correctly."""
        self.tracker.record("test_process", 0.5)
        report = self.tracker.report(TimTheEnchanterReportFormat.CHRONOLOGICAL)
        self.assertEqual(report["format"], "chronological")
        self.assertEqual(report["session"], "test_session")
        self.assertEqual(len(report["events"]), 1)
        self.assertEqual(report["events"][0]["process_name"], "test_process")
        self.assertEqual(report["events"][0]["duration"], 0.5)

    def test_time_process(self):
        """Test the time_process context manager."""
        with self.tracker.time_process("context_test"):
            time.sleep(0.01)  # Small sleep to ensure timing
        
        report = self.tracker.report(TimTheEnchanterReportFormat.BY_PROCESS)
        self.assertEqual(report["format"], "by_process")
        self.assertIn("context_test", report["processes"])
        self.assertEqual(len(report["processes"]["context_test"]), 1)
        self.assertGreater(report["processes"]["context_test"][0]["duration"], 0)


if __name__ == "__main__":
    unittest.main() 