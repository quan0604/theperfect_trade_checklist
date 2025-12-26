# analysis/entry/entry_score.py
from enum import Enum

class EntryGrade(Enum):
    A_PLUS = "A+"
    A = "A"
    B = "B"
    SKIP = "skip"

def grade_entry(context: dict) -> EntryGrade:
    score = 0

    if context["trend"] in ("bullish", "bearish"):
        score += 20

    if context["ema_score"] >= 40:
        score += 20

    if context["entry_signal"] != "none":
        score += 20

    if context["volume"] == "high":
        score += 10

    if score >= 60:
        return EntryGrade.A_PLUS
    if score >= 45:
        return EntryGrade.A
    if score >= 30:
        return EntryGrade.B

    return EntryGrade.SKIP
