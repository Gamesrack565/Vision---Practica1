#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np

class Modelo:
    def __init__(self):
        self.C1 = np.array([[1,1], [1,2], [2,3], [5,5], [4,1], [3,3], [6,2], [2,6]])
        self.C2 = np.array([[6,1], [7,2], [10,1], [8,4], [10,5], [12,3], [8,0], [7,3]])
        self.C3 = np.array([[1,10], [2,9], [5,11], [2,11], [3,13], [6,12], [1,12], [2,14]])
        self.C4 = np.array([[7,10], [9,13], [12,8], [15,11], [12,5], [12,12], [10,12], [11,8]])
        self.C5 = np.array([[15,1], [18,4], [16,0], [19,5], [17,3], [21,2], [20,3], [21,3]])
        self.C6 = np.array([[1,20], [1,21], [2,20], [2,21], [3,20], [3,22], [1,22], [2,22]])
        
        self.u1 = self.centro_gravedad(self.C1)
        self.u2 = self.centro_gravedad(self.C2)
        self.u3 = self.centro_gravedad(self.C3)
        self.u4 = self.centro_gravedad(self.C4)
        self.u5 = self.centro_gravedad(self.C5)
        self.u6 = self.centro_gravedad(self.C6)

        # AHORA GUARDAMOS AMBAS: La matriz de covarianza normal y su inversa
        self.cov1, self.inv_cov1 = self.calcular_covarianza_e_inversa(self.C1, self.u1)
        self.cov2, self.inv_cov2 = self.calcular_covarianza_e_inversa(self.C2, self.u2)
        self.cov3, self.inv_cov3 = self.calcular_covarianza_e_inversa(self.C3, self.u3)
        self.cov4, self.inv_cov4 = self.calcular_covarianza_e_inversa(self.C4, self.u4)
        self.cov5, self.inv_cov5 = self.calcular_covarianza_e_inversa(self.C5, self.u5)
        self.cov6, self.inv_cov6 = self.calcular_covarianza_e_inversa(self.C6, self.u6)
    
    def centro_gravedad(self, C):
        x = C[:,0]
        y = C[:,1]
        u = np.array([sum(x), sum(y)]) * (1/len(C))
        return u

    def calcular_distancia_euclidiana(self, X, u):
        return np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2)    

    def calcular_covarianza_e_inversa(self, C, u):
        """Calcula la matriz de covarianza cruda y su inversa."""
        N = len(C)
        C_centrado = C - u 
        sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
        sigma_inversa = np.linalg.inv(sigma)
        return sigma, sigma_inversa

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(dist_cuadrada)

    def clasificar(self, X, umbrall, metodo="euclidiana"):
        centros = [self.u1, self.u2, self.u3, self.u4, self.u5, self.u6]
        
        if metodo == "euclidiana":
            distancias = [self.calcular_distancia_euclidiana(X, u) for u in centros]
            distancia_min = min(distancias)
            indice_ganador = distancias.index(distancia_min) + 1
            if distancia_min < umbrall:
                return f"El vector pertenece a la Clase {indice_ganador} (Euclidiana)"
            else:
                return "No pertenece a ninguna clase, es huérfano."
                
        elif metodo == "mahalanobis":
            inv_covs = [self.inv_cov1, self.inv_cov2, self.inv_cov3, 
                        self.inv_cov4, self.inv_cov5, self.inv_cov6]
            distancias = [self.calcular_distancia_mahalanobis(X, c, ic) for c, ic in zip(centros, inv_covs)]
            suma_distancias = sum(distancias)
            dist_normalizada = [(d / suma_distancias) * 100 for d in distancias]
            
            minimo_norm = min(dist_normalizada)
            indice_ganador = dist_normalizada.index(minimo_norm) + 1
            distancia_min_cruda = min(distancias)
            
            if distancia_min_cruda < umbrall:
                return f"El vector pertenece a la Clase {indice_ganador} (Mahalanobis: {minimo_norm:.2f}%)"
            else:
                return "No pertenece a ninguna clase, es huérfano (Mahalanobis)."

    # --- NUEVO --- EXPERIMENTAL 
    def obtener_parametros_barrera(self, umbral, metodo):
        """Calcula la geometría exacta de la frontera de decisión para graficarla"""
        parametros = []
        centros = [self.u1, self.u2, self.u3, self.u4, self.u5, self.u6]
        
        if metodo == "euclidiana":
            for c in centros:
                # La Euclidiana dibuja un círculo perfecto (ancho = alto)
                parametros.append((c[0], c[1], umbral*2, umbral*2, 0))
                
        elif metodo == "mahalanobis":
            covs = [self.cov1, self.cov2, self.cov3, self.cov4, self.cov5, self.cov6]
            for c, cov in zip(centros, covs):
                # Usamos Álgebra Lineal para extraer la forma del óvalo de la matriz de covarianza
                eigenvalues, eigenvectors = np.linalg.eigh(cov)
                # Inclinación del óvalo
                angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
                # Estiramiento en X y Y basado en la varianza
                width = 2 * umbral * np.sqrt(eigenvalues[0])
                height = 2 * umbral * np.sqrt(eigenvalues[1])
                parametros.append((c[0], c[1], width, height, angle))
        return parametros