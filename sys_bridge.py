#!/usr/bin/env python3
import sys
import json
from datetime import datetime

Logs = "/var/ossec/logs/active-responses.log"

def logs_WAZUH(message):
    now = datetime.now().strftime("%a %b %d %I:%M:%S %p %Y")
    with open(Logs, "a") as f:
        f.write(f"{now} {message}\n")

def main():
    try:
        input_str = sys.stdin.read()
        if not input_str:
            return
        data = json.loads(input_str)
        
        alert = data.get('parameters', {}).get('alert', data)
        data_fields = alert.get('data', {})
        
        srcip = data_fields.get('srcip') or alert.get('srcip') or "N/A"
        rule_id = alert.get('rule', {}).get('id') or "N/A"

        logs_WAZUH(f"active-response/bin/sys_bridge.py: Execution successful. Rule: {rule_id} , IP: {srcip}")
        
    except Exception as e:
        logs_WAZUH(f"active-response/bin/sys_bridge.py: Error executing the alert: {str(e)}")

main()
