import pandas as pd

FOOD_APPS = ["Swiggy", "Zomato"]

def load_data(file_path):
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    return df

def categorize_spending(df):
    df["category"] = df["merchant"].apply(
        lambda x: "Food Delivery" if any(app in x for app in FOOD_APPS) else "Other"
    )
    return df

def calculate_totals(df):
    total_spend = df["amount"].sum()
    food_spend = df[df["category"] == "Food Delivery"]["amount"].sum()
    return total_spend, food_spend

def check_overspend(food_spend, threshold, income):
    if food_spend > threshold or food_spend > (0.2 * income):
        return True
    return False

def projected_spend(df):
    food_df = df[df["category"] == "Food Delivery"]
    if food_df.empty:
        return 0

    current_day = food_df["date"].dt.day.max()
    current_spend = food_df["amount"].sum()

    projection = (current_spend / current_day) * 30
    return round(projection, 2)