#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QInputDialog, QListWidget, QComboBox)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        """
        Establece el titulo de la ventana y su tamaño.
        Aplica un estilo CSS: fondo blanco y borde azul oscuro.
        """
        self.setWindowTitle("Practica 1 - Clasificacion - CH")
        self.resize(1100, 768) 
        self.setStyleSheet("QMainWindow { background-color: white; border: 6px solid #000080; }")

        #Crea el contenedor central y un layout horizontal. 
        widget_central = QWidget()
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        
        #Crea un panel izquierdo con un layout vertical, ocupando 3 veces más espacio que el panel derecho.
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        panel_izquierdo.setLayout(layout_izquierdo)
        layout_principal.addWidget(panel_izquierdo, stretch=3) 

        #1. Título: Crea el titulo centrado y lo añade al panel izquierdo.
        self.titulo = QLabel("Primera práctica - Clasificación")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #000080; margin: 10px;")
        layout_izquierdo.addWidget(self.titulo)

        #2. Cuadro de la gráfica: Crea un marco para la gráfica.
        self.frame_grafica = QFrame()
        self.frame_grafica.setFrameShape(QFrame.Shape.Box)
        self.frame_grafica.setStyleSheet("background-color: white; border: 2px dashed #000080;")
        self.layout_grafica = QVBoxLayout()
        self.frame_grafica.setLayout(self.layout_grafica)

        #Crea la figura de Matplotlib y el canvas. Aquí se dibujan los vectores, ocupando todo el espacio disponible.
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.layout_grafica.addWidget(self.canvas)
        layout_izquierdo.addWidget(self.frame_grafica, stretch=1) 

        #3. Botón para ingresar nuevo vector: Crea un botón que al hacer clic, se piden las coordenadas.
        self.btn_ingresar_vector = QPushButton("Ingresar Nuevo Vector")
        self.btn_ingresar_vector.setStyleSheet("""
            QPushButton { background-color: #000080; color: white; font-weight: bold; 
                          font-size: 16px; padding: 15px; border-radius: 5px; border: none; }
            QPushButton:hover { background-color: #1A237E; }
        """)
        layout_izquierdo.addWidget(self.btn_ingresar_vector)

        self.btn_ingresar_vector.clicked.connect(self.pedir_coordenadas)


        #Crea el panel derecho con un layout vertical.
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        panel_derecho.setLayout(layout_derecho)
        layout_principal.addWidget(panel_derecho, stretch=1) 

        #1. Título del lado derecho usado para el historial de vectores
        self.titulo_historial = QLabel("Historial de Vectores")
        self.titulo_historial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo_historial.setStyleSheet("font-size: 18px; font-weight: bold; color: #000080; margin: 5px;")
        layout_derecho.addWidget(self.titulo_historial)

        #2. Lista interactiva
        self.lista_historial = QListWidget()
        self.lista_historial.setStyleSheet("""
            QListWidget { 
                background-color: white; 
                color: #333333; 
                border: 2px solid #000080; 
                border-radius: 5px; 
                font-size: 14px; 
                padding: 5px; 
            }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #eeeeee; }
            QListWidget::item:selected { background-color: #000080; color: white; }
        """)
        layout_derecho.addWidget(self.lista_historial)

        self.label_metodo = QLabel("Seleccione el método para calculo de la distancia:")
        self.label_metodo.setStyleSheet("font-weight: bold; color #000080; margin-top: 10px;")
        layout_izquierdo.addWidget(self.label_metodo)

        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Euclidiana", "Mahalanobis"])
        self.combo_metodo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #000080;
                border-radius: 5px;
                font-size: 14px;}""")
        layout_izquierdo.addWidget(self.combo_metodo)

        #3. Botón para mostrar el vector seleccionado en la gráfica.
        self.btn_mostrar_seleccion = QPushButton("Mostrar en Gráfica")
        self.btn_mostrar_seleccion.setStyleSheet("""
            QPushButton { background-color: #000080; color: white; font-weight: bold; 
                          font-size: 14px; padding: 12px; border-radius: 5px; border: none; }
            QPushButton:hover { background-color: #1A237E; }
        """)
        layout_derecho.addWidget(self.btn_mostrar_seleccion)

        #4. Créditos 
        self.label_creditos = QLabel("Desarrollado por: \nCerón Samperio Lizeth Montserrat \nHiguera Pineda Angel Abraham ")
        self.label_creditos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_creditos.setStyleSheet("color: #000080; font-size: 12px; font-weight: bold; margin-top: 10px;")
        layout_derecho.addWidget(self.label_creditos)

    
    """
    Limpia la gráfica anterior y crea un nuevo gráfico. Define 6 colores para cada clase. y muestra su centro de gravedad
    """
    def dibujar_vectores(self, lista_vectores, lista_centros, punto_usuario=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        colores = ['red', 'blue', 'purple', 'cyan', 'orange', 'green']

        for i, vector in enumerate(lista_vectores):
            #Extraemos las coordenadas X y Y directamente de la lista que nos pasó el Modelo
            cx = round(lista_centros[i][0], 2)
            cy = round(lista_centros[i][1], 2)
            
            texto_leyenda = f"Clase {i+1} ({cx}, {cy})"
            
            ax.scatter(vector[:, 0], vector[:, 1], color=colores[i], label=texto_leyenda) 
        
        if punto_usuario is not None:
            ax.scatter(punto_usuario[0], punto_usuario[1], color='black', marker='X', s=150, label='Vector X')

        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best') 
        self.canvas.draw()

    """
    Abre un cuadro de diálogo pidiendo la coordenada X. 
    Si X es válida, pide la coordenada Y.
    Pasa las coordenadas a la función de procesamiento y conecta así la vista con el controlador.
    """
    def pedir_coordenadas(self):
        x_str, ok_x = QInputDialog.getText(self, "Ingresar X", "Ingresa la coordenada X:")
        if ok_x and x_str:
            y_str, ok_y = QInputDialog.getText(self, "Ingresar Y", "Ingresa la coordenada Y:")
            if ok_y and y_str:
                if hasattr(self, 'funcion_procesar'):
                    metodo_sel = self.combo_metodo.currentText().lower()
                    self.funcion_procesar(x_str, y_str, metodo_sel)