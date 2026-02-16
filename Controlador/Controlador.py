import sys
import numpy as np
from PyQt6.QtWidgets import QMessageBox
from Modelo.modelo import Modelo
from Vista.vista import VistaPrincipal

class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VistaPrincipal()
        self.vista.funcion_procesar = self.procesar_datos
        
        #Dibujar los puntos iniciales al abrir el programa ---
        vectores_iniciales = [self.modelo.C1, self.modelo.C2, self.modelo.C3, 
                              self.modelo.C4, self.modelo.C5, self.modelo.C6]
        self.vista.dibujar_vectores(vectores_iniciales)

    def procesar_datos(self, x_str, y_str):
        try: # <--- AGREGAMOS ESTE TRY
            # 1. Conversión de datos
            x_num = float(x_str)
            y_num = float(y_str)

            # 2. Vector dado por el usuario
            vector_nuevo = np.array([x_num, y_num]) 

            # 3. Clasificación
            resultado = self.modelo.clasificar(vector_nuevo, 4.0)

            # 4. Preparar clusters para la gráfica
            vectores = [self.modelo.C1, self.modelo.C2, self.modelo.C3, 
                        self.modelo.C4, self.modelo.C5, self.modelo.C6]
            
            # 5. Dibujar y mostrar resultado
            self.vista.dibujar_vectores(vectores, vector_nuevo)
            QMessageBox.information(self.vista, "Resultado", resultado)

            # 6. Preguntar si desea continuar
            self.vista.preguntar_nuevo_vector()

        except ValueError: # <--- AHORA SÍ ESTÁ ALINEADO CON EL TRY
            # Este mensaje solo sale si float(x_str) o float(y_str) fallan
            QMessageBox.warning(self.vista, "Error", "Ingresa números válidos.")

        
