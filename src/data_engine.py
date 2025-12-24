import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz
import sys

# Define standard multi-timeframes
TIMEFRAMES = {
    "Weekly": mt5.TIMEFRAME_W1,
    "Daily": mt5.TIMEFRAME_D1,
    "4H": mt5.TIMEFRAME_H4,
    "1H": mt5.TIMEFRAME_H1,
    "30m": mt5.TIMEFRAME_M30
}

def connect_mt5(terminal_path=r"C:\Program Files\MetaTrader 5\terminal64.exe", login=270462811, password="Quan0604@", server="Exness-MT5Trial17"):
    """
    Connect to MetaTrader 5 terminal.
    Args:
        terminal_path: path to terminal64.exe (optional).
        login, password, server: credentials if needed (optional).
    Returns:
        None -- raises Exception if connection fails.
    """
    if terminal_path:
        initialized = mt5.initialize(path=terminal_path, login=login, password=password, server=server)
    else:
        initialized = mt5.initialize()
    
    if not initialized:
        raise ConnectionError(f"MT5 initialize failed. Error code: {mt5.last_error()}")
    
    print("MT5 connected successfully. Terminal info:", mt5.terminal_info())

def fetch_rates(symbol, timeframe, from_date, to_date):
    """
    Fetch OHLCV data for a symbol for a given timeframe.
    Returns:
        pd.DataFrame indexed by UTC time (or raises error if not available).
    """
    if not mt5.symbol_select(symbol, True):
        raise ValueError(f"Symbol {symbol} not found or not tradable.")
    rates = mt5.copy_rates_range(symbol, timeframe, from_date, to_date)
    if rates is None or len(rates) == 0:
        raise ValueError(f"No data for {symbol} on {timeframe}.")
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s').dt.tz_localize('UTC')
    return df.set_index('time')

def fetch_multi_timeframe(symbol, days_back=60):
    """
    Fetch data for all timeframes for a symbol.
    Returns a dict of DataFrames {timeframe_label: df}.
    """
    to_date = datetime.utcnow().replace(tzinfo=pytz.UTC)
    from_date = to_date - timedelta(days=days_back)
    data_dict = {}
    errors = {}
    for label, tf in TIMEFRAMES.items():
        try:
            df = fetch_rates(symbol, tf, from_date, to_date)
            data_dict[label] = df
        except Exception as e:
            errors[label] = str(e)
            print(f"Warning: {label} fetch failed for {symbol}: {e}")
    return data_dict, errors

def fetch_all_watchlist(watchlist, days_back=60):
    """
    Fetch all timeframes for all symbols in the watchlist.
    Returns a dict: {symbol: (data_dict, errors_dict)}
    """
    all_data = {}
    for symbol in watchlist:
        print(f"\nFetching data for {symbol}...")
        data, errors = fetch_multi_timeframe(symbol, days_back)
        all_data[symbol] = (data, errors)
    return all_data

import yaml

def load_watchlist_from_yaml(file_path="watchlist.yaml"):
    """
    Load watchlist symbols from a YAML file.
    Supports majors, crosses, commodities groups.
    Returns a flat list of all symbols.
    """
    with open(file_path, encoding="utf-8") as f:
        y = yaml.safe_load(f)
    symbols = []
    for group in y.values():
        symbols.extend([s.replace("/", "") for s in group])
    return symbols

WATCHLIST = load_watchlist_from_yaml()

def shutdown_mt5():
    if mt5.shutdown():
        print("MT5 shutdown successful.")
    else:
        print("MT5 shutdown failed!")

if __name__ == "__main__":

    try:
        # CLI: python src/data_engine.py EURUSD  (or use input)
        symbol = sys.argv[1] if len(sys.argv) > 1 else input("Enter symbol (e.g. EURUSD): ").strip().upper()
        terminal_path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
        login = 270462811
        password = "Quan0604@"
        server = "Exness-MT5Trial17"
        connect_mt5(terminal_path=terminal_path, login=login, password=password, server=server)
        data, errors = fetch_multi_timeframe(symbol)
        for label, df in data.items():
            print(f"\n{label} data shape: {df.shape}")
            print(df.tail(5))
        if errors:
            print("\nThe following timeframes failed:", errors)
    except Exception as e:
        print("Fatal error:", e)
    finally:
        shutdown_mt5()
