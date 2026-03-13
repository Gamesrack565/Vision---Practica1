import numpy as np

class ModeloLetras:
    def generar_letras(self):
        # Genera las clases con exactamente 150 puntos cada una y un poco de ruido
        ruido = 0.1
        clase_A = self._generar_A(offset_x=1, offset_y=1, ruido=ruido)
        clase_H = self._generar_H(offset_x=6, offset_y=1, ruido=ruido)
        clase_P = self._generar_P(offset_x=11, offset_y=1, ruido=ruido)
        
        # Generamos la M y la ponemos lejos (offset_x=20)
        clase_M = self._generar_M(offset_x=20, offset_y=1, ruido=ruido)
        
        return [clase_A, clase_H, clase_P, clase_M]

    def _generar_A(self, offset_x, offset_y, ruido):
        # 60 izq + 60 der + 30 cruz = 150 puntos
        x_izq, y_izq = np.linspace(0, 2, 60), np.linspace(0, 5, 60)
        x_der, y_der = np.linspace(2, 4, 60), np.linspace(5, 0, 60)
        x_mid, y_mid = np.linspace(1, 3, 30), np.full(30, 2.5)
        
        x = np.concatenate([x_izq, x_der, x_mid]) + offset_x + np.random.randn(150) * ruido
        y = np.concatenate([y_izq, y_der, y_mid]) + offset_y + np.random.randn(150) * ruido
        return np.column_stack((x, y))

    def _generar_H(self, offset_x, offset_y, ruido):
        # 60 izq + 60 der + 30 cruz = 150 puntos
        x_izq, y_izq = np.full(60, 0.0), np.linspace(0, 5, 60)
        x_der, y_der = np.full(60, 3.0), np.linspace(0, 5, 60)
        x_mid, y_mid = np.linspace(0, 3, 30), np.full(30, 2.5)
        
        x = np.concatenate([x_izq, x_der, x_mid]) + offset_x + np.random.randn(150) * ruido
        y = np.concatenate([y_izq, y_der, y_mid]) + offset_y + np.random.randn(150) * ruido
        return np.column_stack((x, y))

    def _generar_P(self, offset_x, offset_y, ruido):
        # 75 poste + 25 techo + 25 pared der + 25 piso medio = 150 puntos
        x_izq, y_izq = np.full(75, 0.0), np.linspace(0, 5, 75)
        x_sup, y_sup = np.linspace(0, 3, 25), np.full(25, 5.0)
        x_der, y_der = np.full(25, 3.0), np.linspace(5, 2.5, 25)
        x_mid, y_mid = np.linspace(3, 0, 25), np.full(25, 2.5)
        
        x = np.concatenate([x_izq, x_sup, x_der, x_mid]) + offset_x + np.random.randn(150) * ruido
        y = np.concatenate([y_izq, y_sup, y_der, y_mid]) + offset_y + np.random.randn(150) * ruido
        return np.column_stack((x, y))

    def _generar_M(self, offset_x, offset_y, ruido):
        # 40 poste izq + 35 diag izq + 35 diag der + 40 poste der = 150 puntos
        x_izq, y_izq = np.full(40, 0.0), np.linspace(0, 5, 40)
        x_diag1, y_diag1 = np.linspace(0, 2, 35), np.linspace(5, 2.5, 35)
        x_diag2, y_diag2 = np.linspace(2, 4, 35), np.linspace(2.5, 5, 35)
        x_der, y_der = np.full(40, 4.0), np.linspace(0, 5, 40)
        
        x = np.concatenate([x_izq, x_diag1, x_diag2, x_der]) + offset_x + np.random.randn(150) * ruido
        y = np.concatenate([y_izq, y_diag1, y_diag2, y_der]) + offset_y + np.random.randn(150) * ruido
        return np.column_stack((x, y))

    def calcular_centroides(self, clases):
        return [np.mean(clase, axis=0) for clase in clases]

    def clasificar(self, vector_prueba, centros, umbral_fondo=2.0):
        # Calcula distancias a los centros de A, H, P, M
        distancias = [np.linalg.norm(vector_prueba - centro) for centro in centros]
        distancia_min = min(distancias)
        
        # CONDICIÓN DE FONDO: Si está muy lejos de todas las letras, es fondo.
        if distancia_min > umbral_fondo:
            return -1 # Representa el fondo / zona de rechazo
            
        return np.argmin(distancias) # Retorna 0 (A), 1 (H), 2 (P) o 3 (M)