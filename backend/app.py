from fastapi import FastAPI, Request
import pandas as pd
from model import train_model, anomaly_score
import uvicorn
import os, json, time, threading, requests
from alerts import send_slack_async  # optional async alert system

# ------------------ CONFIG ------------------
app = FastAPI()
backend_url = "http://localhost:8000"
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs.csv")

# Slack Webhook
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX"  # paste yours

def send_slack_alert(user, risk_score):
    """Send Slack alert if risk score is high."""
    message = {
        "text": f"🚨 *High Risk Alert!* User *{user}* has a risk score of *{risk_score:.1f}* ⚠️"
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, json=message)
    except Exception as e:
        print(f"Slack alert failed: {e}")

# ------------------ API ENDPOINTS ------------------

@app.post("/train")
def train():
    df = pd.read_csv(DATA_PATH)
    iso, X = train_model(df)
    return {"status": "trained", "users_trained": len(X)}


@app.get("/score")
def score():
    df = pd.read_csv(DATA_PATH)
    out = anomaly_score(df)

    def rule_score(row):
        score = 0
        if row['avg_hour'] < 6 or row['avg_hour'] > 20:
            score += 30
        if row['file_size_kb'] > 2000:
            score += 25
        if row['event_count'] > 300:
            score += 15
        return score

    out['rule_score'] = out.apply(lambda r: rule_score(r), axis=1)
    min_s, max_s = out['iso_score'].min(), out['iso_score'].max()
    out['iso_norm'] = 50 * (1 - (out['iso_score'] - min_s) / (max_s - min_s + 1e-9))
    out['risk_score'] = out['rule_score'] + out['iso_norm']
    out = out.sort_values('risk_score', ascending=False)

    # 🚨 Send Slack alert for high-risk users
    try:
        high = out[out['risk_score'] > 80]
        for _, row in high.iterrows():
            send_slack_alert(row["user"], row["risk_score"])
            # Optional: async alert (you already have send_slack_async)
            msg = f"ALERT: user={row['user']} risk={row['risk_score']:.1f}"
            send_slack_async(msg)
    except Exception as e:
        print("Alert send error:", e)

    return out.to_dict(orient='records')


@app.post("/alert_user")
async def alert_user(req: Request):
    payload = await req.json()
    user = payload.get("user")
    risk = payload.get("risk")
    text = payload.get("text") or f"Manual alert: user={user} risk={risk}"
    send_slack_async(text)
    return {"status": "ok"}


# ------------------ AUTO RETRAIN ------------------
def auto_retrain_loop():
    while True:
        try:
            print("⏳ Auto retraining model...")
            df = pd.read_csv(DATA_PATH)
            train_model(df)
            print("✅ Auto retraining completed.")
        except Exception as e:
            print(f"Auto retraining error: {e}")
        time.sleep(300)  # retrain every 5 minutes

threading.Thread(target=auto_retrain_loop, daemon=True).start()

# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
