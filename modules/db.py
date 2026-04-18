import sqlite3
import pandas as pd

DB = "data/expenses.db"

def connect():
    return sqlite3.connect(DB)

def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        amount REAL,
        category TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_expense(username, date, amount, category, description):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (username, date, amount, category, description) VALUES (?, ?, ?, ?, ?)",
        (username, date, amount, category, description)
    )
    conn.commit()
    conn.close()

def load_expenses(username):
    conn = connect()
    df = pd.read_sql(f"SELECT * FROM expenses WHERE username='{username}'", conn)
    conn.close()
    return df