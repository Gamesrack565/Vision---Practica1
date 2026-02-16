import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMessageBox

from Modelo.modelo import Modelo
from Vista.vista import VistaPrincipal

class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VistaPrincipal()

        # Esto es un truco de conexión: le decimos a la vista que, cuando tenga 
        # las coordenadas listas, llame a nuestra función 'procesar_datos' de aquí abajo.
        self.vista.funcion_procesar = self.procesar_datos

    def procesar_datos(self, x_str, y_str):
        #Convierte x_str y y_str a números decimales (float).
        x_num = float(x_str)
        y_num = float(y_str)
        
        #VEctor dado por el usuario
        vector_nuevo = np.array([x_num, y_num]) 

        resultado = self.modelo.clasificar(vector_nuevo, 4.0)

        QMessageBox.information(self.vista, "Resultado de Clasificación", resultado)
