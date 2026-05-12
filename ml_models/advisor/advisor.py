import pandas as pd

def generate_advice():

    # Load transactions
    df = pd.read_csv("../../data/transactions.csv")

    # Total spending
    total_spending = df["amount"].sum()

    # Spending by category
    category_spending = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    # Highest category
    top_category = category_spending.index[0]
    top_amount = category_spending.iloc[0]

    # Generate AI advice
    advice = f"""
Your total spending is ${total_spending:.2f}.

Your highest spending category is '{top_category}'
with ${top_amount:.2f} spent.

Recommendation:
Try reducing spending in '{top_category}' by 10%
next month to improve savings.
"""

    return advice


if __name__ == "__main__":
    result = generate_advice()
    print(result)