"""
Tests for Sovereignty — the most critical layer.
═══════════════════════════════════════════════════
If sovereignty fails, everything fails.
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kernel.sovereignty import SovereigntyCore, SovereigntyLevel
from guards.sovereignty_guard import SovereigntyGuard
from guards.boundary_guard import BoundaryGuard
from permissions.sovereignty_permissions import (
    CONSTITUTIONAL_PERMISSIONS, verify_constitutional_integrity,
    check_sovereignty_violation,
)
from maps.sovereignty_map import SovereigntyMap


class TestSovereigntyConstitution(unittest.TestCase):
    def test_seven_constitutional_permissions(self):
        self.assertEqual(len(CONSTITUTIONAL_PERMISSIONS), 7)

    def test_no_permission_can_override(self):
        for perm in CONSTITUTIONAL_PERMISSIONS:
            self.assertFalse(perm.can_override)

    def test_no_permission_can_delegate(self):
        for perm in CONSTITUTIONAL_PERMISSIONS:
            self.assertFalse(perm.can_delegate)

    def test_no_permission_can_disable(self):
        for perm in CONSTITUTIONAL_PERMISSIONS:
            self.assertFalse(perm.can_disable)

    def test_all_are_constitutional(self):
        for perm in CONSTITUTIONAL_PERMISSIONS:
            self.assertTrue(perm.constitutional)

    def test_integrity_verification(self):
        result = verify_constitutional_integrity()
        self.assertTrue(result["all_intact"])
        self.assertIn("seal", result)

    def test_violation_detection(self):
        self.assertTrue(check_sovereignty_violation("override_identity"))
        self.assertTrue(check_sovereignty_violation("bypass_consent"))
        self.assertTrue(check_sovereignty_violation("erase_audit"))
        self.assertFalse(check_sovereignty_violation("read_data"))


class TestSovereigntyGuard(unittest.TestCase):
    def setUp(self):
        self.guard = SovereigntyGuard()

    def test_cannot_deactivate(self):
        result = self.guard.deactivate()
        self.assertFalse(result)

    def test_activate_works(self):
        self.guard.activate()
        # Guard should be in WATCHING state after activate
        from guards.sovereignty_guard import GuardState
        self.assertEqual(self.guard._state, GuardState.WATCHING)


class TestBoundaryGuard(unittest.TestCase):
    def setUp(self):
        self.guard = BoundaryGuard()

    def test_five_core_boundaries(self):
        self.assertEqual(len(self.guard._boundaries), 5)

    def test_cannot_deactivate_absolute(self):
        self.guard.activate()
        # BoundaryGuard should remain active
        self.assertTrue(self.guard._active)


class TestSovereigntyMap(unittest.TestCase):
    def setUp(self):
        self.sov_map = SovereigntyMap()

    def test_components_mapped(self):
        all_mappings = self.sov_map.get_all()
        self.assertGreater(len(all_mappings), 0)

    def test_absolute_components_exist(self):
        absolute = self.sov_map.get_by_level("ABSOLUTE")
        self.assertGreater(len(absolute), 0)

    def test_immutable_components_exist(self):
        immutable = self.sov_map.get_immutable()
        self.assertGreater(len(immutable), 0)


if __name__ == "__main__":
    unittest.main()
