def guardar_resultados(grafo_obj, asincrono=False):
    """Guarda los resultados del cálculo en un archivo de texto."""
    modo = "ASÍNCRONO" if asincrono else "SINCRÓNICO"
    with open("resultados_clique.txt", "a", encoding="utf-8") as f:
        f.write("=====================================\n")
        f.write(f"Modo de ejecución: {modo}\n")
        f.write(f"Nodos: {grafo_obj.n_nodos}\n")
        f.write(f"Probabilidad de conexión: {grafo_obj.probabilidad}\n")
        f.write(f"Clique máximo encontrado: {grafo_obj.clique_maximo}\n")
        f.write(f"Tamaño del clique máximo: {len(grafo_obj.clique_maximo)}\n")
        f.write(f"Tiempo de ejecución: {grafo_obj.tiempo:.4f} segundos\n\n")
