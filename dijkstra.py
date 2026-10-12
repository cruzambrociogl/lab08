##############################
# Implementación del algoritmo Dijkstra
# siguiendo la notación del laboratorio:
# c(w,v), D(v), p(v) y N'
#####

INF = float('inf')

# Estado del algoritmo
graph = {}   # {Nodo1: {Nodo2: Costo}}
dist = {}    # D(v)
prev = {}    # p(v)


'''
Función de costo desde w a v, donde w y v son vecinos.
Retorna  c(w, v) el calculo de resultante de los vecinos w a v
'''
def c(w, v):
	return graph[w].get(v, INF)


'''
Función de Menor costo desde el nodo de origen hasta el destino v.
Retorna  D(v) su costo actual de v
'''
def D(v):
	return dist[v]


'''
Función de Nodo anterior vecino de v
Retorna  p(v)  el nombre del nodo anterior vecino de v
'''
def p(v):
	return prev[v]


'''
Función que arma una fila de la tabla de pasos:
(paso, "D(v), p(v)" de cada nodo distinto al inicial, nodo agregado a N')
Valores no definidos coloca el simbolo ∞
'''
def row(step, initNode, nodes, w):
	cells = []
	for v in nodes:
		if v == initNode: continue
		cells.append("∞" if D(v) == INF else f"{D(v)}, {p(v)}")
	return (step, *cells, w)


'''
Función donde Inicia la Ejecución del Algoritmo de Dijkstra
Retorna una lista de filas, una por cada paso del algoritmo
'''
def init(initNode, routeDict):
	global graph, dist, prev
	graph = routeDict
	nodes = sorted(routeDict.keys())

	# Inicialización: N' = {u}
	# D(v) = c(u,v) y p(v) = u si v es vecino de u, de otro modo D(v) = ∞
	N_prime = [initNode]
	dist = {v: c(initNode, v) for v in nodes}
	prev = {v: initNode if dist[v] != INF else None for v in nodes}
	dist[initNode], prev[initNode] = 0, initNode

	steps = [row(0, initNode, nodes, initNode)]

	# Repetir hasta N' = N
	while len(N_prime) < len(nodes):
		# Encontrar w que no esté en N' tal que D(w) es un mínimo.
		# Empate: el primero alfabéticamente (nodes ya está ordenado).
		candidates = [v for v in nodes if v not in N_prime]
		w = min(candidates, key=D)
		if D(w) == INF: break  # Nodos restantes inalcanzables

		# Añadir w a N'
		N_prime.append(w)

		# Actualizar D(v) para cada vecino v de w que no esté en N':
		# D(v) = min( D(v), D(w) + c(w,v) )
		# Empate: p(v) cambia al nuevo nodo w, por eso se usa <=
		for v in sorted(graph[w]):
			if v in N_prime: continue
			if D(w) + c(w, v) <= D(v):
				dist[v] = D(w) + c(w, v)
				prev[v] = w

		steps.append(row(len(N_prime) - 1, initNode, nodes, w))

	return steps
