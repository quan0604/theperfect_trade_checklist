"""
confluence.py
---------------------------------
Confluence Scoring Engine – CORE (Phase 2.6)

Purpose:
- Orchestrate analysis from multiple modules (Structure, EMA, AOI)
- Calculate final agreement score
- Suggest Trading Bias

Modules Integrated:
- Structure (2.1)
- EMA Logic (2.2)
- EMA Score (2.6)
- AOI (2.3) [Future]
"""

import pandas as pd
from typing import Dict, Optional

# Import Analysis Modules
from . import structure
from . import ema
from . import ema_score

class ConfluenceEngine:
    """
    Main Logic Integrator.
    Computes weighted score from technical factors.
    """
    
    def __init__(self):
        pass

    def analyze_timeframe(
        self, 
        df: pd.DataFrame, 
        timeframe: str,
        structure_lookback: int = 5,
        ema_period: int = 50
    ) -> Dict:
        """
        Run full technical stack on a single dataframe.
        """
        
        # 1. Market Structure (Mandatory)
        struct_res = structure.analyze_market_structure(df, lookback=structure_lookback)
        bias = struct_res["bias"] # Enum: BULLISH, BEARISH, TRANSITION...
        
        # 2. EMA Logic (Mandatory)
        # Adapt Structure Bias to MarketBias Enum if needed, or pass string
        # Here we assume Enums are compatible or convert them
        # structure.py uses StructureBias, ema_score uses MarketBias
        # We need a converter
        
        market_bias = self._convert_bias(bias)
        
        ema_res = ema.analyze_ema(
            df, 
            timeframe=timeframe, 
            ema_period=ema_period,
            market_bias=market_bias
        )
        
        # 3. EMA Scoring (Optional but recommended)
        # Check if EMA analysis was valid
        if ema_res["valid"]:
            score_res = ema_score.score_ema(
                ema_state=ema_res,
                structure_bias=market_bias,
                in_aoi=False # TODO: AOI Integration later
            )
        else:
            score_res = {"ema_score": 0, "confidence": "none", "reasons": ["ema_invalid"]}
            
        # 4. Final Aggregation
        return {
            "timeframe": timeframe,
            "structure": {
                "bias": bias.value,
                "bos": struct_res["bos"],
                "swing_count": len(struct_res["swings"])
            },
            "ema": {
                "slope": ema_res["slope"].value if ema_res["valid"] else "n/a",
                "position": ema_res["position"].value if ema_res["valid"] else "n/a",
                "rejection": ema_res["rejection"].value if ema_res["valid"] else "n/a"
            },
            "confluence": {
                "score_total": score_res["ema_score"], # Currently only EMA contributes
                "confidence": score_res["confidence"],
                "reasons": score_res["reasons"]
            }
        }

    def _convert_bias(self, struct_bias: structure.StructureBias) -> ema_score.MarketBias:
        """
        Adapter to convert structure.StructureBias to ema_score.MarketBias
        """
        if struct_bias == structure.StructureBias.BULLISH:
            return ema_score.MarketBias.BULLISH
        elif struct_bias == structure.StructureBias.BEARISH:
            return ema_score.MarketBias.BEARISH
        elif struct_bias == structure.StructureBias.TRANSITION:
            return ema_score.MarketBias.TRANSITION
        else:
            return ema_score.MarketBias.RANGE

# Singleton instance
engine = ConfluenceEngine()

def run_analysis(df: pd.DataFrame, tf: str) -> Dict:
    return engine.analyze_timeframe(df, tf)
