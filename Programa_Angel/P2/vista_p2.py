import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VistaLetras(QWidget):
    def __init__(self):
        super().__init__()
        # AGREGADO: Título actualizado
        self.setWindowTitle("Problema 2 - IMREF2D e Iniciales (A, H, P, M)")
        # AGREGADO: Ventana más ancha (1000) para que la gráfica no se vea aplastada
        self.resize(1000, 500)

        layout_principal = QVBoxLayout()

        # Entradas X, Y
        layout_entradas = QHBoxLayout()
        self.input_x = QLineEdit()
        self.input_x.setPlaceholderText("X (ej. 22.0)") # Sugerencia ajustada a la nueva letra
        self.input_y = QLineEdit()
        self.input_y.setPlaceholderText("Y (ej. 3.0)")
        
        layout_entradas.addWidget(QLabel("Vector (ah):"))
        layout_entradas.addWidget(self.input_x)
        layout_entradas.addWidget(self.input_y)

        self.btn_clasificar = QPushButton("Evaluar Vector")
        self.label_resultado = QLabel("<b>Resultado:</b> Ingresa coordenadas X, Y.")
        
        # Canvas 2D
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        layout_principal.addLayout(layout_entradas)
        layout_principal.addWidget(self.btn_clasificar)
        layout_principal.addWidget(self.label_resultado)
        layout_principal.addWidget(self.canvas, stretch=1)

        self.setLayout(layout_principal)

    def obtener_vector(self):
        try:
            return np.array([float(self.input_x.text()), float(self.input_y.text())])
        except ValueError:
            return None

    def mostrar_resultado(self, texto):
        self.label_resultado.setText(f"<b>Resultado:</b> {texto}")