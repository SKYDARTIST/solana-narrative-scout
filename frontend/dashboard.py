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
from backend.sentiment_analyzer import analyze_narrative_sentiment

# Page config for Premium Aesthetic
st.set_page_config(
    page_title="SignalVane | Solana Ecosystem Scout",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh configuration
REFRESH_INTERVAL = 300  # 5 minutes in seconds (truly real-time)

# Custom CSS for Neo-Brutalism Style (No Emojis)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;900&family=Space+Mono:wght@400;700&display=swap');

    .stApp {
        background: #0a0a0a;
        color: #ffffff;
        font-family: 'Space Mono', monospace;
    }

    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        letter-spacing: -2px;
        color: #14F195;
        text-transform: uppercase;
        border-bottom: 6px solid #14F195;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    .narrative-card {
        background: #1a1a1a;
        border: 4px solid #000000;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 10px 10px 0px #14F195;
        transition: all 0.15s ease;
    }

    .narrative-card:hover {
        transform: translate(-3px, -3px);
        box-shadow: 13px 13px 0px #14F195;
    }

    .idea-card {
        background: #1a1a1a;
        border: 3px solid #000000;
        padding: 24px;
        margin-top: 15px;
        box-shadow: 7px 7px 0px #9945FF;
        transition: all 0.15s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 480px;
        overflow: hidden;
    }

    .idea-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 10px 10px 0px #9945FF;
    }

    .badge {
        background: #14F195;
        color: #000000;
        padding: 8px 16px;
        border: 3px solid #000000;
        font-size: 0.75rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-right: 10px;
        box-shadow: 3px 3px 0px #000000;
    }

    .trend-indicator {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 8px 16px;
        border: 3px solid currentColor;
        display: inline-block;
        box-shadow: 4px 4px 0px currentColor;
    }

    .rising {
        color: #14F195;
        background: rgba(20, 241, 149, 0.1);
    }
    .falling {
        color: #FF4444;
        background: rgba(255, 68, 68, 0.1);
    }
    .stable {
        color: #FFD700;
        background: rgba(255, 215, 0, 0.1);
    }
    .new-badge {
        color: #9945FF;
        background: rgba(153, 69, 255, 0.1);
    }

    .sentiment-positive {
        color: #14F195;
        font-weight: 900;
        text-transform: uppercase;
        border: 2px solid #14F195;
        padding: 4px 8px;
        background: rgba(20, 241, 149, 0.1);
    }
    .sentiment-negative {
        color: #FF4444;
        font-weight: 900;
        text-transform: uppercase;
        border: 2px solid #FF4444;
        padding: 4px 8px;
        background: rgba(255, 68, 68, 0.1);
    }
    .sentiment-neutral {
        color: #FFD700;
        font-weight: 900;
        text-transform: uppercase;
        border: 2px solid #FFD700;
        padding: 4px 8px;
        background: rgba(255, 215, 0, 0.1);
    }

    .refresh-indicator {
        position: fixed;
        top: 60px;
        right: 30px;
        background: #14F195;
        color: #000000;
        border: 3px solid #000000;
        padding: 12px 24px;
        font-size: 0.8rem;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        z-index: 1000;
        box-shadow: 5px 5px 0px #000000;
        text-transform: uppercase;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    h2 {
        color: #14F195;
        border-left: 6px solid #14F195;
        padding-left: 20px;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes (real-time updates)
def load_data():
    """Load data with caching"""
    with open("data/snapshot.json", "r") as f:
        snapshot = json.load(f)
    with open("data/narratives.json", "r") as f:
        narratives = json.load(f)
    with open("data/ideas.json", "r") as f:
        ideas = json.load(f)
    return snapshot, narratives, ideas

@st.cache_data(ttl=300)  # Cache sentiment analysis for 5 minutes
def get_sentiment_score(narrative):
    """
    AI-powered sentiment analysis using Gemini
    Falls back to heuristic if AI fails
    """
    # Try AI analysis first
    result = analyze_narrative_sentiment(narrative)

    sentiment = result.get('sentiment', 'neutral')

    return sentiment, ""  # No emojis - neo-brutalism style

def get_trend_indicator(trend):
    """Get text-based indicator and class for trend"""
    if trend == "rising":
        return "RISING", "rising"
    elif trend == "falling":
        return "FALLING", "falling"
    elif trend == "stable":
        return "STABLE", "stable"
    else:
        return "NEW", "new-badge"

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
        line=dict(color='#14F195', width=3, shape='spline'),
        marker=dict(size=6, color='#14F195', borderwidth=2, bordercolor='#0a0a1a'),
        fill='tozeroy',
        fillcolor='rgba(20, 241, 149, 0.05)'
    ))

    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        height=180,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#888888', size=11),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=True),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', showticklabels=True)
    )

    return fig

