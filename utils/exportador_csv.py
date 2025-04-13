
import csv
from modelos.curso import Curso
from modelos.docente import Docente
from modelos.salon import Salon
from individuo import Individuo

def exportar_horario_csv(nombre_archivo: str, individuo: Individuo, cursos: list[Curso]):
    cursos_por_codigo = {c.codigo: c for c in cursos}

    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Código", "Nombre", "Carrera", "Semestre", "Sección", "Tipo", "Salón", "Horario", "Docente"])

        for codigo, (salon, horario, docente) in individuo.asignaciones.items():
            curso = cursos_por_codigo[codigo]
            writer.writerow([
                curso.codigo,
                curso.nombre,
                curso.carrera,
                curso.semestre,
                curso.seccion,
                curso.tipo,
                salon.nombre,
                horario,
                docente.nombre if docente else "No asignado"
            ])
            
    print(f"Horario exportado exitosamente como CSV: {nombre_archivo}")

