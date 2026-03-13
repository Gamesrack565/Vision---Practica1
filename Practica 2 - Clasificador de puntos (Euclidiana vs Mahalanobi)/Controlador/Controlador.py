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
        
        # Conexiones 
        self.vista.funcion_procesar = self.procesar_datos
        self.vista.btn_mostrar_seleccion.clicked.connect(self.mostrar_seleccionado)
        
        # ¡NUEVO! Escuchamos si el usuario toca el combobox o el checkbox para redibujar en vivo
        self.vista.combo_metodo.currentTextChanged.connect(self.actualizar_pantalla)
        self.vista.check_barreras.stateChanged.connect(self.actualizar_pantalla)
        
        self.historial_vectores = []

        self.centro_base = [self.modelo.u1, self.modelo.u2, self.modelo.u3, 
                            self.modelo.u4, self.modelo.u5, self.modelo.u6]
        self.vectores_base = [self.modelo.C1, self.modelo.C2, self.modelo.C3, 
                              self.modelo.C4, self.modelo.C5, self.modelo.C6]
        
        # Dibujo inicial
        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        """Redibuja todo. Revisa si mostrar barreras y qué método usar."""
        metodo = self.vista.combo_metodo.currentText().lower()
        
        # Verificamos si la casilla de "Mostrar Barreras" está marcada
        barreras_calculadas = None
        if self.vista.check_barreras.isChecked():
            # Pedimos al modelo que nos devuelva la geometría de las fronteras
            barreras_calculadas = self.modelo.obtener_parametros_barrera(4.0, metodo)
            
        # Si hay un vector en memoria (para no perder el punto negro), lo recuperamos
        vector_reciente = self.historial_vectores[-1] if self.historial_vectores else None
        
        self.vista.dibujar_vectores(self.vectores_base, self.centro_base, vector_reciente, barreras_calculadas)


    def procesar_datos(self, x_str, y_str):
        try: 
            x_num = float(x_str)
            y_num = float(y_str)
            vector_nuevo = np.array([x_num, y_num]) 
            
            # Tomamos el método seleccionado
            metodo_sel = self.vista.combo_metodo.currentText().lower()
            
            resultado = self.modelo.clasificar(vector_nuevo, 4.0, metodo_sel)

            self.historial_vectores.append(vector_nuevo)
            texto_lista = f"X: {x_num} | Y: {y_num} ➔ {resultado}"
            self.vista.lista_historial.addItem(texto_lista)
            
            ultimo_indice = self.vista.lista_historial.count() - 1
            self.vista.lista_historial.setCurrentRow(ultimo_indice)

            # En vez de dibujar directamente, llamamos a nuestro nuevo actualizador central
            self.actualizar_pantalla()

            QMessageBox.information(self.vista, "Resultado", resultado)

        except ValueError: 
            QMessageBox.warning(self.vista, "Error", "Ingresa números válidos.")


    def mostrar_seleccionado(self):
        indice = self.vista.lista_historial.currentRow()
        if indice >= 0:
            # Ponemos temporalmente ese vector viejo al final de la lista mental 
            # y actualizamos pantalla
            vector_viejo = self.historial_vectores.pop(indice)
            self.historial_vectores.append(vector_viejo)
            
            self.actualizar_pantalla()
        else:
            QMessageBox.warning(self.vista, "Aviso", "Primero selecciona un vector del historial.")