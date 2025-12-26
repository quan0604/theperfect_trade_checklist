# analysis/entry/entry_candle.py

def detect_entry_candle(
    df: pd.DataFrame,
    direction: str,
    at_key_level: bool = False,
) -> dict:

    candle = df.iloc[-1]
    prev = df.iloc[-2]

    body = abs(candle["close"] - candle["open"])
    range_ = candle["high"] - candle["low"]

    if range_ == 0:
        return {"signal": EntrySignal.NONE}

    upper_wick = candle["high"] - max(candle["open"], candle["close"])
    lower_wick = min(candle["open"], candle["close"]) - candle["low"]

    close_position = (candle["close"] - candle["low"]) / range_

    # =========================
    # 1. REJECTION (QUALITY)
    # =========================
    if at_key_level:
        if (
            direction == "bullish"
            and candle["close"] > candle["open"]
            and lower_wick > body * 1.3
            and close_position > 0.6
        ):
            return {"signal": EntrySignal.BULLISH_REJECTION}

        if (
            direction == "bearish"
            and candle["close"] < candle["open"]
            and upper_wick > body * 1.3
            and close_position < 0.4
        ):
            return {"signal": EntrySignal.BEARISH_REJECTION}

    # =========================
    # 2. MOMENTUM (BREAK STYLE)
    # =========================
    if body > range_ * 0.65:
        if direction == "bullish" and candle["close"] > prev["high"]:
            return {"signal": EntrySignal.BULLISH_MOMENTUM}

        if direction == "bearish" and candle["close"] < prev["low"]:
            return {"signal": EntrySignal.BEARISH_MOMENTUM}

    return {"signal": EntrySignal.NONE}
