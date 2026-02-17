#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np
from PyQt6.QtWidgets import QMessageBox
from Modelo.modelo import Modelo
from Vista.vista import VistaPrincipal

class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VistaPrincipal()
        
        self.vista.funcion_procesar = self.procesar_datos
        self.vista.btn_mostrar_seleccion.clicked.connect(self.mostrar_seleccionado)
        
        self.historial_vectores = []

        self.vectores_base = [self.modelo.C1, self.modelo.C2, self.modelo.C3, 
                              self.modelo.C4, self.modelo.C5, self.modelo.C6]
        self.vista.dibujar_vectores(self.vectores_base)

    def procesar_datos(self, x_str, y_str):
        try: 
            x_num = float(x_str)
            y_num = float(y_str)

            vector_nuevo = np.array([x_num, y_num]) 
            
            #Clasificamos mandando el umbral fijo de 4.0
            resultado = self.modelo.clasificar(vector_nuevo, 4.0)

            self.historial_vectores.append(vector_nuevo)
            
            texto_lista = f"X: {x_num} | Y: {y_num} ➔ {resultado}"
            self.vista.lista_historial.addItem(texto_lista)
            
            ultimo_indice = self.vista.lista_historial.count() - 1
            self.vista.lista_historial.setCurrentRow(ultimo_indice)

            self.vista.dibujar_vectores(self.vectores_base, vector_nuevo)
            QMessageBox.information(self.vista, "Resultado", resultado)

        except ValueError: 
            QMessageBox.warning(self.vista, "Error", "Ingresa números válidos.")

    def mostrar_seleccionado(self):
        indice = self.vista.lista_historial.currentRow()
        
        if indice >= 0:
            vector_viejo = self.historial_vectores[indice]
            self.vista.dibujar_vectores(self.vectores_base, vector_viejo)
        else:
            QMessageBox.warning(self.vista, "Aviso", "Primero selecciona un vector del historial.")