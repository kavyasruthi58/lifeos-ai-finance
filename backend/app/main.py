from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="LifeOS AI Finance API")

# Get project base directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# Request schema
class CategoryRequest(BaseModel):
    description: str

class FraudRequest(BaseModel):
    amount: float
    merchant: str
    category: str

class ForecastRequest(BaseModel):
    day: int

# Home route
@app.get("/")
def home():
    return {
        "message": "LifeOS AI Finance API is running"
    }

# Health route
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# Prediction route
@app.post("/predict/category")
def predict_category(request: CategoryRequest):

    model_path = os.path.join(
        BASE_DIR,
        "ml_models",
        "categorizer",
        "category_model.pkl"
    )

    model = joblib.load(model_path)

    prediction = model.predict([request.description])

    return {
        "transaction": request.description,
        "predicted_category": prediction[0]
    }

@app.post("/predict/fraud")
def predict_fraud(request: FraudRequest):
    model_path = os.path.join(BASE_DIR, "ml_models", "fraud_detector", "fraud_model.pkl")
    merchant_encoder_path = os.path.join(BASE_DIR, "ml_models", "fraud_detector", "merchant_encoder.pkl")
    category_encoder_path = os.path.join(BASE_DIR, "ml_models", "fraud_detector", "category_encoder.pkl")

    model = joblib.load(model_path)
    merchant_encoder = joblib.load(merchant_encoder_path)
    category_encoder = joblib.load(category_encoder_path)

    merchant_encoded = merchant_encoder.transform([request.merchant])[0]
    category_encoded = category_encoder.transform([request.category])[0]

    prediction = model.predict([[
        request.amount,
        merchant_encoded,
        category_encoded
    ]])

    result = "Fraud detected" if prediction[0] == -1 else "Normal transaction"

    return {
        "amount": request.amount,
        "merchant": request.merchant,
        "category": request.category,
        "fraud_result": result
    }

@app.post("/predict/budget")
def predict_budget(request: ForecastRequest):

    model_path = os.path.join(
        BASE_DIR,
        "ml_models",
        "forecaster",
        "budget_forecaster.pkl"
    )

    model = joblib.load(model_path)

    prediction = model.predict([[request.day]])

    return {
        "day": request.day,
        "predicted_spending": round(float(prediction[0]), 2)
    }

@app.get("/advisor/summary")
def advisor_summary():
    import pandas as pd

    data_path = os.path.join(BASE_DIR, "data", "transactions.csv")
    df = pd.read_csv(data_path)

    total_spending = df["amount"].sum()

    category_spending = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_spending.index[0]
    top_amount = category_spending.iloc[0]

    advice = (
        f"Your total spending is ${total_spending:.2f}. "
        f"Your highest spending category is {top_category} with ${top_amount:.2f}. "
        f"Try reducing {top_category} spending by 10% next month."
    )

    return {
        "total_spending": round(float(total_spending), 2),
        "top_category": top_category,
        "top_category_amount": round(float(top_amount), 2),
        "advice": advice
    }