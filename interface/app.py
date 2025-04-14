import os
import sys
import csv
import webbrowser

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QTextEdit, QTabWidget, QFormLayout,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from interface.runner import ejecutar_algoritmo

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
        layout = QFormLayout()  # más compacto y limpio
        self.csv_labels = {}

        for label in ["Cursos", "Docentes", "Relación Docente-Curso", "Salones"]:
            container = QHBoxLayout()

            le = QLineEdit()
            le.setReadOnly(True)
            le.setMaximumWidth(500)  # limite para que no se desborde

            b = QPushButton("Seleccionar")
            b.setMaximumWidth(100)  # botón más compacto
            b.clicked.connect(lambda _, key=label, line=le: self.load_csv(key, line))

            container.addWidget(le)
            container.addWidget(b)
            layout.addRow(QLabel(label + ":"), container)

            self.csv_labels[label] = le

        return layout

    def load_csv(self, label, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Seleccionar archivo CSV de {label}", "", "CSV Files (*.csv)")
        if file_path:
            line_edit.setText(file_path)
    
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

        self.start_button = QPushButton("Ejecutar Algoritmo")
        self.start_button.setMaximumWidth(150)
        self.start_button.clicked.connect(self.run_algorithm)

        # Botón alineado a la izquierda con un poco de margen
        button_row = QHBoxLayout()
        button_row.setContentsMargins(130, 15, 0, 0)  # margen izquierdo y arriba
        button_row.setAlignment(Qt.AlignLeft)
        button_row.addWidget(self.start_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_row)
        layout.addStretch()

        return layout

    def init_console_tab(self):
        layout = QVBoxLayout()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)
        return layout

    def init_results_tab(self):
        layout = QVBoxLayout()

        # ScrollArea para que la tabla se vea bien aunque sea grande
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
            logs, resultados = ejecutar_algoritmo(
                cursos, docentes, relacion, salones,
                poblacion_size=poblacion,
                generaciones_max=generaciones,
                aptitud_objetivo=aptitud
            )
            for log in logs:
                self.console_output.append(log)
            self.load_schedule_csv_to_table()
            self.load_pdf_result()
            self.load_report_graphs()
        except Exception as e:
            self.console_output.append(f"[ERROR] Error al ejecutar el algoritmo: {e}")
            
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
