#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np #Para manejar vectores y calculos matemáticos
from PyQt6.QtWidgets import QMessageBox #Para mensajes emergentes
from Modelo.modelo import Modelo 
from Vista.vista import VistaPrincipal

class Controlador:
    
    """
    Crea una instancia del modelo y la vista.
    """
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VistaPrincipal()
        
        #Conecta las acciones de la interfaz con los métodos del controlador
        self.vista.funcion_procesar = self.procesar_datos
        self.vista.btn_mostrar_seleccion.clicked.connect(self.mostrar_seleccionado)
        
        #Lista vacía que guarda los vectores ingresados por el usuario
        self.historial_vectores = []

        self.centro_base = [self.modelo.u1, self.modelo.u2, self.modelo.u3, 
                            self.modelo.u4, self.modelo.u5, self.modelo.u6]

        #Obtiene las 6 clases base del modelo.
        self.vectores_base = [self.modelo.C1, self.modelo.C2, self.modelo.C3, 
                              self.modelo.C4, self.modelo.C5, self.modelo.C6]
        
        #Dibuja las 6 clases en la pantalla al iniciar el programa.
        self.vista.dibujar_vectores(self.vectores_base, self.centro_base)

    """
    Recibe las coordenadas X e Y como cadenas.
    """
    def procesar_datos(self, x_str, y_str):

        #Captura errores en caso que el usuario no ingrese números válidos.
        try: 
            #Convierte las cadenas de texto a número flotante.
            x_num = float(x_str)
            y_num = float(y_str)

            #Crea el nuevo vector con las coordenadas que ingresó el usuario.
            vector_nuevo = np.array([x_num, y_num]) 
            
            #Pasa el vector nuevo al modelo para que se encargue de la clasificación.
            resultado = self.modelo.clasificar(vector_nuevo, 4.0)

            #Agrega el nuevo vector al historial.
            self.historial_vectores.append(vector_nuevo)
            
            #Formato del texto que se muestra en el historial.
            texto_lista = f"X: {x_num} | Y: {y_num} ➔ {resultado}"
            self.vista.lista_historial.addItem(texto_lista)
            
            #Se selecciona de forma automática el último vector en la lista (el último en ser agregado)
            ultimo_indice = self.vista.lista_historial.count() - 1
            self.vista.lista_historial.setCurrentRow(ultimo_indice)

            #Redibuja la pantalla con las 6 clases y el nuevo vector.
            self.vista.dibujar_vectores(self.vectores_base, self.centro_base, vector_nuevo)

            #Ventana emergente que muestra el resultado de la clasificación.
            QMessageBox.information(self.vista, "Resultado", resultado)

        #En caso que ocurra un error convirtiendo las coordenadas, se muestra un mensaje de error.
        except ValueError: 
            QMessageBox.warning(self.vista, "Error", "Ingresa números válidos.")

    """
    Obtiene la posición del vector seleccionado en el historial.
    En caso de que haya algo seleccionado, se obtiene el vector del historial y lo dibuja en la pantalla.
    En caso contrario, se muestra un mensaje para que seleccione algún vector.
    """
    def mostrar_seleccionado(self):
        indice = self.vista.lista_historial.currentRow()
        
        if indice >= 0:
            vector_viejo = self.historial_vectores[indice]
            self.vista.dibujar_vectores(self.vectores_base, self.centro_base, vector_viejo)
        else:
            QMessageBox.warning(self.vista, "Aviso", "Primero selecciona un vector del historial.")