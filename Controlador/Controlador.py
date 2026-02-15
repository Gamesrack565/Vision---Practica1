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

