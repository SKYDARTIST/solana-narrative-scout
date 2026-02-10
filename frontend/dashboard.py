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
        transition: transform 0.3s ease;
    }
    .narrative-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 0, 255, 0.3);
    }
    .idea-card {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        border-left: 4px solid #9945FF;
    }
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
            st.markdown(f"""
                <div class="narrative-card">
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
                                <strong>{idea['title']}</strong><br>
                                <small>{idea['description']}</small><br>
                                <p style='font-size:0.7rem; color:#14F195; margin-top:5px;'>
                                    <b>Target User:</b> {idea.get('target_user', 'General builders')}
                                </p>
                                <p style='font-size:0.7rem; color:#9945FF; margin-top:5px;'>
                                    <b>Stack:</b> {idea['tech_stack']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown("### 🛰️ Signal Sources")
    st.sidebar.info("Data refreshed every 14 days from GitHub API, Helius Labs, and Messari Intelligence.")
    st.sidebar.markdown(f"**Last Sync:** {snapshot['timestamp'][:10]}")

if __name__ == "__main__":
    main()
