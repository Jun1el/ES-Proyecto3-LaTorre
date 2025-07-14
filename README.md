# Examen sustiturio DS-Proyecto 3 
Alumno: La Torre Vasquez Andres 

Codigo: 20212100C 
## Parte 1 - Algoritmo sobre el grafo de git 

Para empezar en este proyecto quiero que mi codigo pueda abrir y parsear los archivos en .git/object/<xx>/<yyyy> usando libreria zlib no git log ni rev-list 

Para esto cada objeto commit expone la lista de padres y necesitamos construir un grafo dirigido donde los nodos son SHA-1 de commits y las aristas apuntan a sus padres 

Metricas : 
Densidad de ramas : Para cada nivel de profundida i(distancia minimo del head la nodo) calcula nodes_i/i, luego suma para todos los niveles y divide por el total de niveles 
critical path: definir "deuda de merges" como secuencias de merges consecutivos (commits con >1 padre ). Aplica dijkstra inverso para hallar el camino desde el head hasta un tag raiz v0.0.0 que minimize la suma de "deuda" 
Top-k bottleneck commits identifica los k=5 commits con mayor indegree(>2)

Salida: generar git analysis.json con campos density:float, critical path:[sha...], bottlenecks:[sha...]
# Preguntas Teoricas 

- Porque git es un DAG 
Podemos ver a los commits como vertices que apuntan a otros en una direccion definida y suele confundir cuando hacemos merge o rebases como si las direcciones cambiaran y pudieran generar bucles cosa que no pasa ya que solo cambia el puntero donde se actualiza otro caso donde lo podemos ver es cuando cambiamos un padre cambiamos a un nuevo commit con un nuevo id por eso nos salen advertencia cuando reescribimos historiales compartidos que afecten el orden de nuestro repositorio 
- Mediator vs Adapter 
