import sqlite3

def connect_db():
    return sqlite3.connect("banco.db")

def get_user(id):
    db = connect_db()
    # SQL Injection intencional
    query = f"SELECT * FROM users WHERE id={id}"
    return db.execute(query).fetchall()