#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QInputDialog, QListWidget, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse # <-- Importamos la herramienta de Elipse

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Practica 2 - Clasificacion con EUCLIDIANA y MAHALANOBIS- CH")
        self.resize(1100, 768) 

        widget_central = QWidget()
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # --- PANEL IZQUIERDO ---
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        panel_izquierdo.setLayout(layout_izquierdo)
        layout_principal.addWidget(panel_izquierdo, stretch=3) 

        self.titulo = QLabel("Segunda práctica - Clasificación con MAHALANOBIS y EUCLIDIANA")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_izquierdo.addWidget(self.titulo)

        self.frame_grafica = QFrame()
        self.frame_grafica.setFrameShape(QFrame.Shape.Box)
        self.layout_grafica = QVBoxLayout()
        self.frame_grafica.setLayout(self.layout_grafica)

        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.layout_grafica.addWidget(self.canvas)
        layout_izquierdo.addWidget(self.frame_grafica, stretch=1) 

        self.label_metodo = QLabel("Seleccione el método para cálculo de la distancia:")
        layout_izquierdo.addWidget(self.label_metodo)

        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Euclidiana", "Mahalanobis"])
        layout_izquierdo.addWidget(self.combo_metodo)
        self.combo_metodo.currentTextChanged.connect(self.cambiar_tema_color)

        # --- ¡NUEVO CHECKBOX DE BARRERAS! ---
        self.check_barreras = QCheckBox("Mostrar Barreras de Clasificación (Umbral 4.0)")
        layout_izquierdo.addWidget(self.check_barreras)

        self.btn_ingresar_vector = QPushButton("Ingresar Nuevo Vector")
        layout_izquierdo.addWidget(self.btn_ingresar_vector)
        self.btn_ingresar_vector.clicked.connect(self.pedir_coordenadas)

        # --- PANEL DERECHO ---
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        panel_derecho.setLayout(layout_derecho)
        layout_principal.addWidget(panel_derecho, stretch=1) 

        self.titulo_historial = QLabel("Historial de Vectores")
        self.titulo_historial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_derecho.addWidget(self.titulo_historial)

        self.lista_historial = QListWidget()
        layout_derecho.addWidget(self.lista_historial)

        self.btn_mostrar_seleccion = QPushButton("Mostrar en Gráfica")
        layout_derecho.addWidget(self.btn_mostrar_seleccion)

        self.label_creditos = QLabel("Desarrollado por: \nCerón Samperio Lizeth Montserrat \nHiguera Pineda Angel Abraham ")
        self.label_creditos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_derecho.addWidget(self.label_creditos)

        self.aplicar_estilos("#000080", "#1A237E")


    def cambiar_tema_color(self, metodo_seleccionado):
        if metodo_seleccionado.lower() == "mahalanobis":
            self.aplicar_estilos(color_base="#8B0000", color_hover="#A52A2A")
        else:
            self.aplicar_estilos(color_base="#000080", color_hover="#1A237E")

    def aplicar_estilos(self, color_base, color_hover):
        self.setStyleSheet(f"QMainWindow {{ background-color: white; border: 6px solid {color_base}; }}")
        self.titulo.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color_base}; margin: 10px;")
        self.frame_grafica.setStyleSheet(f"background-color: white; border: 2px dashed {color_base};")
        self.label_metodo.setStyleSheet(f"font-weight: bold; color: {color_base}; margin-top: 10px;")
        
        self.combo_metodo.setStyleSheet(f"QComboBox {{ padding: 10px; border: 2px solid {color_base}; border-radius: 5px; font-size: 14px; }}")
        
        # Estilo dinámico para el checkbox
        self.check_barreras.setStyleSheet(f"font-weight: bold; color: {color_base}; font-size: 14px; margin: 5px;")

        self.btn_ingresar_vector.setStyleSheet(f"QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; font-size: 16px; padding: 15px; border-radius: 5px; border: none; }} QPushButton:hover {{ background-color: {color_hover}; }}")
        self.titulo_historial.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color_base}; margin: 5px;")
        self.lista_historial.setStyleSheet(f"QListWidget {{ background-color: white; color: #333333; border: 2px solid {color_base}; border-radius: 5px; font-size: 14px; padding: 5px; }} QListWidget::item {{ padding: 8px; border-bottom: 1px solid #eeeeee; }} QListWidget::item:selected {{ background-color: {color_base}; color: white; }}")
        self.btn_mostrar_seleccion.setStyleSheet(f"QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; font-size: 14px; padding: 12px; border-radius: 5px; border: none; }} QPushButton:hover {{ background-color: {color_hover}; }}")
        self.label_creditos.setStyleSheet(f"color: {color_base}; font-size: 12px; font-weight: bold; margin-top: 10px;")

    # --- AHORA RECIBE EL PARÁMETRO OPCIONAL 'barreras' ---
    def dibujar_vectores(self, lista_vectores, lista_centros, punto_usuario=None, barreras=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        colores = ['red', 'blue', 'purple', 'cyan', 'orange', 'green']

        for i, vector in enumerate(lista_vectores):
            cx = round(lista_centros[i][0], 2)
            cy = round(lista_centros[i][1], 2)
            texto_leyenda = f"Clase {i+1} ({cx}, {cy})"
            ax.scatter(vector[:, 0], vector[:, 1], color=colores[i], label=texto_leyenda) 
            
            # --- DIBUJAR BARRERAS (Si existen) ---
            if barreras is not None:
                bx, by, width, height, angle = barreras[i]
                # facecolor='none' hace el óvalo transparente por dentro
                elipse = Ellipse((bx, by), width, height, angle=angle, 
                                 edgecolor=colores[i], facecolor='none', linestyle='--', linewidth=2, alpha=0.5)
                ax.add_patch(elipse)
        
        if punto_usuario is not None:
            ax.scatter(punto_usuario[0], punto_usuario[1], color='black', marker='X', s=150, label='Vector X')

        # ESTO ES VITAL: Fuerza a la gráfica a ser cuadrada para que los círculos no se deformen
        ax.set_aspect('equal', adjustable='datalim') 
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best') 
        self.canvas.draw()

    def pedir_coordenadas(self):
        x_str, ok_x = QInputDialog.getText(self, "Ingresar X", "Ingresa la coordenada X:")
        if ok_x and x_str:
            y_str, ok_y = QInputDialog.getText(self, "Ingresar Y", "Ingresa la coordenada Y:")
            if ok_y and y_str:
                if hasattr(self, 'funcion_procesar'):
                    self.funcion_procesar(x_str, y_str)