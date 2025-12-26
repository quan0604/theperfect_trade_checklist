"""
aoi_score.py
---------------------------------
AOI Quality Scoring Engine

Purpose:
- Evaluate AOI zone quality (Demand / Supply)
- Score AOI strength for confluence (NOT entry trigger)
- Used together with EMA score & Structure

Inputs:
- aoi (from aoi.py)
- market_structure (from structure.py)
- optional EMA context

Output:
- aoi_score (int)
- confidence level
- reasoning (list[str])
"""

from enum import Enum
from typing import Dict, List, Optional

# =========================
# ENUMS
# =========================

class AOIConfidence(Enum):
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"


class StructureBias(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    TRANSITION = "transition"
    RANGE = "range"


class AOIType(Enum):
    DEMAND = "demand"
    SUPPLY = "supply"


class AOISource(Enum):
    HTF = "htf"
    LTF = "ltf"


# =========================
# SCORING WEIGHTS
# =========================

AOI_SCORE_WEIGHTS = {
    # Freshness
    "fresh_zone": 20,
    "tested_once": 10,
    "over_tested": -20,

    # Reactions
    "strong_reaction": 15,
    "weak_reaction": 5,

    # Source
    "htf_bonus": 15,
    "ltf_bonus": 5,

    # Structure alignment
    "structure_alignment": 20,
    "structure_conflict": -25,

    # Penalties
    "range_penalty": -10,
}


# =========================
# CORE LOGIC
# =========================

def score_aoi(
    aoi: Dict,
    structure_bias: StructureBias,
    ema_context: Optional[Dict] = None,
) -> Dict:
    """
    Score a single AOI zone.

    aoi: output from aoi.build_aoi()
    structure_bias: HTF structure bias
    ema_context: optional EMA context (from ema.py)
    """

    score = 0
    reasons: List[str] = []

    aoi_type = aoi["type"]
    source = aoi["source"]
    touches = aoi.get("touches", 0)
    reactions = aoi.get("reactions", [])

    # =========================
    # 1. FRESHNESS / TOUCHES
    # =========================

    if touches == 0:
        score += AOI_SCORE_WEIGHTS["fresh_zone"]
        reasons.append("fresh_aoi")

    elif touches == 1:
        score += AOI_SCORE_WEIGHTS["tested_once"]
        reasons.append("aoi_tested_once")

    else:
        score += AOI_SCORE_WEIGHTS["over_tested"]
        reasons.append("aoi_over_tested")

    # =========================
    # 2. REACTION QUALITY
    # =========================

    if reactions:
        strong_reactions = [
            r for r in reactions if r.get("strength") == "strong"
        ]

        if strong_reactions:
            score += AOI_SCORE_WEIGHTS["strong_reaction"]
            reasons.append("strong_reaction_from_aoi")
        else:
            score += AOI_SCORE_WEIGHTS["weak_reaction"]
            reasons.append("weak_reaction_from_aoi")

    # =========================
    # 3. HTF / LTF SOURCE
    # =========================

    if source == AOISource.HTF:
        score += AOI_SCORE_WEIGHTS["htf_bonus"]
        reasons.append("htf_aoi")

    elif source == AOISource.LTF:
        score += AOI_SCORE_WEIGHTS["ltf_bonus"]
        reasons.append("ltf_aoi")

    # =========================
    # 4. STRUCTURE ALIGNMENT
    # =========================

    if structure_bias == StructureBias.RANGE:
        score += AOI_SCORE_WEIGHTS["range_penalty"]
        reasons.append("range_structure_penalty")

    else:
        if (
            aoi_type == AOIType.DEMAND
            and structure_bias == StructureBias.BULLISH
        ):
            score += AOI_SCORE_WEIGHTS["structure_alignment"]
            reasons.append("demand_aligned_with_bull_structure")

        elif (
            aoi_type == AOIType.SUPPLY
            and structure_bias == StructureBias.BEARISH
        ):
            score += AOI_SCORE_WEIGHTS["structure_alignment"]
            reasons.append("supply_aligned_with_bear_structure")

        else:
            score += AOI_SCORE_WEIGHTS["structure_conflict"]
            reasons.append("aoi_conflicts_with_structure")

    # =========================
    # 5. EMA CONTEXT (OPTIONAL)
    # =========================

    if ema_context:
        if ema_context.get("rejection") in (
            "bullish_rejection",
            "bearish_rejection",
        ):
            score += 10
            reasons.append("ema_rejection_inside_aoi")

    # =========================
    # 6. CONFIDENCE MAPPING
    # =========================

    if score >= 50:
        confidence = AOIConfidence.STRONG
    elif score >= 25:
        confidence = AOIConfidence.MODERATE
    else:
        confidence = AOIConfidence.WEAK

    return {
        "aoi_score": score,
        "confidence": confidence,
        "reasons": reasons,
    }
