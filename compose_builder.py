# Builder para docker-compose 
import yaml

class Service:
    def __init__(self, name, image, ports, depends_on=None):
        self.name = name
        self.image = image
        self.ports = ports
        self.depends_on = depends_on or []

    def to_dict(self):
        # convertimos el servicio a un docker-compose 
        d = {
            'image': self.image,
            'ports': self.ports,
            'networks': ['mesh-net']
        }
        # establecemos dependencias si existen 
        if self.depends_on:
            d['depends_on'] = self.depends_on
        return d

class ComposeBuilder:
    def __init__(self):
        self.services = {}
        self.networks = {'mesh-net': {}}

    def add_service(self, service):
        self.services[service.name] = service.to_dict()
        return self

    def build(self):
        return {
            'version': '3',
            'services': self.services,
            'networks': self.networks
        }

    def save(self, path):
        with open(path, 'w') as f:
            yaml.dump(self.build(), f, default_flow_style=False)

if __name__ == '__main__':
    # Creamos los 3 servicios A , B y C con imagenes de Python 3.9 predefinidas y establecemis dependencias
    a = Service('service_a', 'python:3.9', ['5001:5001'])
    b = Service('service_b', 'python:3.9', ['5002:5002'], depends_on=['service_a'])
    c = Service('service_c', 'python:3.9', ['5003:5003'], depends_on=['service_b'])
    # Encadenamos servicios y red mesh-net
    builder = ComposeBuilder()
    builder.add_service(a).add_service(b).add_service(c)
    builder.save('docker-compose.yml')
    print('docker-compose.yml generado con red mesh-net y servicios encadenados')