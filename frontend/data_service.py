import requests
from frontend.local_db import (
    add_user_local,
    get_users_local,
    delete_user_local,
    add_to_queue,
    save_users_local,
    get_landlords_local,
    save_landlords_local,
    delete_landlord_local,
    get_customers_local,
    add_customer_local,
    delete_customer_local
)

SERVER = "http://127.0.0.1:5000"


# ================= ONLINE CHECK =================
def is_online():
    try:
        requests.get(f"{SERVER}/ping", timeout=2)
        return True
    except:
        return False


# ================= AUTH =================
def login(username, password):
    if is_online():
        try:
            r = requests.post(f"{SERVER}/login", json={
                "username": username,
                "password": password
            })

            if r.status_code == 200:
                return {"status": "success", "data": r.json()}

            return {"status": "error", "message": "invalid login"}

        except:
            pass

    return {"status": "offline", "message": "server offline"}


def register(username, password):
    if is_online():
        try:
            r = requests.post(f"{SERVER}/register", json={
                "username": username,
                "password": password
            })
            return r.json()
        except:
            pass

    add_user_local({"username": username, "password": password})
    add_to_queue("CREATE", "users", {
        "username": username,
        "password": password
    })

    return {"message": "saved offline"}


# ================= USERS =================
def get_users():
    if is_online():
        try:
            r = requests.get(f"{SERVER}/users")
            data = r.json()
            save_users_local(data)
            return data
        except:
            return get_users_local()
    return get_users_local()


def delete_user(user_id):
    if is_online():
        try:
            requests.delete(f"{SERVER}/users/{user_id}")
            delete_user_local(user_id)
        except:
            delete_user_local(user_id)
            add_to_queue("DELETE", "users", {"id": user_id})
    else:
        delete_user_local(user_id)
        add_to_queue("DELETE", "users", {"id": user_id})


# ================= LANDLORDS =================
def get_landlords():
    if is_online():
        try:
            r = requests.get(f"{SERVER}/landlords")
            data = r.json()
            save_landlords_local(data)
            return data
        except:
            return get_landlords_local()
    return get_landlords_local()


def delete_landlord(lid):
    if is_online():
        try:
            requests.delete(f"{SERVER}/landlords/{lid}")
            delete_landlord_local(lid)
        except:
            delete_landlord_local(lid)
            add_to_queue("DELETE", "landlords", {"id": lid})
    else:
        delete_landlord_local(lid)
        add_to_queue("DELETE", "landlords", {"id": lid})


# ================= CUSTOMERS =================
def get_customers():
    if is_online():
        try:
            r = requests.get(f"{SERVER}/customers")
            return r.json()
        except:
            return get_customers_local()
    return get_customers_local()


def add_customer(data):
    if is_online():
        try:
            requests.post(f"{SERVER}/customers", json=data)
        except:
            add_customer_local(data)
            add_to_queue("CREATE", "customers", data)
    else:
        add_customer_local(data)
        add_to_queue("CREATE", "customers", data)


def delete_customer(cid):
    if is_online():
        try:
            requests.delete(f"{SERVER}/customers/{cid}")
        except:
            delete_customer_local(cid)
            add_to_queue("DELETE", "customers", {"id": cid})
    else:
        delete_customer_local(cid)
        add_to_queue("DELETE", "customers", {"id": cid})