"""
ema_score.py
---------------------------------
EMA Quality Scoring Engine

Purpose:
- Evaluate EMA 50 reliability & usefulness
- Convert EMA state into weighted score
- Used for HTF confluence (NOT entry trigger)

Input:
- ema_state (from ema.py)
- market_structure (from structure.py)
- AOI context (optional, HTF)

Output:
- ema_score (int)
- confidence level
- reasoning (list[str])
"""

from enum import Enum
from typing import Dict, List, Optional

# =========================
# ENUMS
# =========================

class EmaConfidence(Enum):
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"

class MarketBias(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    TRANSITION = "transition"
    RANGE = "range"

# =========================
# SCORING CONFIG
# =========================

EMA_SCORE_WEIGHTS = {
    "slope_up": 10,
    "slope_down": 10,
    "price_above": 5,
    "price_below": 5,
    "rejection": 10,
    "structure_alignment": 15,
    "structure_conflict": -20,
    "flat_penalty": -15,
    "range_penalty": -10,
}

# =========================
# CORE LOGIC
# =========================

def score_ema(
    ema_state: Dict,
    structure_bias: MarketBias,
    in_aoi: bool = False,
) -> Dict:
    """
    Main EMA scoring function

    ema_state: output from ema.analyze_ema()
    structure_bias: HTF structure bias
    in_aoi: whether EMA is inside HTF AOI
    """

    score = 0
    reasons: List[str] = []

    if not ema_state.get("valid"):
        return {
            "ema_score": 0,
            "confidence": EmaConfidence.WEAK,
            "reasons": ["ema_invalid"]
        }

    slope = ema_state["slope"]
    position = ema_state["position"]
    rejection = ema_state["rejection"]

    # =========================
    # 1. EMA SLOPE (Momentum)
    # =========================
    if slope.name == "UP":
        score += EMA_SCORE_WEIGHTS["slope_up"]
        reasons.append("ema_slope_up")

    elif slope.name == "DOWN":
        score += EMA_SCORE_WEIGHTS["slope_down"]
        reasons.append("ema_slope_down")

    else:
        score += EMA_SCORE_WEIGHTS["flat_penalty"]
        reasons.append("ema_flat")

    # =========================
    # 2. PRICE POSITION
    # =========================
    if position.name == "ABOVE":
        score += EMA_SCORE_WEIGHTS["price_above"]
        reasons.append("price_above_ema")

    elif position.name == "BELOW":
        score += EMA_SCORE_WEIGHTS["price_below"]
        reasons.append("price_below_ema")

    # =========================
    # 3. REJECTION QUALITY
    # =========================
    if rejection in ("bullish_rejection", "bearish_rejection"):
        score += EMA_SCORE_WEIGHTS["rejection"]
        reasons.append(rejection)

    # =========================
    # 4. STRUCTURE ALIGNMENT
    # =========================
    if (
        structure_bias == MarketBias.BULLISH
        and slope.name == "UP"
    ):
        score += EMA_SCORE_WEIGHTS["structure_alignment"]
        reasons.append("ema_aligned_with_bull_structure")

    elif (
        structure_bias == MarketBias.BEARISH
        and slope.name == "DOWN"
    ):
        score += EMA_SCORE_WEIGHTS["structure_alignment"]
        reasons.append("ema_aligned_with_bear_structure")

    elif structure_bias in (MarketBias.TRANSITION, MarketBias.RANGE):
        score += EMA_SCORE_WEIGHTS["range_penalty"]
        reasons.append("structure_not_clean")

    else:
        score += EMA_SCORE_WEIGHTS["structure_conflict"]
        reasons.append("ema_structure_conflict")

    # =========================
    # 5. AOI CONTEXT (Optional)
    # =========================
    if in_aoi:
        score += 10
        reasons.append("ema_inside_htf_aoi")

    # =========================
    # 6. CONFIDENCE MAPPING
    # =========================
    if score >= 40:
        confidence = EmaConfidence.STRONG
    elif score >= 20:
        confidence = EmaConfidence.MODERATE
    else:
        confidence = EmaConfidence.WEAK

    return {
        "ema_score": score,
        "confidence": confidence,
        "reasons": reasons
    }
