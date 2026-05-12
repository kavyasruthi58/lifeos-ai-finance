import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("../../data/transactions.csv")

# Create user spending features
user_features = df.groupby("user_id").agg(
    total_spending=("amount", "sum"),
    avg_transaction=("amount", "mean"),
    transaction_count=("amount", "count")
).reset_index()

# Features
X = user_features[[
    "total_spending",
    "avg_transaction",
    "transaction_count"
]]

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train clustering model
model = KMeans(
    n_clusters=1,
    random_state=42
)

model.fit(X_scaled)

# Save model
joblib.dump(model, "cluster_model.pkl")
joblib.dump(scaler, "cluster_scaler.pkl")

print("Cluster model saved successfully")
print(user_features)