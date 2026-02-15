import numpy as np

class Modelo:
    def __init__(self):
        #Creacion de arreglos
        self.C1 = np.array([[0,0], [1,2], [2,3], [4,5]])
        self.C2 = np.array([[5,6], [7,4], [6,9], [8,4]])
        #C3 = np.array()
        #C4 = np.array()
        #C5 = np.array()

    #Calcular centro de gravedad
    def centro_gravedad(self, C):
        x = C[:,0]
        y = C[:,1]
        
        x_u = sum(x)
        y_u = sum(y)
        
        u = np.array([x_u, y_u]) * (1/len(C))

        return u

    def calcular_distancia(self, X, u):
        d = np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2)    
        return d

    def clasificar(self, X, umbrall):
        #1. El modelo calcula sus propios centros de gravedad usando 'self'
        #AGREGAR LOS DEMÁS 
        u1 = self.centro_gravedad(self.C1)
        u2 = self.centro_gravedad(self.C2)
        
        #2. El modelo calcula las distancias internamente
        d1 = self.calcular_distancia(X, u1)
        d2 = self.calcular_distancia(X, u2)

        #3. Lógica de decisión
        if d1 < d2:
            if d1 < umbrall:
                return "El punto pertenece al Cluster 1"
            else:            
                return "Es huérfano, no pertenece a ningún cluster"

        elif d2 < d1:
            if d2 < umbrall:
                return "El punto pertenece al Cluster 2"
            else:            
                return "Es huérfano, no pertenece a ningún cluster"
        
        else: #d1 == d2
            return "El punto está equidistante a ambos clusters, no se puede clasificar"