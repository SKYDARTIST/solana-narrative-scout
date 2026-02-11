#!/bin/bash
export PATH="/Users/cryptobulla/Library/Python/3.9/bin:$PATH"
python3 -m streamlit run frontend/dashboard.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false > streamlit_server.log 2>&1
