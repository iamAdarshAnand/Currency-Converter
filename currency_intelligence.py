"""Optional offline currency analytics; no forecasting or financial advice."""

from dataclasses import dataclass
from math import isfinite
from statistics import mean, pstdev
from typing import Sequence


def _valid_rates(rates: Sequence[float], minimum: int = 2) -> list[float]:
    values = list(rates)
    if len(values) < minimum:
        raise ValueError(f"at least {minimum} observations are required")
    if any(not isfinite(v) or v <= 0 for v in values):
        raise ValueError("rates must be finite and positive")
    return values


@dataclass(frozen=True)
class TrendReport:
    first: float
    last: float
    percent_change: float
    direction: str
    observations: int


def rate_trend(rates: Sequence[float], *, flat_tolerance_percent: float = 0.1) -> TrendReport:
    """Describe observed history, in chronological order; never extrapolate."""
    values = _valid_rates(rates)
    if not isfinite(flat_tolerance_percent) or flat_tolerance_percent < 0:
        raise ValueError("flat tolerance must be finite and nonnegative")
    change = (values[-1] / values[0] - 1) * 100
    direction = ("stable" if abs(change) <= flat_tolerance_percent
                 else "rising" if change > 0 else "falling")
    return TrendReport(values[0], values[-1], change, direction, len(values))


@dataclass(frozen=True)
class VolatilityReport:
    mean_rate: float
    standard_deviation: float
    coefficient_of_variation_percent: float
    observations: int


def rate_volatility(rates: Sequence[float]) -> VolatilityReport:
    """Compute population standard deviation and relative dispersion."""
    values = _valid_rates(rates)
    average = mean(values)
    deviation = pstdev(values)
    return VolatilityReport(average, deviation, deviation / average * 100, len(values))


def compare_rate_providers(provider_rates: dict[str, float]) -> dict[str, float]:
    """Return each provider's percentage deviation from the median rate."""
    from statistics import median

    if len(provider_rates) < 2:
        raise ValueError("at least two providers are required")
    if any(not name.strip() for name in provider_rates):
        raise ValueError("provider names must not be empty")
    values = list(provider_rates.values())
    if any(not isfinite(rate) or rate <= 0 for rate in values):
        raise ValueError("provider rates must be finite and positive")
    baseline = median(values)
    return {name: (rate / baseline - 1) * 100 for name, rate in provider_rates.items()}
