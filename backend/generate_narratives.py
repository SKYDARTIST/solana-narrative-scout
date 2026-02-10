"""
Complete narrative generation pipeline:
1. Fetch real GitHub data
2. Get onchain metrics (mocked for now, but structure is ready for Helius)
3. Add market intelligence (curated)
4. Call Gemini LLM to synthesize narratives
5. Generate build ideas for each narrative
6. Save to JSON files
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from scout import fetch_github_signals, fetch_onchain_metrics
from llm_analyzer_simple import extract_narratives, generate_build_ideas

# Load environment variables
load_dotenv()

def add_market_intelligence():
    """
    Curated market intelligence signals.
    In production, this could scrape blogs/reports automatically.
    """
    return [
        {"source": "Helius Blog", "summary": "AI agents can now self-fund their API keys via CLI"},
        {"source": "Messari Report", "summary": "Solana SVM becoming a pluggable execution layer for custom rollups"},
        {"source": "Light Protocol Announcement", "summary": "ZK-compression officially live, enabling massive state scaling"},
        {"source": "Anatoly Twitter", "summary": "Discussion on agent-centric design patterns for Solana programs"},
        {"source": "Firedancer Team", "summary": "Modular validator architecture allowing specialized SVM implementations"}
    ]

def main():
    print("=" * 60)
    print("🚀 SignalVane - Autonomous Narrative Generation")
    print("=" * 60)

    # Step 1: Fetch Real GitHub Data
    print("\n📊 Step 1: Fetching GitHub signals...")
    github_data = fetch_github_signals(query="solana", days=14)
    print(f"✅ Found {len(github_data)} Solana repositories")

    # Step 2: Get Onchain Metrics
    print("\n⛓️  Step 2: Fetching onchain metrics...")
    onchain_data = fetch_onchain_metrics()
    print(f"✅ Collected {len(onchain_data)} onchain metrics")

    # Step 3: Add Market Intelligence
    print("\n📰 Step 3: Adding market intelligence...")
    intel_data = add_market_intelligence()
    print(f"✅ Added {len(intel_data)} intelligence signals")

    # Step 4: Combine All Signals
    signals_snapshot = {
        "timestamp": datetime.now().isoformat(),
        "github_momentum": github_data,
        "onchain_metrics": onchain_data,
        "market_intelligence": intel_data
    }

    # Save raw signals
    os.makedirs("data", exist_ok=True)
    with open("data/snapshot.json", "w") as f:
        json.dump(signals_snapshot, f, indent=4)
    print("\n💾 Saved raw signals to data/snapshot.json")

    # Step 5: Generate Narratives with Gemini
    print("\n🤖 Step 5: Analyzing signals with Gemini LLM...")
    try:
        narratives = extract_narratives(signals_snapshot)

        if not narratives:
            print("⚠️  No narratives generated. Using fallback data.")
            return

        # Save narratives
        with open("data/narratives.json", "w") as f:
            json.dump(narratives, f, indent=4)
        print(f"✅ Generated and saved {len(narratives)} narratives")

        # Step 6: Generate Build Ideas for Each Narrative
        print("\n💡 Step 6: Generating build ideas...")
        all_ideas = []

        for narrative in narratives:
            ideas_obj = generate_build_ideas(narrative)
            all_ideas.append(ideas_obj)

        # Save build ideas
        with open("data/ideas.json", "w") as f:
            json.dump(all_ideas, f, indent=4)
        print(f"✅ Generated and saved {len(all_ideas)} sets of build ideas")

        # Summary
        print("\n" + "=" * 60)
        print("✅ GENERATION COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  - GitHub Repos Analyzed: {len(github_data)}")
        print(f"  - Onchain Metrics: {len(onchain_data)}")
        print(f"  - Intelligence Signals: {len(intel_data)}")
        print(f"  - Narratives Generated: {len(narratives)}")
        print(f"  - Build Ideas Generated: {sum(len(i.get('ideas', [])) for i in all_ideas)}")
        print(f"\n📂 Output Files:")
        print(f"  - data/snapshot.json (raw signals)")
        print(f"  - data/narratives.json (AI-generated narratives)")
        print(f"  - data/ideas.json (AI-generated build ideas)")
        print(f"\n🎉 Run 'streamlit run frontend/dashboard.py' to view!")

    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        print("\n💡 Make sure your .env file has GEMINI_API_KEY set")
        print("   Example: GEMINI_API_KEY=your_key_here")

if __name__ == "__main__":
    main()
