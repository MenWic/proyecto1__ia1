
from poblacion import Poblacion

# Este módulo sirve como orquestador del algoritmo genético.
# Define funciones auxiliares si se necesitan en el futuro,
# y centraliza la lógica de evolución de poblaciones.

class AlgoritmoGenetico:
    def __init__(self, cursos, salones, docentes, relacion_docente_curso, horarios_disponibles):
        self.cursos = cursos
        self.salones = salones
        self.docentes = docentes
        self.relacion_docente_curso = relacion_docente_curso
        self.horarios_disponibles = horarios_disponibles

    def evolucionar(self, generaciones=5, tamano_poblacion=40, elitismo=2):
        poblacion = Poblacion(tamano_poblacion, self.cursos, self.salones, self.docentes, self.relacion_docente_curso, self.horarios_disponibles)
        poblacion.inicializar()

        for generacion in range(generaciones):
            nueva_generacion = []

            # Elitismo: mantener los mejores 'elitismo' individuos
            elites = sorted(poblacion.individuos, key=lambda ind: ind.aptitud, reverse=True)[:elitismo]
            nueva_generacion.extend(elites)

            while len(nueva_generacion) < tamano_poblacion:
                padre1 = poblacion.seleccionar()
                padre2 = poblacion.seleccionar()
                hijo = padre1.cruzar(padre2)
                hijo.mutar()
                nueva_generacion.append(hijo)

            poblacion.individuos = nueva_generacion
            mejor = max(poblacion.individuos, key=lambda ind: ind.aptitud)
            print(f"Generación {generacion + 1}: Mejor aptitud = {mejor.aptitud:.2f}")

        return max(poblacion.individuos, key=lambda ind: ind.aptitud)
