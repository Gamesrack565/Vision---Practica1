#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import sys
from PyQt6.QtWidgets import QApplication
from Vista.vista import VistaPrincipal
from Controlador.Controlador import Controlador

# --- Arranque de la aplicación ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Arrancamos el controlador, el cual internamente arrancará el modelo y la vista
    mi_controlador = Controlador()
    
    # Mostramos la ventana de la vista
    mi_controlador.vista.show()
    
    sys.exit(app.exec())