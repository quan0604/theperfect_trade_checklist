"""
aoi.py
---------------------------------
Area of Interest (AOI) Detection Engine

Purpose:
- Detect HTF AOI zones (Daily / H4)
- Detect LTF AOI zones (H1 / M30)
- Provide structured AOI objects (NOT scoring)

AOI Types:
- Demand
- Supply
"""

from enum import Enum
from typing import List, Dict
import pandas as pd

# =========================
# ENUMS
# =========================

class AOIType(Enum):
    DEMAND = "demand"
    SUPPLY = "supply"

class AOISource(Enum):
    HTF = "htf"
    LTF = "ltf"

# =========================
# AOI OBJECT
# =========================

def build_aoi(
    aoi_type: AOIType,
    source: AOISource,
    high: float,
    low: float,
    timeframe: str,
    origin_index: int
) -> Dict:
    return {
        "type": aoi_type,
        "source": source,
        "high": high,
        "low": low,
        "timeframe": timeframe,
        "origin_index": origin_index,
        "touches": 0,
        "reactions": [],
    }

# =========================
# HTF AOI DETECTION
# =========================

def detect_htf_aoi(
    df: pd.DataFrame,
    timeframe: str
) -> List[Dict]:
    """
    Detect HTF AOI zones based on:
    - Impulse move
    - Base candle(s)
    """

    aois = []

    for i in range(3, len(df) - 3):
        candle = df.iloc[i]
        next_candle = df.iloc[i + 1]

        # -------------------------
        # Bullish impulse origin
        # -------------------------
        if (
            candle['close'] < candle['open']  # bearish base
            and next_candle['close'] > next_candle['open']  # bullish expansion
            and (next_candle['close'] - next_candle['open']) >
               (candle['open'] - candle['close']) * 1.5
        ):
            aoi = build_aoi(
                aoi_type=AOIType.DEMAND,
                source=AOISource.HTF,
                high=candle['high'],
                low=candle['low'],
                timeframe=timeframe,
                origin_index=i
            )
            aois.append(aoi)

        # -------------------------
        # Bearish impulse origin
        # -------------------------
        if (
            candle['close'] > candle['open']
            and next_candle['close'] < next_candle['open']
            and (next_candle['open'] - next_candle['close']) >
               (candle['close'] - candle['open']) * 1.5
        ):
            aoi = build_aoi(
                aoi_type=AOIType.SUPPLY,
                source=AOISource.HTF,
                high=candle['high'],
                low=candle['low'],
                timeframe=timeframe,
                origin_index=i
            )
            aois.append(aoi)

    return aois
def detect_ltf_aoi(
    df: pd.DataFrame,
    timeframe: str,
    htf_aois: List[Dict]
) -> List[Dict]:
    """
    Detect LTF AOI only if price is reacting
    inside HTF AOI
    """

    aois = []

    for htf in htf_aois:
        zone_high = htf["high"]
        zone_low = htf["low"]

        # Filter candles inside HTF AOI
        zone_df = df[
            (df["low"] <= zone_high) &
            (df["high"] >= zone_low)
        ]

        for i in range(2, len(zone_df) - 2):
            candle = zone_df.iloc[i]

            # Simple base candle logic
            if abs(candle["close"] - candle["open"]) < (
                candle["high"] - candle["low"]
            ) * 0.3:

                aoi = build_aoi(
                    aoi_type=htf["type"],
                    source=AOISource.LTF,
                    high=candle["high"],
                    low=candle["low"],
                    timeframe=timeframe,
                    origin_index=i
                )
                aois.append(aoi)

    return aois
