
import csv
from modelos.curso import Curso
from modelos.docente import Docente
from modelos.salon import Salon
from datetime import datetime

def cargar_cursos(path: str) -> list[Curso]:
    cursos = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            curso = Curso(
                nombre=row["nombre"],
                codigo=str(row["codigo"]),
                carrera=row["carrera"],
                semestre=int(row["semestre"]),
                seccion=row["seccion"],
                tipo=row["tipo"].lower().strip()
            )
            cursos.append(curso)
    return cursos

def cargar_docentes(path: str) -> list[Docente]:
    docentes = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            docente = Docente(
                nombre=row["nombre"],
                registro=row["registro"],
                hora_entrada=datetime.strptime(row["hora_entrada"], "%H:%M").time(),
                hora_salida=datetime.strptime(row["hora_salida"], "%H:%M").time()
            )
            docentes.append(docente)
    return docentes

def cargar_salones(path: str) -> list[Salon]:
    salones = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            salon = Salon(
                id_salon=row["id"],
                nombre=row["nombre"]
            )
            salones.append(salon)
    return salones

def cargar_relacion_docente_curso(path: str) -> dict[str, list[str]]:
    relacion = {}
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            registro = row["registro"]
            codigo = str(row["codigo"])
            if registro not in relacion:
                relacion[registro] = []
            relacion[registro].append(codigo)
    return relacion
