from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load dataset (temporary Kaggle or sample CSV for now)
data = pd.read_csv("trackman_sample.csv")

@app.get("/")
def root():
    return {"message": "TrackMan Pitching API is running"}

@app.get("/pitchers")
def get_pitchers():
    return {"pitchers": data["Pitcher"].unique().tolist()}

@app.get("/pitcher/{name}")
def get_pitcher_stats(name: str):
    pitcher_data = data[data["Pitcher"] == name]
    
    avg_velocity = pitcher_data["Velocity"].mean()
    avg_spin = pitcher_data["SpinRate"].mean()

    return {
        "pitcher": name,
        "average_velocity": avg_velocity,
        "average_spin_rate": avg_spin
    }
