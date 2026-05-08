"""Strategy evaluation and leaderboard utilities."""
from __future__ import annotations
import pandas as pd

def evaluate_mcs_strategy_v2(strategy_name, strategy_function, ldpc_results, target_bler=0.10, violation_rate_penalty=4.0, violation_magnitude_penalty=10.0, target_distance_penalty=0.75):
    rows=[]
    for ebno in sorted(ldpc_results['ebno_db'].unique()):
        subset=ldpc_results[ldpc_results['ebno_db']==ebno].copy()
        if len(subset)==0: continue
        sel=strategy_function(subset,target_bler)
        bler=float(sel['bler']); excess=max(bler-target_bler,0)
        rows.append({'strategy_name':strategy_name,'ebno_db':ebno,'selected_profile':sel['profile_name'],'selected_mcs_like':sel['mcs_like'],'modulation':sel['modulation'],'bler':bler,'bler_target_met':bler<=target_bler,'bler_excess':excess,'raw_spectral_efficiency_bpshz':sel['raw_spectral_efficiency_bpshz'],'effective_spectral_efficiency_bpshz':sel['effective_spectral_efficiency_bpshz'],'bler_violation':int(bler>target_bler)})
    details=pd.DataFrame(rows)
    avg_eff=details['effective_spectral_efficiency_bpshz'].mean(); avg_raw=details['raw_spectral_efficiency_bpshz'].mean(); avg_bler=details['bler'].mean(); violation=details['bler_violation'].mean(); avg_excess=details['bler_excess'].mean(); dist=abs(avg_bler-target_bler)
    score=avg_eff-violation_rate_penalty*violation-violation_magnitude_penalty*avg_excess-target_distance_penalty*dist
    summary={'strategy_name':strategy_name,'score_v2':score,'avg_effective_se_bpshz':avg_eff,'avg_raw_se_bpshz':avg_raw,'avg_bler':avg_bler,'avg_bler_excess':avg_excess,'avg_distance_from_target':dist,'bler_violation_rate':violation,'num_ebno_points':len(details),'eval_tool_output_v2':f'SUCCESS, {score:.4f}'}
    return summary, details

def evaluate_strategy_set(strategies, ldpc_results, target_bler=0.10):
    rows=[]; details=[]
    for name,fn in strategies.items():
        s,d=evaluate_mcs_strategy_v2(name,fn,ldpc_results,target_bler)
        rows.append(s); details.append(d)
    lb=pd.DataFrame(rows).sort_values(['score_v2','avg_effective_se_bpshz','bler_violation_rate','avg_bler_excess'],ascending=[False,False,True,True]).reset_index(drop=True)
    lb['overall_rank']=lb.index+1
    return lb, pd.concat(details,ignore_index=True)
