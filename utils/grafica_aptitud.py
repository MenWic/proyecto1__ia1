import matplotlib.pyplot as plt

def graficar_aptitudes(nombre_archivo: str, mejores_aptitudes: list[float]):
    generaciones = list(range(1, len(mejores_aptitudes) + 1))
    plt.figure(figsize=(10, 5))
    plt.plot(generaciones, mejores_aptitudes, marker='o', linestyle='-', color='blue')
    plt.title("Evolución de la Aptitud del Mejor Individuo")
    plt.xlabel("Generación")
    plt.ylabel("Aptitud")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("exports/graficas/evolucion_aptitud.png")
    plt.show()
    print(f"Horario exportado exitosamente como PNG: {nombre_archivo}")
