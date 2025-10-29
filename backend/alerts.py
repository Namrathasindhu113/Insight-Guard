import os, threading, requests, json

# Load settings from environment or settings.json
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "settings.json")
try:
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    else:
        settings = {}
except Exception:
    settings = {}

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK") or settings.get("slack_webhook") or ""

def _send_slack(text):
    if not SLACK_WEBHOOK:
        print("Slack webhook not configured, skipping alert:", text)
        return
    payload = {"text": text}
    try:
        r = requests.post(SLACK_WEBHOOK, json=payload, timeout=5)
        if r.status_code >= 400:
            print("Slack send failed", r.status_code, r.text)
    except Exception as e:
        print("Slack send exception:", e)

def send_slack_async(text):
    # fire-and-forget thread so alerting never blocks main request
    t = threading.Thread(target=_send_slack, args=(text,), daemon=True)
    t.start()
