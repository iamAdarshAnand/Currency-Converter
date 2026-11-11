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

## Integration guide for maintainers

The analytics modules are intentionally opt-in. To integrate them into an existing converter:

1. Validate the currency pair, quote direction, rate provider, and observation timestamp.
2. Retrieve historical rates through the application's existing trusted data source.
3. Call `assess_exchange_rate` from `ai_rate_guard.py` before displaying an anomaly warning.
4. Call `rate_trend` and `rate_volatility` from `currency_intelligence.py` only when at least two comparable historical observations are available.
5. Use `compare_rate_providers` only for contemporaneous quotes of the same currency pair.
6. Treat analytics failures as nonfatal: the core currency-conversion functionality should continue to work.
7. Clearly label these values as historical statistics, not AI forecasts or investment advice.

### Maintainer acceptance checks

- [ ] Normal conversion still works when analytics are disabled.
- [ ] Missing or invalid historical data displays a helpful message without crashing the converter.
- [ ] Tests pass with `python -m unittest discover -s tests -v`.
- [ ] No API credentials or personal information are logged.
- [ ] No claims are made about trained models or live-rate accuracy.
