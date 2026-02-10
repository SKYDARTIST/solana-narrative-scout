import json
import os
from scout import fetch_github_signals, fetch_onchain_metrics

def generate_snapshot():
    print("Generating Signal Snapshot...")
    
    # 1. Fetch Quantitative Signals
    github_repos = fetch_github_signals()
    onchain_metrics = fetch_onchain_metrics()
    
    # 2. Load Qualitative Signals (from our search-based JSON)
    qualitative_path = "data/qualitative_signals.json"
    if os.path.exists(qualitative_path):
        with open(qualitative_path, "r") as f:
            qualitative_signals = json.load(f)
    else:
        qualitative_signals = []
        
    # 3. Combine
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "signals": {
            "github_momentum": github_repos,
            "onchain_metrics": onchain_metrics,
            "market_intelligence": qualitative_signals
        }
    }
    
    # 4. Save
    os.makedirs("data", exist_ok=True)
    with open("data/snapshot.json", "w") as f:
        json.dump(snapshot, f, indent=4)
    
    print(f"Snapshot saved to data/snapshot.json. Total signals: {len(github_repos) + len(onchain_metrics) + len(qualitative_signals)}")

if __name__ == "__main__":
    from datetime import datetime
    generate_snapshot()
