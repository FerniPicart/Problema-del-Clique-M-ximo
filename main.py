import asyncio
from Grafo import Grafo


def main():
    print("==== PROBLEMA DEL CLIQUE MÁXIMO ====\n")

    try:
        n = int(input("Ingrese la cantidad de nodos del grafo: "))
        p = float(input("Probabilidad de conexión (0 a 1, ej. 0.3): "))
        modo = input("¿Ejecutar en modo asíncrono? (s/n): ").lower().startswith("s")
    except ValueError:
        print("⚠️ Entrada no válida.")
        return

    grafo = Grafo(n, p)
    grafo.generar()

    if modo:
        asyncio.run(grafo.resolver_asincronico())
    else:
        grafo.resolver_sincronico()

    print("\n✅ Resultados guardados en 'resultados_clique.txt'.")


if __name__ == "__main__":
    main()
