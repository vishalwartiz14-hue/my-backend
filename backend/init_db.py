import sqlite3
import os

# ================= SAFE PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DB_DIR, "users.db")

os.makedirs(DB_DIR, exist_ok=True)


# ================= INIT DB =================
def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cur = conn.cursor()

    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    # ================= USERS =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # ================= LANDLORDS =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS landlords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        company_name TEXT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone_number TEXT,
        account_type TEXT CHECK(account_type IN (
            'Property Management',
            'Landlord',
            'Other'
        )),
        secondary_email TEXT
    )
    """)

    # ================= CUSTOMERS =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        account_number TEXT,
        landlord_name TEXT,
        account_type TEXT,

        first_name TEXT,
        last_name TEXT,

        unit TEXT,
        street_address TEXT,
        city TEXT,
        zip_code TEXT,
        country TEXT,

        email TEXT,
        phone TEXT,
        password TEXT,
        secondary_email TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully with customers")