import unittest
from pathlib import Path
import sys

# Ensure the parent directory is in the path so we can import scripts
sys.path.append(str(Path(__file__).parent.parent))

from scripts.compute_aimra_g import (
    to_float,
    normalise_rli,
    normalise_rlr,
    linear_g,
    geometric_g
)
from scripts.robustness_geometric_mean import fnum

class TestAIMRACalculations(unittest.TestCase):
    def test_to_float(self):
        self.assertEqual(to_float("1.23"), 1.23)
        self.assertEqual(to_float("  0.45  "), 0.45)
        self.assertIsNone(to_float(""))
        self.assertIsNone(to_float("   "))
        self.assertIsNone(to_float(None))

    def test_fnum(self):
        self.assertEqual(fnum("1.23"), 1.23)
        self.assertEqual(fnum("  0.45  "), 0.45)
        self.assertIsNone(fnum(""))
        self.assertIsNone(fnum("   "))
        self.assertIsNone(fnum(None))

    def test_normalise_rli(self):
        # 187 days latency: 1 - 187/365 = ~0.4877
        self.assertEqual(normalise_rli(187, 0.5), 0.4877)
        # If rli_days is None, should return current
        self.assertEqual(normalise_rli(None, 0.49), 0.49)
        # Latency greater than 365 should be bounded to 1 (normalised to 0)
        self.assertEqual(normalise_rli(400, 0.1), 0.0)

    def test_normalise_rlr(self):
        # 0.31 loss: 1 - 0.31 = 0.69
        self.assertEqual(normalise_rlr(0.31, 0.5), 0.69)
        # If rlr is None, should return current
        self.assertEqual(normalise_rlr(None, 0.69), 0.69)
        # Loss greater than 1 should be bounded to 1 (normalised to 0)
        self.assertEqual(normalise_rlr(1.5, 0.1), 0.0)

    def test_linear_g(self):
        self.assertEqual(linear_g([0.5, 0.5, 0.5, 0.5, 0.5]), 0.5)
        self.assertEqual(linear_g([0.1, 0.2, 0.3, 0.4, 0.5]), 0.3)

    def test_geometric_g(self):
        self.assertEqual(geometric_g([0.5, 0.5, 0.5, 0.5, 0.5]), 0.5)
        # (0.1 * 0.2 * 0.3 * 0.4 * 0.5) ** 0.2 = 0.0012 ** 0.2 = ~0.2605
        self.assertEqual(geometric_g([0.1, 0.2, 0.3, 0.4, 0.5]), 0.2605)

if __name__ == "__main__":
    unittest.main()
