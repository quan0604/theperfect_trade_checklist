# Strategy Specification

This document details the multi-timeframe (MTF) trading logic. The tool analyzes high timeframes (Weekly, Daily, 4H) for context and lower timeframes (1H, 30m) for entries, computes confluence, and recommends trade setups based on overall quality.

---

## I. High Timeframe Analysis (Context: Weekly, Daily, 4H)

For each timeframe, analyze the following factors, assign points, and sum for total confluence (max 100%). Example: ≥70% = strong context.

1. **Trend**
    - Bullish: Close > EMA 20 > EMA 50 > EMA 200. +20% (strong), +10% (weak)
    - Bearish: Reverse order. As above.
    - Sideways: Close ~ EMA 20 (±1%). 0%. Avoid trading.
    - Trend Change: Break EMA 200 with volume >150% average and confirmed close. +15%.
2. **Area of Interest (AOI)/Rejection**
    - AOI: Historical S/R from swing high/low (last 50 candles). Zone: 20-50 pips (tighter for 4H).
    - Rejection: Touch AOI & bounce with volume. +15% (strong), +10% (weak)
    - Strong AOI: ≥3 tests. Weak: 1-2 tests.
3. **Touches EMA**
    - Touches EMA 20/50/200 (±5 pips). +10% (dynamic EMA in trend)
    - Bounce from EMA w/rejection candle: +15%.
4. **Psychological Levels**
    - Round levels: e.g., 1.0000, 1.0500 (50 pip intervals). +10% if ≤10 pips and aligns with AOI
5. **Structure Rejection**
    - Rejects former structure (failed break HH/LL then reverses). +15% if confirmed (look back 20 candles)
6. **Rejection Candle in AOI**
    - Wick ≥2x body, volume ≥150% average. +20% at AOI, +10% elsewhere
    - Bullish pin: Long lower wick, Close > Open
    - Bearish pin: Long upper wick, Close < Open
7. **Pattern: Break & Retest / Head & Shoulders**
    - Break & Retest: Break AOI, retest, hold. +20% confirmed
    - H&S (or Inverse): Left/right shoulder, clear neckline, break. +25% (clear, AI confirmed), +15% (partial)

**Scoring:**
- Total = sum (cap at 100%). Example: Trend +20, AOI +15, EMA +10, Psych +10, Structure +15, Candle +20, Pattern +25 = 115% (cap 100%).
- Thresholds: ≥70% Strong / 50-70% Medium / <50% Weak - Avoid

---

## II. Lower Timeframe Signal Analysis (1H, 30m)

1. **Trend** (short-term, as above)
    - +30% if aligned with higher timeframe
2. **Touching EMA**
    - Touches EMA 20/50 (±5 pips). +30% if bounce aligns with trend
3. **Pattern: Break & Retest / H&S**
    - Same as above, focus: last 20 candles. +40% confirmed
4. **Zone/Target/Stop (from 4H AOI)**
    - Tight zone from 4H (≤30 pips, recent swings). Used for entry/exit targets
5. **Signal Confluence Calculation**
    - Score each: trend, EMA, pattern (cap at 100%).
    - Signal confluence = (1H + 30m)/2. Threshold ≥60% is good signal.

---

## III. Trade Setup Aggregation

- **Overall Confluence** = (High TF confluence × 0.6) + (Signal confluence × 0.4)
- ≥80% = High-confidence setup
- Structure Quality: Good if all MTF align, No divergence (e.g. bullish higher, bearish lower = BAD)
- Recommendation logic:
    - "Trade recommended" if ≥80% and structure good
    - "Avoid - bad structure" if <50% or divergence
    - "Wait/Watch only" if medium but risky (e.g. before news)
- AI Opinion: Use AI/LLM to judge pattern clarity (e.g., H&S obviousness)

---

## IV. General Rules

- Always use Close price for confirmations
- Volume must be above average for validity
- Cap total confluence at 100%

---

*Summary Table:*

| Score | Structure | Recommendation         |
|-------|-----------|------------------------|
| ≥80%  | Good      | Trade                  |
| <50%  | Any       | Avoid                  |
| 50-79%| Medium    | Wait/Watch (if risky)  |