import os
from flask import Flask, render_template, jsonify, request
from sys_parser import fetch_stream, fetch_aggregated_metrics

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live_data')
def live_data():
    # updates latest sime alerts
    data = fetch_stream()
    return jsonify(data)

@app.route('/analytics')
def analytics_view():
    return render_template('graph.html')

@app.route('/metric_data')
def metric_data():
    # grab depth from url
    req_depth = request.args.get('depth', default=500, type=int)
    
    # limits at 5000 so it gets a piece of the data per time 
    safe_limit = min(req_depth, 5000) 
    
    # print(f"DEBUG: pulling {safe_limit} logs for graph")
    metrics = fetch_aggregated_metrics(depth=safe_limit)
    return jsonify(metrics)

if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    except Exception as err:
        print("Error code ", err)
