import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("../../data/transactions.csv")

# Encode merchant and category
merchant_encoder = LabelEncoder()
category_encoder = LabelEncoder()

df["merchant_encoded"] = merchant_encoder.fit_transform(df["merchant"])
df["category_encoded"] = category_encoder.fit_transform(df["category"])

# Features
X = df[[
    "amount",
    "merchant_encoded",
    "category_encoded"
]]

# Train Isolation Forest
model = IsolationForest(
    contamination=0.15,
    random_state=42
)

model.fit(X)

# Save everything
joblib.dump(model, "fraud_model.pkl")
joblib.dump(merchant_encoder, "merchant_encoder.pkl")
joblib.dump(category_encoder, "category_encoder.pkl")

print("Fraud detection model saved successfully")