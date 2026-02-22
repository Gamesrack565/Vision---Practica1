#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np

class Modelo:
    def __init__(self):
        #Creacion de arreglos
        self.C1 = np.array([[1,1], [1,2], [2,3], [5,5], [4,1], [3,3], [6,2], [2,6]])
        self.C2 = np.array([[6,1], [7,2], [10,1], [8,4], [10,5], [12,3], [8,0], [7,3]])
        self.C3 = np.array([[1,10], [2,9], [5,11], [2,11], [3,13], [6,12], [1,12], [2,14]])
        self.C4 = np.array([[7,10], [9,13], [12,8], [15,11], [12,5], [12,12], [10,12], [11,8]])
        self.C5 = np.array([[15,1], [18,4], [16,0], [19,5], [17,3], [21,2], [20,3], [21,3]])
        self.C6 = np.array([[1,20], [1,21], [2,20], [2,21], [3,20], [3,22], [1,22], [2,22]])
        
        #Centros calculados una sola vez (Medias)
        self.u1 = self.centro_gravedad(self.C1)
        self.u2 = self.centro_gravedad(self.C2)
        self.u3 = self.centro_gravedad(self.C3)
        self.u4 = self.centro_gravedad(self.C4)
        self.u5 = self.centro_gravedad(self.C5)
        self.u6 = self.centro_gravedad(self.C6)


        #NUEVO ----
        # Matrices de Covarianza Inversas pre-calculadas (Para Mahalanobis)
        self.inv_cov1 = self.calcular_covarianza_inversa(self.C1, self.u1)
        self.inv_cov2 = self.calcular_covarianza_inversa(self.C2, self.u2)
        self.inv_cov3 = self.calcular_covarianza_inversa(self.C3, self.u3)
        self.inv_cov4 = self.calcular_covarianza_inversa(self.C4, self.u4)
        self.inv_cov5 = self.calcular_covarianza_inversa(self.C5, self.u5)
        self.inv_cov6 = self.calcular_covarianza_inversa(self.C6, self.u6)
    
    def centro_gravedad(self, C):
        x = C[:,0]
        y = C[:,1]
        x_u = sum(x)
        y_u = sum(y)
        u = np.array([x_u, y_u]) * (1/len(C))
        return u

    def calcular_distancia_euclidiana(self, X, u):
        d = np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2)    
        return d

    #---NUEVOS MÉTODOS PARA MAHALANOBIS---
    def calcular_covarianza_inversa(self, C, u):
        """Calcula la matriz de covarianza y devuelve su inversa (sigma_inversa)"""
        N = len(C)
        #(C - media)
        C_centrado = C - u 
        #sigma = (1/N) * (C-media)' * (C-media)
        sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
        #inv(sigma)
        sigma_inversa = np.linalg.inv(sigma)
        return sigma_inversa

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        """Calcula la distancia de Mahalanobis usando la matriz de covarianza inversa"""
        v = X - u   #(vector - media)
        #dist = sqrt( (v) * sigma_inversa * (v)' )
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(dist_cuadrada)

    #--- METODO CLASIFICAR ACTUALIZADO ---
    def clasificar(self, X, umbrall, metodo="euclidiana"):
        centros = [self.u1, self.u2, self.u3, self.u4, self.u5, self.u6]
        
        if metodo == "euclidiana":
            #LOgica tvieja
            distancias = [self.calcular_distancia_euclidiana(X, u) for u in centros]
            distancia_min = min(distancias)
            indice_ganador = distancias.index(distancia_min) + 1

            if distancia_min < umbrall:
                return f"El vector pertenece a la Clase {indice_ganador} (Euclidiana)"
            else:
                return "No pertenece a ninguna clase, es huérfano."
        
        #NUEVO--- METODO MAHALANOBIS
        elif metodo == "mahalanobis":
            #Logica nueva para Mahalanobis
            inv_covs = [self.inv_cov1, self.inv_cov2, self.inv_cov3, 
                        self.inv_cov4, self.inv_cov5, self.inv_cov6]
            
            #1. Calculamos las distancias de Mahalanobis
            distancias = [self.calcular_distancia_mahalanobis(X, c, ic) for c, ic in zip(centros, inv_covs)]
            
            #2. Normalizamos: ((dist) / suma) * 100
            suma_distancias = sum(distancias)
            dist_normalizada = [(d / suma_distancias) * 100 for d in distancias]
            
            #3. Encontramos la menor
            minimo_norm = min(dist_normalizada)
            indice_ganador = dist_normalizada.index(minimo_norm) + 1
            
            #Nota: Mahalanobis es una métrica diferente, por lo que el "umbral" de 4.0 
            #de Euclidiana tal vez lo rechace siempre o lo acepte siempre. 
            #Aquí evaluamos la distancia Mahalanobis cruda contra el umbral:
            distancia_min_cruda = min(distancias)
            
            if distancia_min_cruda < umbrall:
                #Retornamos también el porcentaje normalizado para que el profe lo vea
                return f"El vector pertenece a la Clase {indice_ganador} (Mahalanobis: {minimo_norm:.2f}%)"
            else:
                return "No pertenece a ninguna clase, es huérfano (Mahalanobis)."