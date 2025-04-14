import matplotlib.pyplot as plt
import os

def graficar_conflictos_por_generacion(nombre_archivo: str, conflicts_history: list[int]):
    plt.figure(figsize=(10, 5))
    plt.plot(conflicts_history, marker='o', linestyle='-', color='red')
    plt.title("Evolución de Conflictos por Generación")
    plt.xlabel("Generación")
    plt.ylabel("Número de Conflictos")
    plt.grid(True)
    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
    plt.savefig(nombre_archivo)
    plt.close()
    print(f"Grafica de Evolución de Conflictos exportada exitosamente como PNG: {nombre_archivo}")

