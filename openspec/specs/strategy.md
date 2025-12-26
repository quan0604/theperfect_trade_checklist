📌 Strategy Specification – EMA50 MTF Trading System

This document defines the EMA50-centric multi-timeframe (MTF) trading strategy used by the system.
The tool is designed as a decision-support assistant for discretionary traders, not an automated trading system.

🎯 Core Philosophy

EMA 50 is the ONLY moving average used

EMA50 defines:

Trend direction

Dynamic support / resistance

Pullback & continuation zones

Trade only when:

Market structure is clear

Price reacts around EMA50 and AOI

Multi-timeframe confluence exists

I. High Timeframe Context Analysis

Timeframes: Weekly, Daily, 4H
Purpose: Determine directional bias & trade permission

HTF Confluence Score: max 100%
≥70% = Valid market context

1️⃣ Market Structure (MANDATORY)

Bullish structure

Higher High (HH) + Higher Low (HL)

Price respected EMA50 as support

+30%

Bearish structure

Lower Low (LL) + Lower High (LH)

Price respected EMA50 as resistance

+30%

Transition / Range

Mixed HH/LL or EMA50 flat

❌ 0% – No trade allowed

📌 If structure is invalid → system blocks all trades regardless of score

2️⃣ EMA50 Position & Slope

Price above EMA50, EMA50 sloping up → +20%

Price below EMA50, EMA50 sloping down → +20%

EMA50 flat or price crossing back & forth → 0%

📌 EMA50 slope is evaluated over the last 20 candles

3️⃣ Area of Interest (AOI – HTF)

AOI defined by:

Key swing high / low

EMA50 confluence

Previous reaction zones

Scoring:

Strong AOI (≥3 clean reactions) → +20%

Weak AOI (1–2 reactions) → +10%

No AOI → 0%

📌 AOI zone width:

Weekly/Daily: 40–60 pips

4H: 20–40 pips

4️⃣ EMA50 Rejection at AOI

Price touches EMA50 inside AOI and rejects

Rejection candle with:

Wick ≥ 2× body

Close away from EMA50

+20%

5️⃣ Price Action Confirmation (HTF)

Valid rejection candle at AOI:

Pin bar

Strong engulfing

Volume ≥ 150% average

+10%

✅ HTF Confluence Summary
Condition	Score
Structure	30%
EMA50 position & slope	20%
AOI strength	20%
EMA50 rejection	20%
Price action	10%
Total	100%
II. Lower Timeframe Signal Analysis

Timeframes: 1H, 30m
Purpose: Entry timing & execution quality

Signal Confluence Score: max 100%
≥60% = Valid entry signal

1️⃣ Structure Alignment (LTF vs HTF)

LTF structure aligns with HTF bias → +30%

Any conflict → ❌ 0% (signal invalid)

2️⃣ EMA50 Pullback / Rejection

Price pulls back into EMA50

Clear rejection candle

EMA50 slope matches HTF direction

+30%

3️⃣ Entry Price Action

One of the following at EMA50 or LTF AOI:

Rejection candle

Momentum continuation candle

Break & Retest (micro structure)

+40% if clean & obvious

🔢 Signal Score Calculation

Signal score = average of:

1H score

30m score

III. Trade Setup Aggregation
🔗 Overall Confluence Formula
Overall Confluence =
(HTF Confluence × 0.6) + (Signal Confluence × 0.4)

🧠 Structure Quality Rules

Good

HTF & LTF structure aligned

EMA50 respected on all TF

Bad

HTF bullish but LTF bearish

EMA50 flat or violated

📌 Trade Recommendation Logic
Overall Score	Structure	Recommendation
≥80%	Good	✅ Trade
60–79%	Good	⚠️ Wait / Watch
<60%	Any	❌ Avoid
Any	Bad	❌ Avoid (structure conflict)
IV. AI Validation (Optional Layer)

AI is used ONLY for:

Pattern clarity confirmation

EMA50 reaction clarity

AOI quality assessment

Rules:

AI can adjust score ±10% max

AI cannot override invalid structure

Ignore AI if confidence < threshold

V. General Trading Rules

EMA50 is the ONLY indicator

Always use Close price for confirmation

Trade only during London & New York sessions

No trade when:

EMA50 is flat

Market is in range

High-impact news imminent

🧾 Final Summary Table
Score	EMA50 & Structure	Recommendation
≥80%	Clean & aligned	Trade
60–79%	Acceptable	Wait / Watch
<60%	Weak	Avoid
🧠 Final Note

This strategy prioritizes clarity over frequency.
The system must confidently say “NO TRADE” more often than “Trade”.