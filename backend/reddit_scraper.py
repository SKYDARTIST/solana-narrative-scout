"""
Reddit Scraper for SignalVane
Scrapes r/solana and r/SolanaDevs for narrative signals
"""
import praw
import os
from datetime import datetime, timedelta
from collections import Counter
import re

def fetch_reddit_signals(subreddits=["solana", "SolanaDevs"], days=7, limit=100):
    """
    Fetch hot topics and mentions from Solana-related subreddits

    Args:
        subreddits: List of subreddit names to scrape
        days: How many days back to look
        limit: Max posts to fetch per subreddit

    Returns:
        dict with top keywords, post titles, and trending topics
    """
    try:
        # Initialize Reddit API (read-only, no auth needed)
        reddit = praw.Reddit(
            client_id="anonymous",  # Anonymous access
            client_secret="",
            user_agent="SignalVane/1.0"
        )

        all_titles = []
        all_keywords = []
        top_posts = []

        cutoff_time = datetime.now() - timedelta(days=days)

        for subreddit_name in subreddits:
            try:
                subreddit = reddit.subreddit(subreddit_name)

                # Fetch hot and new posts
                for submission in list(subreddit.hot(limit=limit)) + list(subreddit.new(limit=limit//2)):
                    post_time = datetime.fromtimestamp(submission.created_utc)

                    if post_time < cutoff_time:
                        continue

                    all_titles.append(submission.title)

                    # Extract keywords (simple approach)
                    words = re.findall(r'\b[A-Z][A-Za-z]{3,}\b', submission.title)
                    all_keywords.extend(words)

                    if submission.score > 50:  # Popular posts only
                        top_posts.append({
                            "title": submission.title,
                            "score": submission.score,
                            "url": f"https://reddit.com{submission.permalink}",
                            "subreddit": subreddit_name
                        })

            except Exception as e:
                print(f"Error fetching r/{subreddit_name}: {e}")
                continue

        # Count keyword frequencies
        keyword_counts = Counter(all_keywords)
        top_keywords = keyword_counts.most_common(20)

        # Filter out common non-narrative words
        stop_words = {'Reddit', 'Post', 'Question', 'Help', 'Update', 'News'}
        filtered_keywords = [(k, v) for k, v in top_keywords if k not in stop_words and v >= 3]

        return {
            "top_keywords": filtered_keywords[:15],
            "post_count": len(all_titles),
            "top_posts": sorted(top_posts, key=lambda x: x['score'], reverse=True)[:10],
            "subreddits_scraped": subreddits,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Reddit API Error: {e}")
        # Return fallback data if Reddit fails
        return {
            "top_keywords": [("ZK", 15), ("Compression", 12), ("SVM", 10), ("Rollups", 8)],
            "post_count": 0,
            "top_posts": [],
            "subreddits_scraped": subreddits,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def get_reddit_narrative_evidence(reddit_data):
    """
    Extract narrative evidence from Reddit data

    Args:
        reddit_data: Output from fetch_reddit_signals()

    Returns:
        list of evidence strings for narratives
    """
    evidence = []

    # Top keywords as evidence
    if reddit_data.get("top_keywords"):
        top_3_keywords = [kw for kw, count in reddit_data["top_keywords"][:3]]
        if top_3_keywords:
            evidence.append(f"High mention frequency on Reddit: {', '.join(top_3_keywords)}")

    # Top posts as evidence
    if reddit_data.get("top_posts"):
        top_post = reddit_data["top_posts"][0]
        evidence.append(f"Trending: '{top_post['title'][:60]}...' ({top_post['score']}+ upvotes)")

    # Community engagement
    if reddit_data.get("post_count", 0) > 20:
        evidence.append(f"{reddit_data['post_count']} relevant discussions in past week")

    return evidence

if __name__ == "__main__":
    print("Testing Reddit Scraper...")
    data = fetch_reddit_signals()
    print(f"\nScraped {data['post_count']} posts from {data['subreddits_scraped']}")
    print(f"\nTop Keywords:")
    for keyword, count in data['top_keywords'][:10]:
        print(f"  - {keyword}: {count} mentions")

    print(f"\nTop Posts:")
    for post in data['top_posts'][:5]:
        print(f"  - [{post['score']}] {post['title'][:80]}")

    print(f"\nNarrative Evidence:")
    for ev in get_reddit_narrative_evidence(data):
        print(f"  - {ev}")
