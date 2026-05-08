"""Candidate MCS-selection strategies."""
from __future__ import annotations
import numpy as np

def strategy_conservative(subset,target_bler=0.10):
    valid=subset[subset['bler']<=target_bler].copy()
    if len(valid)>0: return valid.sort_values('bler').iloc[0]
    return subset.sort_values('bler').iloc[0]

def strategy_aggressive(subset,target_bler=0.10):
    return subset.sort_values('raw_spectral_efficiency_bpshz',ascending=False).iloc[0]

def strategy_highest_se_under_bler(subset,target_bler=0.10):
    valid=subset[subset['bler']<=target_bler].copy()
    if len(valid)>0: return valid.sort_values('raw_spectral_efficiency_bpshz',ascending=False).iloc[0]
    return subset.sort_values('bler').iloc[0]

def strategy_margin_bler(subset,target_bler=0.10):
    valid=subset[subset['bler']<=target_bler*0.70].copy()
    if len(valid)>0: return valid.sort_values('raw_spectral_efficiency_bpshz',ascending=False).iloc[0]
    return strategy_highest_se_under_bler(subset,target_bler)

def strategy_penalty_score(subset,target_bler=0.10):
    t=subset.copy(); t['bler_excess']=np.maximum(t['bler']-target_bler,0)
    t['strategy_score']=t['raw_spectral_efficiency_bpshz']-8.0*t['bler_excess']
    return t.sort_values('strategy_score',ascending=False).iloc[0]

BASE_STRATEGIES={
    'Conservative Lowest BLER':strategy_conservative,
    'Aggressive Highest SE':strategy_aggressive,
    'Highest SE Under BLER Target':strategy_highest_se_under_bler,
    'Margin BLER Strategy':strategy_margin_bler,
    'Penalty Score Strategy':strategy_penalty_score,
}
