#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import sys
from PyQt6.QtWidgets import QApplication
from Vista.vista import VistaPrincipal
from Controlador.Controlador import Controlador

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mi_controlador = Controlador()
    mi_controlador.vista.show()
    sys.exit(app.exec())