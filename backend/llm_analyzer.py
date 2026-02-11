import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import NARRATIVE_EXTRACTION_PROMPT, BUILD_IDEA_PROMPT

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class NarrativeAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env file or pass as parameter.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def extract_narratives(self, signals_data):
        """
        Takes raw signal data (GitHub, onchain, social) and generates 2-3 narratives.
        """
        print("🤖 Calling Gemini to extract narratives...")

        # Format the signals into a readable prompt
        context = self._format_signals_for_llm(signals_data)

        full_prompt = f"""
{NARRATIVE_EXTRACTION_PROMPT}

Here is the signal data to analyze:

{context}

Respond ONLY with valid JSON array. No markdown, no explanations, just the JSON array.
"""

        try:
            response = self.model.generate_content(full_prompt)
            text = response.text.strip()

            # Clean up markdown if present
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            narratives = json.loads(text)
            print(f"✅ Generated {len(narratives)} narratives")
            return narratives

        except Exception as e:
            print(f"❌ Error extracting narratives: {e}")
            print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
            return []

    def generate_build_ideas(self, narrative):
        """
        Takes a narrative and generates 3-5 build ideas.
        """
        print(f"💡 Generating build ideas for: {narrative.get('narrative_name', 'Unknown')}")

        full_prompt = f"""
{BUILD_IDEA_PROMPT}

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

No markdown, no explanations, just the JSON object.
"""

        try:
            response = self.model.generate_content(full_prompt)
            text = response.text.strip()

            # Clean up markdown
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            ideas_obj = json.loads(text)
            print(f"✅ Generated {len(ideas_obj.get('ideas', []))} build ideas")
            return ideas_obj

        except Exception as e:
            print(f"❌ Error generating build ideas: {e}")
            print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
            return {"narrative_name": narrative.get("narrative_name", "Unknown"), "ideas": []}

    def _format_signals_for_llm(self, signals_data):
        """Format raw signals into readable text for the LLM."""
        github = signals_data.get("github_momentum", [])
        onchain = signals_data.get("onchain_metrics", [])
        intel = signals_data.get("market_intelligence", [])

        formatted = "## GitHub Activity (Last 14 Days)\n"
        for repo in github[:10]:  # Top 10 repos
            formatted += f"- {repo['name']}: {repo['stars']} stars, {repo.get('language', 'Unknown')} | {repo.get('description', 'No description')[:80]}...\n"

        formatted += "\n## On-chain Metrics\n"
        for metric in onchain:
            formatted += f"- {metric['metric']}: {metric['value']} ({metric['change']})\n"

        formatted += "\n## Market Intelligence\n"
        for signal in intel[:5]:
            formatted += f"- {signal.get('source', 'Unknown')}: {signal.get('summary', signal)}\n"

        return formatted

if __name__ == "__main__":
    # Test the analyzer
    print("Testing Gemini Analyzer...")

    # Sample test data
    test_signals = {
        "github_momentum": [
            {"name": "lightprotocol/light-protocol", "stars": 450, "language": "Rust", "description": "ZK compression for Solana"},
            {"name": "helius-labs/helius-sdk", "stars": 320, "language": "TypeScript", "description": "Developer SDK for Solana"}
        ],
        "onchain_metrics": [
            {"metric": "Program Deployments", "value": "142", "change": "+12%"},
            {"metric": "ZK Usage", "value": "Spike", "change": "+45%"}
        ],
        "market_intelligence": [
            {"source": "Helius Blog", "summary": "AI agents now self-fund API keys"},
            {"source": "Messari", "summary": "SVM becoming pluggable execution layer"}
        ]
    }

    analyzer = NarrativeAnalyzer()
    narratives = analyzer.extract_narratives(test_signals)
    print(json.dumps(narratives, indent=2))
