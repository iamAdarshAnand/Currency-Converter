"""Regression tests for exchange-rate validation and threshold boundaries.

Run: python -m unittest discover -s tests -v
"""

import unittest

from ai_rate_guard import assess_exchange_rate
from currency_intelligence import (
    compare_rate_providers,
    rate_trend,
    rate_volatility,
)


class RateAnalyticsBoundaryTests(unittest.TestCase):
    def test_anomaly_threshold_is_strict(self):
        at_threshold = assess_exchange_rate(
            1.1, [1.0, 1.0, 1.0], threshold_percent=10.0
        )
        self.assertFalse(at_threshold.anomalous)
        beyond_threshold = assess_exchange_rate(
            1.11, [1.0, 1.0, 1.0], threshold_percent=10.0
        )
        self.assertTrue(beyond_threshold.anomalous)

    def test_custom_minimum_history(self):
        result = assess_exchange_rate(2.0, [2.0], min_history=1)
        self.assertFalse(result.anomalous)

    def test_invalid_guard_configuration(self):
        for threshold in (0, -1, float("nan"), float("inf")):
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError):
                    assess_exchange_rate(1.0, [1.0, 1.0, 1.0],
                                         threshold_percent=threshold)
        with self.assertRaises(ValueError):
            assess_exchange_rate(1.0, [1.0], min_history=0)

    def test_trend_tolerance_boundary(self):
        self.assertEqual(
            rate_trend([100.0, 100.1], flat_tolerance_percent=0.1).direction,
            "stable",
        )
        self.assertEqual(
            rate_trend([100.0, 100.2], flat_tolerance_percent=0.1).direction,
            "rising",
        )

    def test_invalid_trend_tolerance(self):
        for tolerance in (-0.1, float("nan"), float("inf")):
            with self.subTest(tolerance=tolerance):
                with self.assertRaises(ValueError):
                    rate_trend([1.0, 2.0],
                               flat_tolerance_percent=tolerance)

    def test_provider_equal_rates(self):
        self.assertEqual(
            compare_rate_providers({"Provider A": 1.0, "Provider B": 1.0}),
            {"Provider A": 0.0, "Provider B": 0.0},
        )

    def test_provider_invalid_names_and_rates(self):
        with self.assertRaises(ValueError):
            compare_rate_providers({" ": 1.0, "Valid": 1.1})
        with self.assertRaises(ValueError):
            compare_rate_providers({"A": 1.0, "B": float("nan")})

    def test_volatility_identical_rates(self):
        result = rate_volatility([1.5, 1.5, 1.5])
        self.assertEqual(result.coefficient_of_variation_percent, 0.0)


if __name__ == "__main__":
    unittest.main()
