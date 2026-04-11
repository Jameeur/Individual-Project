#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime

Records = "/tmp/wazuh_attacker_memory.json"
Logs = "/var/ossec/logs/active-responses.log"

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
    except:
        pass

def log_attack(ip, user, count, attack_type):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{now}] Deduction: {attack_type} detected from {ip} (User: {user}, Failures: {count})\n"
    try:
        with open(Logs, "a") as f:
            f.write(msg)
    except:
        pass

def main():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        alert = json.loads(line)
        
        alert_data = alert.get("parameters", {}).get("alert", {})
        rule_id = str(alert_data.get("rule", {}).get("id", "unknown"))
        src_ip = alert_data.get("data", {}).get("srcip")
        user = alert_data.get("data", {}).get("dstuser")
        
        if not src_ip:
            win_data = alert_data.get("data", {}).get("win", {}).get("eventdata", {})
            src_ip = win_data.get("ipAddress", "unknown")
            user = win_data.get("targetUserName", "unknown")
            
        if src_ip == "unknown" or src_ip == "-" or src_ip is None:
            src_ip = "local_console"

    except:
        return

    # Loads database
    db = load_db()
    
    # Checks for successful login
    success_rules = ["40112", "5715", "100099"]
    if rule_id in success_rules:
        if src_ip in db:
            db[src_ip]["count"] = 0
            db[src_ip]["users"] = []
            save_db(db)
        return

    # Processes any failed logins
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
