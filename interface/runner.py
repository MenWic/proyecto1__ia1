from utils.cargador_csv import cargar_cursos, cargar_docentes, cargar_salones, cargar_relacion_docente_curso
from utils.exportador_csv import exportar_horario_csv
from utils.exportador_pdf import exportar_horario_pdf
from utils.grafica_aptitud import graficar_aptitudes
from utils.grafica_conflictos import graficar_conflictos_por_generacion
from utils.exportador_resultado import exportar_resultado_final
from utils.grafica_continuidad import graficar_continuidad_por_semestre
from poblacion import Poblacion
from time import time
import tracemalloc

def ejecutar_algoritmo(path_cursos, path_docentes, path_relacion, path_salones, poblacion_size=10, generaciones_max=250, aptitud_objetivo=125, modo=1, restricciones: dict[str, str] = None):    
    # Cargar los datos
    logs = []  # Asegúrate de que logs esté definido antes de usarlo
    cursos = cargar_cursos(path_cursos)
    docentes = cargar_docentes(path_docentes)
    salones = cargar_salones(path_salones)
    relacion = cargar_relacion_docente_curso(path_relacion)
    horarios = ["13:40", "14:30", "15:20", "16:10", "17:00", "17:50", "18:40", "19:30", "20:20"]
    
    # Verificar las restricciones recibidas
    if restricciones:
        logs.append(f"Restricciones manuales pasadas: {restricciones}")
    else:
        logs.append("No se han pasado restricciones manuales.")
    
    # Conversión de lista (Asi se usa en GUI) a dict (Asi se espera en CLI)
    restricciones_dict = dict(restricciones) if restricciones else {}
        
    # Población
    poblacion = Poblacion(
        size=poblacion_size,
        cursos=cursos,
        salones=salones,
        docentes=docentes,
        relacion_docente_curso=relacion,
        horarios_disponibles=horarios,
        imprimir_diagnostico=False,
        asignaciones_fijas=restricciones_dict   # Aquí pasamos las restricciones a Poblacion
    )

    logs.append("[INFO] Población inicializada.")
    poblacion.inicializar()
    conflicts_history = []
    generacion_final = 0

    tracemalloc.start()
    start_time = time()

    for gen in range(generaciones_max):
        poblacion.evolucionar(generaciones=1)
        mejor = poblacion.mejor_individuo
        logs.append(f"[GEN {gen + 1}] Aptitud: {mejor.aptitud:.2f}")
        generacion_final = gen + 1
        conflictos = mejor.calcular_conflictos()
        conflicts_history.append(conflictos)

        if modo == 1 and mejor.aptitud >= aptitud_objetivo:
            logs.append(f"[OK] Aptitud objetivo alcanzada en la generación {gen + 1}")
            break
        elif modo == 2 and gen + 1 >= generaciones_max:
            logs.append("[OK] Límite de generaciones alcanzado.")
            break
        elif modo == 3 and mejor.aptitud >= aptitud_objetivo:
            logs.append(f"[OK] Aptitud objetivo alcanzada en la generación {gen + 1}")
            break

    end_time = time()
    duracion = end_time - start_time
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    mejor = poblacion.mejor_individuo
    mejor.imprimir_diagnostico = True
    mejor.calcular_aptitud()

    logs.append("\n[Diagnóstico del individuo]")
    logs.append(f"- Conflictos sin docente: {mejor.diagnostico_conflictos['sin_docente']}")
    logs.append(f"- Conflictos docente solapado: {mejor.diagnostico_conflictos['docente_solapado']}")
    logs.append(f"- Conflictos fuera horario: {mejor.diagnostico_conflictos['fuera_horario']}")
    logs.append(f"- Conflictos curso obligatorio traslapado: {mejor.diagnostico_conflictos['curso_obligatorio_traslapado']}")
    logs.append(f"- Bonificaciones por continuidad: {mejor.diagnostico_bonos}")
    logs.append(f"- Aptitud final: {mejor.aptitud}")

    continuidad_por_semestre, continuidad_global = mejor.medir_porcentaje_continuidad_por_semestre()

    resultado_final = {
        "generacion_final": generacion_final,
        "aptitud_final": mejor.aptitud,
        "conflictos_finales": mejor.calcular_conflictos(),
        "duracion_segundos": round(duracion, 2),
        "continuidad_global": continuidad_global,
        "continuidad_por_semestre": continuidad_por_semestre,
        "memoria_actual_MB": round(current_mem / (1024 * 1024), 2),
        "memoria_pico_MB": round(peak_mem / (1024 * 1024), 2)
    }

    exportar_horario_csv("exports/csv/mejor_horario.csv", mejor, cursos)
    logs.append("Horario exportado exitosamente como CSV: exports/csv/mejor_horario.csv")

    exportar_horario_pdf("exports/pdf/mejor_horario.pdf", mejor, cursos)
    logs.append("Horario exportado exitosamente como PDF: exports/pdf/mejor_horario.pdf")

    graficar_aptitudes("exports/graficas/evolucion_aptitud.png", poblacion.mejores_aptitudes)
    logs.append("Grafica de Evolución de Aptitud exportada exitosamente como PNG: exports/graficas/evolucion_aptitud.png")

    graficar_conflictos_por_generacion("exports/graficas/conflictos_por_generacion.png", conflicts_history)
    logs.append("Grafica de Evolución de Conflictos exportada exitosamente como PNG: exports/graficas/conflictos_por_generacion.png")

    exportar_resultado_final("exports/resultados/resumen_resultado.json", resultado_final)
    logs.append("Resumen de resultados (del Individuo Final) exportado exitosamente como JSON: exports/resultados/resumen_resultado.json")

    graficar_continuidad_por_semestre("exports/graficas/continuidad_por_semestre.png", continuidad_por_semestre, continuidad_global)
    logs.append("Gráfica de continuidad exportada como PNG: exports/graficas/continuidad_por_semestre.png")

    logs.append("[SUCCESS] Ejecución finalizada.")
    return logs, resultado_final
