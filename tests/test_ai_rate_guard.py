"""Run with: python -m unittest discover -s tests -v"""

import unittest

from ai_rate_guard import assess_exchange_rate


class RateGuardTests(unittest.TestCase):
    def test_normal_rate(self):
        result = assess_exchange_rate(1.02, [1.0, 1.01, 1.02])
        self.assertFalse(result.anomalous)

    def test_anomalous_rate(self):
        result = assess_exchange_rate(1.5, [1.0, 1.01, 0.99])
        self.assertTrue(result.anomalous)
        self.assertGreater(result.deviation_percent, 40)

    def test_insufficient_history(self):
        with self.assertRaises(ValueError):
            assess_exchange_rate(1.0, [1.0])

    def test_invalid_rate(self):
        for value in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    assess_exchange_rate(value, [1.0, 1.1, 1.2])

    def test_invalid_history(self):
        with self.assertRaises(ValueError):
            assess_exchange_rate(1.0, [1.0, 0.0, 1.2])


if __name__ == "__main__":
    unittest.main()
