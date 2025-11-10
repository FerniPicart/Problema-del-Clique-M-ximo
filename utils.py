import matplotlib.pyplot as plt
import re
import os


def guardar_resultado(grafo_obj, metodo, archivo):
    """
    Guarda los resultados de UNA ejecución individual en un archivo.
    
    Args:
        grafo_obj: instancia de la clase Grafo
        metodo: "exacto" o "heuristico"
        archivo: ruta del archivo donde guardar
    """
    metodo_texto = "EXACTO (Bron-Kerbosch)" if metodo == "exacto" else "HEURÍSTICO (Voraz)"
    
    with open(archivo, "a", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write(f"Método: {metodo_texto}\n")
        f.write(f"Nodos: {grafo_obj.n_nodos}\n")
        f.write(f"Probabilidad de conexión: {grafo_obj.probabilidad}\n")
        f.write(f"Aristas: {len(grafo_obj.G.edges)}\n")
        f.write(f"Clique encontrado: {grafo_obj.clique_maximo}\n")
        f.write(f"Tamaño del clique: {len(grafo_obj.clique_maximo)}\n")
        f.write(f"Tiempo de ejecución: {grafo_obj.tiempo:.4f} segundos\n")
        f.write("="*60 + "\n\n")


def guardar_comparacion(resultado, archivo):
    """
    Guarda el resultado de una comparación entre exacto y heurístico.
    
    Args:
        resultado: diccionario con los datos de la comparación
        archivo: ruta del archivo donde guardar
    """
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"Caso: {resultado['n']} nodos\n")
        f.write(f"Probabilidad: {resultado['probabilidad']}\n")
        f.write(f"Aristas: {resultado['aristas']}\n")
        f.write("-" * 70 + "\n")
        f.write(f"EXACTO:      Tamaño={resultado['exacto']['tamaño']}, "
                f"Tiempo={resultado['exacto']['tiempo']:.4f}s\n")
        f.write(f"HEURÍSTICO:  Tamaño={resultado['heuristico']['tamaño']}, "
                f"Tiempo={resultado['heuristico']['tiempo']:.4f}s\n")
        f.write("-" * 70 + "\n")
        f.write(f"¿Alcanzó óptimo?: {'SÍ' if resultado['alcanzó_optimo'] else 'NO'}\n")
        f.write(f"Error relativo: {resultado['error_relativo']:.2f}%\n")
        f.write(f"Speedup: {resultado['speedup']:.2f}x más rápido\n")
        f.write("="*70 + "\n\n")


def preguntar_graficar(mensaje, funcion_graficar):
    """
    Pregunta al usuario si desea graficar y ejecuta la función si acepta.
    
    Args:
        mensaje: mensaje a mostrar al usuario
        funcion_graficar: función a ejecutar si el usuario acepta
    """
    print("\n" + "="*60)
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    
    if respuesta.startswith('s'):
        funcion_graficar()
    else:
        print("📊 Puedes graficar más tarde desde el menú principal.")