def main():
    # Auto-refresh mechanism
    minutes_since = get_minutes_since_refresh()
    if minutes_since and minutes_since >= 5:
        with st.spinner("Synchronizing data..."):
            refresh_data()
            st.cache_data.clear()
            st.rerun()

    # Load data
    snapshot, narratives, ideas = load_data()
    tracker = HistoricalTracker()
    trends = tracker.get_all_trends()

    # Header section with custom title
    st.markdown("""
        <div class="title-container">
            <h1 class="main-title">SIGNALVANE</h1>
            <p style='color: #888888; letter-spacing: 2px; font-weight: 500;'>AUTONOMOUS NARRATIVE SCOUT / SOLANA</p>
        </div>
    """, unsafe_allow_html=True)

    # Last updated indicator
    minutes_ago = int(minutes_since) if minutes_since else 0
    st.markdown(f"""
        <div class="refresh-indicator">
            LAST SYNC: {minutes_ago}m AGO
            <span style='color: {"#14F195" if minutes_ago < 5 else "#888888"}; margin-left: 10px;'>
                {"ACTIVE" if minutes_ago < 5 else "STALE"}
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Metrics with cleaner appearance
    met1, met2, met3, met4 = st.columns(4)
    met1.metric("PROGRAMS (14D)", "142", "12%")
    met2.metric("DEV DENSITY", "2,450", "8%")
    met3.metric("ZK MOMENTUM", "45%", "PEAK")
    met4.metric("NARRATIVES", len(narratives), f"{len([t for t in trends.values() if t == 'rising'])} TRENDING")

    # Sidebar filters (e-free)
    st.sidebar.markdown("<h3 style='font-family:Outfit;'>FILTERS</h3>", unsafe_allow_html=True)

    sentiment_filter = st.sidebar.multiselect(
        "SENTIMENT",
        ["positive", "neutral", "negative"],
        default=["positive", "neutral", "negative"]
    )

    trend_filter = st.sidebar.multiselect(
        "TREND",
        ["rising", "stable", "falling", "new"],
        default=["rising", "stable", "falling", "new"]
    )

    sort_by = st.sidebar.selectbox(
        "SORT BY",
        ["Novelty (High to Low)", "Novelty (Low to High)", "Alphabetical", "Trend Strength"]
    )

    st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.1)'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#888888; font-size: 0.8rem;'>SIGNAL SOURCES</p>", unsafe_allow_html=True)
    st.sidebar.text("GitHub API, Reddit, On-Chain")
    st.sidebar.markdown(f"<p style='color:#444444; font-size: 0.75rem;'>SYNC: {snapshot['timestamp'][:16]}<br>T-MINUS: {max(0, 5 - minutes_ago)} MIN</p>", unsafe_allow_html=True)

    # Main content
    st.markdown("<h3 style='font-family:Outfit; margin-bottom: 30px;'>LIVE NARRATIVE MAP</h3>", unsafe_allow_html=True)

    # Filter and sort narratives
    filtered_narratives = []
    for narrative in narratives:
        sentiment, _ = get_sentiment_score(narrative)
        trend = trends.get(narrative['narrative_name'], 'new')

        if sentiment in sentiment_filter and trend in trend_filter:
            filtered_narratives.append({
                **narrative,
                'sentiment': sentiment,
                'trend': trend
            })

    if sort_by == "Novelty (High to Low)":
        filtered_narratives.sort(key=lambda x: x.get('novelty_score', 0), reverse=True)
    elif sort_by == "Novelty (Low to High)":
        filtered_narratives.sort(key=lambda x: x.get('novelty_score', 0))
    elif sort_by == "Alphabetical":
        filtered_narratives.sort(key=lambda x: x.get('narrative_name', ''))
    elif sort_by == "Trend Strength":
        trend_order = {'rising': 0, 'new': 1, 'stable': 2, 'falling': 3}
        filtered_narratives.sort(key=lambda x: trend_order.get(x['trend'], 99))

    # Display narratives
    for idx, narrative in enumerate(filtered_narratives):
        with st.container():
            trend_label, trend_class = get_trend_indicator(narrative['trend'])
            sentiment, _ = get_sentiment_score(narrative)

            st.markdown(f"""
                <div class="narrative-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                        <div>
                            <span class="badge" style="background: rgba(153, 69, 255, 0.1); color: #9945FF; border-color: rgba(153, 69, 255, 0.3);">NOVELTY: {narrative['novelty_score']}</span>
                            <span class="badge" style='background: rgba(255,255,255,0.05); color: #888888; border-color: rgba(255,255,255,0.1);'>{sentiment.upper()}</span>
                        </div>
                        <div class="trend-indicator {trend_class}">
                            {trend_label}
                        </div>
                    </div>
                    <h2 style='font-family: Outfit; font-weight: 800; color:white; margin: 0 0 15px 0;'>{narrative['narrative_name'].upper()}</h2>
                    <p style='font-size: 1.1rem; color: #adb5bd; line-height: 1.6;'>{narrative['explanation']}</p>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px; padding-top: 25px; border-top: 1px solid rgba(255,255,255,0.05);'>
                        <div>
                            <p style='color:#14F195; font-size: 0.75rem; font-weight:800; letter-spacing: 1px; margin-bottom: 12px;'>GITHUB SIGNALS</p>
                            <ul style='font-size: 0.9rem; color: #888888; padding-left: 20px;'>
                                {"".join([f"<li style='margin-bottom:8px;'>{e}</li>" for e in narrative['evidence']['github']])}
                            </ul>
                        </div>
                        <div>
                            <p style='color:#14F195; font-size: 0.75rem; font-weight:800; letter-spacing: 1px; margin-bottom: 12px;'>MARKET INTEL</p>
                            <ul style='font-size: 0.9rem; color: #888888; padding-left: 20px;'>
                                {"".join([f"<li style='margin-bottom:8px;'>{e}</li>" for e in narrative['evidence']['market_intel']])}
                            </ul>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Trend chart
            trend_chart = create_trend_chart(narrative['narrative_name'], tracker)
            if trend_chart:
                with st.expander("VIEW HISTORICAL NOVELTY"):
                    st.plotly_chart(trend_chart, use_container_width=True)

            # Ideas
            st.markdown(f"<p style='color: #444444; font-weight: 800; letter-spacing: 1px; margin: 20px 0;'>BUILD OPPORTUNITIES / {narrative['narrative_name'].upper()}</p>", unsafe_allow_html=True)
            narrative_ideas = next((item for item in ideas if item["narrative_name"] == narrative["narrative_name"]), None)
            if narrative_ideas:
                cols = st.columns(3)
                for i, idea in enumerate(narrative_ideas["ideas"]):
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div class="idea-card">
                                <h4 style='font-family: Outfit; font-weight: 800; color:white; margin: 0 0 15px 0;'>{idea['title'].upper()}</h4>
                                <div style='flex-grow: 1;'>
                                    <p style='font-size:0.95rem; color: #888888; line-height:1.5;'>{idea['description']}</p>
                                </div>
                                <div style='margin-top:15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top:15px;'>
                                    <p style='color: #444444; font-size: 0.65rem; font-weight: 800; margin-bottom: 2px;'>TARGET</p>
                                    <p style='font-size:0.85rem; color: #bbb; margin-bottom:10px;'>{idea['target_user']}</p>
                                    <p style='color: #444444; font-size: 0.65rem; font-weight: 800; margin-bottom: 2px;'>STACK</p>
                                    <p style='font-size:0.8rem; font-family: Space Mono; color: #9945FF;'>{idea['tech_stack']}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

    if not filtered_narratives:
        st.info("NO NARRATIVES MATCH SELECTED CRITERIA")

if __name__ == "__main__":
    main()
