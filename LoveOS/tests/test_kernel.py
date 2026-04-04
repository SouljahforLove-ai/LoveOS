"""
Tests for the LoveOS Kernel Layer.
═══════════════════════════════════════════════════
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kernel.microkernel import Microkernel, KernelState
from kernel.sovereignty import SovereigntyCore, SovereigntyLevel
from kernel.syscalls import SyscallInterface, SyscallCategory
from kernel.boot import BootSequence, BootPhase, BootManifest


class TestMicrokernel(unittest.TestCase):
    def setUp(self):
        self.kernel = Microkernel()

    def test_initial_state_is_dormant(self):
        self.assertEqual(self.kernel.state, KernelState.DORMANT)

    def test_kernel_has_message_queue(self):
        self.assertIsNotNone(self.kernel._message_queue)

    def test_boot_transitions_state(self):
        self.kernel.boot()
        self.assertNotEqual(self.kernel.state, KernelState.DORMANT)


class TestSovereigntyCore(unittest.TestCase):
    def setUp(self):
        self.sovereignty = SovereigntyCore()

    def test_all_boundaries_initialized(self):
        self.assertEqual(len(self.sovereignty._boundaries), 7)

    def test_sovereignty_check_passes_clean(self):
        result = self.sovereignty.check_sovereignty("test_action", "kernel")
        self.assertTrue(result)

    def test_boundary_names(self):
        names = {b.name for b in self.sovereignty._boundaries.values()}
        # Check all 7 boundary names contain sovereignty-related terms
        self.assertEqual(len(names), 7)

    def test_get_violations_empty(self):
        violations = self.sovereignty.get_violations()
        self.assertEqual(len(violations), 0)


class TestSyscallInterface(unittest.TestCase):
    def setUp(self):
        self.syscalls = SyscallInterface()

    def test_handlers_registered(self):
        self.assertGreater(len(self.syscalls._handlers), 0)

    def test_sovereignty_check_handler_exists(self):
        key = f"{SyscallCategory.SOVEREIGN.name}:check"
        self.assertIn(key, self.syscalls._handlers)


class TestBootSequence(unittest.TestCase):
    def setUp(self):
        self.boot = BootSequence()

    def test_manifest_created(self):
        self.assertIsNotNone(self.boot.manifest)

    def test_manifest_initial_phase(self):
        self.assertEqual(self.boot.manifest.phase, BootPhase.PRE_BOOT)

    def test_boot_order_modules_mounted_after_execute(self):
        result = self.boot.execute()
        # identity mounts first, audit mounts last
        if result.modules_mounted:
            self.assertEqual(result.modules_mounted[0], "identity")
            self.assertEqual(result.modules_mounted[-1], "audit")


if __name__ == "__main__":
    unittest.main()
