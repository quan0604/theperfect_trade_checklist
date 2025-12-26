# analysis/entry/volume_filter.py

def evaluate_volume(
    df: pd.DataFrame,
    lookback: int = 20,
    entry_type: str | None = None
) -> VolumeState:

    vol_now = df["volume"].iloc[-1]
    vol_avg = df["volume"].rolling(lookback).mean().iloc[-1]

    if entry_type and "momentum" in entry_type:
        if vol_now > vol_avg * 1.4:
            return VolumeState.HIGH
        return VolumeState.LOW

    if vol_now > vol_avg * 1.1:
        return VolumeState.NORMAL

    return VolumeState.LOW
