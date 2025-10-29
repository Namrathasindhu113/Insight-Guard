import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle, os

def featurize(df):
    g = df.groupby('user').agg({
        'event': 'count',
        'file_size_kb': 'sum',
        'dst_count': 'sum',
        'timestamp': lambda s: (pd.to_datetime(s).dt.hour.mean())
    }).rename(columns={'event':'event_count','timestamp':'avg_hour'})
    g = g.fillna(0)
    return g

def train_model(df):
    X = featurize(df)
    iso = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    iso.fit(X)
    model_path = os.path.join(os.path.dirname(__file__), "iso_model.pkl")
    pickle.dump(iso, open(model_path,"wb"))
    return iso, X

def anomaly_score(df, model=None):
    model_path = os.path.join(os.path.dirname(__file__), "iso_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not found. Run /train first.")
    model = pickle.load(open(model_path,"rb"))
    X = featurize(df)
    scores = model.decision_function(X)
    out = pd.DataFrame({
        'user': X.index,
        'iso_score': scores,
        'event_count': X['event_count'],
        'file_size_kb': X['file_size_kb'],
        'avg_hour': X['avg_hour']
    }).reset_index(drop=True)
    return out
