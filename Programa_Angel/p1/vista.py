from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
# Importaciones para integrar Matplotlib en PyQt6
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VistaCubo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problema 1 - Cubo Unitario Integrado")
        self.resize(700, 600)  # Ventana más grande para que luzca el cubo

        layout_principal = QVBoxLayout()

        # --- PANEL SUPERIOR: Entradas ---
        layout_entradas = QHBoxLayout()
        self.input_x = QLineEdit()
        self.input_x.setPlaceholderText("R (ej. 0.5)")
        self.input_y = QLineEdit()
        self.input_y.setPlaceholderText("G (ej. 0.2)")
        self.input_z = QLineEdit()
        self.input_z.setPlaceholderText("B (ej. 0.9)")
        
        layout_entradas.addWidget(QLabel("Vector a evaluar:"))
        layout_entradas.addWidget(self.input_x)
        layout_entradas.addWidget(self.input_y)
        layout_entradas.addWidget(self.input_z)

        self.btn_clasificar = QPushButton("Clasificar Punto")
        self.label_resultado = QLabel("<b>Resultado:</b> Ingresa un vector 3D.")
        
        # --- PANEL INFERIOR: Lienzo de Matplotlib ---
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Ensamblar todo
        layout_principal.addLayout(layout_entradas)
        layout_principal.addWidget(self.btn_clasificar)
        layout_principal.addWidget(self.label_resultado)
        layout_principal.addWidget(self.canvas, stretch=1) # stretch=1 le da todo el espacio sobrante

        self.setLayout(layout_principal)

    def obtener_vector(self):
        try:
            return [float(self.input_x.text()), float(self.input_y.text()), float(self.input_z.text())]
        except ValueError:
            return None

    def mostrar_resultado(self, texto):
        self.label_resultado.setText(f"<b>Resultado:</b> {texto}")

    def mostrar_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)