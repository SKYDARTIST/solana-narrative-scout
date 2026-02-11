"""
Data Refresher for SignalVane
Fetches fresh data, updates narratives, and tracks history
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.scout import fetch_github_signals, fetch_onchain_metrics
from backend.historical_tracker import HistoricalTracker

try:
    from backend.reddit_scraper import fetch_reddit_signals, get_reddit_narrative_evidence
    REDDIT_AVAILABLE = True
except ImportError:
    REDDIT_AVAILABLE = False
    print("Reddit scraper not available")

try:
    from backend.generate_fresh_narratives import generate_fresh_narratives
    NARRATIVE_GEN_AVAILABLE = True
except ImportError:
    NARRATIVE_GEN_AVAILABLE = False
    print("Narrative generator not available")

def refresh_data(force=False, regenerate_narratives=False):
    """
    Refresh all data sources and update historical tracking

    Args:
        force: Force refresh ignoring cache
        regenerate_narratives: Use AI to generate completely fresh narratives from current data

    Returns: (success: bool, last_updated: str)
    """
    try:
        # Check if we need to refresh (cache for 5 minutes - real-time updates)
        cache_file = "backend/data/.last_refresh"
        if not force and os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                last_refresh = datetime.fromisoformat(f.read().strip())
                minutes_since = (datetime.now() - last_refresh).seconds / 60
                if minutes_since < 5:
                    print(f"Using cached data (last refresh: {minutes_since:.1f} min ago)")
                    return True, last_refresh.isoformat()

        print("Fetching fresh data...")

        # Option 1: Regenerate narratives with AI (takes longer but truly fresh)
        if regenerate_narratives and NARRATIVE_GEN_AVAILABLE:
            print("🤖 Regenerating narratives with AI...")
            success, count = generate_fresh_narratives()
            if not success:
                print("⚠️  AI generation failed, using existing narratives")
            else:
                print(f"✅ Generated {count} fresh narratives")
                return True, datetime.now().isoformat()

        # Option 2: Quick refresh - just update data, keep existing narratives
        # Fetch GitHub signals
        github_repos = fetch_github_signals(query="solana", days=14)

        # Fetch on-chain metrics
        onchain_metrics = fetch_onchain_metrics()

        # Fetch Reddit signals (if available)
        reddit_data = None
        if REDDIT_AVAILABLE:
            try:
                print("Fetching Reddit data...")
                reddit_data = fetch_reddit_signals(subreddits=["solana", "SolanaDevs"], days=7)
                print(f"✅ Found {reddit_data['post_count']} Reddit posts")
            except Exception as e:
                print(f"⚠️  Reddit fetch failed: {e}")
                reddit_data = None

        # Load current narratives
        with open("data/narratives.json", 'r') as f:
            narratives = json.load(f)

        # Update snapshot
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "github_signals": len(github_repos),
            "reddit_signals": reddit_data['post_count'] if reddit_data else 0,
            "narratives_count": len(narratives),
            "metrics": onchain_metrics,
            "reddit_data": reddit_data
        }

        with open("data/snapshot.json", 'w') as f:
            json.dump(snapshot, f, indent=2)

        # Track history
        tracker = HistoricalTracker()
        tracker.add_snapshot(narratives, metrics={"github_repos": len(github_repos)})

        # Update cache timestamp
        Path(cache_file).parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'w') as f:
            f.write(datetime.now().isoformat())

        print("✅ Data refreshed successfully")
        return True, datetime.now().isoformat()

    except Exception as e:
        print(f"❌ Error refreshing data: {e}")
        return False, None

def get_last_refresh_time():
    """Get the last refresh timestamp"""
    cache_file = "backend/data/.last_refresh"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return datetime.fromisoformat(f.read().strip())
    return None

def get_minutes_since_refresh():
    """Get minutes since last refresh"""
    last_refresh = get_last_refresh_time()
    if last_refresh:
        return (datetime.now() - last_refresh).seconds / 60
    return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Force refresh ignoring cache')
    args = parser.parse_args()

    success, timestamp = refresh_data(force=args.force)
    if success:
        print(f"Last updated: {timestamp}")
    else:
        print("Refresh failed")
