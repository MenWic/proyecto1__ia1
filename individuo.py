
from modelos.curso import Curso
from modelos.docente import Docente
from modelos.salon import Salon
import random
from collections import defaultdict

class Individuo:
    def __init__(self, cursos: list[Curso], salones: list[Salon], docentes: list[Docente], relacion_docente_curso: dict[str, list[str]], horarios_disponibles: list[str], imprimir_diagnostico: bool):
        self.cursos = cursos
        self.salones = salones
        self.docentes = docentes
        self.relacion_docente_curso = relacion_docente_curso
        self.horarios_disponibles = horarios_disponibles
        self.imprimir_diagnostico = imprimir_diagnostico

        self.asignaciones: dict[str, tuple[Salon, str, Docente]] = {}
        self.aptitud: float = 0.0

        self.generar_asignacion_prioritaria()
        # self.calcular_aptitud()

    def generar_asignacion_prioritaria(self):
        ocupacion_docente = defaultdict(set)  # (registro_docente) -> set(horarios)
        cursos_prioritarios = []

        for curso in self.cursos:
            docentes_posibles = self.relacion_docente_curso.get(curso.codigo, [])
            prioridad = len(docentes_posibles)
            cursos_prioritarios.append((prioridad, curso.tipo, random.random(), curso))

        cursos_ordenados = sorted(cursos_prioritarios, key=lambda x: (x[0], 0 if x[1] == "obligatorio" else 1, x[2]))

        horarios_disponibles = list(self.horarios_disponibles)
        random.shuffle(horarios_disponibles)

        for _, _, _, curso in cursos_ordenados:
            docentes_validos = [
                d for d in self.docentes
                if curso.codigo in self.relacion_docente_curso.get(d.registro, [])
            ]

            random.shuffle(docentes_validos)
            horario_asignado = None
            docente_asignado = None

            for d in docentes_validos:
                horarios_libres = [
                    h for h in horarios_disponibles
                    if d.hora_entrada.strftime("%H:%M") <= h <= d.hora_salida.strftime("%H:%M")
                    and h not in ocupacion_docente[d.registro]
                ]

                if horarios_libres:
                    horario_asignado = sorted(horarios_libres)[0]  # más temprano disponible
                    docente_asignado = d
                    ocupacion_docente[d.registro].add(horario_asignado)
                    break

            salon = random.choice(self.salones)
            if docente_asignado and horario_asignado:
                self.asignaciones[curso.codigo] = (salon, horario_asignado, docente_asignado)
            else:
                self.asignaciones[curso.codigo] = (salon, random.choice(self.horarios_disponibles), None)

    def calcular_aptitud(self):
        conflictos = 0
        bonificaciones = 0

        conteo_conflictos = {
            "sin_docente": 0,
            "docente_solapado": 0,
            "fuera_horario": 0,
            "curso_obligatorio_traslapado": 0
        }

        horario_docente = {}
        horario_semestre = {}

        for curso in self.cursos:
            cod = curso.codigo
            asignacion = self.asignaciones.get(cod)

            if not asignacion:
                conteo_conflictos["sin_docente"] += 1
                conflictos += 5
                continue

            salon, horario, docente = asignacion

            if docente is None:
                conteo_conflictos["sin_docente"] += 1
                conflictos += 5
                continue

            key_doc_hora = (docente.registro, horario)
            if key_doc_hora in horario_docente:
                conteo_conflictos["docente_solapado"] += 1
                conflictos += 3
            else:
                horario_docente[key_doc_hora] = cod

            if not (docente.hora_entrada.strftime("%H:%M") <= horario <= docente.hora_salida.strftime("%H:%M")):
                conteo_conflictos["fuera_horario"] += 1
                conflictos += 3

            if curso.tipo == "obligatorio":
                key_sem_hora = (curso.carrera, curso.semestre, horario)
                if key_sem_hora in horario_semestre:
                    conteo_conflictos["curso_obligatorio_traslapado"] += 1
                    conflictos += 4
                else:
                    horario_semestre[key_sem_hora] = cod

        grupos = defaultdict(list)
        for curso in self.cursos:
            cod = curso.codigo
            _, horario, _ = self.asignaciones.get(cod, (None, None, None))
            if horario:
                grupos[(curso.carrera, curso.semestre)].append(horario)

        horario_a_minuto = lambda h: int(h[:2]) * 60 + int(h[3:])

        for lista_horas in grupos.values():
            horas = sorted([horario_a_minuto(h) for h in lista_horas])
            for i in range(1, len(horas)):
                if horas[i] - horas[i - 1] == 50:
                    bonificaciones += 1

        base = 100 - conflictos + bonificaciones
        self.aptitud = max(0.1, base)
        
        if self.imprimir_diagnostico:
            print("\n[Diagnóstico del individuo]")
            for k, v in conteo_conflictos.items():
                print(f"- Conflictos {k.replace('_', ' ')}: {v}")
            print(f"- Bonificaciones por continuidad: {bonificaciones}")
            print(f"- Aptitud final: {self.aptitud}")
