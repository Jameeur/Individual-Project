import incident_mail
import time
import json
import os
import subprocess

Logs = "/var/ossec/logs/alerts/alerts.json"
TargetID = "5710"

def handle_event(alert):
    rule_id = alert.get('rule', {}).get('id')

    if rule_id == TargetID:
        src_ip = alert.get('data', {}).get('srcip', 'N/A')

        print(f"\n[!] SSH BRUTE FORCE HAS BEEN DETECTED at {src_ip}")
        print(f"    Notifying via Email...")

        success = incident_mail.send_alert(alert)

        if success:
            print("Email Sent")
        else:
            print("ERROR: Email NOT Sent")
        
def follow(file_obj):
    file_obj.seek(0, os.SEEK_END)
    while True:
        line = file_obj.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def main():
    print(f"Monitoring {Logs} for {TargetID}")
    
    try:
        with open(Logs, 'r') as f:
            for line in follow(f):
                try:
                    alert = json.loads(line)
                    handle_event(alert)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"Cannot find {Logs} possibly due to permissions")
        
main()
