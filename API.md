# SignalVane API Documentation

**Base URL:** `http://localhost:8000`

## Quick Start

```bash
# Start the API server
python3 backend/api.py

# Or with uvicorn directly
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

---

## Endpoints

### 🏠 Root
**GET /** - API information and available endpoints

```bash
curl http://localhost:8000/
```

### 📊 Get All Narratives
**GET /narratives** - Retrieve all detected narratives

**Query Parameters:**
- `sort_by` (optional): `novelty` (default), `alphabetical`, or `none`

```bash
# Get all narratives sorted by novelty score
curl http://localhost:8000/narratives

# Get all narratives alphabetically
curl http://localhost:8000/narratives?sort_by=alphabetical
```

**Response:**
```json
[
  {
    "narrative_name": "ZK-Compression on Solana",
    "novelty_score": 10,
    "explanation": "...",
    "evidence": {
      "github": [...],
      "market_intel": [...]
    }
  }
]
```

### 🔍 Get Specific Narrative
**GET /narratives/{narrative_name}** - Get details for a specific narrative

```bash
curl http://localhost:8000/narratives/ZK-Compression%20on%20Solana
```

### 📈 Get Trends
**GET /trends** - Get trend indicators for all narratives

```bash
curl http://localhost:8000/trends
```

**Response:**
```json
{
  "ZK-Compression on Solana": "rising",
  "SVM Rollups": "stable",
  "Autonomous Agents": "new"
}
```

### 💡 Get Build Ideas
**GET /ideas** - Get build ideas for narratives

**Query Parameters:**
- `narrative_name` (optional): Filter by specific narrative

```bash
# Get all build ideas
curl http://localhost:8000/ideas

# Get ideas for specific narrative
curl "http://localhost:8000/ideas?narrative_name=ZK-Compression%20on%20Solana"
```

**Response:**
```json
[
  {
    "narrative_name": "...",
    "ideas": [
      {
        "title": "...",
        "description": "...",
        "tech_stack": "...",
        "target_user": "...",
        "feasibility": "..."
      }
    ]
  }
]
```

### 📸 Get Snapshot
**GET /snapshot** - Get current data snapshot with metadata

```bash
curl http://localhost:8000/snapshot
```

**Response:**
```json
{
  "timestamp": "2026-02-11T10:30:00",
  "github_signals": 15,
  "reddit_signals": 47,
  "narratives_count": 3,
  "metrics": [...],
  "reddit_data": {...}
}
```

### 🔄 Trigger Refresh
**POST /refresh** - Trigger data refresh

**Query Parameters:**
- `regenerate` (optional): If `true`, regenerate narratives with AI (slower)

```bash
# Quick refresh (update data only)
curl -X POST http://localhost:8000/refresh

# Full refresh with AI regeneration
curl -X POST "http://localhost:8000/refresh?regenerate=true"
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2026-02-11T10:35:00",
  "regenerated": false,
  "message": "Data refreshed successfully"
}
```

### ❤️ Health Check
**GET /health** - API health check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-11T10:30:00",
  "data_age_minutes": 2.5,
  "data_fresh": true
}
```

---

## Usage Examples

### Python
```python
import requests

# Get all narratives
response = requests.get("http://localhost:8000/narratives")
narratives = response.json()

for narrative in narratives:
    print(f"{narrative['narrative_name']}: {narrative['novelty_score']}/10")
```

### JavaScript
```javascript
// Get trends
fetch('http://localhost:8000/trends')
  .then(response => response.json())
  .then(trends => console.log(trends));
```

### cURL with jq
```bash
# Get top narrative by novelty score
curl -s http://localhost:8000/narratives | jq '.[0]'

# Get all rising narratives
curl -s http://localhost:8000/trends | jq 'to_entries | map(select(.value == "rising")) | from_entries'
```

---

## CORS

CORS is enabled for all origins (`*`), making the API accessible from web applications.

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200` - Success
- `404` - Resource not found
- `500` - Internal server error
