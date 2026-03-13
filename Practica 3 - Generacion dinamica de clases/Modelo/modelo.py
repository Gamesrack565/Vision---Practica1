#Ceron Samperio Lizeth Montserrat
#Higuera Pineda Angel Abraham

import numpy as np

class Modelo:
    def __init__(self):
        self.clases = []
        self.centros = []
        self.covs = []
        self.inv_covs = []
        # NUEVO: Lista para guardar el determinante de cada matriz de covarianza (necesario para el volumen en Bayes)
        self.det_covs = [] 
        
        parametros_default = [(3, 5, 1, 1), (8, 2, 1, 1), (2, 10, 1.5, 1.5)]
        self.generar_clases_aleatorias(3, 1000, parametros_default)

    # --- NUEVA FUNCIÓN: GENERACIÓN DE PUNTOS SINTÉTICOS (BASADO EN MATLAB) ---
    def generar_clases_aleatorias(self, num_clases, num_reps, parametros):
        # Limpiamos las listas por si el usuario genera nuevas clases, borramos las anteriores
        self.clases.clear()
        self.centros.clear()
        self.covs.clear()
        self.inv_covs.clear()
        self.det_covs.clear()

        # Ciclo principal que se repite por cada clase que el usuario solicitó generar
        for i in range(num_clases):
            # Extraemos los parámetros dictados para esta clase: centro X, centro Y, dispersión X, dispersión Y
            cx, cy, disp_x, disp_y = parametros[i]
            
            # np.random.randn(num_reps) genera 'num_reps' números aleatorios en una campana de Gauss (con centro en 0)
            # Multiplicamos por la dispersión deseada (disp_x) para estirar o encoger la nube de puntos
            # Finalmente le sumamos el centro (cx) para desplazar toda la nube de puntos a esa coordenada en el mapa
            x = (np.random.randn(num_reps) * disp_x) + cx
            y = (np.random.randn(num_reps) * disp_y) + cy
            
            # np.column_stack une la lista de coordenadas X e Y creando pares ordenados (Matriz de Nx2)
            C = np.column_stack((x, y))
            # Guardamos la matriz de puntos recién creada en nuestra lista global de clases
            self.clases.append(C)
            
            # Invocamos la función existente para encontrar el centro de gravedad de estos nuevos puntos
            u = self.centro_gravedad(C)
            # Almacenamos el centroide calculado en su respectiva lista
            self.centros.append(u)
            
            # Obtenemos la matriz de covarianza (para su forma) y su inversa (para usarla en Mahalanobis/Probabilidad)
            cov, inv_cov = self.calcular_covarianza_e_inversa(C, u)
            self.covs.append(cov)
            self.inv_covs.append(inv_cov)
            
            # np.linalg.det calcula el determinante de la matriz de covarianza usando álgebra lineal
            det_cov = np.linalg.det(cov)
            # Guardamos este determinante, el cual nos servirá para saber el "volumen" o densidad en el teorema de Bayes
            self.det_covs.append(det_cov)

    def centro_gravedad(self, C):
        x = C[:,0]
        y = C[:,1]
        u = np.array([sum(x), sum(y)]) * (1/len(C))
        return u

    def calcular_distancia_euclidiana(self, X, u):
        return np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2)    

    def calcular_covarianza_e_inversa(self, C, u):
        N = len(C)
        C_centrado = C - u 
        sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
        sigma_inversa = np.linalg.inv(sigma)
        return sigma, sigma_inversa

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(dist_cuadrada)

    # --- NUEVA FUNCIÓN: PROBABILIDAD (GAUSSIANA MULTIVARIADA) ---
    def calcular_probabilidad(self, X, u, inv_cov, det_cov):
        # n = 2 representa las dimensiones de nuestro espacio (es un plano 2D por tener X y Y)
        n = 2 
        
        # Mandamos a llamar a nuestra función Mahalanobis para reutilizar código y obtener la distancia lineal
        distancia_mah = self.calcular_distancia_mahalanobis(X, u, inv_cov)
        
        # La fórmula de Probabilidad nos pide la distancia al CUADRADO, así que elevamos la respuesta
        # al cuadrado (** 2) para anular el efecto de la raíz cuadrada de la función anterior.
        mah_sq = distancia_mah ** 2
        
        # Calculamos la parte inferior de la fracción (Denominador): (2 * Pi) elevado a la n/2, por la raíz del determinante
        denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(det_cov)
        
        # Calculamos la constante exponencial 'e' elevada a: -0.5 multiplicado por la distancia Mahalanobis al cuadrado
        exponente = np.exp(-0.5 * mah_sq)
        
        # Juntamos la fórmula completa: fracción multiplicada por el exponente
        probabilidad = (1 / denominador) * exponente
        
        # Retornamos el valor de la densidad de probabilidad (usualmente es un número decimal muy pequeño)
        return probabilidad

    def clasificar(self, X, umbrall, metodo="euclidiana"):
        if not self.centros:
            return "No hay clases configuradas."

        if metodo == "euclidiana":
            distancias = [self.calcular_distancia_euclidiana(X, u) for u in self.centros]
            distancia_min = min(distancias)
            indice_ganador = distancias.index(distancia_min) + 1
            if distancia_min < umbrall:
                return f"Pertenece a la Clase {indice_ganador} (Euclidiana)"
            else:
                return "No pertenece, es huérfano."
                
        elif metodo == "mahalanobis":
            distancias = [self.calcular_distancia_mahalanobis(X, c, ic) for c, ic in zip(self.centros, self.inv_covs)]
            suma_distancias = sum(distancias)
            dist_normalizada = [(d / suma_distancias) * 100 for d in distancias]
            
            minimo_norm = min(dist_normalizada)
            indice_ganador = dist_normalizada.index(minimo_norm) + 1
            distancia_min_cruda = min(distancias)
            
            if distancia_min_cruda < umbrall:
                return f"Pertenece a la Clase {indice_ganador} (Mahalanobis: {minimo_norm:.2f}%)"
            else:
                return "No pertenece, es huérfano (Mahalanobis)."
                
        # --- NUEVA LÓGICA DE DECISIÓN PARA PROBABILIDAD MÁXIMA ---
        elif "probabilidad" in metodo:
            # Calculamos las probabilidades de todas las clases en una sola lista comprimida
            probabilidades = [self.calcular_probabilidad(X, c, ic, dc) for c, ic, dc in zip(self.centros, self.inv_covs, self.det_covs)]
            
            # En la teoría de decisión de Bayes, la clase ganadora es la que tiene la probabilidad MÁXIMA (max)
            max_prob = max(probabilidades)
            
            # Buscamos en qué posición de la lista quedó esa probabilidad ganadora y le sumamos 1 para coincidir con su nombre
            indice_ganador = probabilidades.index(max_prob) + 1
            
            # Sumamos el total de todas las probabilidades compitiendo para poder sacar los porcentajes relativos
            suma_probs = sum(probabilidades)
            
            # Normalizamos dividiendo el ganador entre el total y multiplicando por 100 para sacar el porcentaje
            # Se agrega un 'if' de seguridad para que el programa no colapse si la suma da cero absoluto
            prob_normalizada = (max_prob / suma_probs) * 100 if suma_probs > 0 else 0.0
            
            # Revisamos si la probabilidad matemática es extremadamente pequeña (menor a 0.0000000001)
            # Esto se usa como 'umbral', indicando que el punto fue graficado demasiado lejos de cualquier montaña
            if max_prob > 1e-10:
                return f"Pertenece a la Clase {indice_ganador} (Prob: {prob_normalizada:.2f}%)"
            else:
                # Si no supera esa pequeña esperanza mínima, lo declaramos como huérfano sin clase
                return "No pertenece, es huérfano (Probabilidad casi 0)."

    def obtener_parametros_barrera(self, umbral, metodo):
        parametros = []
        if metodo == "euclidiana":
            for c in self.centros:
                parametros.append((c[0], c[1], umbral*2, umbral*2, 0))
                
        elif metodo == "mahalanobis" or "probabilidad" in metodo:
            for c, cov in zip(self.centros, self.covs):
                eigenvalues, eigenvectors = np.linalg.eigh(cov)
                angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
                width = 2 * umbral * np.sqrt(abs(eigenvalues[0]))
                height = 2 * umbral * np.sqrt(abs(eigenvalues[1]))
                parametros.append((c[0], c[1], width, height, angle))
        return parametros