import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Visión Artificial - Práctica 1")
        self.resize(1024, 768)
        self.setStyleSheet("QMainWindow { background-color: white; border: 6px solid #000080; }")

        widget_central = QWidget()
        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # 1. Título
        self.titulo = QLabel("Primera práctica")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #333333; margin: 10px;")
        layout_principal.addWidget(self.titulo)

        # 2. Cuadro de la gráfica (ORDEN IMPORTANTE)
        self.frame_grafica = QFrame()
        self.frame_grafica.setFrameShape(QFrame.Shape.Box)
        self.frame_grafica.setStyleSheet("background-color: #f8f9fa; border: 2px dashed #000080;")
        
        # Primero: Creamos el layout del cuadro
        self.layout_grafica = QVBoxLayout()
        self.frame_grafica.setLayout(self.layout_grafica)

        # Segundo: Creamos la figura y el canvas
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        
        # Tercero: Agregamos el canvas al layout que YA existe
        self.layout_grafica.addWidget(self.canvas)

        # Agregamos el frame al layout de la ventana
        layout_principal.addWidget(self.frame_grafica, stretch=1) 

        # 3. Botón
        self.btn_cambiar_vector = QPushButton("Ingresar vector X")
        self.btn_cambiar_vector.setStyleSheet("""
            QPushButton { background-color: #000080; color: white; font-weight: bold; 
                          font-size: 16px; padding: 15px; border-radius: 5px; }
            QPushButton:hover { background-color: #1A237E; }
        """)
        layout_principal.addWidget(self.btn_cambiar_vector)
        self.btn_cambiar_vector.clicked.connect(self.pedir_coordenadas)


    def dibujar_vectores(self, lista_vectores, punto_usuario=None):
        """Dibuja los clusters y opcionalmente el punto del usuario."""
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        colores = ['red', 'blue', 'purple', 'cyan', 'orange', 'green']

        for i, vector in enumerate(lista_vectores):
            # 'vector' contiene los puntos de cada clase (C1, C2...)
            ax.scatter(vector[:, 0], vector[:, 1], color=colores[i], label=f"Clase {i+1}") 
        
        if punto_usuario is not None:
            ax.scatter(punto_usuario[0], punto_usuario[1], color='black', marker='X', s=150, label='X Usuario')

        ax.grid(True, linestyle='--', alpha=0.6)

        ax.legend()
        self.canvas.draw() 

    def preguntar_nuevo_vector(self):
        respuesta = QMessageBox.question(self, "Nuevo Vector", "¿Deseas probar con otro vector?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if respuesta == QMessageBox.StandardButton.Yes:
            self.pedir_coordenadas()
        else:
            self.close()

    def pedir_coordenadas(self):
        x_str, ok_x = QInputDialog.getText(self, "Ingresar X", "Ingresa la coordenada X:")
        if ok_x and x_str:
            y_str, ok_y = QInputDialog.getText(self, "Ingresar Y", "Ingresa la coordenada Y:")
            if ok_y and y_str:
                if hasattr(self, 'funcion_procesar'):
                    self.funcion_procesar(x_str, y_str)