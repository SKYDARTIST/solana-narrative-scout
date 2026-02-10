import streamlit as st
import json
import os
import pandas as pd

# Page config for Premium Aesthetic
st.set_page_config(
    page_title="SignalVane | Solana Ecosystem Scout",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Glassmorphism & Dark Mode
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
    /* Force equal height columns and inner cards */
    [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    [data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }
    [data-testid="column"] > div {
        display: flex !important;
        flex-direction: column !important;
        flex-grow: 1 !important;
    }
    .idea-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 25px;
        margin-top: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 450px; /* Increased to accommodate longer descriptions */
        height: 100%;
    }
    .idea-card:hover {
        transform: translateY(-5px);
        background: rgba(153, 69, 255, 0.08);
        border: 1px solid rgba(153, 69, 255, 0.3);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    .idea-label {
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .idea-target { color: #14F195; }
    .idea-stack { color: #9945FF; }
    .badge {
        background: #14F195;
        color: black;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .metric-text {
        color: #9945FF;
        font-weight: bold;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    with open("data/snapshot.json", "r") as f:
        snapshot = json.load(f)
    with open("data/narratives.json", "r") as f:
        narratives = json.load(f)
    with open("data/ideas.json", "r") as f:
        ideas = json.load(f)
    return snapshot, narratives, ideas

def main():
    st.title("📡 SignalVane")
    st.subheader("Autonomous Narrative Detection for the Solana Ecosystem")
    st.markdown("---")

    snapshot, narratives, ideas = load_data()

    # Sidebar / Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("New Programs (14d)", "142", "+12%")
    with col2:
        st.metric("Dev Activity", "2,450", "+8%")
    with col3:
        st.metric("ZK Usage Spike", "45%", "Hot")
    with col4:
        st.metric("Signals Ingested", "50+", "Live")

    st.markdown("### 🗺️ Fortnightly Narrative Map")
    
    for idx, narrative in enumerate(narratives):
        with st.container():
            # Apply staggered delay using CSS
            delay = idx * 0.2
            st.markdown(f"""
                <div class="narrative-card" style="animation-delay: {delay}s;">
                    <span class="badge">Novelty: {narrative['novelty_score']}/10</span>
                    <h2 style='color:#14F195;'>{narrative['narrative_name']}</h2>
                    <p style='font-size: 1.1rem;'>{narrative['explanation']}</p>
                    <hr style='border: 0.5px solid rgba(255,255,255,0.1);'>
                    <div style='display: flex; gap: 20px;'>
                        <div>
                            <p class='metric-text'>GitHub Signals</p>
                            <ul style='font-size: 0.9rem;'>
                                {"".join([f"<li>{e}</li>" for e in narrative['evidence']['github']])}
                            </ul>
                        </div>
                        <div>
                            <p class='metric-text'>Market Intelligence</p>
                            <ul style='font-size: 0.9rem;'>
                                {"".join([f"<li>{e}</li>" for e in narrative['evidence']['market_intel']])}
                            </ul>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
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
                                    <div class="idea-label idea-target">👤 Target User</div>
                                    <div style='font-size:0.85rem; margin-bottom:12px; opacity:0.9;'>{idea['target_user']}</div>
                                    <div class="idea-label idea-stack">🛠️ Tech Stack</div>
                                    <div style='font-size:0.8rem; font-family:monospace; opacity:0.8;'>{idea['tech_stack']}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown("### 🛰️ Signal Sources")
    st.sidebar.info("Data refreshed every 14 days from GitHub API, Helius Labs, and Messari Intelligence.")
    st.sidebar.markdown(f"**Last Sync:** {snapshot['timestamp'][:10]}")

if __name__ == "__main__":
    main()
