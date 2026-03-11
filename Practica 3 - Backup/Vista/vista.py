#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import sys
import random
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QInputDialog, 
                             QListWidget, QComboBox, QCheckBox, QDialog, QTableWidget, 
                             QTableWidgetItem, QSpinBox, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
import matplotlib.cm as cm # Para generar colores dinámicos

# =========================================================
# NUEVA VENTANA DE CONFIGURACIÓN DE CLASES
# =========================================================
class DialogoConfiguracion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar Clases Sintéticas")
        self.resize(500, 400)
        self.layout = QVBoxLayout(self)

        # Controles superiores
        panel_controles = QHBoxLayout()
        
        panel_controles.addWidget(QLabel("N° de Clases:"))
        self.spin_clases = QSpinBox()
        self.spin_clases.setRange(1, 20)
        self.spin_clases.setValue(3)
        panel_controles.addWidget(self.spin_clases)

        panel_controles.addWidget(QLabel("Representantes p/clase:"))
        self.spin_reps = QSpinBox()
        self.spin_reps.setRange(10, 100000)
        self.spin_reps.setValue(1000)
        self.spin_reps.setSingleStep(500)
        panel_controles.addWidget(self.spin_reps)

        self.btn_actualizar_tabla = QPushButton("Actualizar Tabla")
        panel_controles.addWidget(self.btn_actualizar_tabla)
        self.layout.addLayout(panel_controles)

        # Tabla de parámetros
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Centro X", "Centro Y", "Dispersión X", "Dispersión Y"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.tabla)

        # Botón de generar
        self.btn_generar = QPushButton("Generar Clases!")
        self.btn_generar.setStyleSheet("background-color: #000080; color: white; font-weight: bold; padding: 10px;")
        self.layout.addWidget(self.btn_generar)

        # Conexiones
        self.btn_actualizar_tabla.clicked.connect(self.dibujar_tabla)
        self.btn_generar.clicked.connect(self.accept)

        self.dibujar_tabla() # Dibuja la tabla al abrir

    def dibujar_tabla(self):
        num_clases = self.spin_clases.value()
        self.tabla.setRowCount(num_clases)
        
        for fila in range(num_clases):
            # Autocompletamos con valores aleatorios para ahorrar tiempo al usuario
            cx = str(random.randint(-10, 20))
            cy = str(random.randint(-10, 20))
            dx = str(round(random.uniform(0.5, 3.0), 1))
            dy = str(round(random.uniform(0.5, 3.0), 1))
            
            self.tabla.setItem(fila, 0, QTableWidgetItem(cx))
            self.tabla.setItem(fila, 1, QTableWidgetItem(cy))
            self.tabla.setItem(fila, 2, QTableWidgetItem(dx))
            self.tabla.setItem(fila, 3, QTableWidgetItem(dy))

    def obtener_datos(self):
        num_clases = self.spin_clases.value()
        num_reps = self.spin_reps.value()
        parametros = []
        try:
            for fila in range(num_clases):
                cx = float(self.tabla.item(fila, 0).text())
                cy = float(self.tabla.item(fila, 1).text())
                dx = float(self.tabla.item(fila, 2).text())
                dy = float(self.tabla.item(fila, 3).text())
                parametros.append((cx, cy, dx, dy))
            return num_clases, num_reps, parametros
        except:
            return None, None, None

