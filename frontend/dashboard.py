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

# Custom CSS for High-Fidelity Neo-Brutalist Style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@800;900&family=Inter:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');

    /* Global App Background */
    .stApp {
        background: #FFFFE0 !important;
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Remove Streamlit default padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* Main Title Styling */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 900;
        font-size: 5rem;
        letter-spacing: -4px;
        color: #000000;
        text-transform: uppercase;
        line-height: 0.85;
        margin-bottom: 10px;
    }

    .subtitle-badge {
        font-family: 'Space Mono', monospace;
        font-size: 14px;
        background: #14F195;
        display: inline-block;
        padding: 6px 15px;
        border: 3px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Metrics Bar */
    .metrics-container {
        display: flex;
        gap: 25px;
        margin-bottom: 40px;
        flex-wrap: wrap;
    }

    .metric-card {
        background: #ffffff;
        border: 4px solid #000000;
        padding: 20px 30px;
        box-shadow: 8px 8px 0px #000000;
        min-width: 180px;
        flex: 1;
    }

    .metric-label {
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        color: #444;
        margin-bottom: 5px;
    }

    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 38px;
        font-weight: 900;
        line-height: 1;
    }

    /* Narrative Map Card */
    .narrative-card {
        background: #ffffff;
        border: 4px solid #000000;
        padding: 0; /* Header handles padding */
        margin-bottom: 40px;
        box-shadow: 12px 12px 0px #000000;
        transition: all 0.2s ease;
        overflow: hidden;
    }

    .narrative-header {
        background: #FF007F;
        color: #ffffff;
        padding: 25px 30px;
        border-bottom: 4px solid #000000;
    }

    .narrative-header h2 {
        font-family: 'Outfit', sans-serif;
        font-size: 32px;
        font-weight: 900;
        margin: 0;
        text-transform: uppercase;
        color: white !important;
    }

    .narrative-body {
        padding: 30px;
    }

    .narrative-body p {
        font-size: 1.15rem;
        line-height: 1.5;
        color: #000000 !important;
    }

    /* Signals Section */
    .signals-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin-top: 30px;
        padding-top: 30px;
        border-top: 4px solid #000000;
    }

    .signal-box h4 {
        font-family: 'Outfit', sans-serif;
        font-size: 18px;
        text-transform: uppercase;
        margin: 0 0 15px 0;
        background: #FFEE00;
        display: inline-block;
        padding: 4px 10px;
        border: 3px solid #000000;
        box-shadow: 3px 3px 0px #000000;
    }

    /* Opportunity Cards (Idea Cards) */
    .sub-section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 26px;
        text-transform: uppercase;
        margin-bottom: 25px;
        padding-left: 15px;
        border-left: 10px solid #9945FF;
        line-height: 1;
    }

    .idea-card {
        background: #ffffff;
        border: 4px solid #000000;
        padding: 25px;
        margin-top: 0px;
        box-shadow: 8px 8px 0px #000000;
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 580px !important; /* Increased for chunky look and consistency */
    }

    .idea-card:hover {
        transform: translate(-3px, -3px);
        box-shadow: 11px 11px 0px #000000;
    }

    .idea-card h4 {
        font-family: 'Outfit', sans-serif;
        font-size: 22px;
        margin: 0 0 15px 0;
        color: #000000 !important;
    }

    .tech-stack-box {
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        background: #f0f0f0;
        padding: 6px;
        border: 2px solid #000000;
        margin-top: auto;
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 5px solid #000000 !important;
    }

    .stMultiSelect div[role="listbox"] {
        border: 3px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }

    /* Status Indicator */
    .refresh-indicator {
        background: #000000;
        color: #ffffff;
        border: 3px solid #000000;
        padding: 10px 20px;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 12px;
        box-shadow: 5px 5px 0px #FF007F;
    }

    /* Utility */
    .brutalist-badge {
        display: inline-block;
        padding: 4px 10px;
        border: 2px solid #000000;
        background: #FFEE00;
        color: #000000; /* Ensure text is visible on yellow/white */
        font-weight: 900;
        font-size: 11px;
        margin-bottom: 10px;
        box-shadow: 3px 3px 0px #000000;
    }

    /* Force Equal Height Columns */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }

    [data-testid="column"] > div {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* Equal height for horizontal blocks */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        align-items: stretch !important;
    }

    /* Hide standard Streamlit header */
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
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

    # Header section with High-Fidelity Branding
    st.markdown("""
<div style="margin-bottom: 20px;">
<div class="subtitle-badge">AUTONOMOUS NARRATIVE SCOUT / SOLANA</div>
<h1 class="main-title">SIGNALVANE</h1>
</div>
""", unsafe_allow_html=True)

    # Last updated indicator (Neo-Brutalist style)
    minutes_ago = int(minutes_since) if minutes_since else 0
    st.markdown(f"""
<div style="display: flex; justify-content: flex-end; margin-top: -80px; margin-bottom: 40px;">
<div class="refresh-indicator">
SYNC: {minutes_ago}m AGO | <span style='color: {"#14F195" if minutes_ago < 5 else "#888888"};'>{"ACTIVE" if minutes_ago < 5 else "STALE"}</span>
</div>
</div>
""", unsafe_allow_html=True)

    # Metrics Bar (Custom HTML for Neo-Brutalist look)
    st.markdown(f"""
<div class="metrics-container">
<div class="metric-card">
<div class="metric-label">PROGRAMS (14D)</div>
<div class="metric-value">142</div>
<div style="font-size: 11px; font-weight: 800; color: #14F195; margin-top: 5px;">↑ 12%</div>
</div>
<div class="metric-card">
<div class="metric-label">DEV DENSITY</div>
<div class="metric-value">2,450</div>
<div style="font-size: 11px; font-weight: 800; color: #14F195; margin-top: 5px;">↑ 8%</div>
</div>
<div class="metric-card">
<div class="metric-label">ZK MOMENTUM</div>
<div class="metric-value">45%</div>
<div style="font-size: 11px; font-weight: 800; color: #9945FF; margin-top: 5px;">PEAK</div>
</div>
<div class="metric-card">
<div class="metric-label">NARRATIVES</div>
<div class="metric-value">{len(narratives):02d}</div>
<div style="font-size: 11px; font-weight: 800; color: #14F195; margin-top: 5px;">{len([t for t in trends.values() if t == 'rising'])} TRENDING</div>
</div>
</div>
""", unsafe_allow_html=True)

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

    st.sidebar.markdown("""
<div style="background: #9945FF; color: white; border: 3px solid black; padding: 10px; font-family: 'Outfit'; font-weight: 800; font-size: 14px; box-shadow: 4px 4px 0px black; text-align: center; text-transform: uppercase; margin-bottom: 15px;">
BUILT BY AAKASH
</div>
<div style="display: flex; flex-direction: column; gap: 10px;">
    <a href="https://x.com/Cryptobullaaa" target="_blank" style="text-decoration: none;">
        <div style="background: #FFEE00; color: black; border: 2px solid black; padding: 8px; font-family: 'Space Mono'; font-weight: 700; font-size: 12px; box-shadow: 3px 3px 0px black; text-align: center;">
            X / CRYPTOBULLAAA
        </div>
    </a>
    <a href="https://github.com/SKYDARTIST" target="_blank" style="text-decoration: none;">
        <div style="background: white; color: black; border: 2px solid black; padding: 8px; font-family: 'Space Mono'; font-weight: 700; font-size: 12px; box-shadow: 3px 3px 0px black; text-align: center;">
            GH / SKYDARTIST
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

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
<div class="narrative-header">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
<div>
<span class="brutalist-badge">NOVELTY: {narrative['novelty_score']}</span>
<span class="brutalist-badge" style="background: white;">{sentiment.upper()}</span>
</div>
<div style="background: white; border: 3px solid black; padding: 4px 10px; font-weight: 900; box-shadow: 3px 3px 0px black; color: black; font-family: 'Space Mono';">
{trend_label}
</div>
</div>
<h2 style='color: white !important;'>{narrative['narrative_name'].upper()}</h2>
</div>
<div class="narrative-body">
<p>{narrative['explanation']}</p>
<div class="signals-grid">
<div class="signal-box">
<h4>GitHub Signals</h4>
<ul style='font-size: 0.9rem; color: #000; padding-left: 20px; font-family: "Inter";'>
{"".join([f"<li style='margin-bottom:8px; border-bottom: 1px dashed black; padding-bottom: 4px;'>{e}</li>" for e in narrative['evidence']['github']])}
</ul>
</div>
<div class="signal-box">
<h4>Market Intel</h4>
<ul style='font-size: 0.9rem; color: #000; padding-left: 20px; font-family: "Inter";'>
{"".join([f"<li style='margin-bottom:8px; border-bottom: 1px dashed black; padding-bottom: 4px;'>{e}</li>" for e in narrative['evidence']['market_intel']])}
</ul>
</div>
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
            st.markdown(f"<div class='sub-section-header'>BUILD OPPORTUNITIES / {narrative['narrative_name'].upper()}</div>", unsafe_allow_html=True)
            narrative_ideas = next((item for item in ideas if item["narrative_name"] == narrative["narrative_name"]), None)
            if narrative_ideas:
                cols = st.columns(3)
                for i, idea in enumerate(narrative_ideas["ideas"]):
                    with cols[i % 3]:
                        st.markdown(f"""
<div class="idea-card">
<h4>{idea['title'].upper()}</h4>
<div style='flex-grow: 1;'>
<p style='font-size:0.95rem; line-height:1.4;'>{idea['description']}</p>
</div>
<div style='margin-top:20px; border-top: 1px solid black; padding-top:15px;'>
<div class="brutalist-badge" style="background: #9945FF; color: white;">TARGET</div>
<p style='font-size:0.9rem; margin-bottom:15px; font-weight: 700;'>{idea['target_user']}</p>
<div class="brutalist-badge">STACK</div>
<div class="tech-stack-box">{idea['tech_stack']}</div>
</div>
</div>
""", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

    if not filtered_narratives:
        st.info("NO NARRATIVES MATCH SELECTED CRITERIA")

if __name__ == "__main__":
    main()
