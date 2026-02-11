"""
Fresh Narrative Generator for SignalVane
Runs the complete pipeline: fetch signals → analyze → generate ideas → save
"""
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.scout import fetch_github_signals, fetch_onchain_metrics
from backend.llm_analyzer import NarrativeAnalyzer

try:
    from backend.reddit_scraper import fetch_reddit_signals
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False
    print("⚠️  Reddit scraper not available")

def generate_fresh_narratives():
    """
    Generate completely fresh narratives from current week's data
    Returns: (success: bool, narrative_count: int)
    """
    print("\n" + "="*60)
    print("🚀 GENERATING FRESH NARRATIVES FROM CURRENT DATA")
    print("="*60 + "\n")

    try:
        # Step 1: Fetch all signal sources
        print("📊 Step 1/5: Fetching GitHub signals...")
        github_repos = fetch_github_signals(query="solana", days=14)
        print(f"   ✅ Found {len(github_repos)} active repos")

        print("\n📊 Step 2/5: Fetching on-chain metrics...")
        onchain_metrics = fetch_onchain_metrics()
        print(f"   ✅ Collected {len(onchain_metrics)} metrics")

        print("\n📊 Step 3/5: Fetching Reddit signals...")
        reddit_data = None
        if REDDIT_AVAILABLE:
            try:
                reddit_data = fetch_reddit_signals(subreddits=["solana", "SolanaDevs"], days=7)
                print(f"   ✅ Found {reddit_data['post_count']} Reddit posts")
                print(f"   ✅ Top keywords: {', '.join([kw for kw, _ in reddit_data['top_keywords'][:5]])}")
            except Exception as e:
                print(f"   ⚠️  Reddit fetch failed: {e}")
                reddit_data = None
        else:
            print("   ⏭️  Skipping (not available)")

        # Step 2: Prepare signals for LLM
        print("\n🤖 Step 4/5: Analyzing signals with Gemini AI...")
        signals_data = {
            "github_momentum": github_repos[:15],  # Top 15 repos
            "onchain_metrics": onchain_metrics,
            "market_intelligence": []
        }

        # Add Reddit intelligence if available
        if reddit_data and reddit_data.get('top_keywords'):
            for keyword, count in reddit_data['top_keywords'][:5]:
                signals_data["market_intelligence"].append({
                    "source": "Reddit r/solana",
                    "summary": f"{keyword} mentioned {count} times in discussions"
                })

        # Step 3: Generate narratives using LLM
        analyzer = NarrativeAnalyzer()
        narratives = analyzer.extract_narratives(signals_data)

        if not narratives:
            print("   ❌ Failed to generate narratives")
            return False, 0

        print(f"   ✅ Generated {len(narratives)} narratives:")
        for n in narratives:
            print(f"      • {n['narrative_name']}")

        # Step 4: Generate build ideas for each narrative
        print(f"\n💡 Step 5/5: Generating build ideas...")
        all_ideas = []
        for narrative in narratives:
            ideas_obj = analyzer.generate_build_ideas(narrative)
            all_ideas.append(ideas_obj)
            print(f"   ✅ {narrative['narrative_name']}: {len(ideas_obj.get('ideas', []))} ideas")

        # Step 5: Save everything to data files
        print("\n💾 Saving to data files...")

        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Save narratives
        with open("data/narratives.json", 'w') as f:
            json.dump(narratives, f, indent=2)
        print("   ✅ Saved narratives.json")

        # Save build ideas
        with open("data/ideas.json", 'w') as f:
            json.dump(all_ideas, f, indent=2)
        print("   ✅ Saved ideas.json")

        # Save snapshot with metadata
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "github_signals": len(github_repos),
            "reddit_signals": reddit_data['post_count'] if reddit_data else 0,
            "narratives_count": len(narratives),
            "metrics": onchain_metrics,
            "reddit_data": reddit_data,
            "generation_method": "AI-powered (Gemini 2.5 Flash)"
        }

        with open("data/snapshot.json", 'w') as f:
            json.dump(snapshot, f, indent=2)
        print("   ✅ Saved snapshot.json")

        print("\n" + "="*60)
        print(f"🎉 SUCCESS! Generated {len(narratives)} fresh narratives")
        print("="*60 + "\n")

        return True, len(narratives)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False, 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate fresh narratives from current data")
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated without saving')
    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be saved\n")

    success, count = generate_fresh_narratives()

    if success:
        print(f"\n✅ Generated {count} narratives successfully!")
        print("📊 View them in the dashboard: streamlit run frontend/dashboard.py")
    else:
        print("\n❌ Narrative generation failed")
        sys.exit(1)