# =========================================================
# VISTA PRINCIPAL
# =========================================================
class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Practica 3 - Clases Dinámicas - CH")
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

        self.titulo = QLabel("Tercera práctica - Generacion dinamica")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_izquierdo.addWidget(self.titulo)

        # --- NUEVO BOTÓN DE CONFIGURACIÓN ---
        self.btn_configurar = QPushButton("Configurar y Generar Clases")
        layout_izquierdo.addWidget(self.btn_configurar)

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
        self.combo_metodo.addItems(["Euclidiana", "Mahalanobis", "Probabilidad"])
        layout_izquierdo.addWidget(self.combo_metodo)
        self.combo_metodo.currentTextChanged.connect(self.cambiar_tema_color)

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
        elif metodo_seleccionado.lower() == "probabilidad":
            self.aplicar_estilos(color_base="#4B0082", color_hover="#301934")
        else:
            self.aplicar_estilos(color_base="#000080", color_hover="#1A237E")

    def aplicar_estilos(self, color_base, color_hover):
        self.setStyleSheet(f"QMainWindow {{ background-color: white; border: 6px solid {color_base}; }}")
        self.titulo.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color_base}; margin: 5px;")
        
        self.btn_configurar.setStyleSheet(f"QPushButton {{ background-color: #2E7D32; color: white; font-weight: bold; font-size: 16px; padding: 10px; border-radius: 5px; border: none; }} QPushButton:hover {{ background-color: #1B5E20; }}")
        
        self.frame_grafica.setStyleSheet(f"background-color: white; border: 2px dashed {color_base};")
        self.label_metodo.setStyleSheet(f"font-weight: bold; color: {color_base}; margin-top: 5px;")
        self.combo_metodo.setStyleSheet(f"QComboBox {{ padding: 10px; border: 2px solid {color_base}; border-radius: 5px; font-size: 14px; }}")
        self.check_barreras.setStyleSheet(f"font-weight: bold; color: {color_base}; font-size: 14px; margin: 5px;")
        self.btn_ingresar_vector.setStyleSheet(f"QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; font-size: 16px; padding: 15px; border-radius: 5px; border: none; }} QPushButton:hover {{ background-color: {color_hover}; }}")
        self.titulo_historial.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color_base}; margin: 5px;")
        self.lista_historial.setStyleSheet(f"QListWidget {{ background-color: white; color: #333333; border: 2px solid {color_base}; border-radius: 5px; font-size: 14px; padding: 5px; }} QListWidget::item {{ padding: 8px; border-bottom: 1px solid #eeeeee; }} QListWidget::item:selected {{ background-color: {color_base}; color: white; }}")
        self.btn_mostrar_seleccion.setStyleSheet(f"QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; font-size: 14px; padding: 12px; border-radius: 5px; border: none; }} QPushButton:hover {{ background-color: {color_hover}; }}")
        self.label_creditos.setStyleSheet(f"color: {color_base}; font-size: 12px; font-weight: bold; margin-top: 10px;")

    def dibujar_vectores(self, lista_vectores, lista_centros, punto_usuario=None, barreras=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        
        # Obtenemos colores dinámicos por si piden 10 o 20 clases
        mapa_colores = cm.get_cmap('tab20')

        for i, vector in enumerate(lista_vectores):
            # Asignamos un color único del mapa
            color_actual = mapa_colores(i % 20)
            
            cx = round(lista_centros[i][0], 2)
            cy = round(lista_centros[i][1], 2)
            texto_leyenda = f"C{i+1} ({cx}, {cy})"
            
            # Dibujamos los puntos
            ax.scatter(vector[:, 0], vector[:, 1], color=color_actual, alpha=0.5, s=10, label=texto_leyenda) 
            
            # Dibujamos el centroide como un diamante grande
            ax.scatter(cx, cy, color=color_actual, edgecolors='black', marker='D', s=100)
            
            if barreras is not None:
                bx, by, width, height, angle = barreras[i]
                elipse = Ellipse((bx, by), width, height, angle=angle, 
                                 edgecolor=color_actual, facecolor='none', linestyle='-', linewidth=2)
                ax.add_patch(elipse)
        
        if punto_usuario is not None:
            ax.scatter(punto_usuario[0], punto_usuario[1], color='black', marker='X', s=200, label='Vector X')

        ax.set_aspect('equal', adjustable='datalim') 
        ax.grid(True, linestyle='--', alpha=0.6)
        # Colocamos la leyenda fuera para que no estorbe si hay muchas clases
        ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0.) 
        self.figura.tight_layout()
        self.canvas.draw()

    def pedir_coordenadas(self):
        x_str, ok_x = QInputDialog.getText(self, "Ingresar X", "Ingresa la coordenada X:")
        if ok_x and x_str:
            y_str, ok_y = QInputDialog.getText(self, "Ingresar Y", "Ingresa la coordenada Y:")
            if ok_y and y_str:
                if hasattr(self, 'funcion_procesar'):
                    self.funcion_procesar(x_str, y_str)