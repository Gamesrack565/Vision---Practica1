import numpy as np

# GENERACIÓN FIJA (2D)
# Utilizada en las Prácticas 1 y 2 para definir clases "quemadas" en el código.
def generar_clases_fijas():
    # Crea y retorna una lista de arreglos numpy con coordenadas predefinidas
    return [
        # Clase 1: Coordenadas fijas en un plano 2D
        np.array([[1,1], [1,2], [2,3], [5,5], [4,1], [3,3], [6,2], [2,6]]),
        # Clase 2: Coordenadas fijas en un plano 2D
        np.array([[6,1], [7,2], [10,1], [8,4], [10,5], [12,3], [8,0], [7,3]])
    ]

# GENERACIÓN ALEATORIA SINTÉTICA (2D)
# Utilizada en la Práctica 3 para crear nubes de puntos dinámicas usando Campanas de Gauss.
def generar_clases_aleatorias(num_reps, cx, cy, disp_x, disp_y):
    # np.random.randn genera números aleatorios centrados en 0. Se multiplica por la dispersión en X
    x = (np.random.randn(num_reps) * disp_x) 
    # Se le suma el centro (cx) para mover toda la nube de puntos a esa coordenada en el eje X
    x = x + cx 
    # Se repite el proceso para el eje Y, multiplicando por su propia dispersión
    y = (np.random.randn(num_reps) * disp_y) 
    # Se desplaza la nube de puntos al centro Y (cy)
    y = y + cy 
    # np.column_stack une las dos listas (X e Y) creando pares de coordenadas (matriz)
    C = np.column_stack((x, y))
    # Retorna la matriz de puntos generada
    return C

# CÁLCULO DEL CENTRO DE GRAVEDAD (Compatible con 2D y 3D)
# Promedia los puntos de una clase para encontrar su centroide.
def centro_gravedad(C):
    # np.mean calcula el promedio. axis=0 indica que promedie por columnas (todas las X, todas las Y, etc.)
    # Esto lo hace compatible tanto para (X,Y) como para colores de imagen (R,G,B)
    u = np.mean(C, axis=0)
    # Retorna el vector que representa el centro del grupo
    return u

# CÁLCULO DE COVARIANZA E INVERSA (Compatible con 2D y 3D)
# Vital para Mahalanobis y Probabilidad a partir de la Práctica 2. Incluye el parche de la Práctica 4.
def calcular_covarianza_e_inversa(C, u):
    # Obtiene la cantidad total de puntos en la clase
    N = len(C)
    # Resta el centro a cada punto para "centrar" los datos en el origen (0,0)
    C_centrado = C - u 
    # Realiza el producto punto matricial transpuesto y divide entre N para obtener la covarianza
    sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
    
    # PARCHE PRÁCTICA 4 (Imágenes 3D): Suma una matriz identidad minúscula para evitar que la matriz colapse
    # Esto ocurre si los colores de una imagen son exactamente iguales (varianza cero).
    sigma += np.eye(sigma.shape[0]) * 1e-2 
    
    # Calcula la matriz inversa usando álgebra lineal de numpy
    sigma_inversa = np.linalg.inv(sigma)
    # Retorna ambas matrices (la normal y la inversa)
    return sigma, sigma_inversa

# DISTANCIA EUCLIDIANA (Compatible con 2D y 3D)
# Calcula la distancia en línea recta entre dos puntos.
def calcular_distancia_euclidiana(X, u):
    # np.linalg.norm es la forma optimizada de calcular el Teorema de Pitágoras
    # Sirve tanto para 2 componentes (X, Y) como para 3 componentes (R, G, B) en imágenes
    distancia = np.linalg.norm(X - u)
    # Retorna el valor de la distancia lineal
    return distancia

# DISTANCIA DE MAHALANOBIS (Compatible con 2D y 3D)
# Calcula la distancia tomando en cuenta la dispersión (forma) de la clase.
def calcular_distancia_mahalanobis(X, u, inv_cov):
    # Calcula el vector de diferencia geométrica entre el punto y el centro
    v = X - u 
    # Realiza una doble multiplicación de matrices: el vector por la inversa, y luego por el vector transpuesto
    dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
    # Saca la raíz cuadrada del valor absoluto (para evitar errores de signos) de la distancia calculada
    distancia = np.sqrt(abs(dist_cuadrada))
    # Retorna la distancia penalizada por la covarianza
    return distancia

