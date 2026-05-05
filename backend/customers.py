from flask import Blueprint, jsonify, request
from backend.local_db import (
    get_customers_local,
    add_customer_local,
    delete_customer_local
)

customers_bp = Blueprint("customers", __name__)


# ================= GET ALL =================
@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    data = get_customers_local()
    return jsonify(data)


# ================= ADD CUSTOMER =================
@customers_bp.route("/customers", methods=["POST"])
def add_customer():
    data = request.json
    cid = add_customer_local(data)
    return jsonify({"status": "success", "id": cid})


# ================= DELETE CUSTOMER =================
@customers_bp.route("/customers/<int:cid>", methods=["DELETE"])
def delete_customer(cid):
    delete_customer_local(cid)
    return jsonify({"status": "deleted"})