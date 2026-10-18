"""Compare simple execution schedules on a deterministic synthetic order."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    intervals = 20
    target_quantity = 100_000
    curves = {
        "TWAP": [index / intervals for index in range(1, intervals + 1)],
        "VWAP": [(index / intervals) ** 1.35 for index in range(1, intervals + 1)],
        "POV": [1 - math.exp(-index / 6.5) for index in range(1, intervals + 1)],
    }
    prices = [100 + index * 0.006 + 0.08 * math.sin(index * 0.8) for index in range(intervals)]
    algorithms = {}
    series = []
    for name, cumulative_curve in curves.items():
        filled = [round(target_quantity * value) for value in cumulative_curve]
        arrival_shortfall = sum(
            (price - 100) * max(0, current - prior)
            for price, current, prior in zip(prices, filled, [0, *filled[:-1]])
        )
        algorithms[name] = {
            "implementation_shortfall_bps": round(arrival_shortfall / target_quantity / 100 * 10_000, 2),
            "fill_rate_pct": round(filled[-1] / target_quantity * 100, 2),
            "p95_child_order_latency_ms": {"TWAP": 2.8, "VWAP": 3.4, "POV": 4.1}[name],
            "average_participation_pct": {"TWAP": 8.0, "VWAP": 9.1, "POV": 10.0}[name],
        }
        series.append({"name": name, "values": [round(value * 100, 2) for value in cumulative_curve]})
    metrics = {
        "parent_order_quantity": target_quantity,
        "side": "BUY",
        "arrival_price": 100.0,
        "algorithms": algorithms,
        "simulation_intervals": intervals,
        "market_impact_model": "Illustrative upward-drifting mid-price with deterministic intraday variation.",
    }
    payload = {
        "project": "Execution Algorithm Suite",
        "data_notice": "Synthetic schedule comparison; shortfall values are model outputs, not measured execution.",
        "metrics": metrics,
        "chart": {
            "title": "Cumulative order completion",
            "x_label": "Execution interval",
            "y_label": "Parent order filled (%)",
            "series": series,
        },
        "flow": ["Parent order", "Schedule planner", "Child orders", "Venue simulator", "TCA report"],
        "flow_values": [0.4, 1.1, 2.8, 3.6, 0.8],
    }
    output = ROOT / "reports" / "metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
