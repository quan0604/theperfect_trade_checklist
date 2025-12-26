"""
psych_levels.py
---------------------------------
Psychological Price Levels Detector

Purpose:
- Detect round-number levels
- Evaluate proximity of price to key levels
"""

from enum import Enum
from typing import Dict, List

class PsychLevelType(Enum):
    BIG = "big_round"     # 1.2000
    HALF = "half_round"   # 1.2050
    QUARTER = "quarter"   # 1.2025

def detect_psych_levels(
    price: float,
    pip_size: float = 0.0001
) -> List[Dict]:
    """
    Return nearby psychological levels.
    """

    levels = []

    base = round(price / pip_size) * pip_size

    candidates = [
        (PsychLevelType.BIG, round(base, 4)),
        (PsychLevelType.HALF, round(base + 50 * pip_size, 4)),
        (PsychLevelType.HALF, round(base - 50 * pip_size, 4)),
    ]

    for level_type, level_price in candidates:
        distance_pips = abs(price - level_price) / pip_size

        if distance_pips <= 15:
            levels.append({
                "type": level_type.value,
                "price": level_price,
                "distance_pips": distance_pips
            })

    return levels
