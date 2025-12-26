"""
ema.py
---------------------------------
EMA 50 Logic Engine – CORE (Phase 2.2 – 2.4)

Responsibilities:
- Calculate EMA 50
- Normalize EMA slope using ATR (volatility aware)
- Determine price position vs EMA (Above / Below / Cross / Touch)
- Detect EMA rejection as dynamic Support / Resistance
- Structure-aware filtering (HTF bias ready)

Timeframes:
- All (M30 / H1 / H4 / D1)
"""

from enum import Enum
import pandas as pd
import numpy as np


# =========================
# ENUMS
# =========================

class EmaSlope(Enum):
    UP = "up"
    DOWN = "down"
    FLAT = "flat"


class EmaPosition(Enum):
    ABOVE = "above"
    BELOW = "below"
    CROSS_UP = "cross_up"
    CROSS_DOWN = "cross_down"
    ON_ZONE = "on_zone"


class EmaRejection(Enum):
    BULLISH = "bullish_rejection"
    BEARISH = "bearish_rejection"
    NONE = "none"


class MarketBias(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


# =========================
# CORE CALCULATIONS
# =========================

def calculate_ema(df: pd.DataFrame, period: int = 50) -> pd.Series:
    """Calculate EMA"""
    return df["close"].ewm(span=period, adjust=False).mean()


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range for volatility normalization"""
    high = df["high"]
    low = df["low"]
    close = df["close"].shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - close).abs(),
            (low - close).abs()
        ],
        axis=1
    ).max(axis=1)

    return tr.rolling(period).mean()


# =========================
# EMA LOGIC
# =========================

def detect_slope(
    ema: pd.Series,
    atr: pd.Series,
    lookback: int = 3,
    slope_factor: float = 0.15
) -> EmaSlope:
    """
    Detect EMA slope normalized by ATR.

    slope = delta EMA / ATR

    - Positive & strong -> UP
    - Negative & strong -> DOWN
    - Otherwise -> FLAT
    """

    if len(ema) < lookback + 1 or atr.isna().iloc[-1]:
        return EmaSlope.FLAT

    delta = ema.iloc[-1] - ema.iloc[-lookback]
    normalized_slope = delta / atr.iloc[-1]

    if normalized_slope > slope_factor:
        return EmaSlope.UP
    elif normalized_slope < -slope_factor:
        return EmaSlope.DOWN
    return EmaSlope.FLAT


def detect_position(
    df: pd.DataFrame,
    ema: pd.Series,
    zone_atr_factor: float = 0.2
) -> EmaPosition:
    """
    Determine price position relative to EMA.
    Structure-aware via candle close sequencing.
    """

    close_now = df["close"].iloc[-1]
    close_prev = df["close"].iloc[-2]

    ema_now = ema.iloc[-1]
    ema_prev = ema.iloc[-2]

    atr = calculate_atr(df).iloc[-1]
    zone_buffer = atr * zone_atr_factor

    # Touch / reaction zone
    if abs(close_now - ema_now) <= zone_buffer:
        return EmaPosition.ON_ZONE

    # Cross logic (momentum shift)
    if close_prev < ema_prev and close_now > ema_now:
        return EmaPosition.CROSS_UP

    if close_prev > ema_prev and close_now < ema_now:
        return EmaPosition.CROSS_DOWN

    if close_now > ema_now:
        return EmaPosition.ABOVE

    return EmaPosition.BELOW


def detect_rejection(
    df: pd.DataFrame,
    ema: pd.Series,
    atr: pd.Series,
    slope: EmaSlope,
    bias: MarketBias = MarketBias.NEUTRAL
) -> EmaRejection:
    """
    Detect EMA rejection as dynamic S/R.
    Structure & trend aware.
    """

    candle = df.iloc[-1]
    ema_val = ema.iloc[-1]
    atr_val = atr.iloc[-1]

    body = abs(candle["close"] - candle["open"])
    upper_wick = candle["high"] - max(candle["open"], candle["close"])
    lower_wick = min(candle["open"], candle["close"]) - candle["low"]

    # Bullish rejection (EMA as support)
    if (
        candle["low"] <= ema_val
        and candle["close"] > ema_val
        and lower_wick > body * 1.2
        and slope != EmaSlope.DOWN
        and bias != MarketBias.BEARISH
    ):
        return EmaRejection.BULLISH

    # Bearish rejection (EMA as resistance)
    if (
        candle["high"] >= ema_val
        and candle["close"] < ema_val
        and upper_wick > body * 1.2
        and slope != EmaSlope.UP
        and bias != MarketBias.BULLISH
    ):
        return EmaRejection.BEARISH

    return EmaRejection.NONE


# =========================
# MAIN ENTRY POINT
# =========================

def analyze_ema(
    df: pd.DataFrame,
    timeframe: str,
    ema_period: int = 50,
    market_bias: MarketBias = MarketBias.NEUTRAL
) -> dict:
    """
    Main EMA analysis entry.
    Used by Confluence Engine (Phase 2.6)
    """

    if len(df) < ema_period + 20:
        return {"valid": False, "reason": "not_enough_data"}

    ema = calculate_ema(df, ema_period)
    atr = calculate_atr(df)

    slope = detect_slope(ema, atr)
    position = detect_position(df, ema)
    rejection = detect_rejection(df, ema, atr, slope, market_bias)

    price = df["close"].iloc[-1]
    ema_val = ema.iloc[-1]

    return {
        "valid": True,
        "timeframe": timeframe,
        "ema_value": ema_val,
        "price": price,
        "distance_atr": (price - ema_val) / atr.iloc[-1],
        "slope": slope,
        "position": position,
        "rejection": rejection,
    }
