import pandas as pd
import datetime, random, time, os

# Path to your data file (same one backend reads)
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "logs.csv")
DATA_FILE = os.path.abspath(DATA_FILE)
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

users = ["user1", "user2", "user3", "user4", "user5"]
activities = ["login", "file_upload", "file_download", "data_transfer", "file_delete"]
ips = [f"192.168.1.{i}" for i in range(5, 50)]

print("🚀 Starting live data simulation... (press Ctrl+C to stop)")

# Keep appending new data every few seconds
while True:
    log_id = random.randint(1000, 9999)
    timestamp = datetime.datetime.now().isoformat()
    user = random.choice(users)
    activity = random.choice(activities)
    file_size = random.choice([0, 200, 500, 2000, 10000, 40000, 80000])
    access_count = random.randint(1, 30)
    ip = random.choice(ips)

    row = [log_id, timestamp, user, activity, file_size, access_count, ip]

    # Append new row to logs.csv
    df = pd.DataFrame([row], columns=["log_id", "timestamp", "user", "activity", "file_size_kb", "access_count", "ip_address"])
    df.to_csv(DATA_FILE, mode="a", header=not os.path.exists(DATA_FILE), index=False)

    print(f"✅ Added log: {user} | {activity} | {file_size} KB | {access_count} ops")
    time.sleep(5)  # wait 5 seconds before adding next log
