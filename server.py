from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}  # simple in-memory storage (later DB bana sakte ho)

# ---------- REGISTER ----------

@app.route("/")
def home():
    return "Server is running ✔"
    
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users:
        return jsonify({"status": "error", "msg": "User already exists"})

    users[username] = password
    return jsonify({"status": "success"})

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if users.get(username) == password:
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

app.run(host="0.0.0.0", port=5000)