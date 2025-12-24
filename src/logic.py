import pandas as pd
import talib

def calculate_ema(df, period=20):
    """
    Add EMA column to DataFrame.
    """
    df[f'EMA_{period}'] = talib.EMA(df['close'], timeperiod=period)
    return df

def detect_aoi(df, window=50, threshold=0.01):
    """
    Detect Area of Interest (support/resistance) zones from swing high/low.
    """
    highs = df['high'].rolling(window).max()
    lows = df['low'].rolling(window).min()
    zones = pd.DataFrame({'AOI_High': highs, 'AOI_Low': lows})
    return zones


