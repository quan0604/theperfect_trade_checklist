📌 Trading Tool – Task List & Project Roadmap (Trader-Grade)

This document defines the full development roadmap for the Trading Decision Support Tool.
The goal is to build a professional MTF confluence-based trading assistant, not an indicator or auto-trading bot.

📊 Project Status Overview

Current Phase: Phase 1 – Foundation & Data
Overall Completion: ~40%
Last Updated: 25/12/2025

Philosophy

❌ No auto-trading

❌ No AI-first logic

✅ Confluence > AI

✅ Structure > Indicator

✅ Trade filtering > Trade frequency

🧭 Development Phases Overview
Phase	Name	Purpose
Phase 1	Foundation & Data	Reliable MT5 data engine
Phase 2	Trading Logic & Confluence	Core trading intelligence
Phase 3	AI Validation Layer	Optional AI confirmation
Phase 4	User Interface	Trader-focused dashboard
Phase 5	Testing & Optimization	Validation & performance
🧱 Phase 1 – Foundation & Data Engineering

Goal: Stable, secure, multi-timeframe data source
Blocking Phase: YES (must be 100% before Phase 2)

ID	Task	Priority	Status	Notes
1.1	Write trading & system specifications	High	✅ Done	strategy.md, architecture.md
1.2	Setup Python environment & dependencies	High	✅ Done	Python 3.13
1.3	Connect to MetaTrader 5 terminal	High	✅ Done	Tested & stable
1.4	Fetch multi-timeframe OHLC data	High	✅ Done	W / D / 4H / 1H / 30m
1.5	Normalize & structure DataFrames	High	✅ Done	Dict {tf: df}
1.6	Load watchlist from YAML	Medium	✅ Done	Flexible symbols
1.7	Robust error handling & retry logic	Medium	✅ Done	Retries added
1.8	Data caching (5-minute TTL)	Medium	✅ Done	Streamlit cache
1.9	Move credentials to .env	🔴 High	✅ Done	os.getenv

Phase 1 Completion: 100%
✅ Phase 1 Complete - Ready for Phase 2

🧠 Phase 2 – Trading Logic & Confluence Engine (CORE)

Goal: Encode discretionary trading logic into deterministic rules
This is the heart of the system

🔹 2.1 Market Structure (MANDATORY)
ID	Task	Priority	Status	Notes
2.1	Detect market structure (HH/HL – LH/LL)	🔴 High	✅ Done	4H & 1H
				Output: Bullish / Bearish / Transition
🔹 2.2 EMA 50 Logic (NOT just calculation)
ID	Task	Priority	Status	Notes
2.2	EMA 50 calculation (all TF)	High	✅ Done	EMA50 + ATR Normalization
2.3	EMA position logic	🔴 High	✅ Done	ATR Zone Buffer & Rejection
2.4	EMA slope detection	High	✅ Done	ATR Normalized Slope
🔹 2.3 AOI (Area of Interest)
ID	Task	Priority	Status	Notes
2.5	Detect HTF AOI zones	🔴 High	✅ Done	4H / Daily
2.6	Detect LTF AOI zones	High	✅ Done	1H / 30m
2.7	Evaluate AOI strength	🔴 High	✅ Done Touches + reaction
🔹 2.4 Trend & Context Filters
ID	Task	Priority	Status	Notes
2.8	Trend classification	High	[/] In Progress	Bull / Bear / Range
2.9	Psychological levels	Medium	⏳ Todo	Round numbers
2.10	Session context detection	Medium	⏳ Todo	Asia / London / NY
🔹 2.5 Entry & Signal Quality
ID	Task	Priority	Status	Notes
2.11	Entry confirmation logic	🔴 High	⏳ Todo	Rejection / Momentum
2.12	Break & Retest detection	High	⏳ Todo	Structure-aware
2.13	Volume confirmation	Medium	⏳ Todo	Above avg volume
🔹 2.6 Confluence Scoring System
ID	Task	Priority	Status	Notes
2.14	HTF confluence score	🔴 High	⏳ Todo	Structure + EMA + AOI
2.15	Signal TF confluence score	High	⏳ Todo	Entry quality
2.16	Weighted overall confluence	🔴 High	⏳ Todo	60% HTF / 40% Signal
🔹 2.7 Trade Filters (Trader Mindset)
ID	Task	Priority	Status	Notes
2.17	Setup validation filter	🔴 High	⏳ Todo	Reject bad setups
2.18	No-trade zone detection	Medium	⏳ Todo	Range / flat EMA
2.19	Structure conflict filter	High	⏳ Todo	HTF vs LTF

Phase 2 Completion: ~10%
🎯 MVP becomes usable when Phase 2 is DONE

🤖 Phase 3 – AI Validation Layer (OPTIONAL, NON-BLOCKING)

Goal: AI acts as a second opinion, never decision maker

ID	Task	Priority	Status	Notes
3.1	OpenAI API integration	High	🚧 In Progress	Basic function
3.2	AI prompt templates	High	⏳ Todo	Trader language
3.3	Format MTF data for AI	Medium	⏳ Todo	Condensed JSON
3.4	Parse AI response	Medium	⏳ Todo	Bias + confidence
3.5	AI confidence gate	Medium	⏳ Todo	Ignore low confidence
3.6	Confluence adjustment ±10%	Medium	⏳ Todo	Controlled impact
3.7	AI fallback logic	Low	⏳ Todo	Non-AI mode
3.8	Rate limit & cost control	Low	⏳ Todo	Safety
🖥️ Phase 4 – User Interface (Trader-Focused)

Goal: Fast decision-making, minimal noise

ID	Task	Priority	Status	Notes
4.1	Streamlit app bootstrap	High	✅ Done	app.py
4.2	Sidebar controls	High	✅ Done	Symbol / TF
4.3	Overview table (CORE UI)	🔴 High	⏳ Todo	Sorted by confluence
4.4	Checklist breakdown view	High	⏳ Todo	Why / why not
4.5	MTF chart visualization	Medium	🚧 In Progress	Clean & minimal
4.6	AI opinion panel	Medium	⏳ Todo	Optional
4.7	Trade suggestion (non-auto)	Medium	⏳ Todo	Entry / SL / TP
4.8	Color coding & alerts	Low	⏳ Todo	Green / Yellow / Red
4.9	Symbol detail expand view	Medium	⏳ Todo	Drill-down
🧪 Phase 5 – Testing & Optimization

Goal: Trust the tool before trusting capital

ID	Task	Priority	Status	Notes
5.1	Unit tests – data engine	High	⏳ Todo	Mock MT5
5.2	Unit tests – logic engine	High	⏳ Todo	Structure & scoring
5.3	Integration testing	High	⏳ Todo	End-to-end
5.4	Backtest individual modules	Medium	⏳ Todo	EMA / AOI / score
5.5	Optimize scoring weights	Medium	⏳ Todo	Data-driven
5.6	Performance optimization	Low	⏳ Todo	Cache / async
5.7	Security audit	Medium	⏳ Todo	API & env
5.8	Documentation & examples	Low	⏳ Todo	README
🎯 Milestones
Milestone	Target	Criteria
M1	Data Engine Ready	Phase 1 = 100%
M2	Trading Logic MVP	Phase 2 = DONE
M3	AI Validation Live	Phase 3 core
M4	UI Beta	Phase 4 core
M5	Production Ready	Phase 5
🧠 Final Notes

This tool is a decision support system, not an EA

The system must be able to say “NO TRADE”

If Phase 2 is solid → AI & UI are just bonuses
