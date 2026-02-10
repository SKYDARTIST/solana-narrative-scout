"""
Find the narrative detection bounty listing ID
"""
import requests
import json

BASE_URL = "https://superteam.fun"

# Use the API key from the agent we just registered
API_KEY = "sk_7ab9f3e289d3ae384bece0e057f1dc256173cd64cded3eaf47b7746aacb3e521"

print("🔍 Searching for narrative detection bounty...")

# Discover agent-eligible listings
response = requests.get(
    f"{BASE_URL}/api/agents/listings/live?take=50",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

if response.status_code == 200:
    listings = response.json()
    print(f"\n✅ Found {len(listings)} agent-eligible listings\n")

    # Search for the narrative detection bounty
    for listing in listings:
        title = listing.get('title', '').lower()
        if 'narrative' in title or 'detection' in title or 'idea generation' in title:
            print(f"🎯 FOUND IT!")
            print(f"   Title: {listing.get('title')}")
            print(f"   ID: {listing.get('id')}")
            print(f"   Slug: {listing.get('slug')}")
            print(f"   Rewards: {listing.get('rewards')}")
            print(f"   Deadline: {listing.get('deadline')}")
            print(f"\n📋 Full listing details:")
            print(json.dumps(listing, indent=2))
            break
    else:
        print("❌ Narrative detection bounty not found in agent-eligible listings")
        print("\nAll available listings:")
        for i, listing in enumerate(listings[:10], 1):
            print(f"{i}. {listing.get('title')} (ID: {listing.get('id')})")
else:
    print(f"❌ Failed to fetch listings: {response.status_code}")
    print(f"   Response: {response.text}")
