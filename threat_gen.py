import os
import sys
import time
import subprocess
import random

Target_IP = "192.168.4.103"
Delay = 1.5

def print_banner():
    print("========================================")
    print("    THREAT SIMULATOR - RED TEAM TOOL    ")
    print("    Author: Jameeur Rahman              ")
    print("========================================")

def ssh_auth(attempts):
    print(f"Starting {attempts} SSH attempts towards {Target_IP}")
  
    users = ["administrator", "root", "jamal", "jameeur", "hacker", "webmaster"]
    
    for i in range(attempts):
        fake_user = random.choice(users)
        print(f" Attempt {i+1}: '{fake_user}'")
        
        cmd = f"ssh -o StrictHostKeyChecking=no -o PreferredAuthentications=password -o PubkeyAuthentication=no -o BatchMode=yes {fake_user}@{Target_IP} 2>/dev/null"
        subprocess.run(cmd, shell=True)
      

def privilege_escalation():
    print(f"\n[*] Simulating attempts...")
    print(" (Will trigger higher rule-based triggers in Wazuh")
    
    for i in range(5):
        print(f" Attempt: {i+1}")
        cmd = "su - root -c 'echo test' < /dev/null 2>/dev/null"
        subprocess.run(cmd, shell=True)
        
   

