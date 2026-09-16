import sqlite3


def connect_db():
    return sqlite3.connect("banco.db")


def get_user(id):
    db = connect_db()
    try:
        return db.execute(
            "SELECT * FROM users WHERE id = ?",
            (id,),
        ).fetchall()
    finally:
        db.close()
