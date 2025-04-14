
import json
import os
from pprint import pprint

def exportar_resultado_final(nombre_archivo: str, resultado: dict):
    """
    Exporta el resumen final del algoritmo genético como archivo JSON.
    También lo muestra en consola de forma legible.
    """
    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

    # Exportar a JSON
    with open(nombre_archivo, "w") as f:
        json.dump(resultado, f, indent=4)

    # Mostrar en consola
    print(f"Resumen de resultados (del Individuo Final) exportado exitosamente como JSON: {nombre_archivo}")

