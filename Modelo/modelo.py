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
        centros = [self.centro_gravedad(self.C1), self.centro_gravedad(self.C2), self.centro_gravedad(self.C3),
                   self.centro_gravedad(self.C4), self.centro_gravedad(self.C5), self.centro_gravedad(self.C6)]
        
        #Calculo de las distancias 
        distancias = [self.calcular_distancia(X, u) for u in centros]

        distancia_min = min(distancias)
        indice_ganador = distancias.index(distancia_min) + 1

        if distancia_min < umbrall:
            return f"El vector pertenece a la clase {indice_ganador}"
        else:
            return "No pertence a ningún vector, es huérfano."