"""Deduplicate strategies that make identical selected-profile decisions."""
from __future__ import annotations
import pandas as pd

def deduplicate_strategy_behaviors(selection_details:pd.DataFrame, leaderboard:pd.DataFrame)->pd.DataFrame:
    rows=[]
    for name in selection_details['strategy_name'].unique():
        s=selection_details[selection_details['strategy_name']==name].copy().sort_values('ebno_db')
        sig=tuple(s['selected_profile'].tolist())
        lb=leaderboard[leaderboard['strategy_name']==name].iloc[0]
        rows.append({'strategy_name':name,'selection_signature':sig,'score_v2':lb['score_v2'],'avg_effective_se_bpshz':lb['avg_effective_se_bpshz'],'avg_bler':lb['avg_bler'],'bler_violation_rate':lb['bler_violation_rate'],'num_unique_profiles_selected':s['selected_profile'].nunique()})
    sig_df=pd.DataFrame(rows)
    groups=(sig_df.groupby('selection_signature').agg(num_strategies=('strategy_name','count'),representative_strategy=('strategy_name','first'),strategies=('strategy_name',lambda x:list(x)),score_v2=('score_v2','first'),avg_effective_se_bpshz=('avg_effective_se_bpshz','first'),avg_bler=('avg_bler','first'),bler_violation_rate=('bler_violation_rate','first'),num_unique_profiles_selected=('num_unique_profiles_selected','first')).reset_index().sort_values('score_v2',ascending=False).reset_index(drop=True))
    groups['behavior_rank']=groups.index+1
    return groups[['behavior_rank','representative_strategy','num_strategies','score_v2','avg_effective_se_bpshz','avg_bler','bler_violation_rate','num_unique_profiles_selected','strategies','selection_signature']]
