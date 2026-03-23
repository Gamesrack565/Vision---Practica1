
import numpy as np 
import matplotlib.image as mpimg
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from PyQt6.QtCore import QTimer
from Modelo.modelo import Modelo 
from Vista.vista import VistaPrincipal, DialogoBaseDatos, DialogoMenuClases
# Asumiendo que tus archivos se llaman modelo.py y vista.py y están en la misma carpeta o módulos accesibles
# from modelo import Modelo
# from vista import VistaPrincipal, DialogoBaseDatos, DialogoMenuClases

class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VistaPrincipal()
        
        self.imagen_matriz = None
        self.modo_manual = False
        self.clases_pendientes = 0
        self.clase_actual_idx = 1
        self.ultimo_vector = None
        
        self.reps_global = 1000
        self.disp_global = 30.0

        self.vista.btn_cargar_img.clicked.connect(self.cargar_imagen)
        self.vista.btn_configurar.clicked.connect(self.iniciar_configuracion)
        self.vista.btn_ver_bd.clicked.connect(self.ver_base_datos)
        self.vista.btn_ingresar_vector.clicked.connect(self.ingresar_vector_manual)
        self.vista.btn_limpiar.clicked.connect(self.vista.lista_historial.clear)
        self.vista.combo_metodo.currentTextChanged.connect(self.reclasificar_ultimo)
        
        self.vista.canvas.mpl_connect('button_press_event', self.on_click_imagen)
        QTimer.singleShot(500, self.cargar_imagen)

    def cargar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Seleccionar Imagen", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if ruta:
            img = mpimg.imread(ruta)
            if img.dtype == np.float32 or img.dtype == np.float64:
                if img.max() <= 1.0: img = (img * 255).astype(np.uint8)
            
            self.imagen_matriz = img
            self.modelo.limpiar_modelo()
            self.ultimo_vector = None
            self.vista.dibujar_imagen_y_puntos(self.imagen_matriz, [], [])
            self.vista.label_estado.setText("Imagen cargada. Da clic en Configurar Clases.")

    def ver_base_datos(self):
        if not self.modelo.clases_rgb:
            QMessageBox.warning(self.vista, "Aviso", "Aún no hay clases.")
            return
        dialogo = DialogoBaseDatos(self.modelo.nombres_clases, self.modelo.clases_rgb, self.vista)
        dialogo.exec()

    def adivinar_color(self, r, g, b):
        if r > 180 and g > 180 and b > 180: return "Pato Blanco"
        if r > 180 and g > 180 and b < 100: return "Patito Amarillo"
        if g > max(r, b) and g > 80: return "Pasto Verde"
        if r > max(g, b) and r > 150: return "Flores Rojas"
        if b > max(r, g) and b > 100: return "Cielo Azul"
        return "Objeto Desconocido"

    def iniciar_configuracion(self):
        if self.imagen_matriz is None: return

        num_clases_max = 5 # Define aquí tu límite basado en el Modelo
        num, ok = QInputDialog.getInt(self.vista, "Clases", "¿Cuántas clases ves?", 1, 1, 20)

        if ok:
            if num > num_clases_max:
                QMessageBox.warning(self.vista, "Límite Superado", 
                                    f"Has superado la cantidad de clases definidas ({num_clases_max}).")
                return # Detiene la ejecución
            reps, ok_r = QInputDialog.getInt(self.vista, "Representantes", "¿Cuántos representantes para TODAS las clases?", 1000, 10, 100000)
            if ok_r:
                disp, ok_d = QInputDialog.getDouble(self.vista, "Dispersión", "Tolerancia/Dispersión global (Ej. 30):", 30.0, 1.0, 200.0)
                if ok_d:
                    self.reps_global = reps
                    self.disp_global = disp
                    
                    opciones = ["Por mí mismo (Clics)", "Por Menú (Tabla de Rangos)"]
                    eleccion, ok2 = QInputDialog.getItem(self.vista, "Método", "¿Deseas ubicar tu clase por ti mismo o por menú?", opciones, 0, False)
                    
                    if ok2:
                        self.modelo.limpiar_modelo()
                        if eleccion == "Por Menú (Tabla de Rangos)":
                            # CORRECCIÓN: Le pedimos los datos al modelo
                            alto, ancho = self.imagen_matriz.shape[0], self.imagen_matriz.shape[1]
                            clases_predef = self.modelo.obtener_clases_predefinidas(alto, ancho)
                            
                            dialogo = DialogoMenuClases(num, clases_predef, self.vista)
                            if dialogo.exec():
                                datos = dialogo.obtener_datos()
                                for d in datos:
                                    nombre, xmin, xmax, ymin, ymax = d
                                    self.modelo.agregar_clase_desde_rangos(nombre, xmin, xmax, ymin, ymax, self.reps_global, self.imagen_matriz)
                                self.actualizar_grafica()
                                QMessageBox.information(self.vista, "Éxito", "Clases generadas mediante rangos aleatorios.")
                        else:
                            self.modo_manual = True
                            self.clases_pendientes = num
                            self.clase_actual_idx = 1
                            self.vista.cambiar_tema_manual() 
                            self.vista.label_estado.setText(f"Modo Clics: Toca la Clase {self.clase_actual_idx}")

    def on_click_imagen(self, event):
        if self.imagen_matriz is None or event.xdata is None or event.ydata is None: return
        x, y = int(event.xdata), int(event.ydata)

        if self.modo_manual and self.clases_pendientes > 0:
            color = self.imagen_matriz[y, x][:3]
            nombre_adivinado = self.adivinar_color(*color)
            
            resp = QMessageBox.question(self.vista, "Confirmación", 
                f"Usted ha seleccionado: {nombre_adivinado} (RGB: {color}).\n¿Estás de acuerdo o quieres otra clase?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if resp == QMessageBox.StandardButton.Yes:
                nombre, ok_n = QInputDialog.getText(self.vista, "Nombre", "Confirma el nombre de la clase:", text=nombre_adivinado)
                if ok_n:
                    self.modelo.agregar_clase_desde_clic(nombre, x, y, self.reps_global, self.disp_global, self.imagen_matriz)
                    self.actualizar_grafica()
                    
                    self.clases_pendientes -= 1
                    self.clase_actual_idx += 1
                    
                    if self.clases_pendientes == 0:
                        self.modo_manual = False
                        self.vista.cambiar_tema_color(self.vista.combo_metodo.currentText()) 
                        self.vista.label_estado.setText("Entrenamiento finalizado.")
                        QMessageBox.information(self.vista, "Fin", "Todas las clases entrenadas.")
                    else:
                        self.vista.label_estado.setText(f"Modo Clics: Toca la Clase {self.clase_actual_idx}")

        elif not self.modo_manual:
            self.clasificar_pixel(x, y)

    def ingresar_vector_manual(self):
        if self.imagen_matriz is None: return
        x_str, ok_x = QInputDialog.getText(self.vista, "X", "Ingresa coordenada X:")
        if ok_x:
            y_str, ok_y = QInputDialog.getText(self.vista, "Y", "Ingresa coordenada Y:")
            if ok_y:
                self.clasificar_pixel(int(x_str), int(y_str))

    def clasificar_pixel(self, x, y):
        try:
            alto, ancho = self.imagen_matriz.shape[0], self.imagen_matriz.shape[1]
            if not (0 <= x < ancho and 0 <= y < alto):
                QMessageBox.warning(self.vista, "Error", "Coordenadas fuera de la imagen.")
                return

            color_rgb = self.imagen_matriz[y, x][:3]
            metodo = self.vista.combo_metodo.currentText()
            
            # 1. Llamamos al modelo para que haga el cálculo
            resultado = self.modelo.clasificar(color_rgb, metodo.lower())

            self.ultimo_vector = (x, y)
            self.actualizar_grafica()
            
            # 2. Agregar al historial lateral (como ya lo hacías)
            texto = f"X:{x}, Y:{y} [RGB:{color_rgb[0]},{color_rgb[1]},{color_rgb[2]}] ➔ {resultado}"
            self.vista.lista_historial.addItem(texto)
            self.vista.lista_historial.setCurrentRow(self.vista.lista_historial.count() - 1)
            
            # --- NUEVO: AVISOS VISUALES PARA EL USUARIO ---
            # Mostramos el resultado en la barra superior de estado
            self.vista.label_estado.setText(f"¡El vector pertenece a: {resultado}!")
            
            # Hacemos que salte una ventana emergente con el resultado
            nombre_limpio = resultado.split('(')[0].strip() # Quitamos los porcentajes para el título
            QMessageBox.information(self.vista, "Resultado de Clasificación", 
                                    f"El píxel seleccionado es:\n\n{resultado}\n\n"
                                    f"RGB: {color_rgb}")
            
        except Exception as e:
            pass

    def reclasificar_ultimo(self):
        if self.ultimo_vector is not None:
            self.clasificar_pixel(self.ultimo_vector[0], self.ultimo_vector[1])

    def actualizar_grafica(self):
        self.vista.dibujar_imagen_y_puntos(self.imagen_matriz, self.modelo.puntos_xy, self.modelo.nombres_clases, self.ultimo_vector)
