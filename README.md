# Problema-del-Clique-M-ximo
🎯 Objetivo: Resolver el problema del **clique máximo** en un grafo no dirigido, usando Python y el paquete NetworkX. El programa puede ejecutar la búsqueda de manera sincrónica o asíncrona para comparar tiempos, y guarda los resultados en un archivo de texto.

1. grafo.py -
-Contiene una clase llamada Grafo que encapsula toda la lógica.
- Atributos:
- - n_nodos (int): número de nodos.
- - probabilidad (float): probabilidad de conexión entre nodos.
- - G: objeto networkx.Graph().
- - clique_maximo: lista con los vértices del clique máximo.
- - tiempo: tiempo de ejecución.
  - - Métodos: - generar(): crea un grafo aleatorio tipo Erdős–Rényi.
  - - resolver_sincronico(): busca el clique máximo usando nx.find_cliques(G), mide tiempo y muestra progreso.
  - - resolver_asincronico(): versión simulada con asyncio que procesa subgrafos en paralelo.
    
  - - Ambas funciones guardan resultados en un archivo resultados_clique.txt (mediante la función guardar_resultados del módulo utils).

2. utils.py
- Contiene la función guardar_resultados(grafo_obj, asincrono=False) que escribe los datos de la ejecución en un archivo TXT con modo, cantidad de nodos, probabilidad, clique encontrado, tamaño y tiempo.

- 3. main.py
- Punto de entrada del programa.
- Pide al usuario: - número de nodos, - probabilidad de conexión, - si desea ejecutar en modo asíncrono.
- Crea el objeto Grafo, genera el grafo y ejecuta el método correspondiente.
- Muestra resultados en consola y confirma guardado del archivo.

- 4. resultados_clique.txt
  - Archivo de salida con el registro de resultados de las ejecuciones anteriores.
