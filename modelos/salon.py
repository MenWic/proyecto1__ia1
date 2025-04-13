
class Salon:
    def __init__(self, nombre: str, id_salon: str):
        self.nombre = nombre
        self.id = id_salon

    def __repr__(self):
        return f"<Salón {self.id} - {self.nombre}>"
