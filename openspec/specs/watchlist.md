# Watchlist Specification

This file lists supported symbols/assets and filtering logic for the trading dashboard. The tool scans all for MTF confluence scoring.

---

## Main List

- **Majors:**
    - EUR/USD
    - GBP/USD
    - USD/JPY
    - AUD/USD
    - USD/CAD
    - USD/CHF
    - NZD/USD
- **Crosses:**
    - EUR/GBP
    - EUR/JPY
    - GBP/JPY
    - AUD/JPY
    - EUR/NZD
    - GBP/AUD
    - GBP/CHF
    - NZD/CAD
    - EUR/CAD
    - AUD/CHF
    - CHF/JPY
    - GBP/CAD
- **Commodities:**
    - XAU/USD (Gold)
    - XAG/USD (Silver)
    - USOIL (Crude Oil)

---

## Logic & Filter Rules
- Only show pairs with total confluence ≥ 50% in main results.
- User can add custom pairs/assets via the UI.
- For Gold/Silver: Psychological levels are at every $50 (e.g. 1800, 1850, 1900, ...).
- Example for extension:
    - To add: Enter new pair in UI ('Add Pair'), takes effect on next scan.
    - Psych levels for any new asset can be entered optionally.

---

*Recommendation: keep this list versioned and sync with backend symbol universe if possible.*