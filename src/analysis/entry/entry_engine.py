# analysis/entry/entry_engine.py
import pandas as pd
from typing import Dict

from analysis.trend import TrendBias
from analysis.entry.entry_candle import detect_entry_candle
from analysis.entry.break_retest import detect_break_retest, BreakRetest
from analysis.entry.volume_filter import evaluate_volume
from analysis.entry.entry_score import grade_entry, EntryGrade

class EntryDecision(Enum):
    TRADE = "trade"
    WAIT = "wait"
    NO_TRADE = "no_trade"

def analyze_entry(
    df: pd.DataFrame,
    context: Dict
) -> Dict:
    """
    Discretionary Entry Engine
    """

    # =========================
    # 1. HARD FILTERS (NO MERCY)
    # =========================
    trend = context["trend_bias"]

    if trend not in (TrendBias.BULLISH, TrendBias.BEARISH):
        return {"decision": EntryDecision.NO_TRADE, "reason": "no_clear_trend"}

    if context["ema_confidence"] == "weak":
        return {"decision": EntryDecision.NO_TRADE, "reason": "ema_weak"}

    if not context.get("in_aoi", False):
        return {"decision": EntryDecision.NO_TRADE, "reason": "outside_aoi"}

    # =========================
    # 2. STRUCTURE CONFIRMATION
    # =========================
    br = detect_break_retest(
        df,
        structure_bias=context["structure_bias"]
    )

    if br == BreakRetest.INVALID:
        return {"decision": EntryDecision.NO_TRADE, "reason": "bad_retest"}

    # =========================
    # 3. ENTRY CANDLE
    # =========================
    entry = detect_entry_candle(
        df,
        direction=trend.value
    )

    if entry["signal"].name == "NONE":
        return {"decision": EntryDecision.WAIT, "reason": "no_entry_candle"}

    # =========================
    # 4. VOLUME CONFIRMATION
    # =========================
    volume_state = evaluate_volume(df)

    # =========================
    # 5. ENTRY QUALITY GRADING
    # =========================
    grading_context = {
        "trend": trend.value,
        "ema_score": context["ema_score"],
        "entry_signal": entry["signal"].value,
        "volume": volume_state.value
    }

    grade = grade_entry(grading_context)

    if grade == EntryGrade.SKIP:
        return {"decision": EntryDecision.NO_TRADE, "reason": "low_quality"}

    # =========================
    # 6. FINAL ENTRY
    # =========================
    return {
        "decision": EntryDecision.TRADE,
        "entry_type": entry["signal"].value,
        "grade": grade.value,
        "volume": volume_state.value,
    }
