import json
from datetime import datetime
from collections import Counter

WAZUH_LOG = "/var/ossec/logs/alerts/alerts.json"

def fetch_stream(limit=50):
    alerts = []
    try:
        with open(WAZUH_LOG, 'r') as f:
            f.seek(0, 2)
            fsize = f.tell()
            
            # limits number of threats visualized in dashboard
            f.seek(max(fsize - 5000 * limit, 0), 0) 
            
            lines = f.readlines()
            for line in lines:
                try:
                    alerts.append(json.loads(line))
                except:
                    pass
    except:
        pass
        
    # returns the requested amount
    return alerts[-limit:][::-1]

def fetch_aggregated_metrics(depth=2000):
    raw_times = []
    try:
        with open(WAZUH_LOG, 'r') as f:
            f.seek(0, 2) 
            
            chunk_size = depth * 500 
            f.seek(max(f.tell() - chunk_size, 0), 0)
            
            lines = f.readlines()[-depth:]
            for line in lines:
                try:
                    log_entry = json.loads(line)
                    ts = log_entry.get('timestamp')
                    if ts:
                        # returns the time in seconds
                        minute_slice = ts[:16].replace('T', ' ')
                        raw_times.append(minute_slice)
                except:
                    continue
    except:
        pass

    alert_counts = Counter(raw_times)
    
    values = []
    labels = []
    
    
    
    for t in sorted(alert_counts.keys()):
        labels.append(t.split(' ')[1])
        values.append(alert_counts[t])
        
    return {"labels": labels, "values": values}
