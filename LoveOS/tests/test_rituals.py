"""
Tests for the LoveOS Ritual Layer.
═══════════════════════════════════════════════════
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rituals.boot_ritual import BootRitual, BootRitualPhase
from rituals.grounding_ritual import GroundingRitual
from rituals.audit_ritual import AuditRitual
from rituals.closure_ritual import ClosureRitual


class TestBootRitual(unittest.TestCase):
    def setUp(self):
        self.ritual = BootRitual()

    def test_execute_completes(self):
        state = self.ritual.execute("Jorge")
        self.assertEqual(state.phase, BootRitualPhase.COMPLETE)

    def test_all_phases_pass(self):
        state = self.ritual.execute()
        self.assertTrue(state.presence_declared)
        self.assertTrue(state.sovereignty_affirmed)
        self.assertTrue(state.identity_verified)
        self.assertTrue(state.purpose_acknowledged)
        self.assertTrue(state.channels_open)

    def test_seal_generated(self):
        state = self.ritual.execute()
        self.assertNotEqual(state.seal, "")


class TestGroundingRitual(unittest.TestCase):
    def setUp(self):
        self.ritual = GroundingRitual()

    def test_execute_completes(self):
        state = self.ritual.execute(current_sovereignty=0.5)
        self.assertTrue(state.processing_resumed)
        self.assertFalse(state.processing_paused)

    def test_sovereignty_improves(self):
        state = self.ritual.execute(current_sovereignty=0.5)
        self.assertGreater(state.post_sovereignty, state.pre_sovereignty)

    def test_breathe_cycles(self):
        state = self.ritual.execute(cycles=5)
        self.assertEqual(state.breathe_cycles_completed, 5)


class TestAuditRitual(unittest.TestCase):
    def setUp(self):
        self.ritual = AuditRitual()

    def test_healthy_by_default(self):
        report = self.ritual.execute()
        self.assertEqual(report.overall_health, "HEALTHY")

    def test_report_sealed(self):
        report = self.ritual.execute()
        self.assertNotEqual(report.report_seal, "")


class TestClosureRitual(unittest.TestCase):
    def setUp(self):
        self.ritual = ClosureRitual()

    def test_execute_completes(self):
        state = self.ritual.execute()
        self.assertTrue(state.gratitude_expressed)
        self.assertTrue(state.session_archived)
        self.assertTrue(state.audit_sealed)
        self.assertTrue(state.closure_declared)
        self.assertTrue(state.sovereign_halt)

    def test_final_seal(self):
        state = self.ritual.execute()
        self.assertNotEqual(state.final_seal, "")


if __name__ == "__main__":
    unittest.main()
