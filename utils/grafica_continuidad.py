
import matplotlib.pyplot as plt
import os

def graficar_continuidad_por_semestre(nombre_archivo: str, continuidad_por_semestre: dict[str, float], continuidad_global: float):
    """
    Genera un gráfico de barras con el porcentaje de continuidad por semestre.
    También muestra el porcentaje global como una línea de referencia.
    """
    etiquetas = list(continuidad_por_semestre.keys())
    valores = list(continuidad_por_semestre.values())

    plt.figure(figsize=(12, 6))
    barras = plt.bar(etiquetas, valores)

    # Línea horizontal del porcentaje global
    plt.axhline(y=continuidad_global, color='green', linestyle='--', label=f'Continuidad Global: {continuidad_global:.2f}%')

    # Etiquetas y estilos
    plt.title("Porcentaje de Continuidad por Semestre")
    plt.ylabel("Continuidad (%)")
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.legend()

    # Etiquetas encima de cada barra
    for bar in barras:
        altura = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, altura + 2, f"{altura:.1f}%", ha='center', fontsize=9)

    # Guardar archivo
    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
    plt.tight_layout()
    plt.savefig(nombre_archivo)
    plt.close()

    print(f"Gráfica de continuidad exportada como PNG: {nombre_archivo}")
