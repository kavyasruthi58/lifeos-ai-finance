import joblib
import pandas as pd

# Load models
model = joblib.load("fraud_model.pkl")
merchant_encoder = joblib.load("merchant_encoder.pkl")
category_encoder = joblib.load("category_encoder.pkl")

# Test transaction
amount = 950.00
merchant = "Unknown"
category = "Shopping"

# Encode
merchant_encoded = merchant_encoder.transform([merchant])[0]
category_encoded = category_encoder.transform([category])[0]

# Create input
X_test = [[
    amount,
    merchant_encoded,
    category_encoded
]]

# Predict
prediction = model.predict(X_test)

# Output
if prediction[0] == -1:
    print("Fraud detected")
else:
    print("Normal transaction")