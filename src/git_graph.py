import zlib
import os
import re
import json
from collections import defaultdict, deque

def parse_git_object(object_dir, object_hash):
    # Abre y descomprime un objeto git
    path = os.path.join(".git", "objects", object_dir, object_hash)
    with open(path, "rb") as f:
        compressed = f.read()
    return zlib.decompress(compressed)

def is_commit_object(data):
    # Verifica si el objeto es un commit
    return data.startswith(b'commit ')

def parseo_commit(data):
    # Extrae los hashes de los padres de un commit
    lines = data.split(b'\n')
    padres = []
    for line in lines:
        if line.startswith(b'parent '):
            padres.append(line.split()[1].decode())
        if line == b'':
            break
    return padres

def find_head_commit():
    # Obtiene el hash del commit HEAD
    head_path = os.path.join(".git", "HEAD")
    with open(head_path) as f:
        ref = f.read().strip()
    if ref.startswith("ref:"):
        ref_path = os.path.join(".git", ref.split()[1])
        with open(ref_path) as rf:
            return rf.read().strip()
    return ref

def find_tag_commits():
    # Obtiene el hash de commit para cada tag
    tags_dir = os.path.join(".git", "refs", "tags")
    tag_commits = {}
    if os.path.isdir(tags_dir):
        for tag in os.listdir(tags_dir):
            with open(os.path.join(tags_dir, tag)) as f:
                tag_commits[tag] = f.read().strip()
    return tag_commits

def build_commit_graph():
    # Construye el grafo de commits y calcula el indegree
    objects_path = os.path.join(".git", "objects")
    grafo = defaultdict(list)
    indegree = defaultdict(int)
    for obj_dir in os.listdir(objects_path):
        if len(obj_dir) != 2 or obj_dir in ("info", "pack"):
            continue
        dir_path = os.path.join(objects_path, obj_dir)
        for obj_hash in os.listdir(dir_path):
            full_hash = obj_dir + obj_hash
            try:
                data = parse_git_object(obj_dir, obj_hash)
                if is_commit_object(data):
                    padres = parseo_commit(data)
                    grafo[full_hash] = padres
                    for p in padres:
                        indegree[p] += 1
            except Exception:
                continue
    return grafo, indegree

def compute_density(grafo, head):
    # Calcula la densidad de ramas
    nivel = defaultdict(int)
    visitados = set()
    cola = deque([(head, 0)])
    max_nivel = 0
    while cola:
        nodo, prof = cola.popleft()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        nivel[prof] += 1
        max_nivel = max(max_nivel, prof)
        for padre in grafo.get(nodo, []):
            cola.append((padre, prof + 1))
    suma = sum(nivel[i]/i for i in range(1, max_nivel+1) if i in nivel)
    return suma / max(1, max_nivel)

def find_critical_path(grafo, head, tag_commits):
    # Encuentra el camino crítico minimizando merges
    roots = [h for t, h in tag_commits.items() if t == "v0.0.0"]
    if not roots:
        return []
    root = roots[0]
    deuda = lambda n: 1 if len(grafo.get(n, [])) > 1 else 0
    dist = {head: 0}
    prev = {head: None}
    cola = deque([head])
    while cola:
        nodo = cola.popleft()
        for padre in grafo.get(nodo, []):
            alt = dist[nodo] + deuda(padre)
            if padre not in dist or alt < dist[padre]:
                dist[padre] = alt
                prev[padre] = nodo
                cola.append(padre)
    # Reconstruye el camino
    camino = []
    n = root
    while n:
        camino.append(n)
        n = prev.get(n)
    return camino[::-1]

def find_bottlenecks(indegree):
    # Top-5 commits con mayor indegree (>2)
    bneck = sorted([k for k, v in indegree.items() if v > 2], key=lambda k: indegree[k], reverse=True)
    return bneck[:5]

def main():
    # Ejecutamos el analisis y guardamos resultados
    grafo, indegree = build_commit_graph()
    head = find_head_commit()
    tags = find_tag_commits()
    densidad = compute_density(grafo, head)
    critico = find_critical_path(grafo, head, tags)
    bneck = find_bottlenecks(indegree)
    resultado = {
        "densidad": densidad,
        "ruta_critica": critico,
        "cuellos_de_botella": bneck
    }
    with open("git_analysis.json", "w") as f:
        json.dump(resultado, f, indent=2)
    print("Analisis guardado en git_analysis.json")

if __name__ == "__main__":
    main()