from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, 
                             QMessageBox, QGroupBox, QDialog, 
                             QDialogButtonBox, QTextEdit, QTabWidget)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from PIL import Image
import numpy as np

class DialogoNombresClases(QDialog):
    def __init__(self, num_clases, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nombres de las Clases")
        self.setStyleSheet("QDialog { background-color: #f0f2f5; } QWidget { color: black; font-family: 'Consolas'; font-size: 13px; }")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Nombra las {num_clases} clases:"))
        
        self.inputs = []
        for i in range(num_clases):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"Clase {i+1}:"))
            inp = QLineEdit()
            h_layout.addWidget(inp)
            layout.addLayout(h_layout)
            self.inputs.append(inp)
        
        self.botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones)
        self.setLayout(layout)

    def obtener_nombres(self):
        return [inp.text().strip() for inp in self.inputs]

class DialogoResultadosCompletos(QDialog):
    def __init__(self, historial, nombres_clases, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de Evaluación Masiva")
        self.resize(1100, 750)
        self.setStyleSheet("background-color: #f0f2f5; color: black; font-family: 'Consolas';")
        self.historial = historial
        self.nombres_clases = nombres_clases
        
        layout_principal = QVBoxLayout()
        
        self.tabs_metodos = QTabWidget()
        for metodo in ["Resustitución", "Leave-One-Out", "Cross-Validation"]:
            tab_distancias = self.crear_tabs_distancias(metodo)
            # Usa el nombre modificado para la pestaña si existe
            nombre_pestaña = self.historial["Euclidiana"][metodo]["nombre_mostrar"]
            self.tabs_metodos.addTab(tab_distancias, nombre_pestaña)
            
        layout_principal.addWidget(self.tabs_metodos, stretch=2)
        
        btn_grafica_final = QPushButton("Ver Gráfica Comparativa Final")
        btn_grafica_final.setStyleSheet("background-color: #ffc107; color: black; font-weight: bold; padding: 10px;")
        btn_grafica_final.clicked.connect(self.mostrar_grafica_final)
        layout_principal.addWidget(btn_grafica_final)
        
        self.setLayout(layout_principal)

    def crear_tabs_distancias(self, metodo):
        tabs_dist = QTabWidget()
        
        for distancia in ["Euclidiana", "Mahalanobis", "Probabilidad"]:
            datos = self.historial[distancia][metodo]
            
            widget_contenido = QWidget()
            h_layout = QHBoxLayout(widget_contenido)
            
            txt_matriz = QTextEdit()
            txt_matriz.setReadOnly(True)
            txt_matriz.setStyleSheet("background-color: white; border: 1px solid gray;")
            
            texto_completo = f"Rendimiento Global ({distancia} - {datos['nombre_mostrar']}): {datos['global']:.2f}%\n\n"
            
            if metodo == "Cross-Validation":
                for i, matriz in enumerate(datos['matrices_txt']):
                    texto_completo += f"--- ITERACIÓN {i+1} ---\n"
                    texto_completo += self.formatear_matriz(matriz) + "\n"
            else:
                texto_completo += "MATRIZ DE CONFUSIÓN:\n"
                texto_completo += self.formatear_matriz(datos['matrices_txt'][0])
                
            txt_matriz.setText(texto_completo)
            h_layout.addWidget(txt_matriz, stretch=1)
            
            fig = Figure(figsize=(4, 3))
            canv = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.bar(self.nombres_clases, datos['clases'], color='#007bff')
            ax.set_ylim(0, 105)
            ax.set_title(f"Eficiencia por Clase")
            for i, p in enumerate(datos['clases']):
                ax.text(i, p + 2, f"{p:.1f}%", ha='center')
            fig.tight_layout()
            h_layout.addWidget(canv, stretch=1)
            
            tabs_dist.addTab(widget_contenido, f"Distancia: {distancia}")
            
        return tabs_dist

    def formatear_matriz(self, matriz):
        texto = f"{'':<12}" + "".join([f"{n:<12}" for n in self.nombres_clases]) + f"{'Suma':<10}\n"
        for i, fila in enumerate(matriz):
            texto += f"{self.nombres_clases[i]:<12}" + "".join([f"{val:<12}" for val in fila]) + f"{sum(fila):<10}\n"
        return texto

    def mostrar_grafica_final(self):
        DialogoGraficaFinal(self.historial, self.nombres_clases, self).exec()

class DialogoGraficaFinal(QDialog):
    def __init__(self, historial, nombres_clases, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rendimiento Global y Rankings")
        self.resize(1100, 850)
        
        layout = QHBoxLayout()
        
        # Panel izquierdo: 3 gráficas de barras (una por distancia)
        panel_grafica = QVBoxLayout()
        fig = Figure(figsize=(7, 9))
        canv = FigureCanvas(fig)
        
        # Colores similares a los de tu imagen de referencia
        colores_barras = ['#0065a3', '#6a0dad', '#006400'] # Azul, Morado, Verde
        metodos = ["Resustitución", "Cross-Validation", "Leave-One-Out"]
        distancias = ["Euclidiana", "Mahalanobis", "Probabilidad"]
        
        x_pos = np.arange(len(metodos))
        
        for idx, dist in enumerate(distancias):
            ax = fig.add_subplot(3, 1, idx + 1)
            
            valores = []
            nombres_x = []
            
            # Recopilar el porcentaje global de cada método para esta distancia
            for met in metodos:
                valores.append(historial[dist][met]['global'])
                nombres_x.append(historial[dist][met]['nombre_mostrar'])
            
            # Crear la gráfica de barras
            barras = ax.bar(x_pos, valores, color=colores_barras, width=0.5, edgecolor='black')
            
            # Formato de cada subplot
            ax.set_xticks(x_pos)
            ax.set_xticklabels(nombres_x, fontweight='bold')
            ax.set_ylim(0, 115) # Margen extra arriba para que quepa el texto
            ax.set_ylabel("Eficiencia Global (Accuracy %)")
            ax.set_title(f"Comparativa de Métodos de Validación\nDistancia: {dist}", fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.6, axis='y') # Solo cuadricula horizontal
            
            # Poner el texto del porcentaje exacto arriba de cada barra
            for barra in barras:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2, altura + 2, 
                        f"{altura:.2f}%", ha='center', fontweight='bold', fontsize=10)
        
        fig.tight_layout() # Ajusta el espacio para que no se encimen
        
        panel_grafica.addWidget(canv)
        layout.addLayout(panel_grafica, stretch=3)
        
        # Panel derecho: Rankings Globales
        panel_ranking = QVBoxLayout()
        lbl_ranking = QLabel("<b>RANKINGS DE RENDIMIENTO GLOBAL</b>")
        lbl_ranking.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_ranking.addWidget(lbl_ranking)
        
        for dist in distancias:
            datos_dist = []
            for met in metodos:
                datos_dist.append((historial[dist][met]['nombre_mostrar'], historial[dist][met]['global']))
                
            # Ordenar de mayor a menor para sacar el 1er, 2do y 3er lugar
            datos_dist.sort(key=lambda x: x[1], reverse=True)
            
            txt = QTextEdit()
            txt.setReadOnly(True)
            contenido = f"MÉTRICA: {dist.upper()}\n"
            contenido += f"1er: {datos_dist[0][0]} ({datos_dist[0][1]:.2f}%)\n"
            contenido += f"2do: {datos_dist[1][0]} ({datos_dist[1][1]:.2f}%)\n"
            contenido += f"3er: {datos_dist[2][0]} ({datos_dist[2][1]:.2f}%)\n"
            txt.setText(contenido)
            txt.setStyleSheet("background-color: white; border: 1px solid #c0c4cc; border-radius: 5px; font-size: 14px;")
            txt.setFixedHeight(100) 
            panel_ranking.addWidget(txt)
            
        layout.addLayout(panel_ranking, stretch=1)
        self.setLayout(layout)

class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clasificador de IA")
        self.resize(1200, 700)
        self.aplicar_estilo_claro()

        self.ruta_actual = None
        self.nombres_clases = []
        self.num_reps = 0
        self.clase_actual_idx = 0
        self.puntos_por_clase = []
        self.selector_rect = None

        self.configurar_interfaz()

    def configurar_interfaz(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)

        panel_controles = QVBoxLayout()

        grupo_imagen = QGroupBox("1. Imagen Base")
        layout_imagen = QVBoxLayout()
        self.btn_cargar = QPushButton("Cargar Imagen")
        self.lbl_ruta_imagen = QLabel("Ninguna imagen")
        layout_imagen.addWidget(self.btn_cargar)
        layout_imagen.addWidget(self.lbl_ruta_imagen)
        grupo_imagen.setLayout(layout_imagen)
        panel_controles.addWidget(grupo_imagen)

        self.grupo_config = QGroupBox("2. Parámetros")
        layout_config = QVBoxLayout()
        self.input_num_clases = QLineEdit()
        self.input_reps = QLineEdit("100")
        layout_config.addWidget(QLabel("¿Cuántas clases hay?:"))
        layout_config.addWidget(self.input_num_clases)
        layout_config.addWidget(QLabel("¿Cuántos representantes?:"))
        layout_config.addWidget(self.input_reps)
        
        self.btn_confirmar_params = QPushButton("Confirmar")
        layout_config.addWidget(self.btn_confirmar_params)
        
        self.grupo_config.setLayout(layout_config)
        self.grupo_config.setEnabled(False)
        panel_controles.addWidget(self.grupo_config)

        self.grupo_extraccion = QGroupBox("3. Selección")
        layout_extra = QVBoxLayout()
        self.lbl_instrucciones = QLabel("Esperando parámetros...")
        self.btn_extraer_datos = QPushButton("Enviar al Modelo")
        self.btn_extraer_datos.setEnabled(False)
        layout_extra.addWidget(self.lbl_instrucciones)
        layout_extra.addWidget(self.btn_extraer_datos)
        self.grupo_extraccion.setLayout(layout_extra)
        panel_controles.addWidget(self.grupo_extraccion)

        self.grupo_evaluacion = QGroupBox("4. Procesamiento")
        layout_eval = QVBoxLayout()
        self.btn_evaluar = QPushButton("Ejecutar Evaluación Completa\n(9 Escenarios)")
        self.btn_evaluar.setStyleSheet("background-color: #28a745;")
        layout_eval.addWidget(self.btn_evaluar)
        self.grupo_evaluacion.setLayout(layout_eval)
        self.grupo_evaluacion.setEnabled(False)
        panel_controles.addWidget(self.grupo_evaluacion)

        self.btn_reiniciar = QPushButton("Reiniciar y Hacer Nuevas Clases")
        self.btn_reiniciar.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; padding: 10px; margin-top: 15px;")
        self.btn_reiniciar.setEnabled(False) 
        panel_controles.addWidget(self.btn_reiniciar)

        panel_controles.addStretch()
        layout_principal.addLayout(panel_controles, stretch=1)

        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_axis_off()
        layout_principal.addWidget(self.canvas, stretch=3)

    def aplicar_estilo_claro(self):
        self.setStyleSheet("QMainWindow { background-color: #f0f2f5; } QLabel, QGroupBox, QLineEdit { color: black; font-family: 'Consolas'; font-size: 13px; } QGroupBox { border: 1px solid #c0c4cc; margin-top: 15px; font-weight: bold; background-color: #ffffff; border-radius: 5px; } QPushButton { background-color: #007bff; border: 1px solid #0056b3; padding: 8px; font-weight: bold; color: white; } QPushButton:disabled { background-color: #e0e0e0; color: #7a7a7a; } QLineEdit { background-color: white; border: 1px solid gray; padding: 5px; }")

    def seleccionar_archivo_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        return ruta

    def mostrar_imagen(self, ruta):
        self.ruta_actual = ruta
        self.ax.clear()
        self.ax.set_axis_on()
        self.ax.imshow(np.array(Image.open(ruta)))
        self.lbl_ruta_imagen.setText(ruta.split('/')[-1])
        self.canvas.draw()

    def habilitar_panel_parametros(self):
        self.grupo_config.setEnabled(True)
        self.btn_reiniciar.setEnabled(True)

    def limpiar_interfaz(self):
        self.nombres_clases = []
        self.puntos_por_clase = []
        self.clase_actual_idx = 0
        
        self.btn_extraer_datos.setEnabled(False)
        self.grupo_evaluacion.setEnabled(False)
        self.grupo_config.setEnabled(True)
        self.lbl_instrucciones.setText("Esperando parámetros...")
        
        if self.selector_rect:
            self.selector_rect.set_active(False)
            self.selector_rect = None
            
        if self.ruta_actual:
            self.mostrar_imagen(self.ruta_actual)

    def obtener_parametros(self):
        try: return int(self.input_num_clases.text()), int(self.input_reps.text())
        except ValueError: return -1, -1

    def solicitar_nombres_clases(self, num_clases):
        dialogo = DialogoNombresClases(num_clases, self)
        if dialogo.exec() == QDialog.DialogCode.Accepted: return dialogo.obtener_nombres()
        return None

    def iniciar_seleccion_roi(self):
        self.grupo_config.setEnabled(False)
        self.puntos_por_clase = []
        self.clase_actual_idx = 0
        self.actualizar_instrucciones_roi()
        self.selector_rect = RectangleSelector(self.ax, self._al_dibujar_rectangulo, useblit=True, button=[1], minspanx=5, minspany=5, interactive=True)

    def actualizar_instrucciones_roi(self):
        if self.clase_actual_idx < len(self.nombres_clases):
            self.lbl_instrucciones.setText(f"Dibuja rectángulo para: {self.nombres_clases[self.clase_actual_idx]}")
            self.canvas.draw()
        else:
            self.lbl_instrucciones.setText("¡Selección terminada!")
            self.selector_rect.set_active(False)
            self.btn_extraer_datos.setEnabled(True)
            self.canvas.draw()

    def _al_dibujar_rectangulo(self, eclick, erelease):
        if self.clase_actual_idx >= len(self.nombres_clases):
            return

        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        
        if xmin == xmax or ymin == ymax:
            self.mostrar_error("Área inválida. Debes dibujar un rectángulo visible.")
            return

        x_coords = np.random.randint(xmin, xmax, self.num_reps)
        y_coords = np.random.randint(ymin, ymax, self.num_reps)
        self.puntos_por_clase.append(list(zip(x_coords, y_coords)))
        
        colores = ['red', 'blue', 'orange', 'cyan', 'magenta', 'yellow', 'white', 'black']
        self.ax.scatter(x_coords, y_coords, c=colores[self.clase_actual_idx % len(colores)], s=5, label=self.nombres_clases[self.clase_actual_idx])
        self.ax.legend()
        self.clase_actual_idx += 1
        self.actualizar_instrucciones_roi()

    def obtener_coordenadas_seleccionadas(self):
        return self.puntos_por_clase

    def habilitar_panel_evaluacion(self):
        self.btn_extraer_datos.setEnabled(False)
        self.grupo_evaluacion.setEnabled(True)

    def mostrar_informacion(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_error(self, mensaje):
        QMessageBox.warning(self, "Atención", mensaje)

    def mostrar_resultados_completos(self, historial):
        DialogoResultadosCompletos(historial, self.nombres_clases, self).exec()