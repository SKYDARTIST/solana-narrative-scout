---
description: How to host SignalVane on GitHub and deploy to Streamlit Cloud
---

### Step 1: Initialize Git and Prepare Repo
Run these commands in your terminal inside `/Users/cryptobulla/.gemini/antigravity/scratch/solana-narrative-scout`:

1.  **Create a .gitignore file** to avoid uploading unnecessary files:
    ```bash
    echo "venv/\n__pycache__/\n.env\ndata/initial_signals.txt" > .gitignore
    ```
2.  **Initialize Git:**
    ```bash
    git init
    git add .
    git commit -m "Initial commit: SignalVane Prototype"
    ```

### Step 2: Host on GitHub
1.  Go to [github.com/new](https://github.com/new).
2.  Name your repository `solana-narrative-scout`.
3.  Click **Create repository**.
4.  Copy the commands under "…or push an existing repository from the command line" and run them in your terminal. They will look like this:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/solana-narrative-scout.git
    git branch -M main
    git push -u origin main
    ```

### Step 3: Deploy to Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Sign in with your GitHub account.
3.  Click **New app**.
4.  Select your repository (`solana-narrative-scout`) and the branch (`main`).
5.  Set the **Main file path** to `frontend/dashboard.py`.
6.  Click **Deploy!**

### Step 4: Submit to Superteam Earn
1.  Once deployed, copy your Streamlit URL (e.g., `https://signalvane.streamlit.app`).
2.  Fill out the submission form on Superteam Earn with:
    - **App Link:** Your Streamlit URL.
    - **Repo Link:** Your GitHub URL.
    - **Description:** Use the content from the provided `README.md`.
