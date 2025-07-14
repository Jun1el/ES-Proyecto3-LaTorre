import requests
import time
import sys

class Mediator:
    def __init__(self, service_a_url, service_b_url, service_c_url):
        self.service_a = service_a_url
        self.service_b = service_b_url
        self.service_c = service_c_url

    def execute(self, data):
        trace_id = data.get('trace_id')
        # 3 reintentos con backoff exponencial
        for intento in range(3):
            try:
                resp = requests.post(f'{self.service_a}/task', json=data, timeout=2)
                resp.raise_for_status()
                data = resp.json()
                break
            except Exception as e:
                if intento == 2:
                    raise Exception('Fallo en servicio A')
                # Si falla espera con backoff exponencial de 2 elevado al intento
                time.sleep(2 ** intento)
        # Envia a B y gestiona lentitud
        inicio = time.time()
        resp = requests.post(f'{self.service_b}/task', json=data, timeout=2)
        if resp.elapsed.total_seconds() > 0.5:
            # Si B es lento reduce la cadena 
            return {"data": "B lento, proceso reducido", "trace_id": trace_id}
        data = resp.json()
        # Envia a C y loguea trace_id
        resp = requests.post(f'{self.service_c}/task', json=data, timeout=2)
        print(f"TRACE_ID: {trace_id}", file=sys.stdout)
        return resp.json()
    
# Facade CLI para ejecutar desde stdin y escribir en stdout
import json
def run_cli():
    entrada = sys.stdin.read()
    req = json.loads(entrada)
    mediator = Mediator('http://service_a:5001', 'http://service_b:5002', 'http://service_c:5003')
    resultado = mediator.execute(req)
    print(json.dumps(resultado))
