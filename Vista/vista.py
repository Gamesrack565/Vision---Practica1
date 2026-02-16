import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Visión Artificial - Práctica 1")
        #Tamaño más grande al iniciar
        self.resize(1024, 768)

        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                border: 6px solid #000080; /* Azul Marino */
            }
        """)

        #Crear el widget central y el layout vertical principal
        widget_central = QWidget()
        layout_principal = QVBoxLayout()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        #1. Título en la parte de arriba
        self.titulo = QLabel("Primera práctica")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #333333; 
            border: none; 
            margin-top: 10px;
            margin-bottom: 10px;
        """)
        layout_principal.addWidget(self.titulo)

        #2. Cuadro de la gráfica ---- IMPLEMENTAR
        self.frame_grafica = QFrame()
        self.frame_grafica.setFrameShape(QFrame.Shape.Box)
        self.frame_grafica.setStyleSheet("""
            background-color: #f8f9fa; 
            border: 2px dashed #000080; /* Borde punteado azul marino */
        """)
        
        #IMPORTANTE: 
        #Creado un layout interno específico para incrustar el canvas de matplotlib
        self.layout_grafica = QVBoxLayout()
        self.frame_grafica.setLayout(self.layout_grafica)
        
        #Etiqueta temporal para marcar el espacio
        self.label_temp = QLabel("Espacio reservado para la gráfica (Matplotlib)")
        self.label_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_temp.setStyleSheet("color: #666666; font-size: 16px; border: none;")
        self.layout_grafica.addWidget(self.label_temp)

        #stretch=1 hace que este cuadro ocupe todo el espacio sobrante en medio
        layout_principal.addWidget(self.frame_grafica, stretch=1) 



        #3. Botón en la parte de abajo
        self.btn_cambiar_vector = QPushButton("Cambiar vector X")
        self.btn_cambiar_vector.setStyleSheet("""
            QPushButton {
                background-color: #000080; /* Azul Marino */
                color: white; /* Texto blanco para contrastar */
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1A237E; /* Un azul marino más brillante al pasar el mouse */
            }
        """)
        layout_principal.addWidget(self.btn_cambiar_vector)

        #conectar el clic del botón a nuestra función
        self.btn_cambiar_vector.clicked.connect(self.preguntar_nuevo_vector)

    #PREGUNTAS PARA LA ASIGNACION DE X

    def preguntar_nuevo_vector(self):
        #ŕobar otro vector
        respuesta = QMessageBox.question(
            self, 
            "Nuevo Vector", 
            "¿Deseas probar con otro vector?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self.pedir_coordenadas()
        else:
            #Si es no, bye
            QMessageBox.information(self, "Despedida", "bye")
            self.close()

    def pedir_coordenadas(self):
        #Pedir coordenada X
        x_str, ok_x = QInputDialog.getText(self, "Ingresar X", "Ingresa la coordenada X:")
        
        #Si el usuario le dio OK y escribió algo
        if ok_x and x_str:
            #Pedir coordenada Y
            y_str, ok_y = QInputDialog.getText(self, "Ingresar Y", "Ingresa la coordenada Y:")
            
            if ok_y and y_str:
                if hasattr(self, 'funcion_procesar'):
                    self.funcion_procesar(x_str, y_str)