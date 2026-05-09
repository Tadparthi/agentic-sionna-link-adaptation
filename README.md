# Agentic Sionna Link Adaptation Mini-Lab

A compact 5G link adaptation mini-lab built with **Sionna PHY** to simulate LDPC-coded BLER curves, evaluate MCS-selection strategies, and identify the best policy for maximizing spectral efficiency under BLER constraints.

---

## Live Demo

Interactive project diagram:

[Open the live interactive diagram](https://Tadparthi.github.io/agentic-sionna-link-adaptation/)

The diagram explains the concept model, Sionna PHY chain, LDPC-coded BLER simulation, MCS profile library, strategy leaderboard, orchestration loop, and final best policy.

---

## Project Objective

The project answers a practical link adaptation question:

> Given radio quality / Eb/N0, which MCS-like profile should be selected to maximize spectral efficiency while keeping BLER near a 10% target?

It compares three scheduler-style behaviors:

| Behavior | Meaning |
|---|---|
| Conservative selection | Protects BLER but may waste capacity |
| Aggressive selection | Improves raw spectral efficiency but may create excessive block errors |
| Balanced selection | Chooses the highest usable MCS while keeping BLER under control |

---

## System Architecture

```text
Concept Model
SINR → CQI → MCS → HARQ ACK/NACK → OLLA

Sionna PHY Simulation
Information Bits → LDPC Encoder → QAM Mapper → AWGN Channel
→ Soft Demapper → LDPC Decoder → BER / BLER

Optimization Loop
MCS Profiles → Candidate Strategies → Evaluator → Leaderboard
→ Orchestrator-Generated Candidates → Deduplicated Best Policy
```

---

## Key Results

Best deduplicated MCS-selection behavior:

**Highest SE Under BLER Target**

| Metric | Result |
|---|---:|
| Average effective spectral efficiency | ~4.75 bits/s/Hz |
| Average BLER | ~9.21% |
| BLER violation rate | ~11.43% |
| Unique MCS profiles selected | 9 |

The best policy was not the most conservative or the most aggressive. It selected the highest usable MCS-like profile while keeping average BLER close to the 10% target.

---

## MCS-like Profiles

The project evaluates 9 simplified MCS-like profiles.

| Profile | Modulation | Code Rate |
|---|---:|---:|
| QPSK_R030 | QPSK / 4-QAM | 0.30 |
| QPSK_R050 | QPSK / 4-QAM | 0.50 |
| 16QAM_R045 | 16-QAM | 0.45 |
| 16QAM_R060 | 16-QAM | 0.60 |
| 64QAM_R050 | 64-QAM | 0.50 |
| 64QAM_R065 | 64-QAM | 0.65 |
| 64QAM_R080 | 64-QAM | 0.80 |
| 256QAM_R070 | 256-QAM | 0.70 |
| 256QAM_R085 | 256-QAM | 0.85 |

These profiles are simplified simulation profiles, not a complete 3GPP MCS table.

---

## Technical Modules

| File | Purpose |
|---|---|
| `main.py` | Runs the full project pipeline |
| `src/mcs_profiles.py` | Defines MCS-like modulation and code-rate profiles |
| `src/sionna_ldpc_sim.py` | Runs Sionna LDPC-coded BLER simulations over AWGN |
| `src/strategies.py` | Defines conservative, aggressive, BLER-target, margin, and penalty-based MCS-selection strategies |
| `src/evaluator.py` | Scores each strategy using effective spectral efficiency, BLER violation rate, BLER excess, and distance from target |
| `src/orchestrator.py` | Generates rule-based and optional LLM-proposed strategy candidates |
| `src/deduplicate.py` | Groups strategies that make identical MCS-profile selections |
| `src/plotting.py` | Generates BLER curve and leaderboard plots |
| `html/sionna_link_adaptation_interactive.html` | Local interactive HTML architecture diagram |
| `docs/index.html` | GitHub Pages version of the interactive diagram |

---

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run a fast simulation:

```bash
python main.py --fast
```

Run the full simulation:

```bash
python main.py
```

Reuse cached results:

```bash
python main.py --use-cache
```

Optional LLM strategy generation:

```bash
export OPENAI_API_KEY="your_key_here"
python main.py --with-llm
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
python main.py --with-llm
```

---

## Outputs

Generated files are saved under `results/`.

| Output | Description |
|---|---|
| `expanded_sionna_ldpc_mcs_results.csv` | Sionna LDPC BLER simulation results by MCS-like profile |
| `expanded_mcs_10pct_bler_threshold_table.csv` | Approximate Eb/N0 threshold for 10% BLER by profile |
| `expanded_mcs_strategy_leaderboard.csv` | Strategy leaderboard before behavior deduplication |
| `expanded_mcs_strategy_selection_details.csv` | Per-Eb/N0 strategy selections |
| `deduplicated_strategy_behavior_leaderboard.csv` | Final unique behavior leaderboard |
| `README_project_summary.md` | Auto-generated project summary |
| `bler_curves.png` | BLER curve plot |
| `leaderboard.png` | Strategy leaderboard plot |

---

## Strategy Evaluation

Each strategy is evaluated across available Eb/N0 points.

The improved score considers:

- Average effective spectral efficiency
- BLER violation rate
- BLER violation magnitude
- Distance from the target BLER

This makes the evaluator prefer policies that achieve high throughput while maintaining reliability.

---

## Why Deduplication Matters

Multiple strategy names can produce the same MCS decisions across all Eb/N0 points.

The project deduplicates strategies by their actual selected-profile sequence, so the final leaderboard ranks **unique behaviors** instead of only strategy names.

---

## Repository Structure

```text
agentic-sionna-link-adaptation/
├── README.md
├── requirements.txt
├── main.py
├── src/
│   ├── mcs_profiles.py
│   ├── sionna_ldpc_sim.py
│   ├── strategies.py
│   ├── evaluator.py
│   ├── orchestrator.py
│   ├── deduplicate.py
│   ├── plotting.py
│   └── reporting.py
├── notebooks/
│   └── 01_agentic_sionna_link_adaptation_demo.ipynb
├── html/
│   └── sionna_link_adaptation_interactive.html
├── docs/
│   └── index.html
└── results/
```

---

## Key Takeaways

- Sionna PHY can generate LDPC-coded BLER curves for MCS-like profiles.
- Higher modulation and higher code rate improve raw spectral efficiency but require higher Eb/N0.
- A balanced MCS-selection policy outperforms overly conservative and overly aggressive strategies.
- Deduplicating strategy behavior helps identify truly unique algorithmic policies.
- The final result aligns with practical link adaptation logic: select the highest usable MCS while keeping BLER near target.

---

## Limitations

- The MCS profiles are simplified and are not a full 3GPP MCS table.
- The current channel model uses AWGN only.
- OFDM, MIMO, fading channels, CSI feedback, HARQ process timing, and full NR PDSCH/PUSCH simulation are future extensions.
- LLM-based strategy generation is optional and requires an API key.

---

## Future Work

Potential next steps:

- Add fading channel models
- Add OFDM resource grid simulation
- Add realistic CQI/MCS table mapping
- Compare AWGN versus fading BLER thresholds
- Add HARQ retransmission modeling
- Extend to PDSCH/PUSCH-style link-level simulation
- Build a richer agentic optimization loop with multiple strategy generations