def graficar_resultados(ruta_archivo):
    """
    Genera un gráfico que relaciona el tamaño de entrada n (eje X)
    con el tiempo de ejecución (eje Y), y comenta la complejidad observada.
    
    Args:
        ruta_archivo: ruta al archivo con los resultados a graficar
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"\n⚠️  No se encontró el archivo '{ruta_archivo}'.")
        print("   Ejecuta primero el experimento correspondiente.")
        return

    # Extraer datos con expresiones regulares
    nodos = [int(x) for x in re.findall(r"Nodos:\s*(\d+)", contenido)]
    tiempos = [float(x) for x in re.findall(r"Tiempo de ejecución:\s*([\d.]+)", contenido)]

    if not nodos or not tiempos:
        print("\n⚠️  No se encontraron datos válidos en el archivo.")
        return

    # Generar gráfico
    plt.figure(figsize=(10, 6))
    
    # Determinar el tipo de algoritmo para el título y color
    if "exacto" in ruta_archivo.lower():
        titulo = "Algoritmo EXACTO: Tamaño del grafo (n) vs Tiempo"
        color = 'red'
        label = 'Algoritmo Exacto'
    elif "heuristico" in ruta_archivo.lower():
        titulo = "Algoritmo HEURÍSTICO: Tamaño del grafo (n) vs Tiempo"
        color = 'green'
        label = 'Algoritmo Heurístico'
    else:
        titulo = "Tamaño del grafo (n) vs Tiempo de ejecución"
        color = 'blue'
        label = 'Algoritmo'
    
    plt.plot(nodos, tiempos, marker='o', linestyle='-', linewidth=2, 
             markersize=8, color=color, label=label)
    
    plt.title(titulo, fontsize=14, fontweight='bold')
    plt.xlabel("Número de nodos (n)", fontsize=12)
    plt.ylabel("Tiempo de ejecución (segundos)", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Interpretación automática
    print("\n" + "="*60)
    print("📈 INTERPRETACIÓN DE LA CURVA")
    print("="*60)
    
    if "exacto" in ruta_archivo.lower():
        print("\n🔴 ALGORITMO EXACTO (Bron-Kerbosch):")
        print("   • Complejidad teórica: O(3^(n/3)) - EXPONENCIAL")
        print("   • A medida que aumenta n, el tiempo crece exponencialmente")
        print("   • Pequeños aumentos en n → grandes aumentos en tiempo")
        print("   • Si la curva se eleva bruscamente, confirma el crecimiento exponencial")
        print("   • NO es viable para grafos grandes (n > 500 aprox.)")
    
    elif "heuristico" in ruta_archivo.lower():
        print("\n🟢 ALGORITMO HEURÍSTICO (Voraz):")
        print("   • Complejidad teórica: O(n²) - POLINOMIAL")
        print("   • El tiempo crece de forma mucho más moderada")
        print("   • Es VIABLE para grafos grandes (n ≥ 1000)")
        print("   • La curva debería ser mucho más suave que la del exacto")
        print("   • Trade-off: rapidez vs. optimalidad (puede no encontrar el máximo)")
    
    print("\n💡 Para el informe:")
    print("   Compara ambos gráficos lado a lado para mostrar la diferencia")
    print("   dramática en escalabilidad entre exacto y heurístico.")
    print("="*60 + "\n")


def graficar_comparacion(archivo="comparacion_metodos.txt"):
    """
    Genera gráficos comparativos entre el algoritmo exacto y el heurístico.
    Lee del archivo de comparación y muestra:
    - Tiempo de ejecución (EXACTO en rojo, HEURÍSTICO en verde)
    - Calidad de solución (tamaño del clique)
    """
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"\n⚠️  No se encontró el archivo '{archivo}'.")
        print("   Ejecuta primero la comparación (opción 5 del menú).")
        return

    # Extraer datos
    casos = re.findall(r"Caso: (\d+) nodos", contenido)
    exactos = re.findall(r"EXACTO:\s+Tamaño=(\d+), Tiempo=([\d.]+)", contenido)
    heuristicos = re.findall(r"HEURÍSTICO:\s+Tamaño=(\d+), Tiempo=([\d.]+)", contenido)

    if not casos or not exactos or not heuristicos:
        print("\n⚠️  No se encontraron datos válidos de comparación.")
        return

    nodos = [int(n) for n in casos]
    
    # Tiempos
    tiempos_exacto = [float(t) for _, t in exactos]
    tiempos_heuristico = [float(t) for _, t in heuristicos]
    
    # Tamaños de clique
    tamaños_exacto = [int(s) for s, _ in exactos]
    tamaños_heuristico = [int(s) for s, _ in heuristicos]

    # Crear figura con 2 subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Tiempos de ejecución
    ax1.plot(nodos, tiempos_exacto, marker='o', label='Exacto', 
             linewidth=2, markersize=8, color='red')
    ax1.plot(nodos, tiempos_heuristico, marker='s', label='Heurístico', 
             linewidth=2, markersize=8, color='green')
    ax1.set_xlabel("Número de nodos (n)", fontsize=11)
    ax1.set_ylabel("Tiempo de ejecución (segundos)", fontsize=11)
    ax1.set_title("Comparación de Tiempos", fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Calidad de solución
    ax2.plot(nodos, tamaños_exacto, marker='o', label='Exacto (óptimo)', 
             linewidth=2, markersize=8, color='red')
    ax2.plot(nodos, tamaños_heuristico, marker='s', label='Heurístico', 
             linewidth=2, markersize=8, color='green')
    ax2.set_xlabel("Número de nodos (n)", fontsize=11)
    ax2.set_ylabel("Tamaño del clique encontrado", fontsize=11)
    ax2.set_title("Comparación de Calidad", fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Análisis estadístico
    print("\n" + "="*60)
    print("📊 ANÁLISIS COMPARATIVO")
    print("="*60)
    
    # Calcular métricas promedio
    coincidencias = sum(1 for e, h in zip(tamaños_exacto, tamaños_heuristico) if e == h)
    tasa_optimalidad = (coincidencias / len(tamaños_exacto)) * 100 if tamaños_exacto else 0
    
    speedup_promedio = sum(te / th for te, th in zip(tiempos_exacto, tiempos_heuristico)) / len(tiempos_exacto)
    
    print(f"\n🎯 CALIDAD DE SOLUCIÓN:")
    print(f"   • El heurístico alcanzó el óptimo en {coincidencias}/{len(tamaños_exacto)} casos")
    print(f"   • Tasa de optimalidad: {tasa_optimalidad:.1f}%")
    
    print(f"\n⚡ VELOCIDAD:")
    print(f"   • Speedup promedio: {speedup_promedio:.2f}x más rápido")
    print(f"   • Tiempo exacto promedio: {sum(tiempos_exacto)/len(tiempos_exacto):.4f}s")
    print(f"   • Tiempo heurístico promedio: {sum(tiempos_heuristico)/len(tiempos_heuristico):.4f}s")
    
    print("\n💡 CONCLUSIÓN:")
    if tasa_optimalidad >= 80:
        print("   El heurístico es EXCELENTE: encuentra el óptimo en la mayoría")
        print("   de casos y es muchísimo más rápido. ¡Ideal para casos reales!")
    elif tasa_optimalidad >= 50:
        print("   El heurístico es BUENO: encuentra soluciones cercanas al óptimo")
        print("   en tiempo muy inferior. Útil cuando el tiempo es crítico.")
    else:
        print("   El heurístico es RÁPIDO pero puede alejarse del óptimo.")
        print("   Evaluar según el contexto: ¿es aceptable una solución subóptima?")
    
    print("="*60 + "\n")


def limpiar_resultados():
    """
    Elimina todos los archivos de resultados anteriores.
    Útil para empezar experimentos desde cero.
    """
    archivos = [
        "resultados_exacto.txt",
        "resultados_heuristico.txt",
        "resultados_exacto_multiple.txt",
        "resultados_heuristico_multiple.txt",
        "comparacion_metodos.txt"
    ]
    
    print("\n" + "="*60)
    print("🗑️  LIMPIEZA DE ARCHIVOS")
    print("="*60)
    
    eliminados = 0
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"   ✓ Eliminado: {archivo}")
            eliminados += 1
        else:
            print(f"   - No existe: {archivo}")
    
    if eliminados > 0:
        print(f"\n✅ {eliminados} archivo(s) eliminado(s).")
    else:
        print("\n💡 No había archivos para eliminar.")
    
    print("="*60)