"""
Tests for the LoveOS Engine Layer.
═══════════════════════════════════════════════════
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.emotional_engine import EmotionalEngine, EmotionalVector, EmotionalFamily
from engines.sovereignty_engine import SovereigntyEngine
from engines.spiritual_engine import SpiritualEngine
from engines.sorting_engine import SortingEngine, InputCategory
from engines.faith_engine import FaithEngine, FaithTradition
from engines.legacy_engine import LegacyEngine, LegacyCategory


class TestEmotionalEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EmotionalEngine()

    def test_seven_dimensions(self):
        vec = EmotionalVector()
        d = vec.to_dict()
        self.assertEqual(len(d), 7)

    def test_emotional_families_exist(self):
        # Families are defined as module-level constants
        families = [f for f in dir(EmotionalFamily) if not f.startswith('_')]
        self.assertGreater(len(families), 0)

    def test_sovereignty_never_blends_down(self):
        v1 = EmotionalVector(sovereignty=0.9)
        v2 = EmotionalVector(sovereignty=0.3)
        blended = v1.blend(v2, 0.5)
        self.assertGreaterEqual(blended.sovereignty, 0.9)

    def test_magnitude(self):
        vec = EmotionalVector(valence=1.0, arousal=0.0, dominance=0.0,
                               sacred=0.0, relational=0.0, temporal=0.0, sovereignty=0.0)
        self.assertGreater(vec.magnitude(), 0)

    def test_distance(self):
        v1 = EmotionalVector(valence=1.0)
        v2 = EmotionalVector(valence=0.0)
        self.assertGreater(v1.distance_to(v2), 0)

    def test_process_returns_dict(self):
        result = self.engine.process(EmotionalVector(valence=0.8))
        self.assertIsInstance(result, dict)


class TestSovereigntyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SovereigntyEngine()

    def test_initial_boundaries(self):
        self.assertGreater(len(self.engine._active_boundaries), 0)

    def test_check_boundary(self):
        result = self.engine.check_action("kernel", "test_action", "system")
        self.assertIsNotNone(result)

    def test_violation_count_starts_zero(self):
        self.assertEqual(self.engine.get_violation_count(), 0)


class TestSpiritualEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SpiritualEngine()

    def test_sovereignty_floor(self):
        self.assertGreaterEqual(self.engine._sovereignty_floor, 0.5)

    def test_current_state_exists(self):
        self.assertIsNotNone(self.engine._current_state)


class TestSortingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SortingEngine()

    def test_routing_table_populated(self):
        self.assertGreater(len(self.engine._routing_table), 0)

    def test_categories_defined(self):
        self.assertEqual(len(InputCategory), 8)

    def test_sort_returns_result(self):
        result = self.engine.sort("test input")
        self.assertIsNotNone(result)


class TestFaithEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FaithEngine()

    def test_integrated_tradition(self):
        self.assertEqual(self.engine._active_tradition, FaithTradition.INTEGRATED)

    def test_grace_quotient_initial(self):
        gq = self.engine.compute_grace_quotient()
        self.assertIsNotNone(gq)


class TestLegacyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LegacyEngine()

    def test_categories(self):
        self.assertEqual(len(LegacyCategory), 6)


if __name__ == "__main__":
    unittest.main()
