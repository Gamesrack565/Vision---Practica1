import sys
from PyQt6.QtWidgets import QApplication
from modelo import ModeloCubo
from vista import VistaCubo
from controlador import ControladorCubo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Instanciamos el MVC
    modelo = ModeloCubo()
    vista = VistaCubo()
    controlador = ControladorCubo(modelo, vista)
    
    # Mostramos la ventana y ejecutamos la app
    vista.show()
    sys.exit(app.exec())