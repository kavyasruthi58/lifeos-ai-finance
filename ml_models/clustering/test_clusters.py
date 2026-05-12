import joblib
import pandas as pd

# Load model
model = joblib.load("cluster_model.pkl")
scaler = joblib.load("cluster_scaler.pkl")

# Example user data
sample_user = [[
    1200,   # total spending
    80,     # avg transaction
    20      # transaction count
]]

# Scale
sample_scaled = scaler.transform(sample_user)

# Predict cluster
cluster = model.predict(sample_scaled)

print("Predicted spending cluster:", cluster[0])