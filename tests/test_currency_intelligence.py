"""Run with: python -m unittest discover -s tests -v"""

import unittest

from currency_intelligence import (
    compare_rate_providers,
    rate_trend,
    rate_volatility,
)


class CurrencyIntelligenceTests(unittest.TestCase):
    def test_rising_trend(self):
        report = rate_trend([1.0, 1.1, 1.2])
        self.assertEqual(report.direction, "rising")
        self.assertAlmostEqual(report.percent_change, 20)

    def test_falling_trend(self):
        self.assertEqual(rate_trend([2.0, 1.0]).direction, "falling")

    def test_stable_trend(self):
        self.assertEqual(rate_trend([1.0, 1.0005]).direction, "stable")

    def test_volatility_constant(self):
        report = rate_volatility([2.0, 2.0, 2.0])
        self.assertEqual(report.standard_deviation, 0)

    def test_provider_comparison(self):
        deviations = compare_rate_providers({"A": 1.0, "B": 1.1})
        self.assertLess(deviations["A"], 0)
        self.assertGreater(deviations["B"], 0)

    def test_invalid_data(self):
        with self.assertRaises(ValueError):
            rate_trend([1.0])
        with self.assertRaises(ValueError):
            rate_volatility([1.0, float("inf")])
        with self.assertRaises(ValueError):
            compare_rate_providers({"A": 1.0})


if __name__ == "__main__":
    unittest.main()
