import numpy as np
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QListWidget, 
                             QComboBox, QFileDialog, QDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm

class DialogoBaseDatos(QDialog):
    def __init__(self, nombres, listas_rgb, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Base de Datos Interna (Colores RGB Extraídos)")
        self.resize(600, 500)
        self.setStyleSheet("background-color: #F8F9FA; color: #000000;")
        layout = QVBoxLayout(self)

        tabla = QTableWidget()
        tabla.setStyleSheet("background-color: #FFFFFF; color: #000000;")
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels(["Clase", "Rojo (R)", "Verde (G)", "Azul (B)"])
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        filas_reales = sum(min(len(c), 500) for c in listas_rgb)
        tabla.setRowCount(filas_reales)
        
        fila_actual = 0
        for i, clase_rgb in enumerate(listas_rgb):
            nombre = nombres[i]
            puntos_a_mostrar = min(len(clase_rgb), 500)
            for j in range(puntos_a_mostrar):
                R, G, B = clase_rgb[j]
                tabla.setItem(fila_actual, 0, QTableWidgetItem(nombre))
                tabla.setItem(fila_actual, 1, QTableWidgetItem(str(round(R))))
                tabla.setItem(fila_actual, 2, QTableWidgetItem(str(round(G))))
                tabla.setItem(fila_actual, 3, QTableWidgetItem(str(round(B))))
                fila_actual += 1

        layout.addWidget(QLabel("Mostrando muestra de hasta 500 píxeles por clase:"))
        layout.addWidget(tabla)

class DialogoMenuClases(QDialog):
    # CORRECCIÓN: Ahora recibe las clases predefinidas desde el controlador
    def __init__(self, num_clases, clases_predefinidas, parent=None): 
        super().__init__(parent)
        self.setWindowTitle("Definición de Clases por Rangos (Cajas)")
        self.resize(700, 300)
        self.layout = QVBoxLayout(self)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "X Min", "X Max", "Y Min", "Y Max"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setRowCount(num_clases)

        opciones = [c[0] for c in clases_predefinidas] + ["Otro"]

        for i in range(num_clases):
            combo = QComboBox()
            combo.addItems(opciones)
            
            if i < len(clases_predefinidas):
                combo.setCurrentText(clases_predefinidas[i][0])
                xmin, xmax, ymin, ymax = clases_predefinidas[i][1:]
            else:
                xmin, xmax, ymin, ymax = 0, 500, 0, 500
                
            self.tabla.setCellWidget(i, 0, combo)
            self.tabla.setItem(i, 1, QTableWidgetItem(str(xmin)))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(xmax)))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(ymin)))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(ymax)))

        self.layout.addWidget(self.tabla)
        self.btn_generar = QPushButton("¡Generar Clases!")
        self.btn_generar.clicked.connect(self.accept)
        self.layout.addWidget(self.btn_generar)

    def obtener_datos(self):
        datos = []
        for i in range(self.tabla.rowCount()):
            nombre = self.tabla.cellWidget(i, 0).currentText()
            xmin = int(self.tabla.item(i, 1).text())
            xmax = int(self.tabla.item(i, 2).text())
            ymin = int(self.tabla.item(i, 3).text())
            ymax = int(self.tabla.item(i, 4).text())
            datos.append((nombre, xmin, xmax, ymin, ymax))
        return datos

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practica 4 - Visión Computacional - CH")
        self.resize(1200, 800) 

        widget_central = QWidget()
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        panel_izquierdo.setLayout(layout_izquierdo)
        layout_principal.addWidget(panel_izquierdo, stretch=3) 

        self.titulo = QLabel("Práctica 4 - Segmentación Inteligente")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_izquierdo.addWidget(self.titulo)

        controles_h = QHBoxLayout()
        self.btn_cargar_img = QPushButton("Cargar Imagen")
        self.btn_configurar = QPushButton("Configurar Clases")
        self.btn_ver_bd = QPushButton("Ver Base de Datos")
        controles_h.addWidget(self.btn_cargar_img)
        controles_h.addWidget(self.btn_configurar)
        controles_h.addWidget(self.btn_ver_bd)
        layout_izquierdo.addLayout(controles_h)

        self.label_estado = QLabel("Estado: Esperando Imagen...")
        self.label_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_izquierdo.addWidget(self.label_estado)

        self.frame_grafica = QFrame()
        self.frame_grafica.setFrameShape(QFrame.Shape.Box)
        self.layout_grafica = QVBoxLayout()
        self.frame_grafica.setLayout(self.layout_grafica)

        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)
        self.ax.axis('on') 
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.layout_grafica.addWidget(self.canvas)
        layout_izquierdo.addWidget(self.frame_grafica, stretch=1) 

        clasif_h = QHBoxLayout()
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Ninguna", "Euclidiana", "Mahalanobis", "Probabilidad"])
        
        self.btn_ingresar_vector = QPushButton("Ingresar Nuevo Vector (Manual)")
        
        clasif_h.addWidget(QLabel("Método:"))
        clasif_h.addWidget(self.combo_metodo)
        clasif_h.addWidget(self.btn_ingresar_vector)
        layout_izquierdo.addLayout(clasif_h)
        
        self.combo_metodo.currentTextChanged.connect(self.cambiar_tema_color)

        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        panel_derecho.setLayout(layout_derecho)
        layout_principal.addWidget(panel_derecho, stretch=1) 

        self.titulo_historial = QLabel("Historial")
        self.titulo_historial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_derecho.addWidget(self.titulo_historial)

        self.lista_historial = QListWidget()
        layout_derecho.addWidget(self.lista_historial)

        self.btn_limpiar = QPushButton("Limpiar Historial")
        layout_derecho.addWidget(self.btn_limpiar)

        self.aplicar_estilos("#37474F", "#263238", fondo_gris=False)

    def dibujar_imagen_y_puntos(self, img_matriz, puntos_xy, nombres, vector_usuario=None):
        self.ax.clear()
        
        if img_matriz is not None:
            self.ax.imshow(img_matriz)
        
        mapa_colores = cm.get_cmap('tab10')
        for i, pts in enumerate(puntos_xy):
            # --- NUEVO: Interceptamos el nombre para cambiar el color ---
            nombre_clase = nombres[i].lower()
            
            if "roja" in nombre_clase or "rojo" in nombre_clase:
                color_punto = 'black'  # <--- Aquí forzamos el color negro
            else:
                color_punto = mapa_colores(i % 10) # Los demás siguen usando la paleta automática
                
            self.ax.scatter(pts[:, 0], pts[:, 1], color=color_punto, alpha=0.8, s=5, label=nombres[i])

        if vector_usuario is not None:
            # La cruz del usuario la dejamos roja para que resalte
            self.ax.scatter(vector_usuario[0], vector_usuario[1], color='red', marker='X', s=200, label='Vector X')

        self.ax.axis('on')
        self.ax.grid(True, linestyle='--', alpha=0.5)
        if puntos_xy:
            self.ax.legend(loc='upper right')
        self.canvas.draw()

    def cambiar_tema_color(self, metodo):
        m = metodo.lower()
        if m == "ninguna":
            self.aplicar_estilos(color_base="#00838F", color_hover="#006064", fondo_gris=False)
        elif m == "euclidiana":
            self.aplicar_estilos(color_base="#0D47A1", color_hover="#1565C0", fondo_gris=False)
        elif m == "mahalanobis":
            self.aplicar_estilos(color_base="#B71C1C", color_hover="#D32F2F", fondo_gris=False)
        elif m == "probabilidad":
            self.aplicar_estilos(color_base="#4A148C", color_hover="#6A1B9A", fondo_gris=False)

    def cambiar_tema_manual(self):
        self.aplicar_estilos(color_base="#757575", color_hover="#9E9E9E", fondo_gris=True)

    def aplicar_estilos(self, color_base, color_hover, fondo_gris):
        bg_color = "#D3D3D3" if fondo_gris else "#F0F2F5"
        
        self.setStyleSheet(f"QMainWindow {{ background-color: {bg_color}; border: 4px solid {color_base}; }}")
        self.titulo.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color_base}; margin: 5px;")
        
        estilo_btn = f"QPushButton {{ background-color: {color_base}; color: white; font-weight: bold; font-size: 13px; padding: 8px; border-radius: 4px; }} QPushButton:hover {{ background-color: {color_hover}; }}"
        
        self.btn_cargar_img.setStyleSheet(estilo_btn)
        self.btn_configurar.setStyleSheet(estilo_btn)
        self.btn_ver_bd.setStyleSheet(estilo_btn)
        self.btn_ingresar_vector.setStyleSheet(estilo_btn)
        self.btn_limpiar.setStyleSheet(estilo_btn)
        
        self.frame_grafica.setStyleSheet(f"background-color: #FFFFFF; border: 2px dashed {color_base};")
        
        estilo_combo = f"QComboBox {{ background-color: #FFFFFF; color: #000000; border: 1px solid {color_base}; padding: 5px; }}"
        self.combo_metodo.setStyleSheet(estilo_combo)
        
        self.titulo_historial.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color_base}; margin: 5px;")
        self.lista_historial.setStyleSheet(f"QListWidget {{ background-color: #FFFFFF; color: #000000; border: 2px solid {color_base}; border-radius: 4px; }}")