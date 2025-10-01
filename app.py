from financial_chatbot import get_financial_insight
from flask import Flask, request, render_template, jsonify
import pandas as pd
from backend import CSV
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
CSV.initialize_csv()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json
    
    # Set the date to today's date if not provided
    date = data.get("date")
    if not date:
        date = datetime.now().strftime(CSV.FORMAT)
    
    CSV.add_entry(date, data["amount"], data["category"], data["description"])
    
    # Reload data for chatbot
    global financial_df
    financial_df = pd.read_csv(CSV.CSV_FILE)
    
    return jsonify({"message": "Transaction added successfully"})

@app.route("/view_transactions", methods=["GET", "POST"])
def view_transactions():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if not start_date or not end_date:
            return render_template("view.html", message="Please provide both start and end dates.", transactions=None)

        transactions_df = CSV.get_transactions(start_date, end_date)

        if transactions_df.empty:
            return render_template("view.html", message="No transactions found for the selected date range.", transactions=None)

        transactions_html = transactions_df.to_html(classes="table table-striped", index=False)

        return render_template("view.html", transactions=transactions_html, start_date=start_date, end_date=end_date, message=None)

    return render_template("view.html", transactions=None)

@app.route("/plot_transactions", methods=["POST"])
def plot_transactions():
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    transactions_df = CSV.get_transactions(start_date, end_date)

    if transactions_df.empty:
        return render_template("view.html", message="No transactions to plot for the selected date range.", transactions=None, plot_url=None)

    # Prepare data for plotting
    transactions_df["date"] = pd.to_datetime(transactions_df["date"], format=CSV.FORMAT)
    transactions_df.set_index("date", inplace=True)
    income_df = transactions_df[transactions_df["category"] == "Income"].groupby("date")["amount"].sum()
    expense_df = transactions_df[transactions_df["category"] == "Expense"].groupby("date")["amount"].sum()

    all_dates = pd.date_range(start=transactions_df.index.min(), end=transactions_df.index.max())
    income_df = income_df.reindex(all_dates, fill_value=0)
    expense_df = expense_df.reindex(all_dates, fill_value=0)

    # Plot and save the graph
    img_path = "static/plot.png"
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df, label="Income", color="green", marker="o")
    plt.plot(expense_df.index, expense_df, label="Expense", color="red", marker="o")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()

    transactions_html = transactions_df.to_html(classes="table table-striped", index=False)
    return render_template("view.html", transactions=transactions_html, plot_url="/static/plot.png", start_date=start_date, end_date=end_date, message=None)

@app.route("/financial-chatbot", methods=["POST"])
def financial_chatbot():
    data = request.get_json()
    user_input = data.get("prompt", "")
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = get_financial_insight(user_input)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
