
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(path):
    df = pd.read_csv(path, parse_dates=["datetime"])
    return df

def preprocess_data(df):
    df = df.dropna()
    X = df[["temperature", "humidity", "pressure", "wind_speed"]]
    y = df["precipitation"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
