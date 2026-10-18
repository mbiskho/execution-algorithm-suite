# Execution Algorithm Suite

A small parent-order schedule comparison for TWAP, VWAP-shaped, and participation-of-volume (POV) execution. The deterministic price path is intentionally synthetic.

Run `python3 run.py` to write implementation-shortfall, fill-rate, child-order latency, and participation summaries to `reports/metrics.json`.

Run the smoke test with `python3 -m unittest discover -s tests -v`. The report images were generated from these metrics by the portfolio's shared screenshot script.

![Execution schedule overview](reports/project-overview.png)

![Execution workflow](reports/project-flow.png)

The schedule comparison is an educational simulation, not measured execution quality or a broker benchmark.
