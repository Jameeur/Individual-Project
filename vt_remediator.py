import sys, json, os

def process_alert():
    try:
        raw_in = sys.stdin.readline()
        if not raw_in: return
        
        data = json.loads(raw_in)
        
        
        vt_block = data.get("parameters", {}).get("alert", {}).get("data", {}).get("virustotal", {})
        bad_file = vt_block.get("source", {}).get("file")
        
        # condition
        if not bad_file:
            bad_file = data.get("parameters", {}).get("alert", {}).get("syscheck", {}).get("path")
            
        if bad_file and os.path.exists(bad_file):
            os.remove(bad_file)
            # print(f"deleted {bad_file}")
            
    except:
        pass

process_alert()
