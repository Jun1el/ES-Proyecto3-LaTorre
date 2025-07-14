# Servicio C
from flask import Flask, request, jsonify
import uuid
import sys
app = Flask(__name__)

@app.route('/task', methods=['POST'])
def task():
    data = request.json
    # Logging del trace_id en stdout
    print(f"TRACE_ID: {data['trace_id']}", file=sys.stdout)
    return jsonify({"data": f"C:{data['data']}", "trace_id": data["trace_id"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
