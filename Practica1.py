import numpy as np

#Creacion de arreglos
C1 = np.array([[0,0], [1,2], [2,3], [4,5]])
C2 = np.array([[5,6], [7,4], [6,9], [8,4]])
#C3 = np.array()
#C4 = np.array()
#C5 = np.array()

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