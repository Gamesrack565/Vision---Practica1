import sys
from PyQt6.QtWidgets import QApplication
from modelo_p2 import ModeloLetras
from vista_p2 import VistaLetras
from controlador_p2 import ControladorLetras

if __name__ == '__main__':
    app = QApplication(sys.argv)
    modelo = ModeloLetras()
    vista = VistaLetras()
    controlador = ControladorLetras(modelo, vista)
    vista.show()
    sys.exit(app.exec())