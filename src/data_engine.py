import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz
import time
import os
import sys
import yaml
import streamlit as st
import streamlit as st
# =========================
# CONFIG
# =========================
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

TIMEFRAMES = {
    "Weekly": mt5.TIMEFRAME_W1,
    "Daily": mt5.TIMEFRAME_D1,
    "4H": mt5.TIMEFRAME_H4,
    "1H": mt5.TIMEFRAME_H1,
    "30m": mt5.TIMEFRAME_M30
}

MIN_BARS = {
    "Weekly": 80,
    "Daily": 120,
    "4H": 200,
    "1H": 300,
    "30m": 500
}

# =========================
# MT5 CONNECTION
# =========================
def connect_mt5():
    terminal_path = os.getenv("MT5_PATH")
    login = int(os.getenv("MT5_LOGIN"))
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")

    if not mt5.initialize(
        path=terminal_path,
        login=login,
        password=password,
        server=server
    ):
        raise ConnectionError(f"MT5 initialize failed: {mt5.last_error()}")

    print("✅ MT5 connected")

def reconnect_mt5():
    print("[INFO] Reconnecting MT5...")
    mt5.shutdown()
    time.sleep(1)
    connect_mt5()

# =========================
# DATA STANDARDIZATION
# =========================
def standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[["open", "high", "low", "close", "tick_volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.sort_index(inplace=True)
    return df

# =========================
# FETCH RAW DATA
# =========================
def fetch_rates(symbol, timeframe, from_date, to_date):
    if not mt5.symbol_select(symbol, True):
        raise ValueError(f"Symbol {symbol} not tradable")

    rates = mt5.copy_rates_range(symbol, timeframe, from_date, to_date)
    if rates is None or len(rates) == 0:
        raise ValueError("No data returned")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s").dt.tz_localize("UTC")
    return df.set_index("time")

# =========================
# RETRY WRAPPER (TASK 1.7 CORE)
# =========================
def fetch_with_retry(symbol, tf_label, tf, from_date, to_date):
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fetch_rates(symbol, tf, from_date, to_date)

        except Exception as e:
            last_error = str(e)
            print(f"[WARN] {symbol} {tf_label} retry {attempt}/{MAX_RETRIES} – {last_error}")
            time.sleep(RETRY_DELAY)

            # Auto reconnect if MT5 issue
            if "initialize" in last_error.lower() or "mt5" in last_error.lower():
                reconnect_mt5()

    raise RuntimeError(last_error)

# =========================


# =========================
# MULTI TIMEFRAME FETCH
# =========================
def fetch_multi_timeframe(symbol, days_back=60):
    to_date = datetime.utcnow().replace(tzinfo=pytz.UTC)
    from_date = to_date - timedelta(days=days_back)
    tf_context = {}

    for label, tf in TIMEFRAMES.items():
        try:
            raw_df = fetch_with_retry(symbol, label, tf, from_date, to_date)
            df = standardize_dataframe(raw_df)

            bars = len(df)
            valid = bars >= MIN_BARS[label]

            tf_context[label] = {
                "df": df,
                "bars": bars,
                "valid": valid,
                "suitable": valid,
                "price": {
                    "close": df["close"].iloc[-1],
                    "high": df["high"].iloc[-1],
                    "low": df["low"].iloc[-1],
                },
                "error": None
            }

        except Exception as e:
            tf_context[label] = {
                "df": None,
                "bars": 0,
                "valid": False,
                "suitable": False,
                "price": None,
                "error": str(e)
            }

    return tf_context

# =========================
# MARKET CONTEXT
# =========================
@st.cache_data(ttl=300, show_spinner="📡 Fetching market data...")
def build_market_context(symbol, days_back=60):
    return {
        "symbol": symbol,
        "last_update": datetime.utcnow(),
        "timeframes": fetch_multi_timeframe(symbol, days_back),
        "meta": {
            "source": "MetaTrader5",
            "timezone": "UTC",
            "cached": True
        }
    }

# =========================
# WATCHLIST
# =========================
def load_watchlist_from_yaml(file_path="watchlist.yaml"):
    with open(file_path, encoding="utf-8") as f:
        y = yaml.safe_load(f)

    symbols = []
    for group in y.values():
        symbols.extend(
            [s.upper().replace("/", "").replace("-", "") for s in group]
        )

    return sorted(set(symbols))

WATCHLIST = load_watchlist_from_yaml()

def fetch_all_watchlist(watchlist, days_back=60):
    results = {}

    for symbol in watchlist:
        try:
            results[symbol] = build_market_context(symbol, days_back)
        except Exception as e:
            print(f"[ERROR] {symbol} skipped – {e}")

    return results

# =========================
# SHUTDOWN
# =========================
def shutdown_mt5():
    mt5.shutdown()
    print("🛑 MT5 shutdown")

# =========================
# CLI TEST
# =========================
if __name__ == "__main__":
    try:
        symbol = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
        connect_mt5()

        ctx = build_market_context(symbol)

        print(f"\n📊 Market Context for {symbol}")
        for tf, info in ctx["timeframes"].items():
            print(
                f"{tf}: valid={info['valid']}, "
                f"suitable={info['suitable']}, "
                f"bars={info['bars']}, "
                f"error={info['error']}"
            )

    except Exception as e:
        print("❌ Fatal error:", e)

    finally:
        shutdown_mt5()
