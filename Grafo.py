import networkx as nx
import random
import time
import asyncio
from utils import guardar_resultados


class Grafo:
    """Clase que modela un grafo y permite resolver el problema del clique máximo."""

    def __init__(self, n_nodos: int, probabilidad: float = 0.3):
        self.n_nodos = n_nodos
        self.probabilidad = probabilidad
        self.G = None
        self.clique_maximo = []
        self.tiempo = 0.0

    # ---------------------------------------------------
    # Generación del grafo
    # ---------------------------------------------------
    def generar(self):
        """Genera un grafo aleatorio con n nodos y probabilidad de conexión."""
        self.G = nx.erdos_renyi_graph(self.n_nodos, self.probabilidad)
        print(f"Grafo generado con {len(self.G.nodes)} nodos y {len(self.G.edges)} aristas.")

    # ---------------------------------------------------
    # Resolución sincrónica
    # ---------------------------------------------------
    def resolver_sincronico(self):
        """Calcula el clique máximo de forma sincrónica con indicador de progreso."""
        if self.G is None:
            raise ValueError("Primero debe generar el grafo con .generar()")

        print("\nBuscando cliques... (esto puede tardar en grafos grandes)")
        start = time.time()
        
        cliques = []
        contador = 0
        for c in nx.find_cliques(self.G):
            cliques.append(c)
            contador += 1
            # Cada 1000 cliques encontrados, mostramos progreso
            if contador % 1000 == 0:
                print(f"  > {contador} cliques explorados...", end="\r")

        self.clique_maximo = max(cliques, key=len)
        self.tiempo = time.time() - start

        print(f"\n\nClique máximo: {self.clique_maximo}")
        print(f"Tamaño: {len(self.clique_maximo)}")
        print(f"Tiempo (sincrónico): {self.tiempo:.4f} s")

        guardar_resultados(self, asincrono=False)

    # ---------------------------------------------------
    # Resolución asíncrona
    # ---------------------------------------------------
    async def resolver_asincronico(self):
        """Calcula el clique máximo de forma asíncrona (simulada)."""
        if self.G is None:
            raise ValueError("Primero debe generar el grafo con .generar()")

        start = time.time()
        cliques = []

        nodos = list(self.G.nodes)
        tam_trozos = max(1, len(nodos) // 4)
        trozos = [nodos[i:i+tam_trozos] for i in range(0, len(nodos), tam_trozos)]

        async def procesar(subnodos):
            subG = self.G.subgraph(subnodos)
            sub_cliques = list(nx.find_cliques(subG))
            await asyncio.sleep(0)  # ceder control
            return sub_cliques

        tareas = [procesar(t) for t in trozos]
        resultados = await asyncio.gather(*tareas)
        for r in resultados:
            cliques.extend(r)

        self.clique_maximo = max(cliques, key=len)
        self.tiempo = time.time() - start

        print(f"\nClique máximo (asíncrono): {self.clique_maximo}")
        print(f"Tamaño: {len(self.clique_maximo)}")
        print(f"Tiempo (asíncrono): {self.tiempo:.4f} s")

        guardar_resultados(self, asincrono=True)
