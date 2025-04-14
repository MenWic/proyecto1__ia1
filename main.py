
def main():
    import tracemalloc
    from time import time
    from pprint import pprint

    from utils.cargador_csv import (
        cargar_cursos,
        cargar_docentes,
        cargar_salones,
        cargar_relacion_docente_curso
    )
    from utils.exportador_csv import exportar_horario_csv
    from utils.exportador_pdf import exportar_horario_pdf
    from utils.grafica_aptitud import graficar_aptitudes
    from utils.grafica_conflictos import graficar_conflictos_por_generacion
    from utils.exportador_resultado import exportar_resultado_final
    from utils.grafica_continuidad import graficar_continuidad_por_semestre

    from poblacion import Poblacion

    HORARIOS_DISPONIBLES = [
        "13:40", "14:30", "15:20", "16:10", "17:00",
        "17:50", "18:40", "19:30", "20:20"
    ]

    cursos = cargar_cursos("data/curso.csv")
    docentes = cargar_docentes("data/docente.csv")
    salones = cargar_salones("data/salon.csv")
    relacion = cargar_relacion_docente_curso("data/docente_curso.csv")
    generacion_final = 0
    conflicts_history = []

    
    poblacion = Poblacion(
        size=10,
        cursos=cursos,
        salones=salones,
        docentes=docentes,
        relacion_docente_curso=relacion,
        horarios_disponibles=HORARIOS_DISPONIBLES,
        imprimir_diagnostico=False # TRUE = Impresión por defecto
    )
    
    print("\nSeleccione el criterio de finalización:")
    print("1. Ejecutar con configuración por defecto (aptitud 125 o hasta 250 generaciones)")
    print("2. Ejecutar hasta alcanzar una aptitud específica")
    print("3. Ejecutar hasta una cantidad máxima de generaciones")

    opcion = ""
    while opcion not in {"1", "2", "3"}:
        opcion = input("Opción (1/2/3): ").strip()
        if opcion not in {"1", "2", "3"}:
            print("Opción no válida. Por favor, elija una opción válida (1, 2 o 3).\n")

    # Parametros de configuracion para el ALgoritmo Genetico
    aptitud_objetivo = 125 # 125 = Aprox.: 0 conflictos + bonus de continuidad
    max_generaciones = 250 # Limite alto de generaciones/intentos para mejores resultados de aptitud

    if opcion == "2":
        while True:
            entrada = input("Ingrese la aptitud objetivo deseada (1 - 125): ").strip()
            try:
                valor = float(entrada)
                # Rango de aptitud definido
                if 1 <= valor <= 125:
                    aptitud_objetivo = valor
                    break
                else:
                    print("El valor debe estar entre 1 y 125.")
            except ValueError:
                print("Ingrese un número válido.")

    elif opcion == "3":
        while True:
            entrada = input("Ingrese el número máximo de generaciones (1 - 250): ").strip()
            try:
                valor = int(entrada)
                # Rango de max. de generaciones definido
                if 1 <= valor <= 250:
                    max_generaciones = valor
                    break
                else:
                    print("El valor debe estar entre 1 y 250.")
            except ValueError:
                print("Ingrese un número entero válido.")

    # SE INICIALIZA LA POBLACIÓN CON CÁLCULO DE APTITUD
    poblacion.inicializar()
    
    print("\n=> Evolución del algoritmo genético:\n")
    tracemalloc.start() # COMENTAR (MEJORAR TIEMPO DE EJECUCION)
    start_time = time()

    for gen in range(max_generaciones):
        poblacion.evolucionar(generaciones=1)
        mejor = poblacion.mejor_individuo
        print(f"Generación {gen + 1}: Mejor aptitud = {mejor.aptitud:.2f}")
        generacion_final = gen + 1 # Guardar numero de ultima generacion
        conflictos_generacion = mejor.calcular_conflictos() # Hallar los conflictos del mejor individuo de la generacion actual
        conflicts_history.append(conflictos_generacion) # Guardar los conflictos del mejor individuo de la generacion actual
        
        if mejor.aptitud >= aptitud_objetivo: # aptitud_objetivo = o conflictos aprox.
            print(f"\nAptitud objetivo alcanzada en la generación {gen + 1}")
            break
        elif opcion == "3" and mejor.aptitud >= 125:
            print(f"\nIndividuo sin conflictos alcanzado en generación {gen + 1} (aptitud: {mejor.aptitud:.2f})")
            break
        elif gen == max_generaciones - 1:
            if opcion == "1":
                print(f"\n⚠ No se alcanzó la aptitud sin conflictos (≥125) en: {max_generaciones} generaciones (limite). Se muestra el último individuo encontrado (mejor posible por los limites).")
            elif opcion == "2":
                print(f"\n⚠ No se alcanzó la aptitud deseada: ({aptitud_objetivo}) en: {max_generaciones} generaciones. Se muestra el último individuo encontrado (mejor posible por los limites).")
            elif opcion == "3":
                print(f"\n⚠ No se encontró un individuo sin conflictos (≥125) en: {max_generaciones} generaciones (indicadas). Se muestra el último individuo encontrado (mejor posible por los limites).")

    end_time = time()
    duracion = end_time - start_time # Tiempo de ejecucion
    current_mem, peak_mem = tracemalloc.get_traced_memory() # COMENTAR (MEJORAR TIEMPO DE EJECUCION)
    tracemalloc.stop() # COMENTAR (MEJORAR TIEMPO DE EJECUCION)


    print("\n=> Asignaciones del mejor individuo final:")
    for codigo, (salon, horario, docente) in poblacion.mejor_individuo.asignaciones.items():
        print(f"Curso {codigo} → Salón: {salon.nombre}, Hora: {horario}, Docente: {docente.nombre if docente else 'No asignado'}")
        
    # Diagnóstico forzado del mejor individuo final
    print("\n[Diagnóstico final del mejor individuo]")
    poblacion.mejor_individuo.imprimir_diagnostico = True
    poblacion.mejor_individuo.calcular_aptitud()
    continuidad_por_semestre, continuidad_global = poblacion.mejor_individuo.medir_porcentaje_continuidad_por_semestre()

    
    resultado_final = {
        "generacion_final": generacion_final,
        "aptitud_final": poblacion.mejor_individuo.aptitud,
        "conflictos_finales": poblacion.mejor_individuo.calcular_conflictos(),
        "duracion_segundos": round(duracion, 2),
        "continuidad_global": continuidad_global,
        "continuidad_por_semestre": continuidad_por_semestre,
        "memoria_actual_MB": round(current_mem / (1024 * 1024), 2), # COMENTAR (MEJORAR TIEMPO DE EJECUCION)
        "memoria_pico_MB": round(peak_mem / (1024 * 1024), 2) # COMENTAR (MEJORAR TIEMPO DE EJECUCION)
    }

    print("\n=> Exportaciones del Mejor Horario final")
    exportar_horario_csv("exports/csv/mejor_horario.csv", poblacion.mejor_individuo, cursos)
    exportar_horario_pdf("exports/pdf/mejor_horario.pdf", poblacion.mejor_individuo, cursos)

    print("\n=> Exportación de Grafica de Aptitud final")
    graficar_aptitudes("exports/graficas/evolucion_aptitud.png", poblacion.mejores_aptitudes)
    
    print("\n=> Exportación de Gráfica de Conflictos por Generación")
    graficar_conflictos_por_generacion('exports/graficas/conflictos_por_generacion.png', conflicts_history)
    
    print("\n=> Exportación de Resumen Final (JSON)")
    exportar_resultado_final("exports/resultados/resumen_resultado.json", resultado_final)
    
    print("\n=> Exportación de Gráfica de Continuidad por Semestre")
    graficar_continuidad_por_semestre("exports/graficas/continuidad_por_semestre.png", continuidad_por_semestre, continuidad_global)

    print(f"\nDuración total del algoritmo: {duracion:.2f} segundos")

if __name__ == "__main__":
    main()
