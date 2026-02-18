import os
import sys
import time
import subprocess
import random

Target_IP = "192.168.4.103"
Delay = 1.5

def print_banner():
    print("    THREAT SIMULATOR - RED TEAM TOOL    ")
    print("    Author: Jameeur Rahman              ")
    print("========================================")

def ssh_auth(attempts):
    print(f"Starting  {attempts} SSH attempts towards {Target_IP}")
    
    users = ["admin", "root", "test", "jameeur", "ghost", "webmaster"]
    
    for i in range(attempts):
        fake_user = random.choice(users)
        print(f" Attempt {i+1}: '{fake_user}'")
        
        cmd = f"ssh -o StrictHostKeyChecking=no -o PreferredAuthentications=password -o PubkeyAuthentication=no -o BatchMode=yes {fake_user}@{Target_IP} 2>/dev/null"
        subprocess.run(cmd, shell=True)
        time.sleep(Delay)
        
    print("Simulation is complete")

def privilege_escalation():
    print(f"\n[*] Simulating attempts...")
    print(" (Will trigger higher rule-based triggers in Wazuh")
    
    for i in range(5):
        print(f" Attempt: {i+1}")
        cmd = "su - root -c 'echo test' < /dev/null 2>/dev/null"
        subprocess.run(cmd, shell=True) 
        time.sleep(Delay)
        
    print("Done")

def launch_sim():
    print_banner()
    print("Select an simulation option:")
    print("1. SSH Brute Force")
    print("2. Local Privilege Escalation (Rule 5503)")
    print("3. Both")
    print("4. Exit")
    
    try:
        choice = input("\n[?] Enter choice (1-4): ")
        
        if choice == '1':
            trigger_ssh_auth(15)
        elif choice == '2':
            trigger_privilege_escalation()
        elif choice == '3':
            trigger_ssh_auth(10)
            trigger_privilege_escalation()
        elif choice == '4':
            print("Quitting")
            sys.exit(0)
        else:
            print("Invalid number, please type again")
    except KeyboardInterrupt:
        print("keyboard interrupted")
        sys.exit(0)

launch_sim()
        
   

