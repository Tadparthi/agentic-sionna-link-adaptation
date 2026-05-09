"""Run the Agentic Sionna Link Adaptation Mini-Lab.

Examples:
  python main.py --fast
  python main.py --use-cache
  python main.py --with-llm
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from src.deduplicate import deduplicate_strategy_behaviors
from src.evaluator import evaluate_strategy_set
from src.mcs_profiles import EXPANDED_MCS_PROFILES
from src.orchestrator import generate_llm_strategies, propose_next_generation_strategies
from src.plotting import plot_bler_curves, plot_leaderboard
from src.reporting import generate_project_summary
from src.sionna_ldpc_sim import build_threshold_table, run_mcs_profile_simulations
from src.strategies import BASE_STRATEGIES

TARGET_BLER=0.10; RESULTS_DIR=Path('results')

def parse_args():
    p=argparse.ArgumentParser(description='Agentic Sionna Link Adaptation Mini-Lab')
    p.add_argument('--fast',action='store_true',help='Use faster simulation settings')
    p.add_argument('--use-cache',action='store_true',help='Reuse existing LDPC results CSV')
    p.add_argument('--with-llm',action='store_true',help='Use optional OpenAI LLM strategy generation')
    return p.parse_args()

def main():
    args=parse_args(); RESULTS_DIR.mkdir(exist_ok=True)
    ldpc_csv=RESULTS_DIR/'expanded_sionna_ldpc_mcs_results.csv'
    if args.use_cache and ldpc_csv.exists():
        print(f'Loading cached results from {ldpc_csv}'); ldpc_results=pd.read_csv(ldpc_csv)
    else:
        print('Running Sionna LDPC simulations...')
        kwargs=dict(n_codeword=1200,batch_size=60,num_batches=2,decoder_iterations=10) if args.fast else dict(n_codeword=1200,batch_size=80,num_batches=3,decoder_iterations=15)
        ldpc_results=run_mcs_profile_simulations(EXPANDED_MCS_PROFILES,**kwargs)
        ldpc_results.to_csv(ldpc_csv,index=False)
    print('Building threshold table...')
    threshold=build_threshold_table(ldpc_results,TARGET_BLER)
    threshold.to_csv(RESULTS_DIR/'expanded_mcs_10pct_bler_threshold_table.csv',index=False)
    print('Evaluating base strategies...')
    leaderboard,details=evaluate_strategy_set(BASE_STRATEGIES,ldpc_results,TARGET_BLER)
    gen2=propose_next_generation_strategies(leaderboard)
    all_strategies={**BASE_STRATEGIES,**gen2}
    if args.with_llm:
        try:
            llm_strategies, plan=generate_llm_strategies(leaderboard,TARGET_BLER)
            all_strategies.update(llm_strategies)
            Path(RESULTS_DIR/'llm_strategy_plan.json').write_text(pd.Series(plan).to_json(indent=2),encoding='utf-8')
        except Exception as exc:
            print(f'LLM strategy generation skipped: {exc}')
    print('Evaluating all strategies...')
    leaderboard,details=evaluate_strategy_set(all_strategies,ldpc_results,TARGET_BLER)
    leaderboard.to_csv(RESULTS_DIR/'expanded_mcs_strategy_leaderboard.csv',index=False)
    details.to_csv(RESULTS_DIR/'expanded_mcs_strategy_selection_details.csv',index=False)
    print('Deduplicating equivalent strategy behaviors...')
    dedup=deduplicate_strategy_behaviors(details,leaderboard)
    dedup.to_csv(RESULTS_DIR/'deduplicated_strategy_behavior_leaderboard.csv',index=False)
    print('Saving plots and project summary...')
    plot_bler_curves(ldpc_results,RESULTS_DIR/'bler_curves.png')
    plot_leaderboard(leaderboard,RESULTS_DIR/'leaderboard.png')
    generate_project_summary(dedup,RESULTS_DIR/'README_project_summary.md')
    print('\nTop deduplicated strategy behaviors:')
    print(dedup[['behavior_rank','representative_strategy','num_strategies','score_v2','avg_effective_se_bpshz','avg_bler','bler_violation_rate']].head(10).to_string(index=False))
    print('\nDone. See results/ folder.')

if __name__=='__main__': main()
