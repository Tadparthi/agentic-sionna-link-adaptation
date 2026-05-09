"""Plotting helpers."""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt

def plot_bler_curves(ldpc_results, output_path=None):
    plt.figure(figsize=(12,7))
    for name in ldpc_results['profile_name'].unique():
        s=ldpc_results[ldpc_results['profile_name']==name].copy(); s['bler_plot']=s['bler'].replace(0,1e-4)
        plt.semilogy(s['ebno_db'],s['bler_plot'],marker='o',label=name)
    plt.axhline(y=0.10,linestyle='--',label='10% BLER Target')
    plt.xlabel('Eb/N0 (dB)'); plt.ylabel('BLER'); plt.title('Sionna PHY: LDPC-Coded BLER Curves by MCS-like Profile'); plt.grid(True,which='both'); plt.legend()
    if output_path:
        Path(output_path).parent.mkdir(parents=True,exist_ok=True); plt.savefig(output_path,dpi=160,bbox_inches='tight')
    return plt.gcf()

def plot_leaderboard(leaderboard, output_path=None, top_n=12):
    p=leaderboard.head(top_n).copy()
    plt.figure(figsize=(14,6)); plt.bar(p['strategy_name'],p['score_v2']); plt.xlabel('Strategy'); plt.ylabel('Evaluation Score V2'); plt.title('MCS Strategy Leaderboard'); plt.xticks(rotation=60,ha='right'); plt.grid(True,axis='y')
    if output_path:
        Path(output_path).parent.mkdir(parents=True,exist_ok=True); plt.savefig(output_path,dpi=160,bbox_inches='tight')
    return plt.gcf()
