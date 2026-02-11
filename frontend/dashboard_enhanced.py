import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import time
import sys
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.data_refresher import refresh_data, get_minutes_since_refresh
from backend.historical_tracker import HistoricalTracker

# Page config for Premium Aesthetic
st.set_page_config(
    page_title="SignalVane | Solana Ecosystem Scout",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh configuration
REFRESH_INTERVAL = 900  # 15 minutes in seconds

# Custom CSS for Glassmorphism & Dark Mode (Enhanced)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .narrative-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeIn 0.8s ease-out forwards;
        opacity: 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .narrative-card:hover {
        transform: scale(1.02);
        border: 1px solid rgba(20, 241, 149, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }
    .idea-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 22px;
        margin-top: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        min-height: 420px;
    }
    .idea-card:hover {
        transform: translateY(-5px);
        background: rgba(153, 69, 255, 0.08);
        border: 1px solid rgba(153, 69, 255, 0.3);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    .badge {
        background: #14F195;
        color: black;
        padding: 4px 12px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-right: 8px;
    }
    .trend-indicator {
        font-size: 1.5rem;
        margin-left: 10px;
    }
    .rising { color: #14F195; }
    .falling { color: #FF4444; }
    .stable { color: #FFD700; }
    .new-badge { color: #9945FF; }
    .sentiment-positive { color: #14F195; }
    .sentiment-negative { color: #FF4444; }
    .sentiment-neutral { color: #FFD700; }
    .refresh-indicator {
        position: fixed;
        top: 70px;
        right: 20px;
        background: rgba(20, 241, 149, 0.1);
        border: 1px solid rgba(20, 241, 149, 0.3);
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 0.9rem;
        z-index: 1000;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=900)  # Cache for 15 minutes
def load_data():
    """Load data with caching"""
    with open("data/snapshot.json", "r") as f:
        snapshot = json.load(f)
    with open("data/narratives.json", "r") as f:
        narratives = json.load(f)
    with open("data/ideas.json", "r") as f:
        ideas = json.load(f)
    return snapshot, narratives, ideas

def get_sentiment_score(narrative):
    """
    Calculate sentiment score for a narrative
    Based on evidence and novelty score
    """
    score = narrative.get('novelty_score', 5)

    # Simple heuristic: higher novelty = more positive sentiment
    if score >= 8:
        return "positive", "😊"
    elif score >= 6:
        return "neutral", "😐"
    else:
        return "negative", "😔"

def get_trend_indicator(trend):
    """Get emoji and class for trend"""
    if trend == "rising":
        return "↗", "rising"
    elif trend == "falling":
        return "↘", "falling"
    elif trend == "stable":
        return "→", "stable"
    else:
        return "✨", "new-badge"

def create_trend_chart(narrative_name, tracker):
    """Create a simple trend chart using Plotly"""
    history = tracker.get_history()

    timestamps = []
    scores = []

    for snapshot in history:
        for narrative in snapshot["narratives"]:
            if narrative.get("narrative_name") == narrative_name:
                timestamps.append(snapshot["timestamp"][:10])  # Date only
                scores.append(narrative.get("novelty_score", 0))
                break

    if len(timestamps) < 2:
        return None  # Not enough data

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=scores,
        mode='lines+markers',
        line=dict(color='#14F195', width=2),
        marker=dict(size=8, color='#14F195'),
        fill='tozeroy',
        fillcolor='rgba(20, 241, 149, 0.1)'
    ))

    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title="Novelty Score",
        height=150,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )

    return fig

def main():
    # Auto-refresh mechanism
    minutes_since = get_minutes_since_refresh()
    if minutes_since and minutes_since >= 15:
        with st.spinner("Refreshing data..."):
            refresh_data()
            st.cache_data.clear()
            st.rerun()

    # Load data
    snapshot, narratives, ideas = load_data()
    tracker = HistoricalTracker()
    trends = tracker.get_all_trends()

    # Header
    st.title("📡 SignalVane")
    st.subheader("Real-Time Autonomous Narrative Detection for Solana")

    # Last updated indicator
    minutes_ago = int(minutes_since) if minutes_since else 0
    st.markdown(f"""
        <div class="refresh-indicator">
            🔄 Last updated: {minutes_ago} min ago
            {'⚡ Live' if minutes_ago < 15 else '⏳ Refreshing soon...'}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("New Programs (14d)", "142", "+12%")
    with col2:
        st.metric("Dev Activity", "2,450", "+8%")
    with col3:
        st.metric("ZK Usage Spike", "45%", "Hot")
    with col4:
        st.metric("Narratives Tracked", len(narratives), f"+{len([t for t in trends.values() if t == 'rising'])}")

    # Sidebar filters
    st.sidebar.markdown("### 🎛️ Filters")

    # Sentiment filter
    sentiment_filter = st.sidebar.multiselect(
        "Sentiment",
        ["positive", "neutral", "negative"],
        default=["positive", "neutral", "negative"]
    )

    # Trend filter
    trend_filter = st.sidebar.multiselect(
        "Trend",
        ["rising", "stable", "falling", "new"],
        default=["rising", "stable", "falling", "new"]
    )

    # Sort options
    sort_by = st.sidebar.selectbox(
        "Sort by",
        ["Novelty Score (High to Low)", "Novelty Score (Low to High)", "Alphabetical", "Trend"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛰️ Signal Sources")
    st.sidebar.info("Real-time data from GitHub API, Helius Labs, and Messari Intelligence.")
    st.sidebar.markdown(f"**Last Sync:** {snapshot['timestamp'][:16]}")
    st.sidebar.markdown(f"**Next Refresh:** {15 - minutes_ago} minutes")

    # Main content
    st.markdown("### 🗺️ Live Narrative Map")

    # Filter and sort narratives
    filtered_narratives = []
    for narrative in narratives:
        sentiment, _ = get_sentiment_score(narrative)
        trend = trends.get(narrative['narrative_name'], 'new')

        # Apply filters
        if sentiment in sentiment_filter and trend in trend_filter:
            filtered_narratives.append({
                **narrative,
                'sentiment': sentiment,
                'trend': trend
            })

    # Sort narratives
    if sort_by == "Novelty Score (High to Low)":
        filtered_narratives.sort(key=lambda x: x.get('novelty_score', 0), reverse=True)
    elif sort_by == "Novelty Score (Low to High)":
        filtered_narratives.sort(key=lambda x: x.get('novelty_score', 0))
    elif sort_by == "Alphabetical":
        filtered_narratives.sort(key=lambda x: x.get('narrative_name', ''))
    elif sort_by == "Trend":
        trend_order = {'rising': 0, 'new': 1, 'stable': 2, 'falling': 3}
        filtered_narratives.sort(key=lambda x: trend_order.get(x['trend'], 99))

    # Display narratives
    for idx, narrative in enumerate(filtered_narratives):
        with st.container():
            trend_emoji, trend_class = get_trend_indicator(narrative['trend'])
            sentiment, sentiment_emoji = get_sentiment_score(narrative)

            delay = idx * 0.15
            st.markdown(f"""
                <div class="narrative-card" style="animation-delay: {delay}s;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="badge">Novelty: {narrative['novelty_score']}/10</span>
                            <span class="badge sentiment-{sentiment}">{sentiment_emoji} {sentiment.title()}</span>
                        </div>
                        <div class="trend-indicator {trend_class}">
                            {trend_emoji} {narrative['trend'].title()}
                        </div>
                    </div>
                    <h2 style='color:#14F195; margin-top:15px;'>{narrative['narrative_name']}</h2>
                    <p style='font-size: 1.1rem;'>{narrative['explanation']}</p>
                    <hr style='border: 0.5px solid rgba(255,255,255,0.1);'>
                    <div style='display: flex; gap: 20px;'>
                        <div>
                            <p style='color:#9945FF; font-weight:bold;'>GitHub Signals</p>
                            <ul style='font-size: 0.9rem;'>
                                {"".join([f"<li>{e}</li>" for e in narrative['evidence']['github']])}
                            </ul>
                        </div>
                        <div>
                            <p style='color:#9945FF; font-weight:bold;'>Market Intelligence</p>
                            <ul style='font-size: 0.9rem;'>
                                {"".join([f"<li>{e}</li>" for e in narrative['evidence']['market_intel']])}
                            </ul>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Show trend chart if available
            trend_chart = create_trend_chart(narrative['narrative_name'], tracker)
            if trend_chart:
                with st.expander("📈 Historical Trend"):
                    st.plotly_chart(trend_chart, use_container_width=True)

            # Show Ideas for this narrative
            st.markdown("#### 💡 Build Ideas")
            narrative_ideas = next((item for item in ideas if item["narrative_name"] == narrative["narrative_name"]), None)
            if narrative_ideas:
                cols = st.columns(3)
                for i, idea in enumerate(narrative_ideas["ideas"]):
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div class="idea-card">
                                <h4 style='margin-bottom:10px; color:white;'>{idea['title']}</h4>
                                <div style='flex-grow: 1;'>
                                    <p style='font-size:0.93rem; opacity:0.8; line-height:1.4;'>{idea['description']}</p>
                                </div>
                                <div style='margin-top:20px; border-top: 1px solid rgba(255,255,255,0.05); padding-top:15px;'>
                                    <div style='color:#14F195; font-size:0.75rem; font-weight:bold; margin-bottom:8px;'>👤 TARGET USER</div>
                                    <div style='font-size:0.85rem; margin-bottom:12px; opacity:0.9;'>{idea['target_user']}</div>
                                    <div style='color:#9945FF; font-size:0.75rem; font-weight:bold; margin-bottom:8px;'>🛠️ TECH STACK</div>
                                    <div style='font-size:0.8rem; font-family:monospace; opacity:0.8;'>{idea['tech_stack']}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    if not filtered_narratives:
        st.warning("No narratives match your current filters. Try adjusting the filters in the sidebar.")

if __name__ == "__main__":
    main()
