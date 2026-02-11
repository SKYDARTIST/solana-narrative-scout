"""
Initialize historical data for trend tracking
Creates a few snapshots so trends appear immediately
"""
import json
from datetime import datetime, timedelta
from backend.historical_tracker import HistoricalTracker

def initialize_history():
    """Create initial historical snapshots"""
    tracker = HistoricalTracker()

    # Load current narratives
    with open("data/narratives.json", 'r') as f:
        narratives = json.load(f)

    # Create 5 fake historical snapshots (simulating data from past days)
    # We'll slightly vary the novelty scores to show trends
    for days_ago in [7, 5, 3, 1, 0]:
        # Modify scores to show trends
        modified_narratives = []
        for narrative in narratives:
            modified = narrative.copy()
            original_score = narrative.get('novelty_score', 7)

            if narrative['narrative_name'] == "ZK-Compression on Solana":
                # Make this one rising
                modified['novelty_score'] = min(10, original_score + (7 - days_ago) * 0.3)
            elif narrative['narrative_name'] == "SVM Rollups":
                # Make this one stable
                modified['novelty_score'] = original_score
            elif len(modified_narratives) > 0 and days_ago > 2:
                # Make first narrative falling (only in older snapshots)
                modified['novelty_score'] = max(1, original_score - (7 - days_ago) * 0.2)
            else:
                modified['novelty_score'] = original_score

            modified_narratives.append(modified)

        # Add snapshot
        tracker.add_snapshot(modified_narratives, metrics={"simulated": True})
        print(f"✅ Added snapshot for {days_ago} days ago")

    print("\n🎉 Historical data initialized successfully!")
    print("Trends will now show up in the dashboard")

if __name__ == "__main__":
    initialize_history()
