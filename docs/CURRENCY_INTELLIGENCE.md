# Currency Intelligence — optional offline analytics

These standalone Python utilities describe historical exchange-rate observations. They do **not** predict future rates, fetch live prices, or recommend trades.

## Systems

1. **Trend analysis** — compares first and last observations to report a rising, falling, or stable historical trend.
2. **Volatility analytics** — computes population standard deviation and coefficient of variation for positive rate samples.
3. **Multi-provider comparison** — measures each provider's percentage deviation from the median quote.

## Example

```python
from currency_intelligence import rate_trend, rate_volatility, compare_rate_providers

history = [1.0, 1.02, 1.01, 1.05]
print(rate_trend(history))
print(rate_volatility(history))
print(compare_rate_providers({"ProviderA": 1.02, "ProviderB": 1.03}))
```

Use chronological history for trends. Compare only the **same currency pair and quote direction**; provider quotes should also have compatible timestamps. Otherwise comparisons are misleading.

## Tests

```bash
python -m unittest discover -s tests -v
```

Python 3.9+; standard library only. This module is not yet wired into the original converter UI.
