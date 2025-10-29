#!/usr/bin/env bash
# Run data generator, train, start backend and streamlit in separate terminals (for demo)
set -e
python3 scripts/gen_data.py
cd backend
# start uvicorn in background
uvicorn app:app --reload --port 8000 > ../backend.log 2>&1 &
UV_PID=$!
echo "Started backend (pid $UV_PID)"
cd ..
# give backend a moment
sleep 2
python -c "import requests; print(requests.post('http://127.0.0.1:8000/train').text)"
# start streamlit
streamlit run dashboard/app.py
