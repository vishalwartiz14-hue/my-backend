from flask import Blueprint, request, jsonify
import sqlite3
import os

users_bp = Blueprint("users", __name__)

# ================= SAFE DB PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "users.db")


# ================= CONNECT =================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ================= CREATE USER =================
@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid data"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (
            data.get("username"),
            data.get("password")
        ))

        conn.commit()

        return jsonify({"message": "User created"}), 201

    finally:
        conn.close()


# ================= GET USERS =================
@users_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, username FROM users")
        rows = cur.fetchall()

        return jsonify([
            {"id": r["id"], "username": r["username"]}
            for r in rows
        ])

    finally:
        conn.close()


# ================= UPDATE USER =================
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE users
            SET username=?, password=?
            WHERE id=?
        """, (
            data.get("username"),
            data.get("password"),
            user_id
        ))

        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User updated"})

    finally:
        conn.close()


# ================= DELETE USER =================
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User deleted"})

    finally:
        conn.close()