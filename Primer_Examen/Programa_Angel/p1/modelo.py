import numpy as np

class ModeloCubo:
    def __init__(self):
        # Mapeo exacto de los vértices a sus nombres de colores
        self.diccionario_colores = {
            (0, 0, 0): "Negro",
            (1, 1, 1): "Blanco",
            (1, 0, 0): "Rojo",
            (0, 1, 0): "Verde",
            (0, 0, 1): "Azul",
            (0, 1, 1): "Cian",
            (1, 0, 1): "Magenta",
            (1, 1, 0): "Amarillo"
        }

    def generar_clases(self):
        clase_rgb = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        clase_cmy = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
        clase_grises = np.array([[0, 0, 0], [1, 1, 1]])
        return [clase_rgb, clase_cmy, clase_grises]

    def validar_limites(self, vector_prueba):
        return np.all((vector_prueba >= 0.0) & (vector_prueba <= 1.0))

    def identificar_color_exacto(self, vector_prueba):
        # Compara el vector del profesor contra los 8 vértices del cubo usando Euclidiana
        distancia_min = float('inf')
        color_ganador = "Desconocido"
        
        for vertice, nombre in self.diccionario_colores.items():
            dist = np.linalg.norm(vector_prueba - np.array(vertice))
            if dist < distancia_min:
                distancia_min = dist
                color_ganador = nombre
                
        return color_ganador

    # --- MATEMÁTICA ESTADÍSTICA (REUTILIZANDO TU LÓGICA) ---
    def obtener_parametros_estadisticos(self, clases):
        centros = []
        inv_covs = []
        det_covs = []
        
        for clase in clases:
            # Centro de gravedad
            u = np.mean(clase, axis=0)
            centros.append(u)
            
            # Covarianza e inversa (con el parche 1e-2 para evitar colapso matricial)
            N = len(clase)
            C_centrado = clase - u
            sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
            sigma += np.eye(sigma.shape[0]) * 1e-2  # Parche vital
            
            inv_covs.append(np.linalg.inv(sigma))
            det_covs.append(np.linalg.det(sigma))
            
        return centros, inv_covs, det_covs

    # --- FUNCIÓN PRINCIPAL DE CLASIFICACIÓN ---
    def clasificar_vector(self, vector_prueba, metodo="euclidiana"):
        if not self.validar_limites(vector_prueba):
            return "Fuera de límites", "Ninguna (Rechazado por regla del cubo)"

        clases = self.generar_clases()
        centros, inv_covs, det_covs = self.obtener_parametros_estadisticos(clases)
        
        # Identificamos a qué color se parece más físicamente
        color_detectado = self.identificar_color_exacto(vector_prueba)
        nombres_clases = ["Clase 1 (RGB)", "Clase 2 (CMY)", "Clase 3 (Grises)"]
        indice_ganador = -1

        if metodo == "euclidiana":
            distancias = [np.linalg.norm(vector_prueba - u) for u in centros]
            indice_ganador = np.argmin(distancias)
            
        elif metodo == "mahalanobis":
            distancias = []
            for u, inv_cov in zip(centros, inv_covs):
                v = vector_prueba - u
                dist = np.sqrt(abs(np.dot(np.dot(v, inv_cov), v.T)))
                distancias.append(dist)
            indice_ganador = np.argmin(distancias)
            
        elif metodo == "probabilidad":
            probabilidades = []
            n = 3 # Dimensiones (3D)
            for u, inv_cov, det_cov in zip(centros, inv_covs, det_covs):
                v = vector_prueba - u
                mah_sq = np.dot(np.dot(v, inv_cov), v.T)
                denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))
                prob = (1 / denominador) * np.exp(-0.5 * mah_sq)
                probabilidades.append(prob)
            indice_ganador = np.argmax(probabilidades) # Aquí gana el MAYOR, no el menor

        resultado_clase = nombres_clases[indice_ganador]
        
        return color_detectado, resultado_clase