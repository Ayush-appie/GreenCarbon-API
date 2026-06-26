import pandas as pd
import joblib
import datetime
from fastapi import FastAPI

# Initialize the FastAPI App
app = FastAPI(title="GreenCompute Grid Optimizer API")

# Load the trained ML model and feature schema
print("Loading model artifacts...")
model = joblib.load('carbon_model.pkl')
feature_cols = joblib.load('model_features.pkl')

# Baseline real-world weather & sensor conditions (Averages from UCI dataset)
# This allows the API to simulate realistic baseline grid conditions
baseline_conditions = {
    'T1': 21.68, 'RH_1': 40.25, 'T2': 20.34, 'RH_2': 40.42,
    'T3': 22.26, 'RH_3': 39.24, 'T4': 20.85, 'RH_4': 39.02,
    'T5': 19.59, 'RH_5': 50.94, 'T6': 7.91, 'RH_6': 54.60,
    'T7': 20.26, 'RH_7': 35.38, 'T8': 22.02, 'RH_8': 42.93,
    'T9': 19.48, 'RH_9': 41.55, 'T_out': 7.41, 'Press_mm_hg': 755.52,
    'RH_out': 79.75, 'Windspeed': 4.03, 'Visibility': 38.33,
    'Tdewpoint': 3.76, 'rv1': 24.98, 'rv2': 24.98
}


@app.get("/")
def home():
    return {"message": "GreenCompute Real-World API is live!"}


@app.get("/optimize")
def optimize_schedule(window_hours: int = 24):
    """
    Simulates grid load for the upcoming hours and returns the optimal
    time to execute heavy ML workloads to minimize carbon footprint.
    """
    now = datetime.datetime.now()
    predictions = []

    # Loop through the upcoming hours to forecast grid load
    for i in range(window_hours):
        target_time = now + datetime.timedelta(hours=i)

        # Build the payload using baseline weather + dynamic time
        input_data = baseline_conditions.copy()
        input_data['hour'] = target_time.hour
        input_data['day_of_week'] = target_time.weekday()
        input_data['month'] = target_time.month

        # Convert to DataFrame ensuring exact column order matches training
        df_input = pd.DataFrame([input_data])[feature_cols]

        # Predict the energy load (Wh)
        pred_load = model.predict(df_input)[0]

        predictions.append({
            "timestamp": target_time.strftime("%Y-%m-%d %H:00:00"),
            "predicted_grid_load_Wh": round(pred_load, 2)
        })

    # Isolate the absolute best time (Lowest grid load)
    best_time = min(predictions, key=lambda x: x["predicted_grid_load_Wh"])

    return {
        "status": "Success",
        "recommendation": "Execute heavy computing tasks at the optimal time below to minimize grid strain.",
        "optimal_execution_time": best_time["timestamp"],
        "lowest_predicted_load_Wh": best_time["predicted_grid_load_Wh"],
        "full_forecast": predictions
    }