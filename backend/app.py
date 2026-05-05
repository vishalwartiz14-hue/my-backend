from flask import Flask
from backend.auth import auth_bp
from backend.users import users_bp
from backend.landlords import landlords_bp
from backend.customers import customers_bp
from backend.init_db import init_db

app = Flask(__name__)

# ================= INIT DB =================
init_db()

# ================= REGISTER BLUEPRINTS =================
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(landlords_bp)
app.register_blueprint(customers_bp)

# ================= HEALTH CHECK =================
@app.route("/ping")
def ping():
    return {"status": "ok"}


# ================= RUN =================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )