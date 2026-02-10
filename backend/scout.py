import os
import requests
import json
from datetime import datetime, timedelta

def fetch_github_signals(query="solana", days=14):
    """
    Fetches hot Solana repositories created or updated in the last N days.
    """
    date_threshold = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    url = f"https://api.github.com/search/repositories?q={query}+pushed:>{date_threshold}&sort=stars&order=desc"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    # Optional: GITHUB_TOKEN for higher rate limits
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        repos = []
        for item in data.get("items", [])[:15]:
            repos.append({
                "name": item["full_name"],
                "stars": item["stargazers_count"],
                "description": item["description"],
                "url": item["html_url"],
                "language": item["language"],
                "updated_at": item["pushed_at"]
            })
        return repos
    except Exception as e:
        print(f"Error fetching GitHub data: {e}")
        return []

def fetch_onchain_metrics():
    """
    Fetches basic Solana on-chain metrics (Mocked or using Public RPC for TPS/Active Addresses).
    In a real scenario, we'd use a Helius API key here.
    """
    # For the prototype, we'll return some realistic 'observed' spikes
    # based on the 14-day window.
    return [
        {"metric": "New Program Deployments", "value": "142", "change": "+12%", "status": "Stable"},
        {"metric": "Active Developer Wallets", "value": "2,450", "change": "+8%", "status": "Growing"},
        {"metric": "ZK-Compression Usage", "value": "Significant Spike", "change": "+45%", "status": "Hot"}
    ]

if __name__ == "__main__":
    print("Testing GitHub Signal Fetcher...")
    gh_data = fetch_github_signals()
    for r in gh_data:
        print(f"- {r['name']} ({r['stars']} stars): {r['description'][:50]}...")
    
    print("\nOn-chain Metrics:")
    for m in fetch_onchain_metrics():
        print(f"- {m['metric']}: {m['value']} ({m['change']})")
