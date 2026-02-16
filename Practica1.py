import numpy as np

#Creacion de arreglos
C1 = np.array([[1,1], [1,2], [2,1], [2,2], [3,1], [3,3], [1,3], [2,3]])
C2 = np.array([[10,1], [10,2], [11,1], [11,2], [12,1], [12,3], [10,3], [11,3]])
C3 = np.array([[1,10], [1,11], [2,10], [2,11], [3,10], [3,12], [1,12], [2,12]])
C4 = np.array([[10,10], [10,11], [11,10], [11,11], [12,10], [12,12], [10,12], [11,12]])
C5 = np.array([[20,1], [20,2], [21,1], [21,2], [22,1], [22,3], [20,3], [21,3]])
C6 = np.array([[1,20], [1,21], [2,20], [2,21], [3,20], [3,22], [1,22], [2,22]])

#Calcular centro de gravedad
def centro_gravedad(C):
    x = C[:,0]
    y = C[:,1]
    
    x_u = sum(x)
    y_u = sum(y)
    
    u = np.array([x_u, y_u]) * (1/len(C))

    return u

def calcular_distancia(X, u):
    d = np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2)    
    return d

def programa_principal():
    #Calcular centro de gravedad de cada cluster
    u1 = centro_gravedad(C1)
    u2 = centro_gravedad(C2)

    #CAMBIAR PARA QUE EL USUARIO INGRESE LOS PUNTOS A CLASIFICAR
    X1 = np.array([5, 1])

    #Calcular distancia de cada punto al centro de gravedad
    d1 = calcular_distancia(X1, u1)
    d2 = calcular_distancia(X1, u2)
    
    umbrall = 4

    if d1 < d2:
        if d1 < umbrall:
            print("El punto pertenece al Cluster 1")
        else:            
            print("Es huerfano, no pertenece a ningun cluster")

    elif d2 < d1:
        if d2 < umbrall:
            print("El punto pertenece al Cluster 2")
        else:            
            print("Es huerfano, no pertenece a ningun cluster")
    
    else: #d1 == d2
        print("El punto esta equidistante a ambos clusters, no se puede clasificar")

    print("Centro de gravedad del Cluster 1:", u1)
    print("Centro de gravedad del Cluster 2:", u2)
    print("Distancias del Cluster 1 al centro de gravedad:", d1)
    print("Distancias del Cluster 2 al centro de gravedad:", d2)


programa_principal()