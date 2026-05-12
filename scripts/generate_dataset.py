import pandas as pd
import random
from faker import Faker

fake = Faker()

categories = {
    "Food": ["DoorDash", "Uber Eats", "Chipotle", "Starbucks", "McDonalds"],
    "Transport": ["Uber", "Lyft", "Shell", "Exxon"],
    "Groceries": ["Walmart", "Target", "Costco", "Kroger"],
    "Entertainment": ["Netflix", "Spotify", "AMC"],
    "Shopping": ["Amazon", "Best Buy", "Apple"],
    "Health": ["CVS", "Walgreens"],
    "Subscription": ["Amazon Prime", "Hulu", "Disney+"]
}

transactions = []
transaction_id = 1

# 50 users, each with 20–40 yearly transactions
for user_number in range(1, 51):
    user_id = f"U{user_number:03}"
    num_transactions = random.randint(20, 40)

    for _ in range(num_transactions):
        category = random.choice(list(categories.keys()))
        merchant = random.choice(categories[category])

        if category == "Food":
            amount = round(random.uniform(5, 60), 2)
        elif category == "Transport":
            amount = round(random.uniform(10, 100), 2)
        elif category == "Groceries":
            amount = round(random.uniform(40, 300), 2)
        elif category == "Entertainment":
            amount = round(random.uniform(10, 80), 2)
        elif category == "Shopping":
            amount = round(random.uniform(20, 1000), 2)
        elif category == "Health":
            amount = round(random.uniform(10, 150), 2)
        else:
            amount = round(random.uniform(5, 40), 2)

        is_fraud = 0

        if amount > 800 and random.random() < 0.5:
            is_fraud = 1

        date = fake.date_between(
            start_date="-1y",
            end_date="today"
        )

        description = f"{merchant.upper()} PURCHASE"

        transactions.append([
            transaction_id,
            user_id,
            date,
            description,
            amount,
            merchant,
            category,
            is_fraud
        ])

        transaction_id += 1

df = pd.DataFrame(transactions, columns=[
    "transaction_id",
    "user_id",
    "date",
    "description",
    "amount",
    "merchant",
    "category",
    "is_fraud"
])

df.to_csv("../data/transactions.csv", index=False)

print("Dataset generated successfully!")
print("Total transactions:", len(df))
print("Total users:", df["user_id"].nunique())
print("Fraud transactions:", df["is_fraud"].sum())
print(df.head())