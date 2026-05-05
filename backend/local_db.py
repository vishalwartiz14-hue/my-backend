import sqlite3
import json
import os
from datetime import datetime

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "users.db")


# ================= CONNECTION =================
def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


# ================= INIT DB =================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # LANDLORDS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS landlords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        company_name TEXT,
        username TEXT,
        password TEXT,
        phone_number TEXT,
        account_type TEXT,
        secondary_email TEXT
    )
    """)

    # CUSTOMERS (FULL STRUCTURE)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT,
        landlord_full_name TEXT,
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

    # SYNC QUEUE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sync_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        table_name TEXT,
        data_json TEXT,
        status TEXT DEFAULT 'pending',
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= USERS =================
def add_user_local(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(username, password) VALUES(?,?)",
        (data["username"], data["password"])
    )

    conn.commit()
    conn.close()


def get_users_local():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]


def delete_user_local(uid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=?", (uid,))

    conn.commit()
    conn.close()


# ================= LANDLORDS =================
def get_landlords_local():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM landlords")
    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]


def delete_landlord_local(lid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM landlords WHERE id=?", (lid,))

    conn.commit()
    conn.close()


# ================= CUSTOMERS =================
def add_customer_local(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO customers (
            account_number, landlord_name, account_type,
            first_name, last_name, unit, street_address,
            city, zip_code, country, email, phone,
            password, secondary_email
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data.get("account_number"),
        data.get("landlord_name"),
        data.get("account_type"),
        data.get("first_name"),
        data.get("last_name"),
        data.get("unit"),
        data.get("street_address"),
        data.get("city"),
        data.get("zip_code"),
        data.get("country"),
        data.get("email"),
        data.get("phone"),
        data.get("password"),
        data.get("secondary_email"),
    ))

    conn.commit()
    conn.close()


def get_customers_local():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]


def delete_customer_local(cid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM customers WHERE id=?", (cid,))

    conn.commit()
    conn.close()


# ================= SYNC QUEUE =================
def add_to_queue(action, table_name, data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sync_queue(action, table_name, data_json, status, timestamp)
        VALUES(?,?,?,?,?)
    """, (
        action,
        table_name,
        json.dumps(data),
        "pending",
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_pending_changes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM sync_queue WHERE status='pending'")
    rows = cur.fetchall()

    conn.close()
    return [dict(r) for r in rows]


def mark_synced(queue_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE sync_queue
        SET status='synced'
        WHERE id=?
    """, (queue_id,))

    conn.commit()
    conn.close()


# ================= INIT =================
init_db()