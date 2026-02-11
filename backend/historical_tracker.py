"""
Historical Data Tracker for SignalVane
Stores narrative data over time to show trends
"""
import json
import os
from datetime import datetime
from pathlib import Path

class HistoricalTracker:
    def __init__(self, history_file="backend/data/history.json"):
        self.history_file = history_file
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create history file if it doesn't exist"""
        Path(self.history_file).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({"snapshots": []}, f)

    def add_snapshot(self, narratives, metrics=None):
        """Add a new snapshot of narratives with timestamp"""
        with open(self.history_file, 'r') as f:
            data = json.load(f)

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "narratives": narratives,
            "metrics": metrics or {}
        }

        data["snapshots"].append(snapshot)

        # Keep only last 30 snapshots (roughly 15 days of data if updated twice daily)
        if len(data["snapshots"]) > 30:
            data["snapshots"] = data["snapshots"][-30:]

        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_history(self, days=7):
        """Get historical snapshots for the last N days"""
        with open(self.history_file, 'r') as f:
            data = json.load(f)

        # For now, return all snapshots (we'll filter by date later)
        return data.get("snapshots", [])

    def get_trend(self, narrative_name):
        """Get trend for a specific narrative over time"""
        history = self.get_history()

        narrative_history = []
        for snapshot in history:
            for narrative in snapshot["narratives"]:
                if narrative.get("narrative_name") == narrative_name:
                    narrative_history.append({
                        "timestamp": snapshot["timestamp"],
                        "novelty_score": narrative.get("novelty_score", 0)
                    })
                    break

        if len(narrative_history) < 2:
            return "new"  # Not enough data

        # Compare latest vs previous
        latest = narrative_history[-1]["novelty_score"]
        previous = narrative_history[-2]["novelty_score"]

        if latest > previous + 1:
            return "rising"
        elif latest < previous - 1:
            return "falling"
        else:
            return "stable"

    def get_all_trends(self):
        """Get trends for all narratives"""
        history = self.get_history()
        if not history:
            return {}

        latest_snapshot = history[-1]
        trends = {}

        for narrative in latest_snapshot["narratives"]:
            name = narrative.get("narrative_name")
            trends[name] = self.get_trend(name)

        return trends

if __name__ == "__main__":
    # Test the tracker
    tracker = HistoricalTracker()

    # Example narratives
    test_narratives = [
        {"narrative_name": "ZK-Compression", "novelty_score": 8},
        {"narrative_name": "SVM Rollups", "novelty_score": 7}
    ]

    tracker.add_snapshot(test_narratives)
    print("Snapshot added successfully")
    print(f"History: {tracker.get_history()}")
