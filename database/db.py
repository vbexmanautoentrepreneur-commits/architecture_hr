import sqlite3
import sys
from pathlib import Path

def get_database_path():

    if getattr(sys, "frozen", False):
        print("Mode PyInstaller")
        app_dir = Path.home() / "AppData" / "Local" / "HRManager"
    else:
        print("Mode PyCharm/Python")
        BASE_DIR = Path(__file__).resolve().parent.parent
        app_dir = BASE_DIR / "database"
    app_dir.mkdir(parents=True, exist_ok=True)
    db_path = app_dir / "employees.db"

    print("Base SQLite :", db_path)

    return db_path

DATABASE_NAME = get_database_path()

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
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
    conn.row_factory = sqlite3.Row
    return conn