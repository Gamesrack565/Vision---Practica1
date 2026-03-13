import numpy as np

class ControladorCubo:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        
        # Conectar el botón
        self.vista.btn_clasificar.clicked.connect(self.procesar_datos)
        
        # ¡IMPORTANTE! Dibuja la gráfica vacía nada más arrancar el programa
        self.actualizar_grafica()

    def procesar_datos(self):
        vector_lista = self.vista.obtener_vector()
        
        if vector_lista is None:
            self.vista.mostrar_error("Por favor ingresa números válidos.")
            return
            
        vector_prueba = np.array(vector_lista)
        
        # Lógica del modelo
        rgb, cmy, grises = self.modelo.generar_clases()
        # Puedes cambiar "euclidiana" por "mahalanobis" o "probabilidad"
        color, clase = self.modelo.clasificar_vector(vector_prueba, metodo="euclidiana")

        resultado_texto = f"El punto tiende al color <b>{color}</b>.<br>Por lo tanto, pertenece a la <b>{clase}</b>."
        self.vista.mostrar_resultado(resultado_texto)
        
        # Refrescar la gráfica con el nuevo punto
        self.actualizar_grafica(vector_prueba)

    def dibujar_caras_cubo(self, ax):
        # Dibuja las líneas que forman el esqueleto del cubo (0 a 1)
        estilo = {'color': 'gray', 'linestyle': '--', 'linewidth': 1.5, 'alpha': 0.7}
        
        # Base (Plano Z=0)
        ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], **estilo)
        # Tapa (Plano Z=1)
        ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [1, 1, 1, 1, 1], **estilo)
        # Postes verticales que unen la base y la tapa
        for x, y in zip([0, 1, 1, 0], [0, 0, 1, 1]):
            ax.plot([x, x], [y, y], [0, 1], **estilo)

    def actualizar_grafica(self, vector_prueba=None):
        ax = self.vista.ax
        ax.clear() # Limpia lo que hubiera antes
        
        rgb, cmy, grises = self.modelo.generar_clases()
        
        # 1. Dibujar la "jaula" del cubo primero
        self.dibujar_caras_cubo(ax)

        # 2. Dibujar las 3 Clases
        ax.scatter(rgb[:,0], rgb[:,1], rgb[:,2], c='red', s=100, label='Clase 1 (RGB)')
        ax.scatter(cmy[:,0], cmy[:,1], cmy[:,2], c='cyan', s=100, label='Clase 2 (CMY)')
        ax.scatter(grises[:,0], grises[:,1], grises[:,2], c='black', s=100, label='Clase 3 (Gris)')


        # --- AGREGAR TEXTOS EN LAS ESQUINAS ---
        # Diccionario con las coordenadas y el nombre que aparecerá en la gráfica
        etiquetas_colores = {
            (0, 0, 0): "Negro",
            (1, 1, 1): "Blanco",
            (1, 0, 0): "Rojo",
            (0, 1, 0): "Verde",
            (0, 0, 1): "Azul",
            (0, 1, 1): "Cian",
            (1, 0, 1): "Magenta",
            (1, 1, 0): "Amarillo"
        }
        
        # Iteramos sobre el diccionario para poner el texto en el espacio 3D
        for coordenadas, nombre in etiquetas_colores.items():
            x, y, z = coordenadas
            # ax.text(x, y, z, texto) coloca la etiqueta. 
            # Le sumamos un poquito a Z (z + 0.05) para que el texto no se encime en la bolita
            ax.text(x, y, z + 0.05, nombre, fontsize=9, fontweight='bold', color='black')
        
        # 3. Dibujar el vector del profesor (si existe y es válido)
        if vector_prueba is not None:
            if self.modelo.validar_limites(vector_prueba):
                ax.scatter(vector_prueba[0], vector_prueba[1], vector_prueba[2], 
                           c='lime', marker='*', s=350, edgecolor='black', label='Vector Evaluado')
            else:
                # Si sale de los límites, lo dibujamos rojo y con una X
                ax.scatter(vector_prueba[0], vector_prueba[1], vector_prueba[2], 
                           c='red', marker='X', s=200, label='Fuera de límite')

        # Configuraciones de estética para que se vea como cubo real
        ax.set_xlim([-0.2, 1.2]) # Damos un poco de margen para ver los bordes
        ax.set_ylim([-0.2, 1.2])
        ax.set_zlim([-0.2, 1.2])
        ax.set_xlabel('Eje R (Rojo)')
        ax.set_ylabel('Eje G (Verde)')
        ax.set_zlabel('Eje B (Azul)')
        ax.legend(loc='upper left', fontsize='small')
        
        # ¡Refrescar el lienzo de PyQt6!
        self.vista.canvas.draw()