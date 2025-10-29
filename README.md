# INSIGHT GUARD — Complete Package

This package includes:
- FastAPI backend with `/train`, `/score`, `/alert_user` and Slack alerting support.
- IsolationForest model training script (auto-saved in backend/iso_model.pkl).
- Streamlit dashboard for quick demo.
- Data generator script to create `data/logs.csv`.
- run_all scripts for Linux/macOS (run_all.sh) and Windows PowerShell (run_all.ps1).
- VS Code launch & task configs for convenience.

## Quick run (VS Code)
1. Open this folder in VS Code.
2. Create and activate a virtual environment (use the integrated terminal):
   - Windows (PowerShell):
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     python -m pip install --upgrade pip
     pip install -r backend/requirements.txt
     pip install streamlit plotly requests
     ```
   - macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     python -m pip install --upgrade pip
     pip install -r backend/requirements.txt
     pip install streamlit plotly requests
     ```
3. (Optional) Put your Slack webhook in `settings.json` at project root or set env var `SLACK_WEBHOOK`.
4. Generate data:
   ```
   python scripts/gen_data.py
   ```
5. Start backend:
   - From VS Code Run & Debug -> "Run FastAPI (uvicorn)" or run:
     ```
     cd backend
     uvicorn app:app --reload --port 8000
     ```
6. Train model:
   ```
   curl -X POST http://127.0.0.1:8000/train
   ```
7. Run dashboard:
   ```
   streamlit run dashboard/app.py
   ```
8. For demo: append suspicious rows and retrain (see earlier instructions).

## Slack alerts
- Add `settings.json` with `slack_webhook` or set environment variable `SLACK_WEBHOOK`.
- Alerts are sent for any user with `risk_score > 80` when `/score` is called.

