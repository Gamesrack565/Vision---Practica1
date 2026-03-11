from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QComboBox, QListWidget,
                             QFileDialog, QInputDialog)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Práctica 4 - Segmentación Inteligente")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f4f7f6;")

        # Widget central y layout principal
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central)

        # --- PANEL IZQUIERDO (Imagen y Controles) ---
        panel_izquierdo = QVBoxLayout()
        
        # Título superior
        titulo = QLabel("Práctica 4 - Segmentación Inteligente")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #00796b; margin-bottom: 10px;")
        panel_izquierdo.addWidget(titulo)

        # Botones Superiores
        layout_botones_sup = QHBoxLayout()
        self.btn_cargar = self.crear_boton("Cargar Imagen")
        self.btn_configurar = self.crear_boton("Configurar Clases")
        self.btn_bd = self.crear_boton("Ver Base de Datos")
        
        layout_botones_sup.addWidget(self.btn_cargar)
        layout_botones_sup.addWidget(self.btn_configurar)
        layout_botones_sup.addWidget(self.btn_bd)
        panel_izquierdo.addLayout(layout_botones_sup)

        # Label de estado
        self.lbl_estado = QLabel("Esperando imagen...")
        self.lbl_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_estado.setStyleSheet("color: #7f8c8d; font-style: italic;")
        panel_izquierdo.addWidget(self.lbl_estado)

        # Canvas de Matplotlib
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.axis('off') # Ocultar ejes iniciales
        panel_izquierdo.addWidget(self.canvas, stretch=1)

        # Controles Inferiores
        layout_inferior = QHBoxLayout()
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Ninguna", "Euclidiana", "Mahalanobis", "Probabilidad"])
        self.combo_metodo.setStyleSheet("padding: 5px; border: 1px solid #00796b;")
        
        self.btn_nuevo_vector = self.crear_boton("Ingresar Nuevo Vector (Manual)")
        
        layout_inferior.addWidget(QLabel("Método:"))
        layout_inferior.addWidget(self.combo_metodo, stretch=1)
        layout_inferior.addWidget(self.btn_nuevo_vector)
        panel_izquierdo.addLayout(layout_inferior)

        # --- PANEL DERECHO (Historial) ---
        panel_derecho = QVBoxLayout()
        lbl_historial = QLabel("Historial")
        lbl_historial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_historial.setStyleSheet("font-weight: bold; color: #00796b;")
        
        self.lista_historial = QListWidget()
        self.lista_historial.setStyleSheet("background-color: white; border: 1px solid #bdc3c7;")
        self.lista_historial.setFixedWidth(350)
        
        self.btn_limpiar_historial = self.crear_boton("Limpiar Historial")
        
        panel_derecho.addWidget(lbl_historial)
        panel_derecho.addWidget(self.lista_historial, stretch=1)
        panel_derecho.addWidget(self.btn_limpiar_historial)

        # Agregar paneles al layout principal
        layout_principal.addLayout(panel_izquierdo, stretch=3)
        layout_principal.addLayout(panel_derecho, stretch=1)

    def crear_boton(self, texto):
        btn = QPushButton(texto)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #00838f;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #006064; }
            QPushButton:disabled { background-color: #b2ebf2; color: #80deea; }
        """)
        return btn

    def mostrar_imagen(self, img):
        self.ax.clear()
        self.ax.imshow(img)
        self.ax.axis('on')
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.canvas.draw()