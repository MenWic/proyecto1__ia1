
from modelos.curso import Curso
from modelos.salon import Salon
from modelos.docente import Docente

class Asignacion:
    def __init__(self, curso: Curso, salon: Salon, docente: Docente, horario: str):
        self.curso = curso
        self.salon = salon
        self.docente = docente
        self.horario = horario  # Ej: "14:30", "15:20", etc.

    def __repr__(self):
        return f"<Asignación {self.curso.codigo} - {self.horario} - {self.salon.nombre}>"
