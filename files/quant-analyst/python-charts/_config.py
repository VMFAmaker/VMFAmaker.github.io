"""
Shared Configuration
====================
Edit these settings before running any chart script.
Run scripts from this directory:  python 01_price_history.py
"""

CONFIG = {
    # ── Asset under analysis ────────────────────────────
    "ticker": "AAPL",
    "name": "Pear Corporation",

    # ── Analysis period ─────────────────────────────────
    "start": "2021-01-01",
    "end": None,                    # None = up to today

    # ── Benchmark index ─────────────────────────────────
    "benchmark_ticker": "^GSPC",
    "benchmark_name": "S&P 500",

    # ── Peer companies (ticker: display name) ───────────
    "peers": {
        "MSFT": "Cedar",
        "GOOGL": "Maple",
        "AMZN": "Oak",
        "META": "Birch",
        "NVDA": "Pine",
    },

    # ── Event study dates (date, label) ─────────────────
    "events": [
        ("2024-06-10", "AI Platform Announcement"),
        ("2024-02-01", "Q1 FY2024 Earnings"),
        ("2024-05-02", "Q2 FY2024 Earnings + Buyback"),
        ("2024-08-01", "Q3 FY2024 Earnings"),
        ("2025-01-30", "Q1 FY2025 Earnings"),
    ],

    # ── Output settings ─────────────────────────────────
    "output_dir": "output",
    "dpi": 150,
    "format": "png",
}
