from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QDialogButtonBox
import pandas as pd
import os

class RestriccionCursoSalonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Restricción Curso - Salón")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Cargar datos desde los paths ya configurados en app.py ---
        self.parent = parent
        self.path_cursos = parent.csv_labels["Cursos"].text()
        self.path_salones = parent.csv_labels["Salones"].text()

        self.df_cursos = pd.read_csv(self.path_cursos) if os.path.exists(self.path_cursos) else pd.DataFrame()
        self.df_salones = pd.read_csv(self.path_salones) if os.path.exists(self.path_salones) else pd.DataFrame()

        # Curso
        layout.addWidget(QLabel("Selecciona un curso:"))
        self.combo_curso = QComboBox()
        self.combo_curso.addItems(
            [f"{row['codigo']} - {row['nombre']}" for _, row in self.df_cursos.iterrows()]
        )
        layout.addWidget(self.combo_curso)

        # Salón
        layout.addWidget(QLabel("Selecciona un salón:"))
        self.combo_salon = QComboBox()
        self.combo_salon.addItems(
            [row["nombre"] for _, row in self.df_salones.iterrows()]
        )
        layout.addWidget(self.combo_salon)

        # Botones
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_result(self):
        codigo_curso = self.combo_curso.currentText().split(" - ")[0]  # Solo el código
        nombre_salon = self.combo_salon.currentText()
        return codigo_curso, nombre_salon
