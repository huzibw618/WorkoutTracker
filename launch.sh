#!/bin/bash
cd "$(dirname "$0")"
pkill -f "streamlit run dashboard.py" 2>/dev/null
sleep 1
uv run streamlit run dashboard.py --server.headless true &
sleep 3
xdg-open http://localhost:8501
wait
