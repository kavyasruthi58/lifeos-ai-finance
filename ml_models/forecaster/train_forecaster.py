import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv("../../data/transactions.csv")
df["date"] = pd.to_datetime(df["date"])

# Create daily spending data
daily_spending = df.groupby(df["date"].dt.day)["amount"].sum().reset_index()
daily_spending.columns = ["day", "total_spending"]

# Train model
X = daily_spending[["day"]]
y = daily_spending["total_spending"]

model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "budget_forecaster.pkl")

print("Budget forecasting model saved successfully")
print("Training data:")
print(daily_spending)