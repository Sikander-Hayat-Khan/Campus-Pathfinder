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

        confidence REAL,

        department TEXT,

        summary TEXT,

        email TEXT,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()


def save_ticket(request, category, urgency, confidence, department, summary, email, status):
    
    conn = sqlite3.connect("tickets.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets
    (
        request,
        category,
        urgency,
        confidence,
        department,
        summary,
        email,
        status
    )
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        request,
        category,
        urgency,
        confidence,
        department,
        summary,
        email,
        status
    ))

    conn.commit()

    conn.close()