# Servicio B
from flask import Flask, request, jsonify
import uuid
import time
app = Flask(__name__)

@app.route('/task', methods=['POST'])
def task():
    data = request.json
    # Simula transformación y posible lentitud de la respuesta
    if data.get('simulate_slow', False):
        time.sleep(1)
    return jsonify({"data": f"B:{data['data']}", "trace_id": data["trace_id"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
