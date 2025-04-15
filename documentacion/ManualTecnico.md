# Manual Técnico del Proyecto - Generador de Horarios (IA1)

## Información General
**Nombre del Proyecto:** Generador de Horarios Asistido por IA (Algoritmo Genético)  
**Curso:** Inteligencia Artificial 1  
**Semestre:** 9° Semestre  
**Centro:** CUNOC - USAC  
**Desarrollador:** Luis Alejandro Méndez Rivera  

---

## Descripción del Proyecto
Este sistema tiene como objetivo generar horarios académicos óptimos mediante el uso de un **algoritmo genético**, respetando restricciones y maximizando la continuidad de clases. Fue desarrollado para su uso tanto por línea de comandos (**CLI**) como mediante una interfaz gráfica (**GUI**) construida en PyQt5.

---

## Tecnologías y Herramientas Utilizadas
- **Lenguaje:** Python 3.12
- **Librerías principales:**
  - `PyQt5`: GUI
  - `pandas`: manejo de CSV
  - `matplotlib`: generación de gráficas
  - `fitz (PyMuPDF)`: generación de PDF
  - `tracemalloc` y `time`: mediciones de rendimiento
  - `csv`, `random`, `collections`
- **Empaquetador:** PyInstaller 6.12.0

---

## Estructura del Proyecto
```plaintext
proyecto_ia1/
├── interface/              # Archivos de interfaz PyQt5 (GUI)
│   ├── app.py              # Ventana principal y lógica de GUI
│   ├── runner.py           # Llama al algoritmo genético y captura resultados
│   └── dialogs/            # Diálogos personalizados (restricciones)
├── utils/                  # Módulos de apoyo
│   ├── cargador_csv.py     # Carga y parseo de archivos CSV
│   ├── exportador_csv.py   # Exportación de horarios en CSV
│   ├── exportador_pdf.py   # Exportación de horarios en PDF
│   ├── grafica_aptitud.py  # Generación de gráfica de aptitud
│   ├── grafica_conflictos.py
│   ├── grafica_continuidad.py
│   └── exportador_resultado.py
├── modelos/                # Clases para representar datos
│   ├── curso.py, docente.py, salon.py
├── individuo.py            # Lógica de un individuo del algoritmo genético
├── poblacion.py            # Lógica de la población y operadores genéticos
├── algoritmo_genetico.py   # Orquestador (modo CLI)
├── main.py                 # Entrada principal para CLI
├── documentacion/
│   ├── README.md
│   ├── ManualTecnico.md
│   └── ManualUsuario.md
└── data/                   # Datos de prueba en CSV
```

---

## Flujo de Ejecución (Resumen General)

### 1. Entrada de Datos
- Desde **GUI:**
  - Se seleccionan archivos CSV desde la pestaña "Cargar CSV".
  - Se permite agregar restricciones manuales **curso → salón**.
  - Se configuran parámetros: tamaño de población, generaciones, modo de ejecución.
- Desde **CLI:**
  - El archivo `main.py` llama directamente al algoritmo genético con configuraciones internas o pasadas por terminal.

### 2. Generación de Población Inicial
El archivo `poblacion.py` instancia varios objetos `Individuo`, cada uno con asignaciones aleatorias respetando:
- Relación curso-docente
- Horarios disponibles
- Salones disponibles
- Restricciones **fijas curso → salón** (si existen)

### 3. Evolución Genética
En cada generación:
- Se seleccionan padres (torneo)
- Se genera un nuevo individuo (cruce)
- Se aplica mutación con probabilidad ajustable
- Se calcula la aptitud del individuo según:
  - Conflictos penalizados: solapamiento, sin docente, fuera de horario
  - Bonos por continuidad de clases (bloques de 50 minutos por semestre)

### 4. Finalización del Algoritmo
El proceso termina al cumplir:
- Alcanzar la aptitud deseada (modo 1)
- Llegar al número de generaciones (modo 2)
- Alcanzar nivel deseado dentro de un máximo de generaciones (modo 3)

### 5. Exportación de Resultados
- `mejor_horario.csv` y `mejor_horario.pdf`
- JSON con resumen de resultados (`resumen_resultado.json`)
- PNGs con gráficas: evolución de aptitud, conflictos por generación y continuidad por semestre

---

## Recomendaciones para Empaquetado
- Crear ejecutable con PyInstaller (versión funcional confirmada):
```bash
pyinstaller app.spec
```
- El archivo `app.spec` incluye todas las carpetas, submódulos y archivos .py requeridos

---

## Referencias
- [Manual del Usuario](./ManualUsuario.md)
- [README Principal](../README.md)

