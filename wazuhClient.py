#!/usr/bin/python3
import sys
import json
import time
from datetime import datetime
import os

Records = "/tmp/wazuh_attacker_memory.json"
Logs = "/tmp/wazuh_project_output.txt"

def load_db():
    try:
        with open(Records, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    try:
        with open(Records, "w") as f:
            json.dump(data, f)
        os.chmod(Records, 0o666)
    except:
        pass

def log_attack(ip, user, count, attack_type):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{now}] DEDUCTION: {attack_type} detected from {ip} (User: {user}, Failures: {count})\n"
    try:
        with open(Logs, "a") as f:
            f.write(msg)
        os.chmod(Logs, 0o666)
    except:
        pass

def main():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        alert = json.loads(line)
        
        win_data = alert.get("data", {}).get("win", {}).get("eventdata", {})
        src_ip = win_data.get("ipAddress", "unknown")
        user = win_data.get("targetUserName", "unknown")
        
        if src_ip == "unknown" or src_ip == "-" or src_ip is None:
            src_ip = "local_console"

    except:
        return
    db = load_db()
    
    if src_ip not in db:
        db[src_ip] = {"count": 0, "users": []}
        
    db[src_ip]["count"] += 1
    
    if user not in db[src_ip]["users"]:
        db[src_ip]["users"].append(user)

    count = db[src_ip]["count"]
    unique_users = len(db[src_ip]["users"])

    if count >= 3 and unique_users == 1:
        log_attack(src_ip, user, count, "Brute Force")

    elif unique_users >= 3:
        log_attack(src_ip, "Multiple Users detected", count)

    save_db(db)

if __name__ == "__main__":
    main()
