"""
structure.py
---------------------------------
Market Structure Detection Engine

Purpose:
- Detect swing highs / lows
- Identify HH / HL / LH / LL
- Detect BOS (Break of Structure)
- Classify structure bias:
    - Bullish
    - Bearish
    - Transition / Range

Timeframes:
- Primary: 4H, 1H
"""

from enum import Enum
import pandas as pd
import numpy as np

class StructureBias(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    TRANSITION = "transition"
    RANGE = "range"

class SwingPoint:
    def __init__(self, index, price, kind):
        """
        kind: 'high' or 'low'
        """
        self.index = index
        self.price = price
        self.kind = kind

    def __repr__(self):
        return f"{self.kind.upper()} @ {self.price:.5f}"

def detect_swings(
    df: pd.DataFrame,
    lookback: int = 5
) -> list[SwingPoint]:
    """
    Detect swing highs and lows using vectorized rolling window logic.
    Includes 'ZigZag' logic to ensure strictly alternating Highs and Lows.
    """
    df = df.copy()
    
    # 1. Vectorized ID of local Max/Min
    # Rolling max/min with center=True looks ahead and behind
    # But Pandas rolling(center=True) is tricky with lookahead in a live loop context.
    # Here we simulate: High[i] > High[i-N...i-1] AND High[i] > High[i+1...i+N]
    
    # Using shift to check neighbors (Vectorized for fixed window)
    # Default lookback=5 means strict pivot
    
    is_pivot_high = np.full(len(df), True)
    is_pivot_low = np.full(len(df), True)
    
    for i in range(1, lookback + 1):
        # Check neighbors left and right
        is_pivot_high &= (df['high'] > df['high'].shift(i)) & (df['high'] > df['high'].shift(-i))
        is_pivot_low &= (df['low'] < df['low'].shift(i)) & (df['low'] < df['low'].shift(-i))

    # Extract potential points
    high_indices = df.index[is_pivot_high]
    low_indices = df.index[is_pivot_low]
    
    candidates = []
    
    for idx in high_indices:
        candidates.append(SwingPoint(idx, df.loc[idx, 'high'], 'high'))
        
    for idx in low_indices:
        candidates.append(SwingPoint(idx, df.loc[idx, 'low'], 'low'))
        
    # Sort by time
    candidates.sort(key=lambda s: s.index)
    
    if not candidates:
        return []

    # 2. Cleanup: Enforce Alternating High/Low (ZigZag Logic)
    # If consecutive Highs: Keep the Higher one
    # If consecutive Lows: Keep the Lower one
    
    clean_swings = [candidates[0]]
    
    for current in candidates[1:]:
        last = clean_swings[-1]
        
        if current.kind == last.kind:
            # Same type? Update if better
            if current.kind == 'high':
                if current.price > last.price:
                    clean_swings[-1] = current # Replace with higher high
            else: # low
                if current.price < last.price:
                    clean_swings[-1] = current # Replace with lower low
        else:
            # Different type? Add it
            clean_swings.append(current)
            
    return clean_swings

def classify_structure_from_swings(swings: list[SwingPoint]) -> StructureBias:
    """
    Determine market structure from last swing sequence.
    Expects strictly alternating swings from detect_swings().
    """

    if len(swings) < 4:
        return StructureBias.TRANSITION

    last = swings[-4:] # Look at last 4 points (L, H, HL, HH)
    
    prices = [s.price for s in last]
    kinds = [s.kind for s in last]

    # Bullish Sequence: Low -> High -> Higher Low -> Higher High
    if (
        kinds == ["low", "high", "low", "high"] and
        prices[2] > prices[0] and  # HL > L
        prices[3] > prices[1]      # HH > H
    ):
        return StructureBias.BULLISH

    # Bearish Sequence: High -> Low -> Lower High -> Lower Low
    if (
        kinds == ["high", "low", "high", "low"] and
        prices[2] < prices[0] and  # LH < H
        prices[3] < prices[1]      # LL < L
    ):
        return StructureBias.BEARISH
        
    # Note: Complex structures (expanding wedge etc) default to TRANSITION
    # until a clear break occurs.
    
    return StructureBias.TRANSITION

def detect_bos(
    df: pd.DataFrame,
    swings: list[SwingPoint],
    bias: StructureBias
) -> bool:
    """
    Detect Break of Structure (BOS) on the live/last candle.
    """
    if not swings or bias == StructureBias.RANGE or bias == StructureBias.TRANSITION:
        return False

    current_close = df["close"].iloc[-1]
    
    # Get last relevant swing
    if bias == StructureBias.BULLISH:
        # Find last High
        last_high = next((s for s in reversed(swings) if s.kind == 'high'), None)
        if last_high and current_close > last_high.price:
            return True
            
    elif bias == StructureBias.BEARISH:
        # Find last Low
        last_low = next((s for s in reversed(swings) if s.kind == 'low'), None)
        if last_low and current_close < last_low.price:
            return True

    return False

def analyze_market_structure(
    df: pd.DataFrame,
    lookback: int = 5
) -> dict:
    swings = detect_swings(df, lookback)
    bias = classify_structure_from_swings(swings)
    bos = detect_bos(df, swings, bias)

    return {
        "bias": bias,
        "swings": swings,
        "bos": bos
    }
