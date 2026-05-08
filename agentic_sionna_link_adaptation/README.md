# Agentic Sionna Link Adaptation Mini-Lab

A compact Sionna-based 5G link adaptation project that simulates LDPC-coded BLER curves for MCS-like modulation/code-rate profiles, evaluates MCS-selection strategies through a leaderboard, and identifies the best policy for maximizing spectral efficiency under BLER constraints.

## Objective

Given radio quality/Eb/N0, choose the highest usable MCS-like profile while keeping BLER near a 10% target.

## Architecture

```text
Concept Model: SINR → CQI → MCS → HARQ ACK/NACK → OLLA
Sionna PHY: information bits → LDPC Encoder → QAM Mapper → AWGN → Demapper → LDPC Decoder → BLER
Optimization: MCS profiles → candidate strategies → evaluator → leaderboard → deduplicated best policy
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py --fast
```

For a fuller run:

```bash
python main.py
```

Reuse cached results:

```bash
python main.py --use-cache
```

Optional LLM generation:

```bash
export OPENAI_API_KEY="your_key_here"
python main.py --with-llm
```

## Outputs

Results are saved in `results/`:

- `expanded_sionna_ldpc_mcs_results.csv`
- `expanded_mcs_10pct_bler_threshold_table.csv`
- `expanded_mcs_strategy_leaderboard.csv`
- `expanded_mcs_strategy_selection_details.csv`
- `deduplicated_strategy_behavior_leaderboard.csv`
- `README_project_summary.md`
- `bler_curves.png`
- `leaderboard.png`

## Interactive Diagram

## Interactive Project Diagram

Open the live interactive block diagram here:

https://Tadparthi.github.io/agentic-sionna-link-adaptation/

The diagram explains the full project flow:

- Concept model: SINR → CQI → MCS → HARQ/OLLA
- Sionna PHY simulation chain
- LDPC-coded BLER curves
- MCS profile library
- Strategy evaluator and leaderboard
- Rule-based / LLM orchestration
- Best unique MCS-selection policy

You can also open the local file directly:

html/sionna_link_adaptation_interactive.html

## Key Takeaways

- Sionna PHY can be used to generate LDPC-coded BLER curves for MCS-like profiles.
- Higher modulation and higher code rate improve raw spectral efficiency but require higher Eb/N0.
- A balanced MCS-selection policy outperforms both overly conservative and overly aggressive  strategies.
- Deduplicating strategy behavior helps identify truly unique algorithmic policies.
