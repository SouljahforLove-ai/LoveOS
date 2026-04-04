"""
Tests for the LoveOS Integration Layer.
═══════════════════════════════════════════════════
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integration.faith_integration import FaithIntegration
from integration.legacy_integration import LegacyIntegration
from integration.external_integration import ExternalIntegration, ConsentStatus


class TestFaithIntegration(unittest.TestCase):
    def setUp(self):
        self.fi = FaithIntegration()

    def test_bindings_initialized(self):
        bindings = self.fi.get_bindings_summary()
        self.assertGreater(len(bindings), 0)

    def test_grace_modulation_reduces_shame(self):
        state = {"shame": 0.8, "love": 0.5, "grace_quotient": 0.8}
        result = self.fi.apply_grace_modulation(state)
        self.assertLess(result["shame"], state["shame"])

    def test_grace_modulation_amplifies_love(self):
        state = {"shame": 0.8, "love": 0.5, "grace_quotient": 0.8}
        result = self.fi.apply_grace_modulation(state)
        self.assertGreater(result["love"], state["love"])


class TestLegacyIntegration(unittest.TestCase):
    def setUp(self):
        self.li = LegacyIntegration()

    def test_capture_above_threshold(self):
        result = self.li.capture("test", "teaching", {"content": "lesson"}, 0.9)
        self.assertIsNotNone(result)

    def test_ignore_below_threshold(self):
        result = self.li.capture("test", "workflow", {}, 0.1)
        self.assertIsNone(result)

    def test_for_zen_default(self):
        self.li.capture("test", "teaching", {}, 0.9)
        zen_items = self.li.get_for_zen()
        self.assertEqual(len(zen_items), 1)


class TestExternalIntegration(unittest.TestCase):
    def setUp(self):
        self.ei = ExternalIntegration()

    def test_consent_required(self):
        status = self.ei.request_consent("/path/to/file", "read")
        self.assertEqual(status, ConsentStatus.PENDING)

    def test_blocked_target(self):
        from integration.external_integration import ExternalRequest, ExternalSource
        self.ei.block_target("bad_target")
        req = ExternalRequest(ExternalSource.FILE_SYSTEM, "read", "bad_target")
        resp = self.ei.process_request(req)
        self.assertFalse(resp.success)


if __name__ == "__main__":
    unittest.main()
