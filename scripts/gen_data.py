import csv, random, datetime, uuid, os
os.makedirs("data", exist_ok=True)
users = [f"user{i}" for i in range(1,11)]
events = ["login", "file_access", "data_transfer", "logout"]
start = datetime.datetime.now() - datetime.timedelta(days=7)

with open("data/logs.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["event_id","timestamp","user","event","file_size_kb","dst_count","ip"])
    for day in range(7):
        for _ in range(200):
            t = start + datetime.timedelta(days=day, minutes=random.randint(0,1440))
            user = random.choice(users)
            ev = random.choices(events, weights=[3,6,1,2])[0]
            size = random.randint(1,5000) if ev=="data_transfer" else 0
            dst = random.randint(1,10) if ev=="data_transfer" else 0
            ip = f"10.0.{random.randint(1,5)}.{random.randint(1,254)}"
            w.writerow([str(uuid.uuid4()), t.isoformat(), user, ev, size, dst, ip])
print("data/logs.csv created")
