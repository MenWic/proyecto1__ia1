
from datetime import time

class Docente:
    def __init__(self, nombre: str, registro: str, hora_entrada: time, hora_salida: time):
        self.nombre = nombre
        self.registro = registro
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida

    def __repr__(self):
        return f"<Docente {self.registro} - {self.nombre}>"
