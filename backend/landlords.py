from flask import Blueprint, request, jsonify
import sqlite3 
import os

landlords_bp = Blueprint("landlords", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "users.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ================= CREATE =================
@landlords_bp.route("/landlords", methods=["POST"])
def create_landlord():
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO landlords (
            first_name, last_name, company_name,
            username, password, phone_number,
            account_type, secondary_email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("first_name"),
        data.get("last_name"),
        data.get("company_name"),
        data.get("username"),
        data.get("password"),
        data.get("phone_number"),
        data.get("account_type"),
        data.get("secondary_email")
    ))

    conn.commit()
    conn.close()

    return {"message": "Landlord created"}, 201


# ================= GET =================
@landlords_bp.route("/landlords", methods=["GET"])
def get_landlords():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM landlords")
    rows = cur.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


# ================= DELETE =================
@landlords_bp.route("/landlords/<int:lid>", methods=["DELETE"])
def delete_landlord(lid):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM landlords WHERE id=?", (lid,))
    conn.commit()

    conn.close()

    return {"message": "Deleted"}, 200


    