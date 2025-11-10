import networkx as nx
import time


class Grafo:
    """Clase que modela un grafo y permite resolver el problema del clique máximo."""

    def __init__(self, n_nodos: int, probabilidad: float = 0.3):
        self.n_nodos = n_nodos
        self.probabilidad = probabilidad
        self.G = None
        self.clique_maximo = []
        self.tiempo = 0.0

    def generar(self):
        """Genera un grafo aleatorio con n nodos y probabilidad de conexión."""
        self.G = nx.erdos_renyi_graph(self.n_nodos, self.probabilidad)
        print(f"✓ Grafo generado: {len(self.G.nodes)} nodos, {len(self.G.edges)} aristas.")

    def copiar_grafo(self, otro_grafo):
        """Copia el grafo de otra instancia para usar el MISMO grafo."""
        self.G = otro_grafo.G.copy()
        self.n_nodos = otro_grafo.n_nodos
        self.probabilidad = otro_grafo.probabilidad

    # ===================================================================
    # ALGORITMO EXACTO (Bron-Kerbosch)
    # ===================================================================
    
    def recorrer_exacto(self):
        """
        Calcula el clique máximo usando el algoritmo de Bron-Kerbosch (EXACTO).
        Este es un algoritmo de fuerza bruta que explora todas las posibles cliques.
        Complejidad: O(3^(n/3)) en el peor caso - EXPONENCIAL
        
        NOTA: Esta función NO guarda resultados automáticamente.
        """
        if self.G is None:
            raise ValueError("Primero debe generar el grafo con .generar()")

        print("\n🔍 Buscando clique máximo con algoritmo EXACTO...")
        print("   (Esto puede tardar en grafos grandes)\n")
        
        start = time.time()
        
        cliques = []
        contador = 0
        for c in nx.find_cliques(self.G):
            cliques.append(c)
            contador += 1
            if contador % 5000 == 0:
                print(f"   > {contador} cliques explorados...", end="\r")

        self.clique_maximo = max(cliques, key=len)
        self.tiempo = time.time() - start

        print(f"\n\n✅ Clique máximo encontrado: {self.clique_maximo}")
        print(f"📏 Tamaño: {len(self.clique_maximo)}")
        print(f"⏱️  Tiempo: {self.tiempo:.4f} segundos")

    # ===================================================================
    # HEURÍSTICA VORAZ
    # ===================================================================
    
    def recorrer_heuristico(self):
        """
        Heurística voraz basada en el grado de los vértices.
        
        Estrategia: Selecciona nodos con más conexiones primero e 
        iterativamente agrega aquellos que mantienen la propiedad 
        de adyacencia completa (todos conectados entre sí).
        
        Ventajas: Rápido, simple, escalable
        Limitaciones: Puede quedar en óptimo local, no garantiza 
                      encontrar el clique máximo global
        
        NOTA: Esta función NO guarda resultados automáticamente.
        """
        if self.G is None:
            raise ValueError("Primero debe generar el grafo con .generar()")

        print("\n🚀 Ejecutando heurística VORAZ...\n")
        
        start = time.time()

        # Ordenar nodos por grado (más conexiones primero)
        nodos_ordenados = sorted(
            self.G.nodes(), 
            key=lambda n: self.G.degree[n], 
            reverse=True
        )

        clique = []
        for v in nodos_ordenados:
            # Agregar v solo si está conectado con TODOS los nodos ya en la clique
            if all(self.G.has_edge(v, u) for u in clique):
                clique.append(v)

        self.clique_maximo = clique
        self.tiempo = time.time() - start

        print(f"✅ Clique encontrado: {clique}")
        print(f"📏 Tamaño: {len(clique)}")
        print(f"⏱️  Tiempo: {self.tiempo:.4f} segundos")

    # ===================================================================
    # EXPERIMENTACIÓN MÚLTIPLE
    # ===================================================================
    
    @staticmethod
    def recorrer_exacto_multiple(duracion_maxima=3600, limpiar_anterior=False):
        """
        PUNTO 3: Ejecuta el algoritmo exacto en bucle con grafos de tamaño creciente.
        Se detiene automáticamente cuando el tiempo total excede la duración máxima.
        
        Args:
            duracion_maxima: tiempo máximo en segundos
            limpiar_anterior: si True, borra el archivo anterior antes de empezar
        """
        from utils import guardar_resultado, preguntar_graficar
        import os
        
        archivo_salida = "resultados_exacto_multiple.txt"
        
        # Limpiar archivo anterior si se solicita
        if limpiar_anterior and os.path.exists(archivo_salida):
            os.remove(archivo_salida)
            print(f"🗑️  Archivo anterior eliminado: {archivo_salida}")
        
        print("\n" + "="*60)
        print("PUNTO 3: EXPERIMENTACIÓN - Algoritmo EXACTO")
        print("="*60)
        
        n_inicial = 50
        incremento = 50
        prob = 0.3
        
        tiempo_inicio = time.time()
        iteracion = 1

        print(f"\n⚙️  Configuración:")
        print(f"   • Tamaño inicial: {n_inicial} nodos")
        print(f"   • Incremento: {incremento} nodos")
        print(f"   • Probabilidad: {prob}")
        print(f"   • Tiempo máximo: {duracion_maxima}s ({duracion_maxima/60:.1f} min)")
        print(f"   • Archivo de salida: {archivo_salida}")

        while True:
            n_actual = n_inicial + (iteracion - 1) * incremento
            print(f"\n--- Iteración {iteracion}: {n_actual} nodos ---")

            grafo = Grafo(n_actual, prob)
            grafo.generar()
            grafo.recorrer_exacto()
            
            # Guardar resultados DESPUÉS de ejecutar
            guardar_resultado(grafo, "exacto", archivo_salida)

            tiempo_transcurrido = time.time() - tiempo_inicio
            
            if tiempo_transcurrido > duracion_maxima:
                print(f"\n⏰ Tiempo máximo alcanzado ({duracion_maxima}s). Finalizando.")
                break
            else:
                restante = duracion_maxima - tiempo_transcurrido
                print(f"⏳ Tiempo acumulado: {tiempo_transcurrido:.2f}s / {duracion_maxima}s")
                print(f"   Tiempo restante: {restante:.2f}s ({restante/60:.1f} min)")
            
            iteracion += 1

        print(f"\n✅ Experimentación finalizada.")
        print(f"   • Iteraciones completadas: {iteracion}")
        print(f"   • Tiempo total: {tiempo_transcurrido:.2f}s")
        print(f"   • Resultados guardados en: '{archivo_salida}'")
        
        # Preguntar si quiere graficar
        preguntar_graficar(
            mensaje="¿Quieres graficar resultados del algoritmo EXACTO (Punto 4)?",
            funcion_graficar=lambda: __import__('utils').graficar_resultados(archivo_salida)
        )

    @staticmethod
    def recorrer_heuristico_multiple(duracion_maxima=1200, limpiar_anterior=False):
        """
        PUNTO 7: Ejecuta el heurístico en bucle con grafos grandes (n >= 1000).
        
        Args:
            duracion_maxima: tiempo máximo en segundos
            limpiar_anterior: si True, borra el archivo anterior antes de empezar
        """
        from utils import guardar_resultado, preguntar_graficar
        import os
        
        archivo_salida = "resultados_heuristico_multiple.txt"
        
        # Limpiar archivo anterior si se solicita
        if limpiar_anterior and os.path.exists(archivo_salida):
            os.remove(archivo_salida)
            print(f"🗑️  Archivo anterior eliminado: {archivo_salida}")
        
        print("\n" + "="*60)
        print("PUNTO 7: ESCALABILIDAD - Algoritmo HEURÍSTICO")
        print("="*60)
        
        n_inicial = 1000
        incremento = 500
        prob = 0.3
        
        tiempo_inicio = time.time()
        iteracion = 1

        print(f"\n⚙️  Configuración:")
        print(f"   • Tamaño inicial: {n_inicial} nodos")
        print(f"   • Incremento: {incremento} nodos")
        print(f"   • Probabilidad: {prob}")
        print(f"   • Tiempo máximo: {duracion_maxima}s ({duracion_maxima/60:.1f} min)")
        print(f"   • Archivo de salida: {archivo_salida}")

        while True:
            n_actual = n_inicial + (iteracion - 1) * incremento
            print(f"\n--- Iteración {iteracion}: {n_actual} nodos ---")

            grafo = Grafo(n_actual, prob)
            grafo.generar()
            grafo.recorrer_heuristico()
            
            # Guardar resultados DESPUÉS de ejecutar
            guardar_resultado(grafo, "heuristico", archivo_salida)

            tiempo_transcurrido = time.time() - tiempo_inicio
            
            if tiempo_transcurrido > duracion_maxima:
                print(f"\n⏰ Tiempo máximo alcanzado ({duracion_maxima}s). Finalizando.")
                break
            else:
                restante = duracion_maxima - tiempo_transcurrido
                print(f"⏳ Tiempo acumulado: {tiempo_transcurrido:.2f}s / {duracion_maxima}s")
                print(f"   Tiempo restante: {restante:.2f}s ({restante/60:.1f} min)")
            
            iteracion += 1

        print(f"\n✅ Experimentación finalizada.")
        print(f"   • Iteraciones completadas: {iteracion}")
        print(f"   • Tiempo total: {tiempo_transcurrido:.2f}s")
        print(f"   • Resultados guardados en: '{archivo_salida}'")
        
        # Preguntar si quiere graficar
        preguntar_graficar(
            mensaje="¿Quieres graficar resultados de ESCALABILIDAD del heurístico (Punto 7)?",
            funcion_graficar=lambda: __import__('utils').graficar_resultados(archivo_salida)
        )

    @staticmethod
    def recorrer_comparacion(limpiar_anterior=False):
        """
        PUNTO 6: Ejecuta AMBOS algoritmos sobre los MISMOS grafos.
        Usa tamaños fijos: 200, 600, 1000, 1500 nodos con probabilidad 0.3
        
        Args:
            limpiar_anterior: si True, borra el archivo anterior antes de empezar
        """
        from utils import guardar_comparacion, preguntar_graficar
        import os
        
        archivo_salida = "comparacion_metodos.txt"
        
        # Limpiar archivo anterior si se solicita
        if limpiar_anterior and os.path.exists(archivo_salida):
            os.remove(archivo_salida)
            print(f"🗑️  Archivo anterior eliminado: {archivo_salida}")
        
        print("\n" + "="*60)
        print("PUNTO 6: COMPARACIÓN - Exacto vs Heurístico")
        print("="*60)
        
        # Grafos a recorrer
        tamaños = [200, 600, 1000, 1500]
        prob = 0.3
        
        print(f"\n⚙️  Configuración:")
        print(f"   • Tamaños a probar: {tamaños}")
        print(f"   • Probabilidad: {prob}")
        print(f"   • Archivo de salida: {archivo_salida}")
        print("\n⚠️  IMPORTANTE: Se ejecutarán AMBOS algoritmos sobre los MISMOS grafos\n")
        
        # Crear encabezado del archivo si no existe o se limpió
        if not os.path.exists(archivo_salida):
            with open(archivo_salida, "w", encoding="utf-8") as f:
                f.write("="*70 + "\n")
                f.write("COMPARACIÓN: Algoritmo EXACTO vs HEURÍSTICO\n")
                f.write(f"Tamaños: {tamaños}\n")
                f.write(f"Probabilidad: {prob}\n")
                f.write("="*70 + "\n\n")
        
        for idx, n in enumerate(tamaños, 1):
            print(f"\n{'='*60}")
            print(f"Caso {idx}/{len(tamaños)}: {n} nodos")
            print(f"{'='*60}")
            
            # 1. Generar el grafo UNA SOLA VEZ
            print(f"\n📊 Generando grafo de {n} nodos...")
            grafo_base = Grafo(n, prob)
            grafo_base.generar()
            
            # 2. EJECUTAR ALGORITMO EXACTO
            print("\n🔴 Ejecutando algoritmo EXACTO...")
            grafo_exacto = Grafo(n, prob)
            grafo_exacto.copiar_grafo(grafo_base)
            grafo_exacto.recorrer_exacto()
            
            tamaño_exacto = len(grafo_exacto.clique_maximo)
            tiempo_exacto = grafo_exacto.tiempo
            
            # 3. EJECUTAR HEURÍSTICA
            print("\n🟢 Ejecutando HEURÍSTICA...")
            grafo_heuristico = Grafo(n, prob)
            grafo_heuristico.copiar_grafo(grafo_base)
            grafo_heuristico.recorrer_heuristico()
            
            tamaño_heuristico = len(grafo_heuristico.clique_maximo)
            tiempo_heuristico = grafo_heuristico.tiempo
            
            # 4. CALCULAR MÉTRICAS
            alcanzó_optimo = (tamaño_heuristico == tamaño_exacto)
            if tamaño_exacto > 0:
                error_relativo = ((tamaño_exacto - tamaño_heuristico) / tamaño_exacto) * 100
            else:
                error_relativo = 0
            
            speedup = tiempo_exacto / tiempo_heuristico if tiempo_heuristico > 0 else float('inf')
            
            # 5. GUARDAR RESULTADOS
            resultado = {
                'n': n,
                'probabilidad': prob,
                'aristas': len(grafo_base.G.edges),
                'exacto': {
                    'tamaño': tamaño_exacto,
                    'tiempo': tiempo_exacto,
                    'clique': grafo_exacto.clique_maximo
                },
                'heuristico': {
                    'tamaño': tamaño_heuristico,
                    'tiempo': tiempo_heuristico,
                    'clique': grafo_heuristico.clique_maximo
                },
                'alcanzó_optimo': alcanzó_optimo,
                'error_relativo': error_relativo,
                'speedup': speedup
            }
            
            guardar_comparacion(resultado, archivo_salida)
            
            # 6. MOSTRAR RESUMEN
            print(f"\n{'─'*60}")
            print(f"📊 RESUMEN COMPARATIVO:")
            print(f"{'─'*60}")
            print(f"   🔴 Exacto:     tamaño={tamaño_exacto:2d}, tiempo={tiempo_exacto:8.4f}s")
            print(f"   🟢 Heurístico: tamaño={tamaño_heuristico:2d}, tiempo={tiempo_heuristico:8.4f}s")
            print(f"{'─'*60}")
            print(f"   ¿Óptimo?: {'✓ SÍ' if alcanzó_optimo else '✗ NO'}")
            print(f"   Error: {error_relativo:.2f}%")
            print(f"   Speedup: {speedup:.2f}x más rápido")
            print(f"{'─'*60}")
        
        print(f"\n✅ Comparación completada.")
        print(f"   • Casos analizados: {len(tamaños)}")
        print(f"   • Resultados guardados en: '{archivo_salida}'")
        
        # Preguntar si quiere graficar
        preguntar_graficar(
            mensaje="¿Quieres graficar la COMPARACIÓN (Punto 6)?",
            funcion_graficar=lambda: __import__('utils').graficar_comparacion(archivo_salida)
        )