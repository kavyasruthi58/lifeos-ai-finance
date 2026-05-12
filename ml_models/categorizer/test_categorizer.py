import joblib

model = joblib.load("category_model.pkl")

test_transactions = [
    "DOORDASH BURGER ORDER",
    "UBER RIDE TO OFFICE",
    "NETFLIX PAYMENT",
    "WALMART GROCERIES",
    "STARBUCKS LATTE"
]

for transaction in test_transactions:
    prediction = model.predict([transaction])
    print(transaction, "=>", prediction[0])