# Exchange-rate anomaly guard

This optional Python module provides a lightweight, offline statistical check for suspicious exchange-rate observations. It is not a trained AI model, does not forecast prices, and should not be used as financial advice.

## Example

```python
from ai_rate_guard import assess_exchange_rate

result = assess_exchange_rate(
    1.25,
    [1.00, 1.01, 0.99, 1.02],
    threshold_percent=10,
)
print(result.anomalous)
print(result.explanation)
```

## How it works

The module calculates the median of prior rates and compares the candidate rate to that median. A deviation greater than the configured percentage threshold is flagged for review. The default threshold is 10%, with at least three historical observations.

Only compare rates for the same currency pair, quote direction, and compatible rate provider. Historical rates must predate the candidate observation.

## Limitations

- No live exchange-rate data is retrieved.
- No model is trained; this is an explainable statistical rule.
- Sudden legitimate market movements can be flagged.
- A contaminated or stale historical sample can lead to misleading results.
- This feature is currently standalone and does not modify the existing converter.

## Tests

```bash
python -m unittest discover -s tests -v
```

Requires Python 3.9+ and only the standard library.
