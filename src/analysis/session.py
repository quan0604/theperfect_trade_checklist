"""
session.py
---------------------------------
Market Session Detection
"""

from enum import Enum
from datetime import datetime, time

class TradingSession(Enum):
    ASIA = "asia"
    LONDON = "london"
    NEW_YORK = "new_york"
    DEAD = "dead_zone"

def detect_session(timestamp: datetime) -> TradingSession:
    hour = timestamp.hour

    if 0 <= hour < 7:
        return TradingSession.ASIA

    if 7 <= hour < 13:
        return TradingSession.LONDON

    if 13 <= hour < 20:
        return TradingSession.NEW_YORK

    return TradingSession.DEAD
