"""
Simple Gemini API integration using REST API (no SDK issues)
"""
import os
import json
import requests
from dotenv import load_dotenv
from prompts import NARRATIVE_EXTRACTION_PROMPT, BUILD_IDEA_PROMPT

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("GEMINI_API_KEY")
# Use v1beta API with gemini-2.5-flash (latest fast model)
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def call_gemini(prompt):
    """Call Gemini API via REST"""
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        return text
    except Exception as e:
        print(f"❌ API Error: {e}")
        if hasattr(response, 'text'):
            print(f"Response: {response.text}")
        return None

def extract_narratives(signals_data):
    """Generate narratives from signals"""
    print("🤖 Calling Gemini to extract narratives...")

    context = format_signals(signals_data)
    full_prompt = f"""{NARRATIVE_EXTRACTION_PROMPT}

Here is the signal data to analyze:

{context}

Respond ONLY with valid JSON array. No markdown, no explanations, just the JSON array."""

    text = call_gemini(full_prompt)
    if not text:
        return []

    # Clean up markdown
    text = text.strip()
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    try:
        narratives = json.loads(text)
        print(f"✅ Generated {len(narratives)} narratives")
        return narratives
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Raw response: {text[:200]}...")
        return []

def generate_build_ideas(narrative):
    """Generate build ideas for a narrative"""
    print(f"💡 Generating build ideas for: {narrative.get('narrative_name', 'Unknown')}")

    full_prompt = f"""{BUILD_IDEA_PROMPT}

Narrative:
{json.dumps(narrative, indent=2)}

Respond ONLY with valid JSON object in this format:
{{
  "narrative_name": "...",
  "ideas": [
    {{
      "title": "...",
      "description": "...",
      "tech_stack": "...",
      "target_user": "...",
      "feasibility": "..."
    }}
  ]
}}

No markdown, no explanations, just the JSON object."""

    text = call_gemini(full_prompt)
    if not text:
        return {"narrative_name": narrative.get("narrative_name", "Unknown"), "ideas": []}

    # Clean up markdown
    text = text.strip()
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    try:
        ideas_obj = json.loads(text)
        print(f"✅ Generated {len(ideas_obj.get('ideas', []))} build ideas")
        return ideas_obj
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        return {"narrative_name": narrative.get("narrative_name", "Unknown"), "ideas": []}

def format_signals(signals_data):
    """Format signals for LLM"""
    github = signals_data.get("github_momentum", [])
    onchain = signals_data.get("onchain_metrics", [])
    intel = signals_data.get("market_intelligence", [])

    formatted = "## GitHub Activity (Last 14 Days)\n"
    for repo in github[:10]:
        formatted += f"- {repo['name']}: {repo['stars']} stars, {repo.get('language', 'Unknown')} | {repo.get('description', 'No description')[:80]}...\n"

    formatted += "\n## On-chain Metrics\n"
    for metric in onchain:
        formatted += f"- {metric['metric']}: {metric['value']} ({metric['change']})\n"

    formatted += "\n## Market Intelligence\n"
    for signal in intel[:5]:
        formatted += f"- {signal.get('source', 'Unknown')}: {signal.get('summary', signal)}\n"

    return formatted

if __name__ == "__main__":
    print("🧪 Testing Gemini REST API...")

    # Quick test
    test_prompt = "Say 'API works!' if you can read this."
    result = call_gemini(test_prompt)

    if result:
        print(f"✅ API Response: {result[:100]}...")
        print("\n✅ SUCCESS! API is working")
    else:
        print("❌ API test failed")
