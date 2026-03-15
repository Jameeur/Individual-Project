#!/usr/bin/env python3
import sys
import json
from datetime import datetime

track_db = "/tmp/wazuh_attacker_memory.json"
ar_log = "/var/ossec/logs/active-responses.log"

def load_mem():
    try:
        with open(track_db, "r") as f:
            return json.load(f)
    except:
        return {}

def save_mem(state):
    try:
        with open(track_db, "w") as f:
            json.dump(state, f)
    except:
        pass

def trigger_alert(ip, user, hits, atype):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] DEDUCTION: {atype} detected from {ip} (User: {user}, Failures: {hits})\n"
    try:
        with open(ar_log, "a") as f:
            f.write(entry)
    except:
        pass

def main():
    try:
        raw_in = sys.stdin.readline()
        if not raw_in:
            return
            
        data = json.loads(raw_in)
        alert_info = data.get("parameters", {}).get("alert", {})
        rid = str(alert_info.get("rule", {}).get("id", "0"))
        
        src = alert_info.get("data", {}).get("srcip")
        usr = alert_info.get("data", {}).get("dstuser")
        
        if not src:
            wevent = alert_info.get("data", {}).get("win", {}).get("eventdata", {})
            src = wevent.get("ipAddress", "local_console")
            usr = wevent.get("targetUserName", "unknown")
            
        if src in ["unknown", "-", None]:
            src = "local_console"

    except:
        return

    state = load_mem()
    
    success_ids = ["40112", "5715", "100099", "60106"]
    
    if rid in success_ids:
        if src in state:
            state[src]["count"] = 0
            state[src]["users"] = []
            save_mem(state)
        return

    fail_ids = ["60122", "5716", "5710"]
    if rid not in fail_ids:
        return 

    if src not in state:
        state[src] = {"count": 0, "users": []}
        
    state[src]["count"] += 1
    
    if usr not in state[src]["users"]:
        state[src]["users"].append(usr)

    strikes = state[src]["count"]
    ucount = len(state[src]["users"])

    if strikes >= 3 and ucount == 1:
        trigger_alert(src, usr, strikes, "Brute Force")
    elif ucount >= 3:
        trigger_alert(src, "Multiple Users detected", strikes, "User Enumeration")

    save_mem(state)

if __name__ == "__main__":
    main()
