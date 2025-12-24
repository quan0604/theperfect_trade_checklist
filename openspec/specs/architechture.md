# Architecture Overview

System architecture: **Python + Streamlit**. Major modules:
- **Data**: Multi-Timeframe (MTF) data fetch from MetaTrader5
- **Logic**: Calculation of indicators, patterns, and confluence
- **AI**: Advanced contextual analysis (confirmation/scoring)
- **UI**: Interactive visualization and trade recommendations

---

## 1. Technology Stack
- **Backend**: Python 3.10+
- **Frontend**: Streamlit
- **Market Data**: MetaTrader5
- **Indicators**: ta-lib
- **AI/LLM**: openai, claude
- **Charts**: plotly

---

## 2. Module Responsibilities and Interfaces
- **Data**: Fetches MTF data (Weekly/Daily/4H/1H/30m)
    - Output: `{ symbol: { timeframe: df } }`
- **Logic**: Calculates EMA, AOI (Area of Interest, especially from 4H), patterns, and confluence scores
    - Output: `{ context: { trend: 'bullish', confluence_large: 75 }, signal: { confluence_small: 65 } }`
- **AI**: Receives data/patterns for higher-order validation (e.g., "Is Head & Shoulders clear?")
    - Output: AI opinion + score adjustment (±10%)
- **UI**: Renders overview tables (sorted by total confluence) & detailed charts with checklists and recommendations
    - Display: MTF confluence, checklist per factor, "Safe to Trade" / "Avoid" advice

---

## 3. App Flow
1. Fetch MTF market data
2. Calculate large-frame confluence (logic module)
3. Calculate small-frame confluence (zone alignment)
4. Aggregate results & apply AI opinion
5. Display trade setup & dashboards

---

## 4. Best Practices
- Use async calls for AI/LLM interactions
- Cache MTF data for 5 minutes to reduce load
- Load sensitive configuration (API keys, etc) from environment variables
- Document inter-module APIs and data contracts clearly

---

*Note: All specs and APIs are in English for code clarity. Use Vietnamese comments for special logic/edge notes where necessary.*