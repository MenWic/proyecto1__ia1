
from individuo import Individuo
import random

class Poblacion:
    def inicializar(self):
        for individuo in self.individuos:
            individuo.calcular_aptitud()
        self.mejor_individuo = max(self.individuos, key=lambda ind: ind.aptitud)
        self.mejor_aptitud_historica = self.mejor_individuo.aptitud
        
    def __init__(self, size: int, cursos, salones, docentes, relacion_docente_curso, horarios_disponibles, imprimir_diagnostico=True, asignaciones_fijas=None):
        self.size = size
        self.cursos = cursos
        self.salones = salones
        self.docentes = docentes
        self.relacion_docente_curso = relacion_docente_curso
        self.horarios_disponibles = horarios_disponibles
        self.imprimir_diagnostico = imprimir_diagnostico
        self.asignaciones_fijas = asignaciones_fijas or {}
        
        self.mejores_aptitudes: list[float] = []
        self.individuos: list[Individuo] = [
            Individuo(cursos, salones, docentes, relacion_docente_curso, horarios_disponibles, imprimir_diagnostico, asignaciones_fijas=self.asignaciones_fijas)
            for _ in range(size)
        ]
        self.mejor_individuo = None
        self.sin_mejora_consecutiva = 0
        self.mejor_aptitud_historica = 0

    def seleccionar_padres(self, torneo_base=3) -> tuple[Individuo, Individuo]:
        torneo_size = torneo_base + min(3, self.sin_mejora_consecutiva)

        def torneo():
            candidatos = random.sample(self.individuos, torneo_size)
            return max(candidatos, key=lambda ind: ind.aptitud)

        return torneo(), torneo()

    def evolucionar(self, generaciones: int, prob_mutacion_base=0.1):
        for _ in range(generaciones):
            nueva_generacion = []
            elite = self.mejor_individuo
            nueva_generacion.append(elite)

            prob_mutacion = min(0.5, prob_mutacion_base + self.sin_mejora_consecutiva * 0.05)

            while len(nueva_generacion) < self.size:
                padre1, padre2 = self.seleccionar_padres()
                hijo = self.cruzar(padre1, padre2)

                if random.random() < prob_mutacion:
                    self.mutar(hijo)

                hijo.calcular_aptitud()
                nueva_generacion.append(hijo)

            if self.sin_mejora_consecutiva >= 10:
                cantidad_reemplazo = int(0.3 * self.size)
                nuevos = [
                    Individuo(self.cursos, self.salones, self.docentes, self.relacion_docente_curso, self.horarios_disponibles, self.imprimir_diagnostico, self.asignaciones_fijas)
                    for _ in range(cantidad_reemplazo)
                ]
                nueva_generacion[-cantidad_reemplazo:] = nuevos

            self.individuos = nueva_generacion
            nuevo_mejor = max(self.individuos, key=lambda ind: ind.aptitud)

            if nuevo_mejor.aptitud > self.mejor_aptitud_historica:
                self.mejor_individuo = nuevo_mejor
                self.mejor_aptitud_historica = nuevo_mejor.aptitud
                self.sin_mejora_consecutiva = 0
            else:
                self.sin_mejora_consecutiva += 1
                self.mejores_aptitudes.append(self.mejor_individuo.aptitud)

    def cruzar(self, padre1: Individuo, padre2: Individuo) -> Individuo:
        hijo = Individuo(
            self.cursos, self.salones, self.docentes,
            self.relacion_docente_curso, self.horarios_disponibles,
            self.imprimir_diagnostico, asignaciones_fijas=self.asignaciones_fijas
        )
        # NO hacer .clear() para conservar las asignaciones fijas generadas

        horario_docente = {}

        for curso in self.cursos:
            cod = curso.codigo

            # Si el curso ya fue asignado con salón fijo en generar_asignacion_prioritaria(), lo dejamos
            if cod in self.asignaciones_fijas:
                continue

            # Si no tiene restricción, intentamos tomar mejor asignación entre los padres
            asign1 = padre1.asignaciones.get(cod)
            asign2 = padre2.asignaciones.get(cod)

            mejor = None
            for asign in [asign1, asign2]:
                if asign is None:
                    continue
                salon, horario, docente = asign
                if docente and docente.hora_entrada.strftime("%H:%M") <= horario <= docente.hora_salida.strftime("%H:%M"):
                    key = (docente.registro, horario)
                    if key not in horario_docente:
                        mejor = asign
                        horario_docente[key] = cod
                        break

            if mejor:
                hijo.asignaciones[cod] = mejor
            else:
                hijo.asignaciones[cod] = self._generar_asignacion_aleatoria(curso, horario_docente)

        # Verificación opcional: asegurarnos de que se cumplan las restricciones de salón
        for cod, salon_fijo in self.asignaciones_fijas.items():
            if cod in hijo.asignaciones:
                salon_asignado = hijo.asignaciones[cod][0].nombre
                if salon_asignado != salon_fijo:
                    print(f"!> RESTRICCIÓN NO CUMPLIDA: {cod} debería estar en {salon_fijo}, pero está en {salon_asignado}")

        return hijo

    def _generar_asignacion_aleatoria(self, curso, horario_docente=None):
        docentes_validos = [
            d for d in self.docentes if curso.codigo in self.relacion_docente_curso.get(d.registro, [])
        ]
        for _ in range(5):
            horario = random.choice(self.horarios_disponibles)
            docente = random.choice(docentes_validos) if docentes_validos else None
            if docente and docente.hora_entrada.strftime("%H:%M") <= horario <= docente.hora_salida.strftime("%H:%M"):
                if horario_docente and (docente.registro, horario) in horario_docente:
                    continue
                salon = random.choice(self.salones)
                return (salon, horario, docente)

        return (random.choice(self.salones), random.choice(self.horarios_disponibles), None)

    def mutar(self, individuo: Individuo):
        curso = random.choice(self.cursos)
        codigo = curso.codigo

        # Si el curso tiene restricción fija, NO se muta
        if codigo in self.asignaciones_fijas:
            return  # No tocar asignaciones fijas

        nuevo_salon = random.choice(individuo.salones)
        nuevo_horario = random.choice(individuo.horarios_disponibles)

        posibles_docentes = [
            d for d in individuo.docentes
            if codigo in self.relacion_docente_curso.get(d.registro, [])
            and d.hora_entrada.strftime("%H:%M") <= nuevo_horario <= d.hora_salida.strftime("%H:%M")
        ]

        for _ in range(5):
            nuevo_docente = random.choice(posibles_docentes) if posibles_docentes else None
            key = (nuevo_docente.registro, nuevo_horario) if nuevo_docente else None
            ocupado = any(
                key == (d.registro, h)
                for _, h, d in individuo.asignaciones.values()
                if d and h
            )
            if not ocupado:
                individuo.asignaciones[codigo] = (nuevo_salon, nuevo_horario, nuevo_docente)
                break
