
from utils.cargador_csv import (
    cargar_cursos,
    cargar_docentes,
    cargar_salones,
    cargar_relacion_docente_curso
)

from utils.exportador_csv import exportar_horario_csv
from utils.exportador_pdf import exportar_horario_pdf

from poblacion import Poblacion

from utils.grafica_aptitud import graficar_aptitudes

# Lista de horarios posibles en bloques de 50 minutos
HORARIOS_DISPONIBLES = [
    "13:40", "14:30", "15:20", "16:10", "17:00",
    "17:50", "18:40", "19:30", "20:20"
]

def main():
    # Cargar datos base
    cursos = cargar_cursos("data/curso.csv")
    docentes = cargar_docentes("data/docente.csv")
    salones = cargar_salones("data/salon.csv")
    relacion = cargar_relacion_docente_curso("data/docente_curso.csv")

    # Inicializar población
    poblacion = Poblacion(
        size=10,
        cursos=cursos,
        salones=salones,
        docentes=docentes,
        relacion_docente_curso=relacion,
        horarios_disponibles=HORARIOS_DISPONIBLES
    )

    print("=> Evolución del algoritmo genético:\n")

    for gen in range(5):
        poblacion.evolucionar(generaciones=1)
        mejor = poblacion.mejor_individuo
        print(f"Generación {gen + 1}: Mejor aptitud = {mejor.aptitud:.2f}")

    print("\n=> Asignaciones del mejor individuo final:")
    for codigo, (salon, horario, docente) in poblacion.mejor_individuo.asignaciones.items():
        print(f"Curso {codigo} → Salón: {salon.nombre}, Hora: {horario}, Docente: {docente.nombre if docente else 'No asignado'}")

    # Mejor Horario
    print("\n=> Exportaciones del Mejor Horario final")
    # Exportar CSV
    exportar_horario_csv("exports/csv/mejor_horario.csv", poblacion.mejor_individuo, cursos)
    # Exportar PDF
    exportar_horario_pdf("exports/pdf/mejor_horario.pdf", poblacion.mejor_individuo, cursos)
    
    # Evolucion de Aptitud
    print("\n=> Exportación de Grafica de Aptitud final")
    # Exportar PNG
    graficar_aptitudes("exports/graficas/evolucion_aptitud.png", poblacion.mejores_aptitudes)

if __name__ == "__main__":
    main()
