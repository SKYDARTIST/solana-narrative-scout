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

def refresh_data(force=False):
    """
    Refresh all data sources and update historical tracking
    Returns: (success: bool, last_updated: str)
    """
    try:
        # Check if we need to refresh (cache for 15 minutes)
        cache_file = "backend/data/.last_refresh"
        if not force and os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                last_refresh = datetime.fromisoformat(f.read().strip())
                minutes_since = (datetime.now() - last_refresh).seconds / 60
                if minutes_since < 15:
                    print(f"Using cached data (last refresh: {minutes_since:.1f} min ago)")
                    return True, last_refresh.isoformat()

        print("Fetching fresh data...")

        # Fetch GitHub signals
        github_repos = fetch_github_signals(query="solana", days=14)

        # Fetch on-chain metrics
        onchain_metrics = fetch_onchain_metrics()

        # Load current narratives (in production, we'd regenerate with LLM)
        # For now, just update the snapshot timestamp
        with open("data/narratives.json", 'r') as f:
            narratives = json.load(f)

        # Update snapshot
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "github_signals": len(github_repos),
            "narratives_count": len(narratives),
            "metrics": onchain_metrics
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
