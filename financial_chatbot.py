import pandas as pd
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import pandas as pd
from datetime import datetime

# Load the CSV data
financial_path = "fiance_data.csv"

def load_financial_data():
    df = pd.read_csv(financial_path)
    # Preprocess data
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["description"] = df["description"].fillna("").str.lower()  # Fill NaN and convert to lowercase
    return df

# Function to filter data by month and year
def filter_by_month_year(df, month, year):
    return df[(df['date'].dt.month == month) & (df['date'].dt.year == year)]

# Function to filter data by today
def filter_by_today(df):
    today = datetime.now().date()
    return df[df['date'].dt.date == today]

# Function to get spending on specific items
def spending_on_item(df, item):
    item_spending = df[df["description"].str.contains(item, na=False)]["amount"].sum()
    return item_spending

# Enhanced chatbot logic
def get_financial_insight(prompt):
    # Load the latest financial data
    financial_df = load_financial_data()
    
    prompt = prompt.lower()
    if "total income" in prompt:
        if "month" in prompt and "year" in prompt:
            month_year = prompt.split("month ")[1].split(" year ")
            month = int(month_year[0])
            year = int(month_year[1])
            filtered_df = filter_by_month_year(financial_df, month, year)
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            return f"Your total income for {month}/{year} is ₹{total_income:.2f}"
        else:
            total_income = financial_df[financial_df["category"] == "Income"]["amount"].sum()
            return f"Your total income is ₹{total_income:.2f}"
    
    elif "total expense" in prompt:
        if "month" in prompt and "year" in prompt:
            month_year = prompt.split("month ")[1].split(" year ")
            month = int(month_year[0])
            year = int(month_year[1])
            filtered_df = filter_by_month_year(financial_df, month, year)
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            return f"Your total expenses for {month}/{year} are ₹{total_expense:.2f}"
        else:
            total_expense = financial_df[financial_df["category"] == "Expense"]["amount"].sum()
            return f"Your total expenses are ₹{total_expense:.2f}"
    
    elif "net savings" in prompt:
        if "month" in prompt and "year" in prompt:
            month_year = prompt.split("month ")[1].split(" year ")
            month = int(month_year[0])
            year = int(month_year[1])
            filtered_df = filter_by_month_year(financial_df, month, year)
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            net_savings = total_income - total_expense
            return f"Your net savings for {month}/{year} are ₹{net_savings:.2f}"
        else:
            total_income = financial_df[financial_df["category"] == "Income"]["amount"].sum()
            total_expense = financial_df[financial_df["category"] == "Expense"]["amount"].sum()
            net_savings = total_income - total_expense
            return f"Your net savings are ₹{net_savings:.2f}"
    
    elif "highest expense" in prompt:
        if "today" in prompt:
            filtered_df = filter_by_today(financial_df)
            highest_expense = filtered_df[filtered_df["category"] == "Expense"].nlargest(1, "amount")
        elif "month" in prompt and "year" in prompt:
            month_year = prompt.split("month ")[1].split(" year ")
            month = int(month_year[0])
            year = int(month_year[1])
            filtered_df = filter_by_month_year(financial_df, month, year)
            highest_expense = filtered_df[filtered_df["category"] == "Expense"].nlargest(1, "amount")
        else:
            highest_expense = financial_df[financial_df["category"] == "Expense"].nlargest(1, "amount")
        
        if not highest_expense.empty:
            desc = highest_expense.iloc[0]["description"]
            amount = highest_expense.iloc[0]["amount"]
            date = highest_expense.iloc[0]["date"]
            return f"Your highest expense was ₹{amount:.2f} on {date.strftime('%d-%m-%Y')} for {desc}."
        return "No expenses recorded."
    
    elif "transactions" in prompt:
        return f"Here are your recorded transactions:\n{financial_df.to_string(index=False)}"
    
    elif "spend on" in prompt:
        item = prompt.split("spend on ")[1].strip().lower()
        item_spending = spending_on_item(financial_df, item)
        if "month" in prompt and "year" in prompt:
            month_year = prompt.split("month ")[1].split(" year ")
            month = int(month_year[0])
            year = int(month_year[1])
            filtered_df = filter_by_month_year(financial_df, month, year)
            item_spending = spending_on_item(filtered_df, item)
            return f"You spent ₹{item_spending:.2f} on {item} in {month}/{year}"
        return f"You spent ₹{item_spending:.2f} on {item}"
    
    else:
        return "I didn't understand that. Can you ask about total income, expenses, savings, or specific categories?"

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("Ask me something about your finances: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = get_financial_insight(user_input)
        print(response)
