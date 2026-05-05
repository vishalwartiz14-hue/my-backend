import threading
import time
import requests
import json

from frontend.local_db import get_pending_changes, mark_synced

API_URL = "http://127.0.0.1:5000"


def is_online():
    try:
        requests.get(f"{API_URL}/ping", timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False


def sync_once():
    if not is_online():
        return

    changes = get_pending_changes()

    for change in changes:
        try:
            action = change["action"]
            table = change["table_name"]
            data = json.loads(change["data_json"])

            # ================= USERS =================
            if table == "users":
                if action == "CREATE":
                    requests.post(f"{API_URL}/users", json=data)

                elif action == "UPDATE":
                    requests.put(f"{API_URL}/users/{data['id']}", json=data)

                elif action == "DELETE":
                    requests.delete(f"{API_URL}/users/{data['id']}")

            # ================= LANDLORDS =================
            elif table == "landlords":
                if action == "DELETE":
                    requests.delete(f"{API_URL}/landlords/{data['id']}")

            mark_synced(change["id"])

        except Exception as e:
            print("Sync error:", e)
            continue


def start_auto_sync(interval=5):
    def run():
        while True:
            sync_once()
            time.sleep(interval)

    threading.Thread(target=run, daemon=True).start()