# PROBABILIDAD GAUSSIANA (Dinámica para 2D y 3D)
# Prácticas 3 y 4: Calcula el porcentaje de pertenencia usando el Teorema de Bayes.
def calcular_probabilidad(X, u, inv_cov, det_cov, dimensiones):
    # 'dimensiones' debe ser 2 para planos cartesianos (P3) o 3 para colores RGB de imágenes (P4)
    n = dimensiones 
    # Llama a la función Mahalanobis para obtener la distancia inicial
    distancia_mah = calcular_distancia_mahalanobis(X, u, inv_cov)
    # Eleva la distancia de Mahalanobis al cuadrado, como lo pide la fórmula
    mah_sq = distancia_mah ** 2
    
    # Calcula el denominador: (2 * Pi) elevado a la n/2, multiplicado por la raíz del determinante
    denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))
    # Calcula el exponente: número 'e' elevado a -0.5 por la distancia al cuadrado
    exponente = np.exp(-0.5 * mah_sq)
    
    # Divide 1 entre el denominador y lo multiplica por el exponente para sacar la probabilidad
    probabilidad = (1 / denominador) * exponente
    # Retorna la densidad de probabilidad bruta (suele ser un número muy pequeño)
    return probabilidad

# FUNCIÓN DE CLASIFICACIÓN GENERAL (Estructura base)
# Consolida la lógica de decisión para los tres métodos matemáticos.
def clasificar(X, centros, inv_covs, det_covs, umbral_euclidiano, dimensiones, metodo="probabilidad"):
    
    # Verifica qué método pidió el usuario a través de la interfaz
    if metodo == "euclidiana":
        # Genera una lista calculando la distancia Euclidiana contra todos los centros disponibles
        distancias = [calcular_distancia_euclidiana(X, u) for u in centros]
        # Encuentra el valor más pequeño (el centro más cercano)
        distancia_min = min(distancias)
        # Encuentra en qué posición de la lista estaba ese valor mínimo (se le suma 1 para nombre de clase)
        indice_ganador = distancias.index(distancia_min) + 1
        
        # Evalúa si la distancia es menor al límite permitido
        if distancia_min < umbral_euclidiano:
            # Si está dentro, pertenece a esa clase
            return f"Pertenece a la Clase {indice_ganador} (Euclidiana)"
        else:
            # Si está muy lejos, es huérfano
            return "No pertenece, es huérfano."
            
    # Verifica si el método elegido es Mahalanobis
    elif metodo == "mahalanobis":
        # Genera una lista de distancias emparejando cada centro con su respectiva matriz inversa
        distancias = [calcular_distancia_mahalanobis(X, c, ic) for c, ic in zip(centros, inv_covs)]
        # Encuentra el valor más pequeño de Mahalanobis
        distancia_min = min(distancias)
        # Encuentra el índice del ganador
        indice_ganador = distancias.index(distancia_min) + 1
        
        # En Mahalanobis el umbral suele ser pequeño (ej. 4.0) porque escala distinto a la Euclidiana
        umbral_mah = 4.0 
        # Evalúa contra el umbral de Mahalanobis
        if distancia_min < umbral_mah:
            return f"Pertenece a la Clase {indice_ganador} (Mahalanobis)"
        else:
            return "No pertenece, es huérfano (Mahalanobis)."
            
    # Verifica si el método elegido es la Probabilidad Bayesiana
    elif metodo == "probabilidad":
        # Genera una lista de probabilidades pasando el centro, la inversa, el determinante y las dimensiones (2D o 3D)
        probabilidades = [calcular_probabilidad(X, c, ic, dc, dimensiones) for c, ic, dc in zip(centros, inv_covs, det_covs)]
        
        # A diferencia de las distancias (donde gana el menor), en probabilidad gana el número MÁS ALTO
        max_prob = max(probabilidades)
        # Encuentra en qué índice está la mayor probabilidad
        indice_ganador = probabilidades.index(max_prob) + 1
        # Suma todas las probabilidades compitiendo
        suma_probs = sum(probabilidades)
        
        # Saca el porcentaje relativo para el usuario (si la suma es mayor a cero para evitar división entre cero)
        porcentaje = (max_prob / suma_probs) * 100 if suma_probs > 0 else 0.0
        
        # Un umbral mínimo de esperanza (1e-10 es casi cero) para evitar clasificar puntos en el vacío absoluto
        if max_prob > 1e-10:
            return f"Pertenece a la Clase {indice_ganador} con {porcentaje:.2f}% de seguridad."
        else:
            return "No pertenece, probabilidad casi nula."