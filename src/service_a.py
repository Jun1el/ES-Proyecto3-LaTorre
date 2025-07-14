# Servicio A para recibir datos y retornar un trace_id y se conecta a un endpoint específico.
from flask import Flask, request, jsonify
import uuid
app = Flask(__name__)

@app.route('/task', methods=['POST'])
def task():
    data = request.json
    # Procesa y retorna el mismo trace_id
    return jsonify({"data": f"A:{data['data']}", "trace_id": data["trace_id"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
