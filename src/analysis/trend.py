# analysis/trend.py
from enum import Enum
from typing import Dict

class TrendBias(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    RANGE = "range"
    TRANSITION = "transition"

def classify_trend(
    structure: Dict,
    ema: Dict
) -> TrendBias:
    """
    Classify overall market trend.
    Conservative by design.
    """

    struct_bias = structure["bias"]
    ema_slope = ema["slope"]
    ema_pos = ema["position"]

    # 1. Strong bullish trend
    if (
        struct_bias == "bullish"
        and ema_slope == "up"
        and ema_pos in ("above", "cross_up")
    ):
        return TrendBias.BULLISH

    # 2. Strong bearish trend
    if (
        struct_bias == "bearish"
        and ema_slope == "down"
        and ema_pos in ("below", "cross_down")
    ):
        return TrendBias.BEARISH

    # 3. EMA flat or compression
    if ema_slope == "flat":
        return TrendBias.RANGE

    # 4. Conflict = transition
    return TrendBias.TRANSITION
