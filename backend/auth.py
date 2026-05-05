from flask import Blueprint, request, jsonify
import sqlite3
import os

auth_bp = Blueprint("auth", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "users.db")


# ================= DB HELPER =================
def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, username
            FROM users
            WHERE username=? AND password=?
        """, (username, password))

        user = cur.fetchone()

        if user:
            return jsonify({
                "status": "success",
                "user": {
                    "id": user["id"],
                    "username": user["username"]
                }
            })

        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    finally:
        conn.close()


# ================= REGISTER =================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing fields"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        conn.commit()

        return jsonify({
            "status": "success",
            "message": "User registered"
        })

    except sqlite3.IntegrityError:
        return jsonify({
            "status": "error",
            "message": "User already exists"
        }), 400

    finally:
        conn.close()


# ================= GET USERS =================
@auth_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, username FROM users")
        users = cur.fetchall()

        return jsonify([
            {"id": u["id"], "username": u["username"]}
            for u in users
        ])

    finally:
        conn.close()


# ================= DELETE USER =================
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "Deleted successfully"})

    finally:
        conn.close()



# ================= GET CUSTOMERS =================
@auth_bp.route("/customers", methods=["GET"])
def get_customers():
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                id,
                account_number,
                landlord_name,
                account_type,
                first_name,
                last_name,
                unit,
                street_address,
                city,
                zip_code,
                country,
                email,
                phone,
                password,
                secondary_email
            FROM customers
        """)

        rows = cur.fetchall()

        return jsonify([
            {
                "id": r["id"],
                "account_number": r["account_number"],
                "landlord_name": r["landlord_name"],
                "account_type": r["account_type"],
                "first_name": r["first_name"],
                "last_name": r["last_name"],
                "unit": r["unit"],
                "street_address": r["street_address"],
                "city": r["city"],
                "zip_code": r["zip_code"],
                "country": r["country"],
                "email": r["email"],
                "phone": r["phone"],
                "password": r["password"],
                "secondary_email": r["secondary_email"]
            }
            for r in rows
        ])

    finally:
        conn.close()


# ================= ADD CUSTOMER =================
@auth_bp.route("/customers", methods=["POST"])
def add_customer():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO customers (
                account_number,
                landlord_name,
                account_type,
                first_name,
                last_name,
                unit,
                street_address,
                city,
                zip_code,
                country,
                email,
                phone,
                password,
                secondary_email
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
            data.get("secondary_email"),
        ))

        conn.commit()

        return jsonify({"message": "customer added successfully"})

    finally:
        conn.close()