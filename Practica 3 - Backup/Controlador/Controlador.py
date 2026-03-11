#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np 
from PyQt6.QtWidgets import QMessageBox 
from Modelo.modelo import Modelo 
from Vista.vista import VistaPrincipal, DialogoConfiguracion

class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = VistaPrincipal()
        
        self.vista.funcion_procesar = self.procesar_datos
        self.vista.btn_mostrar_seleccion.clicked.connect(self.mostrar_seleccionado)
        
        # Conectamos el nuevo botón verde de Configurar Clases
        self.vista.btn_configurar.clicked.connect(self.abrir_configuracion)
        
        self.vista.combo_metodo.currentTextChanged.connect(self.actualizar_pantalla)
        self.vista.check_barreras.stateChanged.connect(self.actualizar_pantalla)
        
        self.historial_vectores = []
        self.actualizar_pantalla()

    def abrir_configuracion(self):
        # Abre la ventana de la tabla
        dialogo = DialogoConfiguracion(self.vista)
        if dialogo.exec(): # Si el usuario le dio al botón "Generar"
            num_clases, num_reps, parametros = dialogo.obtener_datos()
            
            if num_clases is not None:
                # 1. Le pedimos al modelo que regenere todo
                self.modelo.generar_clases_aleatorias(num_clases, num_reps, parametros)
                
                # 2. Limpiamos la memoria porque el universo cambió
                self.historial_vectores.clear()
                self.vista.lista_historial.clear()
                
                # 3. Dibujamos el nuevo escenario
                self.actualizar_pantalla()
            else:
                QMessageBox.warning(self.vista, "Error", "Verifica que todos los datos en la tabla sean números válidos.")

    def actualizar_pantalla(self):
        metodo = self.vista.combo_metodo.currentText().lower()
        barreras_calculadas = None
        
        if self.vista.check_barreras.isChecked():
            barreras_calculadas = self.modelo.obtener_parametros_barrera(4.0, metodo)
            
        vector_reciente = self.historial_vectores[-1] if self.historial_vectores else None
        
        # Ahora extraemos las clases directamente de las listas dinámicas del modelo
        self.vista.dibujar_vectores(self.modelo.clases, self.modelo.centros, vector_reciente, barreras_calculadas)

    def procesar_datos(self, x_str, y_str):
        try: 
            x_num = float(x_str)
            y_num = float(y_str)
            vector_nuevo = np.array([x_num, y_num]) 
            
            metodo_sel = self.vista.combo_metodo.currentText().lower()
            resultado = self.modelo.clasificar(vector_nuevo, 4.0, metodo_sel)

            self.historial_vectores.append(vector_nuevo)
            texto_lista = f"X: {x_num} | Y: {y_num} ➔ {resultado}"
            self.vista.lista_historial.addItem(texto_lista)
            
            ultimo_indice = self.vista.lista_historial.count() - 1
            self.vista.lista_historial.setCurrentRow(ultimo_indice)

            self.actualizar_pantalla()
            QMessageBox.information(self.vista, "Resultado", resultado)

        except ValueError: 
            QMessageBox.warning(self.vista, "Error", "Ingresa números válidos.")

    def mostrar_seleccionado(self):
        indice = self.vista.lista_historial.currentRow()
        if indice >= 0:
            vector_viejo = self.historial_vectores.pop(indice)
            self.historial_vectores.append(vector_viejo)
            self.actualizar_pantalla()
        else:
            QMessageBox.warning(self.vista, "Aviso", "Primero selecciona un vector del historial.")