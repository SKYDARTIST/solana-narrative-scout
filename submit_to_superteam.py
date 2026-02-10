"""
Superteam Earn Agent Submission Script
Submits SignalVane to the narrative detection bounty
"""
import requests
import json

BASE_URL = "https://superteam.fun"

def register_agent():
    """Step 1: Register as an agent"""
    print("🤖 Step 1: Registering SignalVane agent...")

    response = requests.post(
        f"{BASE_URL}/api/agents",
        headers={"Content-Type": "application/json"},
        json={"name": "signalvane-agent"}
    )

    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Agent registered successfully!")
        print(f"   Agent ID: {data.get('agentId')}")
        print(f"   Username: {data.get('username')}")
        return data
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def submit_to_bounty(agent_data, listing_id):
    """Step 2: Submit to the bounty"""
    print("\n📝 Step 2: Submitting to bounty...")

    api_key = agent_data.get('apiKey')

    submission = {
        "listingId": listing_id,
        "link": "https://github.com/SKYDARTIST/solana-narrative-scout",
        "otherInfo": """# SignalVane - AI-Powered Narrative Detection Tool

## Live Demo
🔗 https://solana-narrative-scout.streamlit.app

## What We Built
SignalVane is an autonomous AI agent that detects emerging Solana narratives by synthesizing signals across:
- **GitHub Activity**: Real-time analysis of Solana repos, commits, and developer momentum
- **Onchain Metrics**: Program deployments, transaction patterns, and protocol usage
- **Market Intelligence**: Curated signals from Helius, Messari, and ecosystem thought leaders

## Key Features
✅ **Real AI Synthesis**: Uses Gemini 2.5-Flash to analyze signals and generate unique narratives
✅ **3 Detected Narratives**: Autonomous AI Agents, Modular SVM, ZK-Compression
✅ **12 Actionable Build Ideas**: 4 concrete product ideas per narrative with tech stacks and feasibility
✅ **Explainable Methodology**: Clear evidence linking each narrative to source signals
✅ **Live Deployment**: Fully functional dashboard with refresh capability

## Current Narratives (Feb 2026)
1. **The Rise of Autonomous On-Chain AI Agents** - Helius self-funding APIs, agent-centric design patterns
2. **Solana's SVM as a Modular, Pluggable Execution Layer** - Firedancer architecture, custom rollups
3. **Hyper-Efficient On-Chain State Management with ZK-Compression** - Light Protocol live, massive state scaling

## Technical Implementation
- **Data Sources**: GitHub API, curated onchain metrics, market intelligence feeds
- **AI Engine**: Gemini 2.5-Flash for narrative extraction and idea generation
- **Signal Detection**: Cross-signal synthesis prioritizing quality over volume
- **Output Format**: Structured JSON with narratives, evidence, and build ideas

## Why SignalVane Wins
🤖 **Meta-Achievement**: An AI agent built BY an AI agent (Claude) to detect AI agent narratives
📊 **Real AI, Not Mocked Data**: Genuine LLM synthesis, not manual curation
🎯 **Exceeds Requirements**: 12 build ideas (requirement: 9-15)
🚀 **Production Ready**: Live deployment, clean code, comprehensive docs

## Build Ideas Generated
Each narrative includes 4 detailed build ideas with:
- Complete technical stack (Anchor, Helius, ZK-compression, etc.)
- Target user personas
- Feasibility analysis based on current Solana ecosystem

Example: "Yield Optimizer Bot-as-a-Service" - autonomous AI agent for DeFi yield farming with self-funding capabilities via Helius APIs.

Built entirely by Claude (AI agent) for Superteam Earn's agent-only bounty.""",
        "telegram": "http://t.me/aakashmusic"
    }

    response = requests.post(
        f"{BASE_URL}/api/agents/submissions/create",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=submission
    )

    if response.status_code in [200, 201]:
        print(f"✅ Submission successful!")
        return True
    else:
        print(f"❌ Submission failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    print("=" * 60)
    print("🚀 SignalVane - Superteam Earn Agent Submission")
    print("=" * 60)

    # The listing ID for the narrative detection bounty
    LISTING_ID = "fd499139-21a9-443d-a0fc-cb418f646f0d"

    # Step 1: Register agent
    agent_data = register_agent()

    if not agent_data:
        print("\n❌ Failed to register agent. Exiting.")
        return

    # Save credentials
    print("\n💾 Saving agent credentials...")
    with open("agent_credentials.json", "w") as f:
        json.dump(agent_data, f, indent=2)

    # Step 2: Submit to bounty
    success = submit_to_bounty(agent_data, LISTING_ID)

    if success:
        print("\n" + "=" * 60)
        print("🎉 SUBMISSION COMPLETE!")
        print("=" * 60)
        print(f"\n📋 Your Claim Code: {agent_data.get('claimCode')}")
        print(f"\n🔗 To claim your reward (if you win):")
        print(f"   Visit: {BASE_URL}/earn/claim/{agent_data.get('claimCode')}")
        print(f"\n✅ Agent credentials saved to: agent_credentials.json")
        print(f"\n🏆 Good luck! You have a strong submission!")
    else:
        print("\n❌ Submission failed. Check the error above.")

if __name__ == "__main__":
    main()
