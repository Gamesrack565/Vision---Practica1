from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, 
                             QMessageBox, QGroupBox, QComboBox, QDialog, QDialogButtonBox)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image
import numpy as np

# =======================================================
# CLASE PARA EL DIÁLOGO EMERGENTE DE SELECCIÓN DE CLASES
# =======================================================
class DialogoSeleccionClases(QDialog):
    def __init__(self, num_clases, opciones, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selección de Clases")
        # Se fuerza un fondo claro para contrarrestar temas oscuros del sistema operativo
        self.setStyleSheet("""
            QDialog { background-color: #f0f2f5; }
            QWidget { color: black; font-family: 'Consolas', monospace; font-size: 13px; }
            QComboBox { background-color: white; border: 1px solid gray; }
        """)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Has indicado que ves {num_clases} clases. ¿Cuáles son?"))
        
        self.combos = []
        for i in range(num_clases):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"Clase {i+1}:"))
            combo = QComboBox()
            combo.addItems(opciones)
            h_layout.addWidget(combo)
            layout.addLayout(h_layout)
            self.combos.append(combo)
        
        self.botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones)
        self.setLayout(layout)

    def obtener_seleccion(self):
        return [combo.currentText() for combo in self.combos]


# =======================================================
# VENTANA PRINCIPAL
# =======================================================
class Vista(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clasificador de Píxeles MVC - Visión Artificial")
        self.resize(1150, 650)
        self.aplicar_estilo_claro()

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)

        panel_controles = QVBoxLayout()

        # 1. Cargar Imagen
        grupo_imagen = QGroupBox("1. Imagen Base")
        layout_imagen = QVBoxLayout()
        self.btn_cargar_imagen = QPushButton("Cargar e Inspeccionar Imagen")
        self.lbl_ruta_imagen = QLabel("Ninguna imagen seleccionada")
        self.lbl_ruta_imagen.setWordWrap(True)
        layout_imagen.addWidget(self.btn_cargar_imagen)
        layout_imagen.addWidget(self.lbl_ruta_imagen)
        grupo_imagen.setLayout(layout_imagen)
        panel_controles.addWidget(grupo_imagen)

        # 2. Configuración de Clases
        grupo_config = QGroupBox("2. Configuración")
        layout_config = QVBoxLayout()
        
        fila_clases = QHBoxLayout()
        lbl_clases = QLabel("¿Cuántas clases ves?:")
        self.input_num_clases = QLineEdit()
        self.input_num_clases.setEnabled(False)
        self.btn_confirmar_clases = QPushButton("Confirmar")
        self.btn_confirmar_clases.setEnabled(False)
        fila_clases.addWidget(lbl_clases)
        fila_clases.addWidget(self.input_num_clases)
        fila_clases.addWidget(self.btn_confirmar_clases)
        layout_config.addLayout(fila_clases)

        fila_reps = QHBoxLayout()
        lbl_reps = QLabel("Representantes:")
        self.input_reps = QLineEdit("100")
        self.input_reps.setEnabled(False)
        self.btn_generar_reps = QPushButton("Generar Puntos")
        self.btn_generar_reps.setEnabled(False)
        fila_reps.addWidget(lbl_reps)
        fila_reps.addWidget(self.input_reps)
        fila_reps.addWidget(self.btn_generar_reps)
        layout_config.addLayout(fila_reps)

        grupo_config.setLayout(layout_config)
        panel_controles.addWidget(grupo_config)

        # 3. Evaluar Punto
        grupo_punto = QGroupBox("3. Evaluación del Punto")
        layout_punto = QVBoxLayout()
        
        layout_metodo = QHBoxLayout()
        lbl_metodo = QLabel("Método:")
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Euclidiana", "Mahalanobis", "Probabilidad"])
        self.combo_metodo.setEnabled(False)
        layout_metodo.addWidget(lbl_metodo)
        layout_metodo.addWidget(self.combo_metodo)
        layout_punto.addLayout(layout_metodo)

        layout_coords = QHBoxLayout()
        lbl_px = QLabel("Px:")
        self.input_px = QLineEdit()
        self.input_px.setEnabled(False)
        layout_coords.addWidget(lbl_px)
        layout_coords.addWidget(self.input_px)
        
        lbl_py = QLabel("Py:")
        self.input_py = QLineEdit()
        self.input_py.setEnabled(False)
        layout_coords.addWidget(lbl_py)
        layout_coords.addWidget(self.input_py)
        layout_punto.addLayout(layout_coords)

        self.btn_clasificar = QPushButton("Clasificar Punto")
        self.btn_clasificar.setEnabled(False) 
        layout_punto.addWidget(self.btn_clasificar)

        grupo_punto.setLayout(layout_punto)
        panel_controles.addWidget(grupo_punto)

        # ================= NUEVO BLOQUE =================
        # 4. Evaluación de Clasificadores (Performance)
        grupo_eval = QGroupBox("4. Evaluación (Performance)")
        layout_eval = QVBoxLayout()
        
        layout_metodo_eval = QHBoxLayout()
        lbl_metodo_eval = QLabel("Tipo:")
        self.combo_tipo_eval = QComboBox()
        self.combo_tipo_eval.addItems(["Resustitución", "Cross-Validation", "Leave-One-Out"])
        self.combo_tipo_eval.setEnabled(False)
        layout_metodo_eval.addWidget(lbl_metodo_eval)
        layout_metodo_eval.addWidget(self.combo_tipo_eval)
        layout_eval.addLayout(layout_metodo_eval)

        self.btn_evaluar = QPushButton("Evaluar Rendimiento")
        self.btn_evaluar.setEnabled(False)
        self.btn_evaluar.setStyleSheet("background-color: #28a745; color: white;") # Botón verde
        layout_eval.addWidget(self.btn_evaluar)
        
        grupo_eval.setLayout(layout_eval)
        panel_controles.addWidget(grupo_eval)
        # ================================================

        # 5. Botón de reinicio general
        self.btn_reiniciar = QPushButton("Reiniciar Programa")
        self.btn_reiniciar.setStyleSheet("background-color: #dc3545; color: white;")
        panel_controles.addWidget(self.btn_reiniciar)
        
        panel_controles.addStretch()
        layout_principal.addLayout(panel_controles, stretch=1)

        # Gráfica
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_title("Esperando imagen...")
        self.ax.set_axis_off()
        
        layout_principal.addWidget(self.canvas, stretch=3)

    def aplicar_estilo_claro(self):
        estilo = """
        QMainWindow { background-color: #f0f2f5; }
        QLabel, QGroupBox, QLineEdit, QComboBox { 
            color: #000000; 
            font-family: 'Consolas', monospace; 
            font-size: 13px; 
        }
        QGroupBox { 
            border: 1px solid #c0c4cc; 
            margin-top: 15px; 
            font-weight: bold; 
            background-color: #ffffff; 
            border-radius: 5px;
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left: 10px; 
            padding: 0 5px 0 5px; 
            color: #0056b3;
        }
        QPushButton { 
            background-color: #007bff; 
            border: 1px solid #0056b3; 
            padding: 8px; 
            border-radius: 4px; 
            font-weight: bold; 
            color: #ffffff;
        }
        QPushButton:hover { background-color: #0056b3; }
        QPushButton:disabled { 
            background-color: #e0e0e0; 
            border: 1px solid #cccccc; 
            color: #7a7a7a; 
        }
        QLineEdit, QComboBox { 
            background-color: #ffffff; 
            border: 1px solid #b0b5bd; 
            color: #000000; 
            padding: 5px; 
            border-radius: 3px;
        }
        QLineEdit:disabled, QComboBox:disabled {
            background-color: #f5f5f5;
            color: #a0a0a0;
        }
        """
        self.setStyleSheet(estilo)

    def solicitar_nombres_clases(self, num_clases, opciones):
        dialogo = DialogoSeleccionClases(num_clases, opciones, self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            seleccion = dialogo.obtener_seleccion()
            if len(set(seleccion)) != len(seleccion):
                self.mostrar_error("No puedes seleccionar la misma clase más de una vez.")
                return None
            return seleccion
        return None

    def mostrar_informacion(self, titulo, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec()

    def mostrar_error(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Aviso")
        msg.setText(mensaje)
        msg.exec()

    def mostrar_resultados(self, metodo, resultados):
        box = QMessageBox()
        box.setWindowTitle("Resultado de Clasificación")

        if metodo == "Euclidiana":
            res = resultados["Euclidiana"]
            texto = f"Resultado Euclidiana:\n{res['ganador']}\n(Distancia mínima calculada: {res['valor']:.2f})"
        elif metodo == "Mahalanobis":
            res = resultados["Mahalanobis"]
            texto = f"Resultado Mahalanobis:\n{res['ganador']}\n(Distancia mínima calculada: {res['valor']:.2f})"
        elif metodo == "Probabilidad":
            res = resultados["Probabilidad"]
            texto = f"Resultado Probabilidad:\n{res['ganador']}\n\nDetalles por clase:\n"
            texto += "\n".join(res['detalle'])

        box.setText(texto)
        box.exec()

    def mostrar_imagen_cuadricula(self, ruta_imagen, modelo=None, punto_usuario=None):
        self.ax.clear()
        self.ax.set_axis_on()

        try:
            imagen_pil = Image.open(ruta_imagen)
            img = np.array(imagen_pil)
            self.ax.imshow(img)
        except Exception as e:
            self.mostrar_error(f"No se pudo cargar la imagen.\nDetalle:\n{str(e)}")
            return

        self.ax.set_title('Inspección de Píxeles' if punto_usuario is None else 'Clasificación Final')
        self.ax.set_xlabel('Coordenada X (Píxeles)')
        self.ax.set_ylabel('Coordenada Y (Píxeles)')
        
        self.ax.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.7)
        self.ax.minorticks_on()
        self.ax.grid(which='minor', color='lightgray', linestyle=':', linewidth=0.5, alpha=0.5)

        if modelo and modelo.clases:
            for i, clase in enumerate(modelo.clases):
                nombre_clase = modelo.nombres_clases[i]
                
                if nombre_clase == "Negro":
                    color_puntos = "white"
                elif nombre_clase == "Rojo":
                    color_puntos = "lightblue"
                elif nombre_clase == "Amarillo":
                    color_puntos = "black"
                else:
                    color_puntos = "blue" 

                self.ax.scatter(clase[:, 0], clase[:, 1], c=color_puntos, label=nombre_clase, alpha=0.6, s=5)
                centro = modelo.centros[i]
                self.ax.plot(centro[0], centro[1], marker='X', color='red', markersize=10, markeredgecolor='white')

        if punto_usuario is not None:
            self.ax.plot(punto_usuario[0], punto_usuario[1], marker='*', color='yellow', markersize=15, markeredgecolor='black', label='Punto Evaluado')
            self.ax.legend(loc='upper right')

        self.figura.tight_layout()
        self.canvas.draw()