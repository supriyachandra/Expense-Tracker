from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)


import sqlite3 

def get_db_connection():
    con = sqlite3.connect('expenses.db')
    con.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return con


# Database initialization
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

#get all expenses
def get_all_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = c.fetchall()
    conn.close()
    return expenses

#aggregate expenses by category
def aggregate_expenses_by_category():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = c.fetchall()
    conn.close()
    return dict(data)

#get spending trends using a sliding window
def get_spending_trends(days=7):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    today = datetime.today()
    start_date = today - timedelta(days=days)
    c.execute('''
        SELECT date, SUM(amount) 
        FROM expenses 
        WHERE date BETWEEN ? AND ? 
        GROUP BY date
    ''', (start_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
    data = c.fetchall()
    conn.close()

    #list of daily totals
    trends = {}
    for i in range(days + 1):
        day = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        trends[day] = 0 
    for date, amount in data:
        trends[date] = amount
    return trends


@app.route('/')
def home():
    conn = get_db_connection()

   
    six_months_ago = (datetime.now().replace(day=1) - timedelta(days=180)).strftime('%Y-%m-01')

    #expenses grouped by month (last 6 months)
    query = """
        SELECT 
            strftime('%Y-%m', date) AS month, 
            strftime('%Y', date) AS year,
            strftime('%m', date) AS month_number,
            SUM(amount) AS monthly_total
        FROM expenses
        WHERE date >= ?
        GROUP BY month
        ORDER BY month DESC;
    """
    monthly_totals = conn.execute(query, (six_months_ago,)).fetchall()

    # Fetch individual expenses for the last 6 months
    expenses_query = """
        SELECT 
            id, 
            date, 
            amount, 
            category, 
            description,
            strftime('%Y-%m', date) AS month
        FROM expenses
        WHERE date >= ?
        ORDER BY date DESC;
    """
    expenses = conn.execute(expenses_query, (six_months_ago,)).fetchall()
    conn.close()


    grouped_expenses = {}
    for month_row in monthly_totals:
        month_name = datetime.strptime(f"{month_row['month_number']}", "%m").strftime('%B')
        month_key = f"{month_name} {month_row['year']}"
        grouped_expenses[month_key] = {
            "monthly_total": month_row["monthly_total"],
            "expenses": [expense for expense in expenses if expense["month"] == month_row["month"]]
        }

    return render_template('index.html', grouped_expenses=grouped_expenses)


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        amount = float(request.form['amount'])

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)',
                  (date, description, category, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_expense.html')

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/categories')
def categories():
    category_data = aggregate_expenses_by_category()
    category_names = list(category_data.keys())
    category_amounts = list(category_data.values())

    #last 6 months for dropdown
    today = datetime.now()
    grouped_months = {}
    for i in range(6):
        month_date = today - timedelta(days=i * 30)
        month_name = month_date.strftime('%B %Y')
        grouped_months[month_name] = month_name

    return render_template(
        'categories.html',
        categories=category_data,
        category_names=category_names,
        category_amounts=category_amounts,
        grouped_months=grouped_months
    )



@app.route('/categories/filter')
def filter_categories():
    selected_month = request.args.get('month')

    conn = get_db_connection()
    if selected_month and selected_month != 'all':

        month_start = datetime.strptime(selected_month, '%B %Y').replace(day=1)
        next_month_start = (month_start + timedelta(days=31)).replace(day=1)

        query = """
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE date BETWEEN ? AND ? 
            GROUP BY category
        """
        data = conn.execute(query, (month_start.strftime('%Y-%m-%d'), next_month_start.strftime('%Y-%m-%d'))).fetchall()
    else:
        
        six_months_ago = (datetime.now().replace(day=1) - timedelta(days=180)).strftime('%Y-%m-01')
        query = """
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE date >= ? 
            GROUP BY category
        """
        data = conn.execute(query, (six_months_ago,)).fetchall()

    conn.close()

    categories = {row["category"]: row["SUM(amount)"] for row in data}
    return {
        "categories": [{"name": k, "amount": v} for k, v in categories.items()],
        "category_names": list(categories.keys()),
        "category_amounts": list(categories.values()),
    }



@app.route('/trends')
def trends():
    trends_data = get_spending_trends(days=7)
    dates = list(trends_data.keys())
    amounts = list(trends_data.values())
    return render_template('trends.html', trends=trends_data, dates=dates, amounts=amounts)


@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    expenses_list = [
        {
            'date': datetime.strptime(expense['date'], '%Y-%m-%d'),
            'amount': expense['amount'],
            'category': expense['category']
        }
        for expense in expenses
    ]
    
    # Sliding Window for Weekly/Monthly Expense Analysis
    
    expenses_by_date = defaultdict(float)
    for expense in expenses_list:
        expenses_by_date[expense['date']] += expense['amount']
    sorted_dates = sorted(expenses_by_date.keys())
    
    # Generate sliding window totals (weekly)
    weekly_totals = []
    window_size = 7  
    for i in range(len(sorted_dates)):
        start_date = sorted_dates[i]
        end_date = start_date + timedelta(days=window_size)
        total = sum(
            amount for date, amount in expenses_by_date.items()
            if start_date <= date < end_date
        )
        weekly_totals.append({'start': start_date, 'total': total})
    
    # Expense breakdown by category
    category_totals = defaultdict(float)
    for expense in expenses_list:
        category_totals[expense['category']] += expense['amount']
    
    # Monthly view
    monthly_totals = defaultdict(float)
    for expense in expenses_list:
        month_year = expense['date'].strftime('%Y-%m')
        monthly_totals[month_year] += expense['amount']
    

    return render_template(
        'dashboard.html',
        weekly_totals=weekly_totals,
        monthly_totals=monthly_totals,
        category_totals=category_totals
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
