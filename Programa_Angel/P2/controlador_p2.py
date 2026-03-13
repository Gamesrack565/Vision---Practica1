import numpy as np
from PyQt6.QtWidgets import QMessageBox # Importación necesaria para las alertas

class ControladorLetras:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.vista.btn_clasificar.clicked.connect(self.procesar_datos)
        
        # Dibujar las letras al iniciar
        self.actualizar_grafica()

    def procesar_datos(self):
        vector_prueba = self.vista.obtener_vector()
        if vector_prueba is None:
            QMessageBox.warning(self.vista, "Error", "Ingresa números válidos.")
            return

        clases = self.modelo.generar_letras()
        centros = self.modelo.calcular_centroides(clases)
        
        indice = self.modelo.clasificar(vector_prueba, centros, umbral_fondo=2.5)
        
        # AGREGADO: La clase 4 para la letra M
        nombres = ["Clase 1 (Letra A)", "Clase 2 (Letra H)", "Clase 3 (Letra P)", "Clase 4 (Letra M)"]
        
        if indice == -1:
            texto = "El vector cayó en el <b>Fondo</b>. NO pertenece a ninguna clase."
        else:
            texto = f"El vector pertenece a la <b>{nombres[indice]}</b>."
            
        self.vista.mostrar_resultado(texto)
        self.actualizar_grafica(vector_prueba)

    def actualizar_grafica(self, vector_prueba=None):
        ax = self.vista.ax
        ax.clear()
        
        clases = self.modelo.generar_letras()
        
        # AGREGADO: 4 colores y 4 etiquetas para coincidir con las 4 clases
        colores = ['blue', 'green', 'red', 'purple']
        etiquetas = ['A (Clase 1)', 'H (Clase 2)', 'P (Clase 3)', 'M (Clase 4)']
        
        # Dibujar los 150 puntos de cada letra
        for i, clase in enumerate(clases):
            ax.scatter(clase[:,0], clase[:,1], c=colores[i], label=etiquetas[i], s=10)
            
        if vector_prueba is not None:
            ax.scatter(vector_prueba[0], vector_prueba[1], c='black', marker='X', s=200, label='Vector (ah)')

        # SIMULACIÓN DE IMREF2D (Cuadrícula y límites fijos ampliados para la M)
        ax.set_xlim(-2, 26) # Ampliado de 16 a 26
        ax.set_ylim(-2, 8)
        ax.set_xticks(np.arange(-2, 27, 1)) # Ampliado hasta 27
        ax.set_yticks(np.arange(-2, 9, 1))
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        
        ax.set_title("Procedimiento IMREF2D - Reconocimiento de Patrones")
        ax.legend(loc='upper right')
        
        self.vista.canvas.draw()