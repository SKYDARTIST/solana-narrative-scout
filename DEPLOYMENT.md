# SignalVane Deployment Guide

## 🚀 Deploying to Streamlit Cloud

### Prerequisites
- GitHub repository with your SignalVane code
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Gemini API key

### Step 1: Prepare Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to** https://share.streamlit.io/
2. **Click** "New app"
3. **Select** your repository
4. **Set** main file path: `frontend/dashboard.py`
5. **Advanced settings:**
   - Python version: 3.10 or higher
   - Main file path: `frontend/dashboard.py`

### Step 3: Configure Secrets

In Streamlit Cloud dashboard, go to **Settings → Secrets** and add:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

### Step 4: Initial Data Generation

After deployment, run this **ONCE** to generate initial narratives:

```bash
# Locally, then commit the generated data files
python3 backend/generate_fresh_narratives.py
git add data/narratives.json data/ideas.json data/snapshot.json
git commit -m "Add initial narrative data"
git push
```

This will trigger auto-redeploy with fresh data.

---

## 📊 Post-Deployment Setup

### Optional: Schedule Fresh Narrative Generation

For truly dynamic narratives, set up a weekly cron job:

**Option A: GitHub Actions** (Recommended)

Create `.github/workflows/refresh-narratives.yml`:

```yaml
name: Refresh Narratives

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:  # Manual trigger

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Generate fresh narratives
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python3 backend/generate_fresh_narratives.py

      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data/
          git commit -m "Auto-update: Fresh narratives $(date +'%Y-%m-%d')" || exit 0
          git push
```

**Don't forget to add GEMINI_API_KEY to GitHub repository secrets!**

---

## 🔧 Configuration Options

### Environment Variables

Create a `.streamlit/config.toml` file for custom settings:

```toml
[theme]
primaryColor = "#14F195"
backgroundColor = "#0f0c29"
secondaryBackgroundColor = "#302b63"
textColor = "#ffffff"
font = "sans serif"

[server]
enableCORS = true
enableXsrfProtection = true
```

### Refresh Frequency

To change refresh frequency, edit `frontend/dashboard.py`:

```python
# Line 26
REFRESH_INTERVAL = 300  # seconds (5 minutes)

# Line 115
@st.cache_data(ttl=300)  # Cache duration
```

---

## 🌐 Deploying the API (Optional)

### Option 1: Railway.app (Easiest)

1. Go to https://railway.app/
2. Connect your GitHub repo
3. Set environment variable: `GEMINI_API_KEY`
4. Set start command: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`

### Option 2: Render.com

1. Go to https://render.com/
2. Create new Web Service
3. Connect GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable:** `GEMINI_API_KEY`

### Option 3: Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch app
fly launch

# Set secret
fly secrets set GEMINI_API_KEY=your-key-here

# Deploy
fly deploy
```

---

## 📈 Monitoring & Maintenance

### Health Checks

Monitor your deployment:
- **Dashboard:** Check if https://your-app.streamlit.app/ loads
- **API:** Check https://your-api.railway.app/health

### Narrative Freshness

Check when narratives were last updated:
```bash
# Check snapshot timestamp
curl https://your-api.railway.app/snapshot | jq '.timestamp'
```

### Usage Monitoring

**Gemini API Usage:**
- Check usage at https://aistudio.google.com/app/apikey
- Free tier: 15 requests/minute, 1500/day
- Each narrative generation = ~3-5 API calls

**Streamlit Cloud:**
- Free tier: Unlimited apps, 1GB RAM
- Check resource usage in Streamlit dashboard

---

## 🐛 Troubleshooting

### Dashboard won't load
1. Check Streamlit logs for errors
2. Ensure `data/narratives.json` exists
3. Verify GEMINI_API_KEY is set in secrets

### "No module named 'backend'"
- Ensure `frontend/dashboard.py` has correct sys.path setup:
  ```python
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
  ```

### API key not working
1. Verify key is correct in Streamlit secrets
2. Check key hasn't expired
3. Verify you're within API rate limits

### Narratives not updating
1. Check if auto-refresh is working (see "Last updated" indicator)
2. Manually trigger refresh with `python3 backend/generate_fresh_narratives.py`
3. Commit and push the new data files

---

## 💰 Cost Estimation

### Free Tier (Recommended for Bounty)
- **Streamlit Cloud:** Free
- **Gemini API:** Free (1500 requests/day)
- **GitHub:** Free
- **Total:** $0/month ✅

### Paid Tier (For Production)
- **Streamlit Cloud:** $200/month (Team plan)
- **Gemini API:** ~$5-20/month
- **Railway/Render:** ~$5-10/month (API)
- **Total:** ~$210-230/month

---

## 🎯 Quick Deployment Checklist

- [ ] Code committed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed with `frontend/dashboard.py`
- [ ] GEMINI_API_KEY added to secrets
- [ ] Initial narratives generated and committed
- [ ] Test the live URL
- [ ] (Optional) API deployed
- [ ] (Optional) GitHub Actions workflow added
- [ ] Update README with live demo link

---

## 📝 Final Steps for Bounty Submission

1. **Update README.md** with your live demo link:
   ```markdown
   ## 🚀 Live Demo
   **[View Live Dashboard →](https://your-app.streamlit.app)**
   ```

2. **Test everything:**
   - Open the live dashboard
   - Verify all narratives load
   - Check sentiment analysis displays
   - Test filters and sorting
   - Ensure trend indicators work

3. **Screenshot for submission:**
   - Take clean screenshots of dashboard
   - Show the narrative cards with evidence
   - Capture the real-time update indicator

4. **Submit to Superteam:**
   - Include GitHub repo link
   - Include live demo link
   - Mention key differentiators (AI sentiment, API, real-time)

---

## 🏆 You're Ready!

Your SignalVane deployment is production-ready and competitive for 1st place. Good luck! 🚀
