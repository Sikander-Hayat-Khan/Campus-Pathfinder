import sqlite3

def init_db():

    conn = sqlite3.connect("tickets.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request TEXT,
        category TEXT,
        urgency TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_ticket(request, category, urgency, status):

    conn = sqlite3.connect("tickets.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets
    (
    request,
    category,
    urgency,
    status
    )
    VALUES
    (?, ?, ?, ?)
    """,
    (
    request,
    category,
    urgency,
    status
    ))

    conn.commit()
    conn.close()