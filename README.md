# Generador de Horarios con Algoritmo Genético

Este proyecto implementa un sistema inteligente capaz de generar horarios académicos automáticamente utilizando algoritmos genéticos. Se desarrolló como parte del curso de **Inteligencia Artificial 1** del 9º semestre de la carrera de Ingeniería en Ciencias y Sistemas en el **Centro Universitario de Occidente (CUNOC)**, USAC.

## Descripción
La aplicación permite cargar información de cursos, docentes, relación docente-curso y salones desde archivos CSV, para posteriormente ejecutar un algoritmo genético que genera una asignación de horarios óptima, respetando restricciones como disponibilidad horaria, salones y relaciones docentes-cursos. El resultado se exporta en formatos CSV y PDF, y puede visualizarse desde una interfaz gráfica desarrollada con PyQt5.

## Herramientas y Tecnologías Utilizadas

- **Lenguaje principal:** Python 3.12
- **Interfaz gráfica:** PyQt5
- **Empaquetado:** PyInstaller
- **Visualización de gráficas:** matplotlib
- **Manipulación de datos:** pandas
- **Exportación PDF:** fitz (PyMuPDF)
- **Gestor de entorno:** venv (entorno virtual Python)

## Estructura del Proyecto
```
proyecto_ia1/
├── data/                   # Archivos CSV de entrada
├── interface/              # Interfaz gráfica PyQt
├── modelos/                # Definición de entidades Curso, Docente, Salón
├── utils/                  # Exportadores, cargadores y gráficas
├── exports/                # Resultados generados (CSV, PDF, gráficas)
├── documentacion/          # Documentos Markdown (ManualUsuario, ManualTecnico)
├── main.py                 # Ejecución desde consola (CLI)
├── app.spec                # Archivo de empaquetado para PyInstaller
├── README.md               # Este archivo
└── dist/                   # Ejecutable generado (.exe)
```

## Instalación y Dependencias

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv env

# Activar entorno en Windows
env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

> Asegúrate de tener Python >= 3.12 y pip correctamente configurado.

## Ejecución desde código fuente

### Modo Consola (CLI)
```bash
python main.py
```

### Modo Gráfico (GUI)
```bash
python -m interface.app
```

## Ejecución del Ejecutable

Se ha empaquetado un ejecutable funcional ubicado en el directorio:
```
dist/app/app.exe
```
Para ejecutar simplemente haz doble clic o ejecútalo desde PowerShell o CMD:
```bash
./dist/app/app.exe
```

## Documentación Complementaria

- [Manual Técnico](documentacion/ManualTecnico.md)
- [Manual de Usuario](documentacion/ManualUsuario.md)

---

## Autor del Proyecto

**Luis Alejandro Méndez Rivera**  
Registro Académico: 202030627  
9º semestre de Ingeniería en Ciencias y Sistemas  
Centro Universitario de Occidente - USAC  
[GitHub - @MenWic](https://github.com/MenWic/)

