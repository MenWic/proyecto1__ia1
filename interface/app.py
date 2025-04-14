import os
import sys
import csv
import webbrowser
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QTextEdit, QTabWidget, QFormLayout,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
    QRadioButton, QButtonGroup, QGroupBox
)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from interface.runner import ejecutar_algoritmo
from modelos.curso import Curso
from modelos.salon import Salon

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Horarios - IA1")
        self.setGeometry(100, 100, 900, 700)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.csv_tab = QWidget()
        self.csv_tab.setLayout(self.init_csv_tab())
        self.tabs.addTab(self.csv_tab, "Cargar CSV")
        
        self.data_tab = QWidget()
        self.data_tab_layout = QVBoxLayout()
        self.data_tab.setLayout(self.data_tab_layout)
        self.tabs.addTab(self.data_tab, "Datos")

        

        self.config_tab = QWidget()
        self.config_tab.setLayout(self.init_config_tab())
        self.tabs.addTab(self.config_tab, "Configuración")

        self.console_tab = QWidget()
        self.console_tab.setLayout(self.init_console_tab())
        self.tabs.addTab(self.console_tab, "Consola")

        self.results_tab = QWidget()
        self.results_tab.setLayout(self.init_results_tab())
        self.tabs.addTab(self.results_tab, "Resultados")

        self.reports_tab = QWidget()
        self.reports_tab.setLayout(self.init_reports_tab())
        self.tabs.addTab(self.reports_tab, "Reportes")

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.auto_set_csv_defaults()

    def init_csv_tab(self):
        layout = QFormLayout()
        self.csv_labels = {}

        for label in ["Cursos", "Docentes", "Relación Docente-Curso", "Salones"]:
            container = QHBoxLayout()

            le = QLineEdit()
            le.setReadOnly(True)
            le.setMaximumWidth(500)

            b = QPushButton("Seleccionar")
            b.setMaximumWidth(100)
            b.clicked.connect(lambda _, key=label, line=le: self.load_csv(key, line))

            container.addWidget(le)
            container.addWidget(b)
            layout.addRow(QLabel(label + ":"), container)

            self.csv_labels[label] = le
            
        # Botón para cargar y mostrar datos
        load_btn = QPushButton("Cargar datos")
        load_btn.clicked.connect(self.actualizar_pestania_datos)
        layout.addRow(load_btn)


        return layout
    
    # Nuevo
    def init_data_tab(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout()

        csv_files = {
            "Cursos": self.csv_labels["Cursos"].text(),
            "Docentes": self.csv_labels["Docentes"].text(),
            "Relación Docente-Curso": self.csv_labels["Relación Docente-Curso"].text(),
            "Salones": self.csv_labels["Salones"].text()
        }

        for titulo, path in csv_files.items():
            if not os.path.exists(path):
                continue

            df = pd.read_csv(path)

            label = QLabel(f"{titulo}")
            label.setStyleSheet("font-weight: bold; padding: 6px 0;")
            table = QTableWidget()
            table.setRowCount(len(df))
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels(df.columns)

            for row_idx, row in df.iterrows():
                for col_idx, val in enumerate(row):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

            container_layout.addWidget(label)
            container_layout.addWidget(table)

        container.setLayout(container_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def actualizar_pestania_datos(self):
        # Limpiar layout actual
        for i in reversed(range(self.data_tab_layout.count())):
            widget = self.data_tab_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        csv_files = {
            "Cursos": self.csv_labels["Cursos"].text(),
            "Docentes": self.csv_labels["Docentes"].text(),
            "Relación Docente-Curso": self.csv_labels["Relación Docente-Curso"].text(),
            "Salones": self.csv_labels["Salones"].text()
        }

        for titulo, path in csv_files.items():
            if not os.path.exists(path):
                continue

            df = pd.read_csv(path)

            label = QLabel(titulo)
            label.setStyleSheet("font-weight: bold; padding: 6px 0;")
            table = QTableWidget()
            table.setRowCount(len(df))
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels(df.columns)
            table.setEditTriggers(QTableWidget.AllEditTriggers)  # permite edición si quieres

            for row_idx, row in df.iterrows():
                for col_idx, val in enumerate(row):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

            self.data_tab_layout.addWidget(label)
            self.data_tab_layout.addWidget(table)


    def load_csv(self, label, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Seleccionar archivo CSV de {label}", "", "CSV Files (*.csv)")
        if file_path:
            line_edit.setText(file_path)
        self.data_tab.setLayout(self.init_data_tab().layout())  # Refrescar el contenido
    
    def init_config_tab(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignTop)
        form_layout.setSpacing(10)

        self.population_input = QLineEdit("10")
        self.population_input.setMaximumWidth(100)
        form_layout.addRow("Tamaño de población:", self.population_input)

        self.generations_input = QLineEdit("250")
        self.generations_input.setMaximumWidth(100)
        form_layout.addRow("Número de generaciones:", self.generations_input)

        self.fitness_input = QLineEdit("125")
        self.fitness_input.setMaximumWidth(100)
        form_layout.addRow("Aptitud objetivo:", self.fitness_input)
        
        # Radio buttons para elegir modo
        self.option_group = QButtonGroup()

        radio_box = QGroupBox("Modo de Ejecución")
        radio_layout = QVBoxLayout()

        self.option1 = QRadioButton("1. Aptitud objetivo (default)")
        self.option1.setChecked(True)  # Opción por defecto
        self.option2 = QRadioButton("2. Número máximo de generaciones definida (A menos que alcance antes la aptitud objetivo)")
        self.option3 = QRadioButton("3. Nivel de aptitud definido (Siempre que no sobrepase max. de generaciones)")

        self.option_group.addButton(self.option1, 1)
        self.option_group.addButton(self.option2, 2)
        self.option_group.addButton(self.option3, 3)

        radio_layout.addWidget(self.option1)
        radio_layout.addWidget(self.option2)
        radio_layout.addWidget(self.option3)

        radio_box.setLayout(radio_layout)
        layout.addWidget(radio_box)

        # Botón de Ejecutar
        self.start_button = QPushButton("Ejecutar Algoritmo")
        self.start_button.setMaximumWidth(150)
        self.start_button.clicked.connect(self.run_algorithm)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(130, 15, 0, 0)
        button_row.setAlignment(Qt.AlignLeft)
        button_row.addWidget(self.start_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_row)
        layout.addStretch()
        
        # Pestaña Restricciones: Restricciones Curso-Salón
        self.restricciones_label = QLabel("Restricciones Curso → Salón")
        self.restricciones_label.setStyleSheet("font-weight: bold;")

        self.restricciones_output = QTextEdit()
        self.restricciones_output.setPlaceholderText("Aquí se mostrarán las restricciones agregadas...")
        self.restricciones_output.setReadOnly(True)
        self.restricciones_output.setMaximumHeight(80)

        self.restricciones_data = []  # Lista de tuplas (codigo_curso, nombre_salon)

        # # Inputs para seleccionar restricción
        # self.curso_input = QLineEdit()
        # self.curso_input.setPlaceholderText("Código del curso (ej: C001)")
        # self.curso_input.setMaximumWidth(150)

        # self.salon_input = QLineEdit()
        # self.salon_input.setPlaceholderText("Nombre del salón (ej: Edificio G - Aula 103)")
        # self.salon_input.setMaximumWidth(250)

        # self.agregar_restriccion_btn = QPushButton("Agregar Restricción")
        # self.agregar_restriccion_btn.setMaximumWidth(150)
        # self.agregar_restriccion_btn.clicked.connect(self.agregar_restriccion_manual)

        # restricciones_layout = QHBoxLayout()
        # restricciones_layout.addWidget(self.curso_input)
        # restricciones_layout.addWidget(self.salon_input)
        # restricciones_layout.addWidget(self.agregar_restriccion_btn)
        
        #
        # Botón para abrir selector de restricción
        self.restricciones_data = []  # Lista de tuplas (codigo_curso, nombre_salon)

        self.restricciones_label = QLabel("Restricciones Curso → Salón")
        self.restricciones_label.setStyleSheet("font-weight: bold;")

        self.restricciones_output = QTextEdit()
        self.restricciones_output.setPlaceholderText("Aquí se mostrarán las restricciones agregadas...")
        self.restricciones_output.setReadOnly(True)
        self.restricciones_output.setMaximumHeight(80)

        self.abrir_dialogo_btn = QPushButton("Agregar Restricción (Curso-Salón)")
        self.abrir_dialogo_btn.setMaximumWidth(200)
        self.abrir_dialogo_btn.clicked.connect(self.abrir_dialogo_restriccion)

        layout.addWidget(self.restricciones_label)
        layout.addWidget(self.abrir_dialogo_btn)
        layout.addWidget(self.restricciones_output)

        #

        # layout.addWidget(self.restricciones_label)
        # layout.addLayout(restricciones_layout)
        # layout.addWidget(self.restricciones_output)

        return layout

    def init_console_tab(self):
        layout = QVBoxLayout()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)
        return layout

    def init_results_tab(self):
        layout = QVBoxLayout()

        # ScrollArea para que la tabla se deslice cuando sea muy grande
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout()

        # Tabla
        self.schedule_table = QTableWidget()
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        container_layout.addWidget(self.schedule_table)

        # Botón Ver en PDF
        open_pdf_button = QPushButton("Ver en PDF")
        open_pdf_button.clicked.connect(self.load_pdf_result)
        container_layout.addWidget(open_pdf_button)

        container.setLayout(container_layout)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        return layout

    def init_reports_tab(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout()

        # Resumen del JSON
        self.json_summary_label = QLabel("Resumen del Resultado Final")
        self.json_summary_output = QTextEdit()
        self.json_summary_output.setReadOnly(True)
        self.json_summary_output.setMaximumHeight(180)

        content_layout.addWidget(self.json_summary_label)
        content_layout.addWidget(self.json_summary_output)
        
        # Gráficas
        self.graph_paths = [
            ("Evolución de Aptitud", "exports/graficas/evolucion_aptitud.png"),
            ("Conflictos por Generación", "exports/graficas/conflictos_por_generacion.png"),
            ("Continuidad por Semestre", "exports/graficas/continuidad_por_semestre.png")
        ]

        self.graph_labels = []
        for title, path in self.graph_paths:
            label = QLabel(title)
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            content_layout.addWidget(label)
            content_layout.addWidget(img_label)
            self.graph_labels.append((img_label, path))

        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        return layout        

    def run_algorithm(self):
        cursos = self.csv_labels["Cursos"].text()
        docentes = self.csv_labels["Docentes"].text()
        relacion = self.csv_labels["Relación Docente-Curso"].text()
        salones = self.csv_labels["Salones"].text()
    
        try:
            poblacion = int(self.population_input.text())
            generaciones = int(self.generations_input.text())
            aptitud = float(self.fitness_input.text())
        except ValueError:
            self.console_output.append("[ERROR] Parámetros inválidos. Verifica los valores numéricos.")
            return

        self.console_output.append("[INFO] Ejecutando el algoritmo genético...\n")
        
        try:
            modo = self.option_group.checkedId()
            
            # Aseguramos que las restricciones se pasen correctamente
            print(f"Pasando restricciones al algoritmo: {self.restricciones_data}")  # Print para depuración

            logs, resultados = ejecutar_algoritmo(
                cursos, docentes, relacion, salones,
                poblacion_size=poblacion,
                generaciones_max=generaciones,
                aptitud_objetivo=aptitud,
                modo=modo,
                restricciones=self.restricciones_data  # Aquí pasamos las restricciones
            )

            for log in logs:
                self.console_output.append(log)

            # Mostrar en consola
            self.console_output.append("\n[Resumen del Resultado Final]")
            
            for clave, valor in resultados.items():
                self.console_output.append(f"- {clave.replace('_', ' ').capitalize()}: {valor}")

            # Mostrar en sección Reportes
            summary_text = "[Resumen del Resultado Final]\n"
            for clave, valor in resultados.items():
                if isinstance(valor, dict):
                    summary_text += f"- {clave.replace('_', ' ').capitalize()}:\n"
                    for subkey, subval in valor.items():
                        summary_text += f"    > {subkey}: {subval}\n"
                else:
                    summary_text += f"- {clave.replace('_', ' ').capitalize()}: {valor}\n"
            self.json_summary_output.setPlainText(summary_text)

            # Cargar resultados
            self.load_schedule_csv_to_table()
            self.load_pdf_result()
            self.load_report_graphs()

        except Exception as e:
            self.console_output.append(f"[ERROR] Error al ejecutar el algoritmo: {e}")
            
    def abrir_dialogo_restriccion(self):
        from interface.dialogs.restriccion_dialog import RestriccionCursoSalonDialog  # o donde lo pongas

        dialog = RestriccionCursoSalonDialog(self)
        if dialog.exec_():
            curso, salon = dialog.get_result()
            self.restricciones_data.append((curso, salon))
            self.restricciones_output.append(f"{curso} → {salon}")
            print(f"Restricción agregada: {curso} → {salon}")  # Print para depurar
            
    # AGREGADO
    def agregar_restriccion_manual(self):
        codigo = self.curso_input.text().strip()
        salon = self.salon_input.text().strip()

        if codigo and salon:
            self.restricciones_data.append((codigo, salon))
            self.restricciones_output.append(f"{codigo} → {salon}")
            self.curso_input.clear()
            self.salon_input.clear()
        else:
            self.console_output.append("[ERROR] Ambos campos son obligatorios para agregar la restricción.")
    # FIN AGREGADO

    def load_schedule_csv_to_table(self):
        path = os.path.abspath("exports/csv/mejor_horario.csv")
        if not os.path.exists(path):
            self.console_output.append("[ERROR] No se encontró el archivo CSV del horario.")
            return

        if self.schedule_table is None:
            self.console_output.append("[ERROR] La tabla no ha sido inicializada.")
            return

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Lee encabezados directamente del archivo
            rows = list(reader)

            self.schedule_table.setRowCount(len(rows))
            self.schedule_table.setColumnCount(len(headers))
            self.schedule_table.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(rows):
                for col_idx, cell in enumerate(row_data):
                    self.schedule_table.setItem(row_idx, col_idx, QTableWidgetItem(cell))

        self.tabs.setCurrentWidget(self.results_tab)

    def load_pdf_result(self):
        path = os.path.abspath("exports/pdf/mejor_horario.pdf")
        webbrowser.open_new(f"file:///{path}")

    def load_report_graphs(self):
        for label, path in self.graph_labels:
            if os.path.exists(path):
                pixmap = QPixmap(path)
                label.setPixmap(pixmap.scaledToWidth(750, Qt.SmoothTransformation))

    def auto_set_csv_defaults(self):
        base_path = os.path.abspath("data")
        archivos = {
            "Cursos": "curso.csv",
            "Docentes": "docente.csv",
            "Relación Docente-Curso": "docente_curso.csv",
            "Salones": "salon.csv"
        }
        for key, filename in archivos.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                self.csv_labels[key].setText(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainApp()
    main_win.show()
    sys.exit(app.exec_())
