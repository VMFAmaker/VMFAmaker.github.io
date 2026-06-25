"""
Shared Data Loader
==================
Downloads market data once and caches to CSV inside the output folder.
Subsequent runs read from cache instantly.
Delete the _cache_*.csv files in output/ to force a fresh download.
"""

import os
import numpy as np
import pandas as pd
import yfinance as yf
from _config import CONFIG


# ── Internal helpers ───────────────────────────────────────

def _cache_path(label):
    """Return the cache filepath for a given label, creating output dir if needed."""
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    safe_label = label.replace("^", "idx_").replace("/", "_")
    return os.path.join(CONFIG["output_dir"], f"_cache_{safe_label}.csv")


def _download(ticker, start, end):
    """Download OHLCV from Yahoo Finance and flatten MultiIndex columns."""
    df = yf.download(ticker, start=start, end=end, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


# ── Public loaders ─────────────────────────────────────────

def load_prices(cfg=None):
    """
    Load daily OHLCV + Return + Log_Return for the main asset.
    Returns a DatetimeIndex DataFrame.
    """
    cfg = cfg or CONFIG
    cache = _cache_path(cfg["ticker"])

    if os.path.exists(cache):
        df = pd.read_csv(cache, index_col=0, parse_dates=True)
        print(f"Cached: {cfg['name']} ({len(df)} rows)")
        return df

    print(f"Downloading: {cfg['name']} ({cfg['ticker']})...")
    df = _download(cfg["ticker"], cfg["start"], cfg["end"])
    df["Return"] = df["Close"].pct_change()
    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
    df = df.dropna(subset=["Return"])

    df.to_csv(cache)
    print(f"Cached: {len(df)} rows -> {cache}")
    return df


def load_benchmark(cfg=None):
    """Load daily OHLCV + Return for the benchmark index."""
    cfg = cfg or CONFIG
    cache = _cache_path(cfg["benchmark_ticker"])

    if os.path.exists(cache):
        df = pd.read_csv(cache, index_col=0, parse_dates=True)
        return df

    print(f"Downloading benchmark: {cfg['benchmark_name']}...")
    df = _download(cfg["benchmark_ticker"], cfg["start"], cfg["end"])
    df["Return"] = df["Close"].pct_change()
    df = df.dropna(subset=["Return"])

    df.to_csv(cache)
    return df


def load_peers(cfg=None):
    """
    Load price data for every peer in the config.
    Returns dict  {display_name: DataFrame}.
    """
    cfg = cfg or CONFIG
    peers = {}

    for ticker, name in cfg["peers"].items():
        cache = _cache_path(ticker)

        if os.path.exists(cache):
            df = pd.read_csv(cache, index_col=0, parse_dates=True)
        else:
            print(f"Downloading peer: {name} ({ticker})...")
            df = _download(ticker, cfg["start"], cfg["end"])
            df["Return"] = df["Close"].pct_change()
            df = df.dropna(subset=["Return"])
            df.to_csv(cache)

        peers[name] = df

    return peers


def load_aligned(cfg=None):
    """
    Align asset and benchmark returns on shared dates.
    Returns DataFrame with columns ['asset', 'benchmark'].
    """
    cfg = cfg or CONFIG
    asset = load_prices(cfg)
    bench = load_benchmark(cfg)

    aligned = pd.DataFrame({
        "asset": asset["Return"],
        "benchmark": bench["Return"],
    }).dropna()

    return aligned


def load_fundamentals(cfg=None):
    """Return the yfinance Ticker.info dict (market cap, P/E, etc.)."""
    cfg = cfg or CONFIG
    return yf.Ticker(cfg["ticker"]).info


def load_financials(cfg=None):
    """Return (income_stmt, balance_sheet, cashflow) as DataFrames."""
    cfg = cfg or CONFIG
    tk = yf.Ticker(cfg["ticker"])
    return tk.income_stmt, tk.balance_sheet, tk.cashflow


def load_peer_fundamentals(cfg=None):
    """Return dict  {display_name: info_dict}  for all peers."""
    cfg = cfg or CONFIG
    result = {}
    for ticker, name in cfg["peers"].items():
        try:
            result[name] = yf.Ticker(ticker).info
        except Exception:
            result[name] = {}
    return result
