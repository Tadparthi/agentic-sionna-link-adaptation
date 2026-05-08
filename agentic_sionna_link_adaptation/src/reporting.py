"""Project summary generator."""
from __future__ import annotations
from pathlib import Path

def generate_project_summary(dedup_behavior_leaderboard, output_path='results/README_project_summary.md'):
    best=dedup_behavior_leaderboard.sort_values('behavior_rank').iloc[0]
    md=f"""# Agentic Sionna Link Adaptation Mini-Lab - Project Summary

## Best Unique Policy

- Strategy: **{best['representative_strategy']}**
- Score V2: **{best['score_v2']:.4f}**
- Avg effective SE: **{best['avg_effective_se_bpshz']:.4f} bits/s/Hz**
- Avg BLER: **{best['avg_bler']:.2%}**
- BLER violation rate: **{best['bler_violation_rate']:.2%}**
- Unique MCS profiles selected: **{int(best['num_unique_profiles_selected'])}**

## Engineering Meaning

The best policy selects the highest spectral-efficiency MCS-like profile that stays under the BLER target whenever possible. This balances throughput and reliability better than blindly conservative or blindly aggressive MCS selection.

## Resume Bullet

Built an agentic Sionna link adaptation mini-lab that simulates 5G LDPC-coded BLER curves for MCS-like modulation and code-rate profiles, evaluates multiple MCS-selection strategies through a leaderboard, and identifies the best policy for maximizing spectral efficiency under BLER constraints.
"""
    Path(output_path).parent.mkdir(parents=True,exist_ok=True); Path(output_path).write_text(md,encoding='utf-8')
    return md
