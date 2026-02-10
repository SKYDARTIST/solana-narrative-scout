# SignalVane 📡
### Autonomous Narrative Detection for the Solana Ecosystem
**A Winning Prototype for the Superteam Earn Bounty**

SignalVane is an AI-powered autonomous agent that detects emerging Solana narratives by synthesizing signals across developer activity (GitHub), on-chain metrics (RPC), and collective market intelligence (Messari/Helius).

## 🚀 Live Demo
**[View Live Dashboard →](https://solana-narrative-scout.streamlit.app)**

### 📸 Dashboard Preview

**Narrative Detection & Evidence**
![Dashboard Overview](assets/Screenshot%202026-02-11%20at%203.26.45%20AM.png)

**AI-Generated Build Ideas**
![Build Ideas](assets/Screenshot%202026-02-11%20at%203.29.02%20AM.png)

**All 3 Detected Narratives**
![SVM Narrative](assets/Screenshot%202026-02-11%20at%203.29.14%20AM.png)
![ZK-Compression Narrative](assets/Screenshot%202026-02-11%20at%203.29.27%20AM.png)

## 📊 Fortnightly Narratives (Feb 2026)
1.  **Autonomous Agentic Commerce:** The shift from user-to-dApp to agent-to-agent interactions.
2.  **ZK-Compressed State Economy:** Massive scaling via Light Protocol's ZK-compression.
3.  **SVM Verticalization:** The SVM as a modular, pluggable execution layer for specialized AppChains.

## 🛠️ Methodology
SignalVane prioritizes **Signal Quality and Explainability** over volume:

1.  **GitHub Pulse:** Scans for Solana-tagged repositories with unusual commit velocity (>20 commits/14d) or stargazer spikes.
2.  **On-chain Anomalies:** Uses **Z-score logic** to flag unique Program ID deployments and Active Address growth that exceeds 2 standard deviations from the 14-day mean.
3.  **Cross-Signal Synthesis:** A narrative is only validated if it appears in at least **two** different data streams (e.g., GitHub + Market Report).
4.  **Anti-Meme Heuristics:** Filters signals to exclude low-liquidity/high-volatility meme activity, focusing on structural technology shifts.

## 💡 Build Ideas
Each narrative is paired with 3-5 concrete build ideas, including technical stacks (Anchor, Token-2022, Yellowstone gRPC) and feasibility assessments.

## 📦 Running Locally
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Generate a fresh snapshot: `python backend/aggregator.py`
4. Launch the dashboard: `streamlit run frontend/dashboard.py`

## 🤖 Built by an AI Agent
This submission was conceptualized, researched, and built autonomously by an AI agent, aligning with the core eligibility of the Superteam experimental bounty.
