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
        
        self.setWindowTitle("Practica 1 - Clasificacion - CH")
        self.resize(1100, 768) 

        # --- LAYOUT PRINCIPAL ---
        widget_central = QWidget()
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # =========================================================
        # PANEL IZQUIERDO (Gráfica y Controles)
        # =========================================================
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        panel_izquierdo.setLayout(layout_izquierdo)
        layout_principal.addWidget(panel_izquierdo, stretch=3) 

        # 1. Título
        self.titulo = QLabel("Primera práctica - Clasificación")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_izquierdo.addWidget(self.titulo)

        # 2. Cuadro de la gráfica
        self.frame_grafica = QFrame()
        self.frame_grafica.setFrameShape(QFrame.Shape.Box)
        self.layout_grafica = QVBoxLayout()
        self.frame_grafica.setLayout(self.layout_grafica)

        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.layout_grafica.addWidget(self.canvas)
        layout_izquierdo.addWidget(self.frame_grafica, stretch=1) 

        # 3. Combobox para seleccionar método
        self.label_metodo = QLabel("Seleccione el método para cálculo de la distancia:")
        layout_izquierdo.addWidget(self.label_metodo)

        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Euclidiana", "Mahalanobis"])
        layout_izquierdo.addWidget(self.combo_metodo)

        # ¡NUEVO! Conectamos el cambio del combobox a nuestra función de temas
        self.combo_metodo.currentTextChanged.connect(self.cambiar_tema_color)

        # 4. Botón para ingresar nuevo vector
        self.btn_ingresar_vector = QPushButton("Ingresar Nuevo Vector")
        layout_izquierdo.addWidget(self.btn_ingresar_vector)
        self.btn_ingresar_vector.clicked.connect(self.pedir_coordenadas)


        # =========================================================
        # PANEL DERECHO (Historial y Créditos)
        # =========================================================
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        panel_derecho.setLayout(layout_derecho)
        layout_principal.addWidget(panel_derecho, stretch=1) 

        # 1. Título del historial
        self.titulo_historial = QLabel("Historial de Vectores")
        self.titulo_historial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_derecho.addWidget(self.titulo_historial)

        # 2. Lista interactiva
        self.lista_historial = QListWidget()
        layout_derecho.addWidget(self.lista_historial)

        # 3. Botón para mostrar el vector seleccionado
        self.btn_mostrar_seleccion = QPushButton("Mostrar en Gráfica")
        layout_derecho.addWidget(self.btn_mostrar_seleccion)

        # 4. Créditos 
        self.label_creditos = QLabel("Desarrollado por: \nCerón Samperio Lizeth Montserrat \nHiguera Pineda Angel Abraham ")
        self.label_creditos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_derecho.addWidget(self.label_creditos)

        # ¡IMPORTANTE! Llamamos a esta función al iniciar para aplicar el color azul por defecto
        self.aplicar_estilos("#000080", "#1A237E")

    # --- FUNCIONES DE DISEÑO Y TEMAS ---

    def cambiar_tema_color(self, metodo_seleccionado):
        """Detecta qué método se eligió y cambia los colores de la interfaz."""
        if metodo_seleccionado.lower() == "mahalanobis":
            # Tema Rojo Oscuro (Mahalanobis)
            self.aplicar_estilos(color_base="#8B0000", color_hover="#A52A2A")
        else:
            # Tema Azul Marino (Euclidiana)
            self.aplicar_estilos(color_base="#000080", color_hover="#1A237E")

    def aplicar_estilos(self, color_base, color_hover):
        """Aplica las hojas de estilo CSS dinámicamente a todos los elementos usando f-strings."""
        
        self.setStyleSheet(f"QMainWindow {{ background-color: white; border: 6px solid {color_base}; }}")
        
        self.titulo.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color_base}; margin: 10px;")
        
        self.frame_grafica.setStyleSheet(f"background-color: white; border: 2px dashed {color_base};")
        
        self.label_metodo.setStyleSheet(f"font-weight: bold; color: {color_base}; margin-top: 10px;")
        
        self.combo_metodo.setStyleSheet(f"""
            QComboBox {{ padding: 10px; border: 2px solid {color_base}; border-radius: 5px; font-size: 14px; }}
        """)

        estilo_btn_grande = f"""
            QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; 
                          font-size: 16px; padding: 15px; border-radius: 5px; border: none; }}
            QPushButton:hover {{ background-color: {color_hover}; }}
        """
        self.btn_ingresar_vector.setStyleSheet(estilo_btn_grande)

        self.titulo_historial.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color_base}; margin: 5px;")
        
        self.lista_historial.setStyleSheet(f"""
            QListWidget {{ 
                background-color: white; color: #333333; border: 2px solid {color_base}; 
                border-radius: 5px; font-size: 14px; padding: 5px; 
            }}
            QListWidget::item {{ padding: 8px; border-bottom: 1px solid #eeeeee; }}
            QListWidget::item:selected {{ background-color: {color_base}; color: white; }}
        """)
        
        estilo_btn_chico = f"""
            QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; 
                          font-size: 14px; padding: 12px; border-radius: 5px; border: none; }}
            QPushButton:hover {{ background-color: {color_hover}; }}
        """
        self.btn_mostrar_seleccion.setStyleSheet(estilo_btn_chico)
        
        self.label_creditos.setStyleSheet(f"color: {color_base}; font-size: 12px; font-weight: bold; margin-top: 10px;")


    # --- FUNCIONES DE DIBUJO E INTERACCIÓN ---

    def dibujar_vectores(self, lista_vectores, lista_centros, punto_usuario=None):
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        colores = ['red', 'blue', 'purple', 'cyan', 'orange', 'green']

        for i, vector in enumerate(lista_vectores):
            cx = round(lista_centros[i][0], 2)
            cy = round(lista_centros[i][1], 2)
            texto_leyenda = f"Clase {i+1} ({cx}, {cy})"
            ax.scatter(vector[:, 0], vector[:, 1], color=colores[i], label=texto_leyenda) 
        
        if punto_usuario is not None:
            ax.scatter(punto_usuario[0], punto_usuario[1], color='black', marker='X', s=150, label='Vector X')

        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best') 
        self.canvas.draw()

    def pedir_coordenadas(self):
        x_str, ok_x = QInputDialog.getText(self, "Ingresar X", "Ingresa la coordenada X:")
        if ok_x and x_str:
            y_str, ok_y = QInputDialog.getText(self, "Ingresar Y", "Ingresa la coordenada Y:")
            if ok_y and y_str:
                if hasattr(self, 'funcion_procesar'):
                    metodo_sel = self.combo_metodo.currentText().lower()
                    self.funcion_procesar(x_str, y_str, metodo_sel)