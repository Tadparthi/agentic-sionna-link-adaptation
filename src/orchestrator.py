"""Rule-based and optional LLM strategy generation."""
from __future__ import annotations
import json, os, re
import numpy as np

def make_penalty_strategy(strategy_label,safety_factor=1.0,penalty_weight=8.0):
    def strategy(subset,target_bler=0.10):
        t=subset.copy(); preferred=target_bler*safety_factor
        t['bler_excess']=np.maximum(t['bler']-preferred,0)
        t['candidate_score']=t['raw_spectral_efficiency_bpshz']-penalty_weight*t['bler_excess']
        return t.sort_values('candidate_score',ascending=False).iloc[0]
    strategy.__name__=strategy_label
    return strategy

def propose_next_generation_strategies(leaderboard):
    configs=[(1.00,4.0),(1.00,8.0),(0.90,8.0),(0.80,8.0),(0.70,8.0),(0.90,12.0),(0.80,12.0),(0.70,12.0),(0.60,16.0),(0.60,20.0),(0.70,20.0),(0.80,20.0)]
    out={}
    for i,(sf,pw) in enumerate(configs,1):
        name=f'Gen2_Candidate_{i:02d}_Safety{sf}_Penalty{pw}'
        out[name]=make_penalty_strategy(name,sf,pw)
    return out

def make_llm_strategy(strategy_name,safety_factor=1.0,penalty_weight=8.0,low_ebno_extra_margin=False,high_ebno_aggressiveness=False):
    def strategy(subset,target_bler=0.10):
        t=subset.copy(); ebno=t['ebno_db'].iloc[0]; preferred=target_bler*safety_factor
        if low_ebno_extra_margin and ebno<=8: preferred*=0.75
        if high_ebno_aggressiveness and ebno>=18: preferred=min(target_bler*1.10,preferred*1.15)
        t['bler_excess']=np.maximum(t['bler']-preferred,0)
        t['candidate_score']=t['raw_spectral_efficiency_bpshz']-penalty_weight*t['bler_excess']
        return t.sort_values('candidate_score',ascending=False).iloc[0]
    strategy.__name__=strategy_name
    return strategy

def extract_json_from_text(text):
    try: return json.loads(text)
    except Exception: pass
    m=re.search(r'\{.*\}',text,flags=re.DOTALL)
    if m: return json.loads(m.group(0))
    raise ValueError('No valid JSON object found')

def build_llm_orchestrator_prompt(leaderboard,target_bler=0.10,top_n=10):
    cols=[c for c in ['overall_rank','strategy_name','score_v2','avg_effective_se_bpshz','avg_bler','bler_violation_rate'] if c in leaderboard.columns]
    text=leaderboard[cols].head(top_n).to_string(index=False)
    return f"""You are the manager/orchestrator for a 5G link adaptation optimization task.
Goal: propose next-generation MCS-selection strategy configs that maximize effective spectral efficiency while keeping BLER close to or below target.
Target BLER: {target_bler}
Current leaderboard:\n{text}
Return only valid JSON in this exact format:
{{"strategies":[{{"strategy_name":"name","safety_factor":0.85,"penalty_weight":10.0,"low_ebno_extra_margin":true,"high_ebno_aggressiveness":false,"explanation":"short explanation"}}]}}
Create 8 strategies."""

def generate_llm_strategies(leaderboard,target_bler=0.10,model='gpt-4.1-mini'):
    if not os.environ.get('OPENAI_API_KEY'): raise EnvironmentError('OPENAI_API_KEY is not set')
    from openai import OpenAI
    client=OpenAI(); prompt=build_llm_orchestrator_prompt(leaderboard,target_bler)
    resp=client.responses.create(model=model,input=prompt); plan=extract_json_from_text(resp.output_text)
    strategies={}
    for item in plan['strategies']:
        name='LLM_'+item['strategy_name'].replace(' ','_')
        strategies[name]=make_llm_strategy(name,float(item['safety_factor']),float(item['penalty_weight']),bool(item['low_ebno_extra_margin']),bool(item['high_ebno_aggressiveness']))
    return strategies, plan
