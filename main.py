import sys
from Grafo import Grafo
from utils import graficar_resultados, graficar_comparacion, limpiar_resultados, guardar_resultado


def main():
    while True:
        print("\n" + "="*60)
        print("PROBLEMA DEL CLIQUE MÁXIMO - MENÚ PRINCIPAL")
        print("="*60)
        print("\n📋 PUNTOS DEL TRABAJO:\n")
        print(" 1: Ejecutar algoritmo EXACTO - una vez (Punto 2)")
        print(" 2: Multiples pruebas algoritmo EXACTO (Punto 3)")
        print(" 3: Graficar EXACTO - múltiples pruebas (Punto 4)")
        print(" 4: Ejecutar HEURÍSTICA - una vez (Punto 5)")
        print(" 5: COMPARACIÓN Exacto vs Heurístico (Punto 6)")
        print(" 6: Graficar COMPARACIÓN (Punto 6)")
        print(" 7: Multiples pruebas algoritmo HEURÍSTICO (Punto 7)")
        print(" 8: Graficar HEURÍSTICO - múltiples pruebas (Punto 7)")
        print(" 9: Limpiar todos los archivos de resultados")
        print(" 0: Salir")
        
        opcion = input("\n👉 Seleccione una opción (0-9): ").strip()
        
        if opcion == "1":
            ejecutar_exacto_una_vez()
        elif opcion == "2":
            ejecutar_experimentacion_exacto()
        elif opcion == "3":
            graficar_resultados("resultados_exacto_multiple.txt")
        elif opcion == "4":
            ejecutar_heuristica_una_vez()
        elif opcion == "5":
            ejecutar_comparacion()
        elif opcion == "6":
            graficar_comparacion("comparacion_metodos.txt")
        elif opcion == "7":
            ejecutar_escalabilidad_heuristica()
        elif opcion == "8":
            graficar_resultados("resultados_heuristico_multiple.txt")
        elif opcion == "9":
            limpiar_resultados()
        elif opcion == "0":
            print("\n👋 Saliendo del programa.")
            sys.exit(0)
        else:
            print("\n⚠️  Opción no válida. Intente nuevamente.")


def ejecutar_exacto_una_vez():
    """PUNTO 2: Ejecuta el algoritmo exacto una sola vez"""
    print("\n" + "="*60)
    print("PUNTO 2: ALGORITMO EXACTO - Ejecución única")
    print("="*60)
    
    try:
        n = int(input("\n📊 Ingrese la cantidad de nodos del grafo: "))
        p = float(input("🔗 Probabilidad de conexión (0 a 1, ej. 0.3): "))
    except ValueError:
        print("⚠️  Entrada no válida.")
        return
    
    grafo = Grafo(n, p)
    grafo.generar()
    grafo.recorrer_exacto()
    
    # Guardar resultados DESPUÉS de ejecutar
    guardar_resultado(grafo, "exacto", "resultados_exacto.txt")
    
    print("\n✅ Resultados guardados en 'resultados_exacto.txt'")


def ejecutar_experimentacion_exacto():
    """PUNTO 3: Experimenta con el algoritmo exacto incrementando n"""
    print("\n" + "="*60)
    print("PUNTO 3: EXPERIMENTACIÓN CON ALGORITMO EXACTO")
    print("="*60)
    print("\nEsto ejecutará el algoritmo exacto con tamaños crecientes de grafos.")
    print("Se detendrá automáticamente al alcanzar el tiempo máximo.\n")
    
    # Preguntar si quiere limpiar datos anteriores
    limpiar = input("¿Deseas borrar los datos anteriores? (s/n): ").strip().lower()
    limpiar_anterior = limpiar.startswith('s')
    
    try:
        duracion = int(input("\n⏱️  Duración máxima en segundos (ej. 3600 = 1 hora): "))
    except ValueError:
        print("⚠️  Entrada no válida. Usando 1800 segundos (30 min) por defecto.")
        duracion = 1800
    
    Grafo.recorrer_exacto_multiple(duracion_maxima=duracion, limpiar_anterior=limpiar_anterior)


def ejecutar_heuristica_una_vez():
    """PUNTO 5: Ejecuta la heurística una sola vez"""
    print("\n" + "="*60)
    print("PUNTO 5: HEURÍSTICA VORAZ - Ejecución única")
    print("="*60)
    
    try:
        n = int(input("\n📊 Ingrese la cantidad de nodos del grafo: "))
        p = float(input("🔗 Probabilidad de conexión (0 a 1, ej. 0.3): "))
    except ValueError:
        print("⚠️  Entrada no válida.")
        return
    
    grafo = Grafo(n, p)
    grafo.generar()
    grafo.recorrer_heuristico()
    
    # Guardar resultados DESPUÉS de ejecutar
    guardar_resultado(grafo, "heuristico", "resultados_heuristico.txt")
    
    print("\n✅ Resultados guardados en 'resultados_heuristico.txt'")


def ejecutar_comparacion():
    """PUNTO 6: Compara exacto vs heurístico en los MISMOS casos con tamaños fijos"""
    print("\n" + "="*60)
    print("PUNTO 6: COMPARACIÓN Exacto vs Heurístico")
    print("="*60)
    print("\nSe ejecutarán AMBOS algoritmos sobre los MISMOS grafos.")
    print("Tamaños fijos: 200, 600, 1000, 1500 nodos")
    print("Esto permite comparar calidad y tiempo de ejecución.\n")
    
    # Preguntar si quiere limpiar datos anteriores
    limpiar = input("¿Deseas borrar los datos anteriores? (s/n): ").strip().lower()
    limpiar_anterior = limpiar.startswith('s')
    
    confirmar = input("\n¿Desea continuar? (s/n): ").lower()
    if not confirmar.startswith('s'):
        print("Operación cancelada.")
        return
    
    Grafo.recorrer_comparacion(limpiar_anterior=limpiar_anterior)


def ejecutar_escalabilidad_heuristica():
    """PUNTO 7: Prueba la heurística con grafos grandes (n >= 1000)"""
    print("\n" + "="*60)
    print("PUNTO 7: ESCALABILIDAD DE LA HEURÍSTICA")
    print("="*60)
    print("\nSe ejecutará la heurística con grafos de tamaño grande (n >= 1000).")
    print("Esto demuestra su viabilidad en casos reales.\n")
    
    # Preguntar si quiere limpiar datos anteriores
    limpiar = input("¿Deseas borrar los datos anteriores? (s/n): ").strip().lower()
    limpiar_anterior = limpiar.startswith('s')
    
    try:
        duracion = int(input("\n⏱️  Duración máxima en segundos (ej. 1800 = 30 min): "))
    except ValueError:
        print("⚠️  Entrada no válida. Usando 1200 segundos (20 min) por defecto.")
        duracion = 1200
    
    Grafo.recorrer_heuristico_multiple(duracion_maxima=duracion, limpiar_anterior=limpiar_anterior)


if __name__ == "__main__":
    main()