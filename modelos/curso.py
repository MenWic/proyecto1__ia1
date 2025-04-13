
class Curso:
    def __init__(self, nombre: str, codigo: str, carrera: str, semestre: int, seccion: str, tipo: str):
        self.nombre = nombre
        self.codigo = codigo
        self.carrera = carrera
        self.semestre = semestre
        self.seccion = seccion
        self.tipo = tipo  # 'obligatorio' u 'optativo'

    def __repr__(self):
        return f"<Curso {self.codigo} - {self.nombre}>"
