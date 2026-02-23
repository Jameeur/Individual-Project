import os
import sys
import time
import random
import subprocess
import getpass

Bait_User = getpass.getuser()

def windows_breach():
    os.system('cls')
    print(f"   Windows RDP THREAT INJECTOR")
    print(f"   Author: Jameeur Rahman")
    print("-------------------------------------------")
    print("Attacking local database")
    
    n = "".join(chr(c) for c in [110, 101, 116, 32, 117, 115, 101, 32])
    ni = "".join(chr(c) for c in [92, 92, 49, 50, 55, 46, 48, 46, 48, 46, 49, 92, 73, 80, 67, 36, 32])
    u = "".join(chr(c) for c in [47, 117, 115, 101, 114, 58])
    
    
    print("Generating Windows Event 4625, check for this event in Wazuh Manager for validation")
    for i in range(10):
        print(f"       Failed attempt {i+1}/10..")
        
        p = f"RND_pass_{random.randint(1000,9999)}"
        cmd = f"{n}{ni}{u}{Bait_User} {p}"
        
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5)
        
    print("Letting Wazuh Agent move the logs to Wazuh Manager. Wait")
    for i in range(5, 0, -1):
        print(f"       {i} seconds")
        time.sleep(1)
        
    print("Injector is complete. Check your dashboard")

if __name__ == "__main__":
    windows_breach()
