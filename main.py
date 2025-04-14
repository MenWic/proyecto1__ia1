
def main():
    from time import time
    from utils.cargador_csv import (
        cargar_cursos,
        cargar_docentes,
        cargar_salones,
        cargar_relacion_docente_curso
    )
    from utils.exportador_csv import exportar_horario_csv
    from utils.exportador_pdf import exportar_horario_pdf
    from utils.grafica_aptitud import graficar_aptitudes
    from poblacion import Poblacion

    HORARIOS_DISPONIBLES = [
        "13:40", "14:30", "15:20", "16:10", "17:00",
        "17:50", "18:40", "19:30", "20:20"
    ]

    cursos = cargar_cursos("data/curso.csv")
    docentes = cargar_docentes("data/docente.csv")
    salones = cargar_salones("data/salon.csv")
    relacion = cargar_relacion_docente_curso("data/docente_curso.csv")
    
    poblacion = Poblacion(
        size=10,
        cursos=cursos,
        salones=salones,
        docentes=docentes,
        relacion_docente_curso=relacion,
        horarios_disponibles=HORARIOS_DISPONIBLES,
        imprimir_diagnostico=0 # TRUE = Impresión por defecto
    )
    
    print("\nSeleccione el criterio de finalización:")
    print("1. Ejecutar con configuración por defecto (aptitud 110 o hasta 50 generaciones)")
    print("2. Ejecutar hasta alcanzar una aptitud específica")
    print("3. Ejecutar hasta una cantidad máxima de generaciones")

    opcion = ""
    while opcion not in {"1", "2", "3"}:
        opcion = input("Opción (1/2/3): ").strip()
        if opcion not in {"1", "2", "3"}:
            print("Opción no válida. Por favor, elija una opción válida (1, 2 o 3).\n")

    # Parametros de configuracion para el ALgoritmo Genetico
    aptitud_objetivo = 120
    max_generaciones = 50

    if opcion == "2":
        while True:
            entrada = input("Ingrese la aptitud objetivo deseada (1 - 120): ").strip()
            try:
                valor = float(entrada)
                # Rango de aptitud definido
                if 1 <= valor <= 120:
                    aptitud_objetivo = valor
                    break
                else:
                    print("El valor debe estar entre 1 y 120.")
            except ValueError:
                print("Ingrese un número válido.")

    elif opcion == "3":
        while True:
            entrada = input("Ingrese el número máximo de generaciones (1 - 150): ").strip()
            try:
                valor = int(entrada)
                # Rango de max. de generaciones definido
                if 1 <= valor <= 150:
                    max_generaciones = valor
                    break
                else:
                    print("El valor debe estar entre 1 y 150.")
            except ValueError:
                print("Ingrese un número entero válido.")

    # SE INICIALIZA LA POBLACIÓN CON CÁLCULO DE APTITUD
    poblacion.inicializar()
    
    print("\n=> Evolución del algoritmo genético:\n")
    start_time = time()

    for gen in range(max_generaciones):
        poblacion.evolucionar(generaciones=1)
        mejor = poblacion.mejor_individuo
        print(f"Generación {gen + 1}: Mejor aptitud = {mejor.aptitud:.2f}")
        if mejor.aptitud >= aptitud_objetivo:
            print(f"\nAptitud objetivo alcanzada en la generación {gen + 1}")
            break

    end_time = time()
    duracion = end_time - start_time

    print("\n=> Asignaciones del mejor individuo final:")
    for codigo, (salon, horario, docente) in poblacion.mejor_individuo.asignaciones.items():
        print(f"Curso {codigo} → Salón: {salon.nombre}, Hora: {horario}, Docente: {docente.nombre if docente else 'No asignado'}")

    print("\n=> Exportaciones del Mejor Horario final")
    exportar_horario_csv("exports/csv/mejor_horario.csv", poblacion.mejor_individuo, cursos)
    exportar_horario_pdf("exports/pdf/mejor_horario.pdf", poblacion.mejor_individuo, cursos)

    print("\n=> Exportación de Grafica de Aptitud final")
    graficar_aptitudes("exports/graficas/evolucion_aptitud.png", poblacion.mejores_aptitudes)

    print(f"\nDuración total del algoritmo: {duracion:.2f} segundos")

if __name__ == "__main__":
    main()
