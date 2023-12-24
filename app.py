# app.py
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load initial data or create a new DataFrame if the file does not exist
try:
    df = pd.read_excel('financial_data.xlsx')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount', 'Source', 'Notes'])

@app.route('/delete_transaction/<int:index>', methods=['POST'])
def delete_transaction(index):
    global df

    # Delete the transaction at the specified index
    df = df.drop(index)

    # Save the updated DataFrame to the Excel file
    df.to_excel('financial_data.xlsx', index=False)

    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Calculate income, expenses, and net income based on the 'Type' column
    income = df[df['Type'] == 'Income']['Amount'].sum()
    expenses = df[df['Type'] == 'Expense']['Amount'].sum()
    net_income = income - expenses

    # Sort the DataFrame by 'Date' in ascending order by default
    df_sorted = df.sort_values(by='Date', ascending=False)

    # List of predefined categories
    categories = ['Groceries', 'Utilities', 'Rent', 'Entertainment', 'lqr', 'uber', 'salary', 'fule',
                  'shopping', 'furniture&applinace', 'Others']

    return render_template('index.html', income=income, expenses=expenses,
                           net_income=net_income, df=df_sorted, categories=categories)


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    notes = request.form['notes']
    transaction_type = request.form['transaction_type']
    transaction_source = request.form['transaction_source']
    # if transaction_source == 'Card':
    # # Set the 'Type' column to 'Expense' for expense transactions
    #     df.loc[len(df)] = [date, category, 'Card', amount, notes]
    # else:
    #     df.loc[len(df)] = [date, category, 'Cash', amount, notes]
    if transaction_type == 'Expense':
    # Set the 'Type' column to 'Expense' for expense transactions
        df.loc[len(df)] = [date, category, 'Expense', amount, transaction_source, notes]
    else:
        df.loc[len(df)] = [date, category, 'Income', amount,transaction_source, notes]


    # df.loc[len(df)] = [date, category, transaction_type, amount, notes]
    df.to_excel('financial_data.xlsx', index=False)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
