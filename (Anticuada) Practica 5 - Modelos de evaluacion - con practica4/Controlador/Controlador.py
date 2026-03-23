from PyQt6.QtWidgets import QFileDialog
import numpy as np

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.clases_activas = ["Negro", "Rojo", "Amarillo"]
        self.conectar_senales()

    def conectar_senales(self):
        self.vista.btn_cargar_imagen.clicked.connect(self.cargar_imagen)
        self.vista.btn_confirmar_clases.clicked.connect(self.validar_cantidad_clases)
        self.vista.btn_generar_reps.clicked.connect(self.generar_representantes)
        self.vista.btn_clasificar.clicked.connect(self.evaluar_punto)
        self.vista.btn_evaluar.clicked.connect(self.evaluar_rendimiento) # NUEVO CONECTOR
        self.vista.btn_reiniciar.clicked.connect(self.reiniciar_programa)

    def cargar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Selecciona una imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if ruta:
            self.modelo.establecer_imagen(ruta)
            self.vista.lbl_ruta_imagen.setText(ruta.split('/')[-1]) 
            self.vista.mostrar_imagen_cuadricula(ruta, modelo=None)
            self.vista.mostrar_informacion("Paso 1", "Imagen cargada correctamente.\n\nAhora, observa la imagen y escribe cuántas clases (franjas) ves en ella.")
            
            self.vista.btn_cargar_imagen.setEnabled(False)
            self.vista.input_num_clases.setEnabled(True)
            self.vista.btn_confirmar_clases.setEnabled(True)

    def validar_cantidad_clases(self):
        try:
            num_clases = int(self.vista.input_num_clases.text())
        except ValueError:
            self.vista.mostrar_error("Por favor, ingresa un número entero.")
            return

        if num_clases not in [1, 2, 3]:
            self.vista.mostrar_error("El número de clases debe ser 1, 2 o 3.")
            return

        opciones_disponibles = ["Negro", "Rojo", "Amarillo"]

        if num_clases == 3:
            self.clases_activas = opciones_disponibles
        else:
            seleccion = self.vista.solicitar_nombres_clases(num_clases, opciones_disponibles)
            if not seleccion:
                return 
            self.clases_activas = seleccion

        self.vista.input_num_clases.setEnabled(False)
        self.vista.btn_confirmar_clases.setEnabled(False)
        self.vista.mostrar_informacion("Paso 2", "¡Correcto!\n\nAhora indica la cantidad de representantes por clase que deseas generar y presiona 'Generar Puntos'.")
        self.vista.input_reps.setEnabled(True)
        self.vista.btn_generar_reps.setEnabled(True)

    def generar_representantes(self):
        try:
            num_reps = int(self.vista.input_reps.text())
            if num_reps <= 0:
                raise ValueError
        except ValueError:
            self.vista.mostrar_error("El número de representantes debe ser un número entero positivo.")
            return

        self.modelo.inicializar_datos_entrenamiento(num_reps, self.clases_activas)
        self.vista.mostrar_imagen_cuadricula(self.modelo.ruta_imagen, self.modelo)
        self.vista.mostrar_informacion("Listo", "Los puntos han sido generados.\n\nYa puedes clasificar puntos o evaluar el rendimiento del clasificador.")

        self.vista.combo_metodo.setEnabled(True)
        self.vista.input_px.setEnabled(True)
        self.vista.input_py.setEnabled(True)
        self.vista.btn_clasificar.setEnabled(True)
        
        # Habilitar nueva sección de evaluación
        self.vista.combo_tipo_eval.setEnabled(True)
        self.vista.btn_evaluar.setEnabled(True)

    def evaluar_punto(self):
        try:
            px = float(self.vista.input_px.text())
            py = float(self.vista.input_py.text())
        except ValueError:
            self.vista.mostrar_error("Las coordenadas del punto deben ser numéricas.")
            return

        metodo_seleccionado = self.vista.combo_metodo.currentText()
        resultados = self.modelo.clasificar_punto(px, py)
        
        self.vista.mostrar_resultados(metodo_seleccionado, resultados)
        self.vista.mostrar_imagen_cuadricula(self.modelo.ruta_imagen, self.modelo, resultados["Punto"])

    # NUEVO: Función para ejecutar la evaluación
    def evaluar_rendimiento(self):
        tipo_eval = self.vista.combo_tipo_eval.currentText()
        metodo_distancia = self.vista.combo_metodo.currentText() 
        
        # Calcular según el método seleccionado en la Vista
        if tipo_eval == "Resustitución":
            matriz = self.modelo.evaluar_resustitucion(metodo_distancia)
        elif tipo_eval == "Cross-Validation":
            matriz = self.modelo.evaluar_cross_validation(metodo_distancia)
        elif tipo_eval == "Leave-One-Out":
            matriz = self.modelo.evaluar_leave_one_out(metodo_distancia)
            
        # Calcular exactitud (Performance)
        correctos = np.trace(matriz)
        total = np.sum(matriz)
        performance = (correctos / total) * 100 if total > 0 else 0
        
        # Generar texto con la Matriz de Confusión formateada
        texto_matriz = f"Métrica Usada: {metodo_distancia}\n\nMatriz de Confusión:\n"
        texto_matriz += f"{'':<12}" + "".join([f"{c:<10}" for c in self.modelo.nombres_clases]) + "\n"
        for i, fila in enumerate(matriz):
            texto_matriz += f"{self.modelo.nombres_clases[i]:<12}" + "".join([f"{val:<10}" for val in fila]) + "\n"
            
        texto_matriz += f"\nPerformance General: {performance:.2f}%"
        
        self.vista.mostrar_informacion(f"Resultados: {tipo_eval}", texto_matriz)

    def reiniciar_programa(self):
        self.clases_activas = ["Negro", "Rojo", "Amarillo"]
        self.vista.btn_cargar_imagen.setEnabled(True)
        
        self.vista.input_num_clases.setEnabled(False)
        self.vista.input_num_clases.clear()
        self.vista.btn_confirmar_clases.setEnabled(False)
        
        self.vista.input_reps.setEnabled(False)
        self.vista.btn_generar_reps.setEnabled(False)
        
        self.vista.combo_metodo.setEnabled(False)
        self.vista.input_px.setEnabled(False)
        self.vista.input_py.setEnabled(False)
        self.vista.input_px.clear()
        self.vista.input_py.clear()
        self.vista.btn_clasificar.setEnabled(False)
        
        # Reiniciar UI de evaluación
        self.vista.combo_tipo_eval.setEnabled(False)
        self.vista.btn_evaluar.setEnabled(False)
        
        self.modelo.ruta_imagen = None
        self.vista.lbl_ruta_imagen.setText("Ninguna imagen seleccionada")
        
        self.vista.ax.clear()
        self.vista.ax.set_title("Esperando imagen...")
        self.vista.ax.set_axis_off()
        self.vista.canvas.draw()