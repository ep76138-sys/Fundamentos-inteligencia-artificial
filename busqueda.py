import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# ==========================================================
# PROBLEMA 1: RUTA MAS RAPIDA A UN HOSPITAL
# ==========================================================

def generar_grafo_rutas():
    """Crea un grafo dirigido con tiempos en minutos."""
    G = nx.DiGraph()

    conexiones = [
        ("Casa", "Parque", 4),
        ("Casa", "Escuela", 6),
        ("Parque", "Centro", 5),
        ("Escuela", "Centro", 2),
        ("Parque", "Hospital", 12),
        ("Centro", "Hospital", 3),
        ("Escuela", "Hospital", 10)
    ]

    G.add_weighted_edges_from(conexiones)
    return G


def resolver_ruta_hospital(G, inicio, objetivo):
    """Busca la ruta de menor tiempo con Dijkstra."""
    ruta = nx.shortest_path(
        G, source=inicio, target=objetivo, weight="weight"
    )
    costo = nx.shortest_path_length(
        G, source=inicio, target=objetivo, weight="weight"
    )
    return ruta, costo


def dibujar_rutas(G, ruta):
    """Dibuja el grafo y destaca la ruta encontrada."""
    posiciones = {
        "Casa": (0, 1),
        "Parque": (1, 2),
        "Escuela": (1, 0),
        "Centro": (2, 1),
        "Hospital": (3, 1)
    }

    aristas_ruta = list(zip(ruta[:-1], ruta[1:]))

    nx.draw(
        G, posiciones, with_labels=True,
        node_color="lightblue", node_size=2200,
        arrows=True
    )
    nx.draw_networkx_edges(
        G, posiciones, edgelist=aristas_ruta,
        edge_color="red", width=3, arrows=True
    )
    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, posiciones, edge_labels=etiquetas
    )
    plt.title("Problema 1: Ruta al hospital")
    plt.show()


# ==========================================================
# PROBLEMA 2: ROBOT EN UNA BODEGA CON OBSTACULOS
# ==========================================================

def generar_grafo_bodega(filas, columnas, obstaculos):
    """Genera estados transitables y sus movimientos."""
    G = nx.Graph()

    for fila in range(filas):
        for columna in range(columnas):
            posicion = (fila, columna)

            if posicion not in obstaculos:
                G.add_node(posicion)

    # Conecta posiciones adyacentes transitables.
    for fila, columna in list(G.nodes()):
        for df, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            vecino = (fila + df, columna + dc)

            if vecino in G:
                G.add_edge((fila, columna), vecino)

    return G


def buscar_ruta_bfs(G, inicio, objetivo):
    """Encuentra una ruta con el menor numero de movimientos."""
    cola = deque([inicio])
    padres = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == objetivo:
            break

        for vecino in G.neighbors(actual):
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)

    if objetivo not in padres:
        return None

    # Reconstruye el camino desde el objetivo.
    ruta = []
    actual = objetivo

    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()
    return ruta


def dibujar_bodega(G, ruta, filas, columnas, obstaculos):
    """Dibuja las posiciones, los obstaculos y la ruta."""
    posiciones = {
        nodo: (nodo[1], -nodo[0])
        for nodo in G.nodes()
    }

    nx.draw(
        G, posiciones, with_labels=True,
        node_color="lightgray", node_size=650,
        font_size=8
    )

    if ruta:
        nx.draw_networkx_nodes(
            G, posiciones, nodelist=ruta,
            node_color="orange", node_size=650
        )
        nx.draw_networkx_edges(
            G, posiciones,
            edgelist=list(zip(ruta[:-1], ruta[1:])),
            edge_color="red", width=3
        )

    # Los obstaculos se muestran como cruces.
    for obstaculo in obstaculos:
        plt.scatter(
            obstaculo[1], -obstaculo[0],
            marker="s", s=500, color="black"
        )

    plt.title("Problema 2: Ruta del robot")
    plt.axis("equal")
    plt.show()


# ==========================================================
# EJECUCION Y RESULTADOS
# ==========================================================

if _name_ == "_main_":

    # Problema 1
    G1 = generar_grafo_rutas()
    ruta1, costo1 = resolver_ruta_hospital(
        G1, "Casa", "Hospital"
    )

    print("PROBLEMA 1: RUTA AL HOSPITAL")
    print("Ruta:", " -> ".join(ruta1))
    print("Tiempo total:", costo1, "minutos")
    print("Estados:", G1.number_of_nodes())
    print("Conexiones:", G1.number_of_edges())

    dibujar_rutas(G1, ruta1)

    # Problema 2
    filas, columnas = 4, 4
    obstaculos = {(1, 1), (1, 2), (2, 1)}
    inicio = (0, 0)
    objetivo = (3, 3)

    G2 = generar_grafo_bodega(
        filas, columnas, obstaculos
    )
    ruta2 = buscar_ruta_bfs(G2, inicio, objetivo)

    print("\nPROBLEMA 2: ROBOT EN LA BODEGA")

    if ruta2:
        print("Ruta:", " -> ".join(map(str, ruta2)))
        print("Movimientos:", len(ruta2) - 1)
    else:
        print("No existe una ruta al objetivo.")

    print("Estados transitables:", G2.number_of_nodes())
    print("Conexiones:", G2.number_of_edges())

    dibujar_bodega(
        G2, ruta2, filas, columnas, obstaculos
    )