import numpy as np
import matplotlib.image as mpimg
from PyQt6.QtWidgets import QFileDialog, QMessageBox

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        
        self.imagen_actual = None
        self.estado = "ESPERANDO" 
        
        # --- AQUÍ ESTÁ LA TRAMPA: Las coordenadas que definiste ---
        # Formato: ("Nombre", X_min, X_max, Y_min, Y_max)
        # Formato: ("Nombre", X_min, X_max, Y_min, Y_max)
        self.regiones_clases = [
            # Un cuadro justo en el pecho del pato grande
            ("Pato Blanco", 1500, 1700, 550, 750),     
            # Un cuadro justo en el cuerpo del patito de la extrema derecha
            ("Patitos Amarillos", 2050, 2250, 1250, 1350),     
            # Un parche de puro pasto en la esquina inferior izquierda
            ("Pasto Verde", 50, 300, 1400, 1500),       
            # Un cuadro muy chiquito apuntando a la flor roja grande de la izquierda
            ("Flores Rojas", 50, 100, 350, 400),      
            # Un rectángulo en la parte superior donde solo hay cielo
            ("Cielo Azul", 1000, 1500, 50, 150)        
        ]
        
        # Colores para graficar los puntos de cada clase
        self.colores_plot = ['#3498db', '#f1c40f', '#2ecc71', '#e74c3c', '#9b59b6']
        
        self.conectar_senales()

    def conectar_senales(self):
        self.vista.btn_cargar.clicked.connect(self.cargar_imagen)
        # Cambiamos el comportamiento del botón de configurar
        self.vista.btn_configurar.clicked.connect(self.entrenamiento_automatico)
        self.vista.btn_limpiar_historial.clicked.connect(self.vista.lista_historial.clear)
        self.vista.btn_nuevo_vector.clicked.connect(self.activar_modo_prediccion)
        
        # Conectar el evento de clic (ahora solo servirá para predecir)
        self.vista.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def cargar_imagen(self):
        archivo, _ = QFileDialog.getOpenFileName(self.vista, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if archivo:
            self.imagen_actual = mpimg.imread(archivo)
            self.vista.mostrar_imagen(self.imagen_actual)
            self.vista.lbl_estado.setText("Imagen cargada. Haz clic en 'Configurar Clases' para entrenar automáticamente.")
            self.estado = "ESPERANDO"

    def entrenamiento_automatico(self):
        if self.imagen_actual is None:
            QMessageBox.warning(self.vista, "Error", "Primero debes cargar una imagen.")
            return

        nombres_clases = []
        datos_entrenamiento_rgb = []
        
        # Como en el código de MATLAB, extraeremos 100 puntos al azar por clase
        puntos_por_clase = 100 
        
        # Obtenemos las dimensiones de la imagen para evitar errores de coordenadas fuera de límite
        alto_img, ancho_img, _ = self.imagen_actual.shape

        # Limpiamos gráficos anteriores si los hubiera
        self.vista.mostrar_imagen(self.imagen_actual) 

        for idx, (nombre, x_min, x_max, y_min, y_max) in enumerate(self.regiones_clases):
            nombres_clases.append(nombre)
            rgb_clase = []
            
            # Seguridad: aseguramos que tus coordenadas no se salgan de la foto real
            x_max = min(x_max, ancho_img - 1)
            y_max = min(y_max, alto_img - 1)
            x_min = max(0, x_min)
            y_min = max(0, y_min)

            # Equivalente a randi([min, max], 1, 100) en MATLAB
            xs = np.random.randint(x_min, x_max + 1, puntos_por_clase)
            ys = np.random.randint(y_min, y_max + 1, puntos_por_clase)
            
            for x, y in zip(xs, ys):
                r, g, b = self.imagen_actual[y, x][:3]
                rgb_clase.append([r, g, b])
            
            datos_entrenamiento_rgb.append(rgb_clase)
            
            # Dibujar los puntitos en la interfaz como en tu foto de ejemplo
            color = self.colores_plot[idx % len(self.colores_plot)]
            self.vista.ax.scatter(xs, ys, c=color, s=15, label=nombre, alpha=0.7, edgecolors='none')

        # Mostramos la cajita de leyendas en la gráfica
        self.vista.ax.legend(loc='upper right')
        self.vista.canvas.draw()
        
        # Entrenar el modelo matemático con todos los RGBs extraídos
        self.modelo.entrenar_con_pixeles(datos_entrenamiento_rgb, nombres_clases)
        
        self.estado = "LISTO"
        self.vista.lbl_estado.setText("¡Trampa exitosa! Se extrajeron 100 puntos automáticos por clase. Listo para clasificar.")
        QMessageBox.information(self.vista, "Éxito", "Se han extraído 100 píxeles aleatorios por clase dentro de las coordenadas indicadas.")

    def on_canvas_click(self, event):
        # Esta función ahora SOLO se activa cuando vas a predecir el punto misterioso
        if event.xdata is None or event.ydata is None or self.imagen_actual is None:
            return

        if self.estado == "LISTO" or self.estado == "PREDICIENDO":
            x, y = int(event.xdata), int(event.ydata)
            r, g, b = self.imagen_actual[y, x][:3]

            metodo = self.vista.combo_metodo.currentText()
            if metodo == "Ninguna":
                QMessageBox.warning(self.vista, "Aviso", "Selecciona un método en la parte inferior primero.")
                return

            vector_rgb = [float(r), float(g), float(b)]
            resultados = self.modelo.clasificar(vector_rgb)
            resultado_final = resultados[metodo]
            
            # Dibujar la cruz roja (Vector Desconocido)
            self.vista.ax.plot(x, y, marker='X', color='red', markersize=10, markeredgecolor='black')
            self.vista.canvas.draw()
            
            # Escribir en el historial
            texto_historial = f"X:{x}, Y:{y} [RGB:{int(r)},{int(g)},{int(b)}] ➔ {resultado_final} ({metodo[:3]})"
            self.vista.lista_historial.addItem(texto_historial)
            self.vista.lista_historial.scrollToBottom()

    def activar_modo_prediccion(self):
        if self.estado != "LISTO":
            QMessageBox.warning(self.vista, "Aviso", "Primero debes configurar las clases.")
            return
        self.vista.lbl_estado.setText("Modo Predicción: Haz clic en cualquier parte de la imagen para clasificar el píxel.")