"""Offline exchange-rate anomaly checks for a currency converter.

This optional module does not fetch rates, predict future prices, or claim
to be a trained machine-learning model. It uses robust statistics to flag
unusual observations for human review.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
from statistics import median
from typing import Sequence


@dataclass(frozen=True)
class RateAssessment:
    rate: float
    baseline: float
    deviation_percent: float
    anomalous: bool
    explanation: str


def assess_exchange_rate(
    rate: float,
    historical_rates: Sequence[float],
    *,
    threshold_percent: float = 10.0,
    min_history: int = 3,
) -> RateAssessment:
    """Compare a positive rate against the median of prior observations.

    Rates must all represent the same currency pair and quote direction.
    Historical observations should be trusted and collected before the
    candidate rate. A result is a warning, not a trading recommendation.
    """
    if not isfinite(rate) or rate <= 0:
        raise ValueError("rate must be a finite positive number")
    if not isfinite(threshold_percent) or threshold_percent <= 0:
        raise ValueError("threshold_percent must be finite and positive")
    if min_history < 1:
        raise ValueError("min_history must be at least 1")
    if len(historical_rates) < min_history:
        raise ValueError("not enough historical rates for assessment")
    if any(not isfinite(value) or value <= 0 for value in historical_rates):
        raise ValueError("historical rates must be finite and positive")

    baseline = median(historical_rates)
    deviation = abs(rate - baseline) / baseline * 100.0
    anomalous = deviation > threshold_percent and not isclose(\n        deviation, threshold_percent, rel_tol=1e-12, abs_tol=1e-12\n    )
    explanation = (
        f"Rate differs from historical median by {deviation:.2f}%; "
        + ("review the provider, pair, and timestamp." if anomalous
           else "within configured tolerance.")
    )
    return RateAssessment(rate, baseline, deviation, anomalous, explanation)
