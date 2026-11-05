from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    age INTEGER,
    service TEXT,
    salary REAL,
    date_embauche TEXT,
    email TEXT,
    manager TEXT,
    telephone TEXT,
    ville TEXT,
    pays TEXT,
    date_naissance TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modification_date TEXT,
    user_name TEXT,
    employee_id INTEGER,
    field_name TEXT,
    old_value TEXT,
    new_value TEXT
)
""")

conn.commit()

conn.close()

print("Base créée")