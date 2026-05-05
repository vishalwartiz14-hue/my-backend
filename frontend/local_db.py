import sqlite3
import json

DB = "users.db"


# ================= CONNECTION =================
def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


# ================= INIT =================
def init():
    c = conn()
    cur = c.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # LANDLORDS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS landlords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT
    )
    """)

    # CUSTOMERS TABLE (FULL STRUCTURE)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
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

    # SYNC QUEUE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sync_queue(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        table_name TEXT,
        data_json TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    c.commit()
    c.close()


# ================= USERS =================
def add_user_local(data):
    c = conn()
    cur = c.cursor()

    cur.execute(
        "INSERT INTO users(username, password) VALUES(?,?)",
        (data["username"], data["password"])
    )

    c.commit()
    c.close()


def get_users_local():
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    c.close()
    return [dict(r) for r in rows]


def delete_user_local(uid):
    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM users WHERE id=?", (uid,))

    c.commit()
    c.close()


def save_users_local(users):
    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM users")

    for u in users:
        cur.execute(
            "INSERT INTO users(id, username) VALUES(?,?)",
            (u["id"], u["username"])
        )

    c.commit()
    c.close()


# ================= LANDLORDS =================
def save_landlords_local(data):
    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM landlords")

    for l in data:
        cur.execute("""
            INSERT INTO landlords(id, first_name, last_name)
            VALUES(?,?,?)
        """, (l["id"], l["first_name"], l["last_name"]))

    c.commit()
    c.close()


def get_landlords_local():
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT * FROM landlords")
    rows = cur.fetchall()

    c.close()
    return [dict(r) for r in rows]


def delete_landlord_local(lid):
    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM landlords WHERE id=?", (lid,))

    c.commit()
    c.close()


# ================= CUSTOMERS =================
def add_customer_local(data):
    c = conn()
    cur = c.cursor()

    cur.execute("""
        INSERT INTO customers(
            account_number, landlord_name, account_type,
            first_name, last_name, unit,
            street_address, city, zip_code, country,
            email, phone, password, secondary_email
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
        data.get("secondary_email")
    ))

    c.commit()
    c.close()


def get_customers_local():
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()

    c.close()
    return [dict(r) for r in rows]


def delete_customer_local(cid):
    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM customers WHERE id=?", (cid,))

    c.commit()
    c.close()


# ================= SYNC QUEUE =================
def add_to_queue(action, table, data):
    c = conn()
    cur = c.cursor()

    cur.execute("""
        INSERT INTO sync_queue(action, table_name, data_json, status)
        VALUES(?,?,?,?)
    """, (action, table, json.dumps(data), "pending"))

    c.commit()
    c.close()


def get_pending_changes():
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT * FROM sync_queue WHERE status='pending'")
    rows = cur.fetchall()

    c.close()
    return [dict(r) for r in rows]


def mark_synced(id):
    c = conn()
    cur = c.cursor()

    cur.execute(
        "UPDATE sync_queue SET status='synced' WHERE id=?",
        (id,)
    )

    c.commit()
    c.close()


# ================= INIT CALL =================
init()