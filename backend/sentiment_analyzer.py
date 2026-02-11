"""
Sentiment Analyzer for SignalVane
Uses Gemini AI to analyze narrative sentiment and momentum
"""
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_narrative_sentiment(narrative):
    """
    Use Gemini AI to analyze the sentiment and momentum of a narrative

    Args:
        narrative: dict with narrative_name, explanation, evidence

    Returns:
        dict with sentiment, confidence, reasoning
    """
    try:
        # Build the prompt
        prompt = f"""Analyze the sentiment and momentum of this Solana ecosystem narrative:

**Narrative:** {narrative['narrative_name']}

**Explanation:** {narrative['explanation']}

**GitHub Evidence:**
{chr(10).join(['- ' + e for e in narrative['evidence']['github']])}

**Market Intelligence:**
{chr(10).join(['- ' + e for e in narrative['evidence']['market_intel']])}

**Novelty Score:** {narrative.get('novelty_score', 5)}/10

Analyze the overall sentiment (positive/neutral/negative) based on:
1. The strength and quality of evidence
2. The narrative's potential impact on Solana ecosystem
3. The momentum indicators (GitHub activity, market signals)
4. The novelty and innovation level

Respond in JSON format:
{{
    "sentiment": "positive|neutral|negative",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation (1-2 sentences)",
    "momentum_score": 0-10
}}"""

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        # Parse the JSON response
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line (```)
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines).strip()

        result = json.loads(response_text)

        # Validate the response
        if result['sentiment'] not in ['positive', 'neutral', 'negative']:
            raise ValueError(f"Invalid sentiment: {result['sentiment']}")

        return result

    except Exception as e:
        print(f"⚠️ Sentiment analysis failed for '{narrative['narrative_name']}': {e}")

        # Fallback to heuristic if AI fails
        score = narrative.get('novelty_score', 5)
        if score >= 8:
            sentiment = "positive"
        elif score >= 6:
            sentiment = "neutral"
        else:
            sentiment = "negative"

        return {
            "sentiment": sentiment,
            "confidence": 0.5,
            "reasoning": "Fallback heuristic based on novelty score",
            "momentum_score": score,
            "error": str(e)
        }

def batch_analyze_narratives(narratives):
    """
    Analyze sentiment for multiple narratives
    Returns dict mapping narrative_name to sentiment results
    """
    results = {}

    for narrative in narratives:
        name = narrative['narrative_name']
        print(f"Analyzing sentiment: {name}...")
        results[name] = analyze_narrative_sentiment(narrative)

    return results

def get_sentiment_emoji(sentiment):
    """Get indicator for sentiment (formerly emoji)"""
    return ""  # Emojis removed as requested

if __name__ == "__main__":
    # Test with sample narrative
    print("Testing Sentiment Analyzer...")
    # ... (rest of test code)

if __name__ == "__main__":
    # Test with sample narrative
    print("Testing Sentiment Analyzer...")

    sample_narrative = {
        "narrative_name": "ZK-Compression on Solana",
        "explanation": "Light Protocol's ZK-compression allows storing state off-chain while keeping proofs on-chain, dramatically reducing costs.",
        "evidence": {
            "github": [
                "Light Protocol repos: 145+ commits in 14 days",
                "ZK tooling libraries gaining traction"
            ],
            "market_intel": [
                "90% cost reduction vs traditional state storage",
                "Early adopters seeing significant improvements"
            ]
        },
        "novelty_score": 8
    }

    result = analyze_narrative_sentiment(sample_narrative)

    print(f"\n{'='*50}")
    print(f"Narrative: {sample_narrative['narrative_name']}")
    print(f"Sentiment: {result['sentiment']} {get_sentiment_emoji(result['sentiment'])}")
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Momentum Score: {result['momentum_score']}/10")
    print(f"Reasoning: {result['reasoning']}")
    print(f"{'='*50}")
