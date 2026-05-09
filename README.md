Agentic Sionna Link Adaptation Mini-Lab

A compact Sionna-based 5G link adaptation project that simulates LDPC-coded BLER curves for MCS-like modulation/code-rate profiles, evaluates MCS-selection strategies through a leaderboard, and identifies the best policy for maximizing spectral efficiency under BLER constraints.

Objective

Given radio quality / Eb/N0, choose the highest usable MCS-like profile while keeping BLER near a 10% target.

In practical RF terms, this project studies the link adaptation tradeoff between:

Conservative MCS selection, which protects BLER but may waste capacity
Aggressive MCS selection, which improves raw spectral efficiency but may create excessive block errors
Balanced MCS selection, which chooses the highest usable MCS under BLER control
Live Interactive Diagram

Open the live interactive block diagram here:

https://Tadparthi.github.io/agentic-sionna-link-adaptation/

The diagram explains the full project flow:

Concept model: SINR → CQI → MCS → HARQ/OLLA
Sionna PHY simulation chain
LDPC-coded BLER curves
MCS profile library
Strategy evaluator and leaderboard
Rule-based / LLM orchestration
Best unique MCS-selection policy

You can also open the local file directly:

html/sionna_link_adaptation_interactive.html
Architecture
Concept Model:
SINR → CQI → MCS → HARQ ACK/NACK → OLLA

Sionna PHY:
Information bits → LDPC Encoder → QAM Mapper → AWGN Channel
→ Soft Demapper → LDPC Decoder → BER / BLER

Optimization:
MCS profiles → candidate strategies → evaluator
→ leaderboard → orchestrator-generated candidates
→ deduplicated best policy
Key Results

The best deduplicated MCS-selection behavior was:

Highest SE Under BLER Target

Final result from the expanded MCS profile experiment:

Metric	Result
Avg effective spectral efficiency	~4.75 bits/s/Hz
Avg BLER	~9.21%
BLER violation rate	~11.43%
Unique MCS profiles selected	9

The result shows that the best policy was not the most conservative or the most aggressive. It selected the highest usable MCS-like profile while keeping average BLER close to the 10% target.

MCS-like Profiles

The project evaluates 9 MCS-like profiles:

QPSK R0.30
QPSK R0.50
16QAM R0.45
16QAM R0.60
64QAM R0.50
64QAM R0.65
64QAM R0.80
256QAM R0.70
256QAM R0.85

These are simplified simulation profiles, not a full 3GPP MCS table.

Technical Modules
Module	Purpose
mcs_profiles.py	Defines MCS-like profiles using modulation order, code rate, and Eb/N0 sweep ranges
sionna_ldpc_sim.py	Runs Sionna LDPC-coded BLER simulations over AWGN
strategies.py	Defines conservative, aggressive, BLER-target, margin, and penalty-based MCS-selection strategies
evaluator.py	Scores each strategy using effective spectral efficiency, BLER violation rate, BLER excess, and distance from target
orchestrator.py	Generates rule-based and optional LLM-proposed strategy candidates
deduplicate.py	Groups strategies that make identical MCS-profile selections
plotting.py	Generates BLER curve and leaderboard plots
main.py	Runs the full project pipeline
Quick Start
pip install -r requirements.txt
python main.py --fast

For a fuller run:

python main.py

Reuse cached results:

python main.py --use-cache

Optional LLM generation:

export OPENAI_API_KEY="your_key_here"
python main.py --with-llm
Outputs

Results are saved in results/:

expanded_sionna_ldpc_mcs_results.csv
expanded_mcs_10pct_bler_threshold_table.csv
expanded_mcs_strategy_leaderboard.csv
expanded_mcs_strategy_selection_details.csv
deduplicated_strategy_behavior_leaderboard.csv
README_project_summary.md
bler_curves.png
leaderboard.png
Key Takeaways
Sionna PHY can be used to generate LDPC-coded BLER curves for MCS-like profiles.
Higher modulation and higher code rate improve raw spectral efficiency but require higher Eb/N0.
A balanced MCS-selection policy outperforms both overly conservative and overly aggressive strategies.
Deduplicating strategy behavior helps identify truly unique algorithmic policies.
