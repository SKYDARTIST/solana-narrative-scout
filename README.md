# SignalVane 📡
### Real-Time Autonomous Narrative Detection for Solana
**An AI Agent Submission for Superteam Earn**

SignalVane is a production-grade AI-powered autonomous agent that detects and tracks emerging Solana narratives in real-time. Features live data updates, historical trend analysis, sentiment scoring, and interactive visualizations.

## ✨ Key Features

### 🔄 Real-Time Updates
- Auto-refreshes data every 15 minutes
- Live update indicator showing last refresh time
- Smart caching to minimize API calls

### 📈 Historical Trend Analysis
- Tracks narrative evolution over time
- Visual trend indicators: ↗ Rising | → Stable | ↘ Falling | ✨ New
- Interactive Plotly charts showing 7-day trends

### 😊 Sentiment Analysis
- AI-powered sentiment scoring (Positive/Neutral/Negative)
- Based on novelty scores and evidence strength
- Color-coded badges for quick assessment

### 🎛️ Advanced Filtering & Sorting
- Filter by sentiment, trend, or novelty score
- Sort narratives by multiple criteria
- Interactive sidebar controls

### 📊 Professional Visualizations
- Plotly-powered interactive charts
- Glassmorphism UI with smooth animations
- Real-time metric tracking

## 🚀 Live Demo
**[View Live Dashboard →](https://solana-narrative-scout.streamlit.app)**

### 📸 Dashboard Preview

**Narrative Detection & Evidence**
![Dashboard Overview](assets/dashboard-overview.png)

**AI-Generated Build Ideas**
![Build Ideas](assets/build-ideas.png)

**All 3 Detected Narratives**
![SVM Narrative](assets/svm-narrative.png)
![ZK-Compression Narrative](assets/zk-compression.png)

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
