import sys
from PyQt6.QtWidgets import QApplication
from Modelo.Modelo import Modelo
from VIsta.Vista import Vista
from Controlador.Controlador import Controlador

def main():
    app = QApplication(sys.argv)
    
    modelo = Modelo()
    vista = Vista()
    controlador = Controlador(modelo, vista)
    
    vista.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()