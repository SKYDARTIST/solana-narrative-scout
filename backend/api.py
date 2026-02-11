"""
FastAPI Backend for SignalVane
Provides programmatic access to narrative data
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.data_refresher import refresh_data, get_minutes_since_refresh
from backend.historical_tracker import HistoricalTracker

app = FastAPI(
    title="SignalVane API",
    description="Real-time Solana narrative detection and tracking",
    version="1.0.0"
)

# Enable CORS for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_json_file(filename: str):
    """Helper to load JSON data files"""
    try:
        filepath = os.path.join("data", filename)
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"{filename} not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in {filename}")

@app.get("/")
def root():
    """API root - shows available endpoints"""
    return {
        "name": "SignalVane API",
        "version": "1.0.0",
        "description": "Real-time Solana narrative detection and tracking",
        "endpoints": {
            "/narratives": "Get all detected narratives",
            "/narratives/{name}": "Get specific narrative by name",
            "/trends": "Get trend indicators for all narratives",
            "/ideas": "Get build ideas for all narratives",
            "/snapshot": "Get current data snapshot with metadata",
            "/refresh": "Trigger data refresh (POST)",
            "/health": "API health check"
        },
        "docs": "/docs"
    }

@app.get("/narratives")
def get_narratives(sort_by: str = "novelty") -> List[Dict[str, Any]]:
    """
    Get all detected narratives

    Query params:
        - sort_by: 'novelty' (default), 'alphabetical', or 'none'
    """
    narratives = load_json_file("narratives.json")

    # Sort if requested
    if sort_by == "novelty":
        narratives.sort(key=lambda x: x.get('novelty_score', 0), reverse=True)
    elif sort_by == "alphabetical":
        narratives.sort(key=lambda x: x.get('narrative_name', ''))

    return narratives

@app.get("/narratives/{narrative_name}")
def get_narrative(narrative_name: str) -> Dict[str, Any]:
    """Get a specific narrative by name"""
    narratives = load_json_file("narratives.json")

    # Find matching narrative (case-insensitive)
    for narrative in narratives:
        if narrative.get('narrative_name', '').lower() == narrative_name.lower():
            return narrative

    raise HTTPException(status_code=404, detail=f"Narrative '{narrative_name}' not found")

@app.get("/trends")
def get_trends() -> Dict[str, str]:
    """
    Get trend indicators for all narratives

    Returns dict mapping narrative_name -> trend ('rising', 'stable', 'falling', 'new')
    """
    try:
        tracker = HistoricalTracker()
        trends = tracker.get_all_trends()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trends: {str(e)}")

@app.get("/ideas")
def get_ideas(narrative_name: str = None) -> List[Dict[str, Any]]:
    """
    Get build ideas

    Query params:
        - narrative_name: Filter by specific narrative (optional)
    """
    all_ideas = load_json_file("ideas.json")

    if narrative_name:
        # Filter for specific narrative (case-insensitive)
        filtered = [
            item for item in all_ideas
            if item.get('narrative_name', '').lower() == narrative_name.lower()
        ]
        if not filtered:
            raise HTTPException(status_code=404, detail=f"Ideas for '{narrative_name}' not found")
        return filtered

    return all_ideas

@app.get("/snapshot")
def get_snapshot() -> Dict[str, Any]:
    """
    Get current data snapshot with metadata

    Includes:
        - Timestamp
        - Signal counts
        - On-chain metrics
        - Reddit data
    """
    return load_json_file("snapshot.json")

@app.post("/refresh")
def trigger_refresh(regenerate: bool = False) -> Dict[str, Any]:
    """
    Trigger data refresh

    Query params:
        - regenerate: If true, regenerate narratives with AI (slower)
    """
    try:
        success, timestamp = refresh_data(force=True, regenerate_narratives=regenerate)

        if success:
            return {
                "status": "success",
                "timestamp": timestamp,
                "regenerated": regenerate,
                "message": "Data refreshed successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Refresh failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refresh error: {str(e)}")

@app.get("/health")
def health_check() -> Dict[str, Any]:
    """
    API health check

    Returns API status and data freshness
    """
    minutes_since = get_minutes_since_refresh()

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_age_minutes": minutes_since,
        "data_fresh": minutes_since < 10 if minutes_since else False
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SignalVane API server...")
    print("📖 API docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
