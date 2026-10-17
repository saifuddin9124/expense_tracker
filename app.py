from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this_later"

def init_db():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    
    # 1. Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    
    # 2. Create Expenses Table with user_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    connection.commit()
    connection.close()

# Initialize database on startup
init_db()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_pw = generate_password_hash(password)
        
        connection = sqlite3.connect('expenses.db')
        cursor = connection.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_pw))
            connection.commit()
        except sqlite3.IntegrityError:
            return "Error: Username already taken!", 400
        finally:
            connection.close()
            
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = sqlite3.connect('expenses.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        connection.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            return "Error: Invalid username or password", 401
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    connection = sqlite3.connect("expenses.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (session['user_id'],))
    expenses = cursor.fetchall()
    
    total = sum(expense['amount'] for expense in expenses)
    connection.close()
    
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["POST"])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    amount = request.form['amount']
    description = request.form['description']
    location = request.form['location']
    category = request.form['category']
    date = request.form['date']
    
    if not amount or not description or not location or not category or not date:
        return "Error: All fields are required!", 400
        
    if category.strip().isdigit() or location.strip().isdigit() or description.strip().isdigit():
        return "Error: Category, location, and description cannot be just numbers!", 400
    
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            return "Error: Amount must be greater than zero!", 400
    except ValueError: 
        return "Error: Amount must be a valid number!", 400
        
    try:
        parsed_date = datetime.strptime(date, "%d%m%y")
        formated_date = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return "Error: Date must be a real date in DDMMYY format (e.g., 261224)!", 400
    
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    
    cursor.execute(
        "INSERT INTO expenses (user_id, amount, description, location, category, date) VALUES (?,?,?,?,?,?)",
        (session['user_id'], amount_float, description, location, category, formated_date)
    )
    connection.commit()
    connection.close()

    return redirect(url_for("home"))

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_expense(id):
    if 'user_id' not in session:
        return {"status": "unauthorized"}, 401

    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (id, session['user_id']))
    
    connection.commit()
    connection.close()

    return {"status": "success"}, 200

if __name__ == "__main__":
    app.run(debug=True)
