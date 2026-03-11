import sys
from PyQt6.QtWidgets import QApplication

from Modelo.modelo import Modelo
from Vista.vista import Vista
from Controlador.Controlador import Controlador

def main():
    # Inicializar la aplicación Qt
    app = QApplication(sys.argv)
    
    # Instanciar MVC
    modelo = Modelo()
    vista = Vista()
    controlador = Controlador(modelo, vista)
    
    # Mostrar la ventana principal
    vista.show()
    
    # Ejecutar el bucle de la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()