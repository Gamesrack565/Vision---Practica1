#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np

class Modelo:
    def __init__(self):
        # Creacion de arreglos
        self.C1 = np.array([[1,1], [1,2], [2,3], [5,5], [4,1], [3,3], [6,2], [2,6]])
        self.C2 = np.array([[6,1], [7,2], [10,1], [8,4], [10,5], [12,3], [8,0], [7,3]])
        self.C3 = np.array([[1,10], [2,9], [5,11], [2,11], [3,13], [6,12], [1,12], [2,14]])
        self.C4 = np.array([[7,10], [9,13], [12,8], [15,11], [12,5], [12,12], [10,12], [11,8]])
        self.C5 = np.array([[15,1], [18,4], [16,0], [19,5], [17,3], [21,2], [20,3], [21,3]])
        self.C6 = np.array([[1,20], [1,21], [2,20], [2,21], [3,20], [3,22], [1,22], [2,22]])
        
        # Centros calculados una sola vez
        self.u1 = self.centro_gravedad(self.C1)
        self.u2 = self.centro_gravedad(self.C2)
        self.u3 = self.centro_gravedad(self.C3)
        self.u4 = self.centro_gravedad(self.C4)
        self.u5 = self.centro_gravedad(self.C5)
        self.u6 = self.centro_gravedad(self.C6)
    
    """
    Recibe un conjunto de puntos C y extrae todas las coordenadas en X 
    y todas las Y. 
    """
    def centro_gravedad(self, C):
        x = C[:,0]
        y = C[:,1]

        # Suma todas las coordenadas X y todas las Y por separado.
        x_u = sum(x)
        y_u = sum(y)

        # Divide cada suma por la cantidad de puntos en el conjunto, dando el promedio.
        # El resultado es el centro de gravedad.
        u = np.array([x_u, y_u]) * (1/len(C))
        return u

    """
    Calcula la distancia euclidiana entre un punto X y un centro u.
    """
    def calcular_distancia(self, X, u):
        d = np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2)    
        return d

    """
    Recibe un vector X y un umbral. El umbral es la distancia máxima para decidir 
    si el vector pertenece o no a una clase.
    """
    def clasificar(self, X, umbrall):

        # Crea una lista con los centros de gravedad de las 6 clases.
        centros = [self.u1, self.u2, self.u3, self.u4, self.u5, self.u6]
        
        """
        Calcula la distancia desde el punto X a cada uno de los 6 centros, utilizando
        una list comprehension como una forma compacta de crear listas
        """
        distancias = [self.calcular_distancia(X, u) for u in centros]

        # Encuentra la distancia más cercana.
        distancia_min = min(distancias)

        # Encuentra la posición de la distancia más cercana.
        indice_ganador = distancias.index(distancia_min) + 1

        """
        En caso que la distancia mínima sea menor que el umbral (4.0) significa que el punto
        está cerca de algún centro, haciendo que pertenezca a esa clase. 
        En caso contrario, el punto es huérfano.  
        """
        if distancia_min < umbrall:
            return f"El vector pertenece a la Clase {indice_ganador}"
        else:
            return "No pertenece a ninguna clase, es huérfano."