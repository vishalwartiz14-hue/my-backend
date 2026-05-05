import tkinter as tk
import requests

SERVER = "http://192.168.1.10:5000"

def register():
    data = {
        "username": user.get(),
        "password": pwd.get()
    }

    try:
        res = requests.post(SERVER + "/register", json=data)
        result.set(res.json().get("message", res.json().get("error", "Unknown response")))
    except:
        result.set("Server offline")

def login():
    data = {
        "username": user.get(),
        "password": pwd.get()
    }

    try:
        res = requests.post(SERVER + "/login", json=data)
        resp = res.json()

        if "message" in resp and "success" in resp["message"].lower():
            result.set("Login success ✔")
        else:
            result.set(resp.get("message", "Wrong credentials ❌"))

    except:
        result.set("Offline mode")

# -------- UI --------
root = tk.Tk()
root.title("Login System")
root.geometry("300x250")

tk.Label(root, text="Username").pack()
user = tk.Entry(root)
user.pack()

tk.Label(root, text="Password").pack()
pwd = tk.Entry(root, show="*")
pwd.pack()

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Register", command=register).pack(pady=5)

result = tk.StringVar()
tk.Label(root, textvariable=result).pack()

root.mainloop()