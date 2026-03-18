import numpy as np
from PIL import Image

class Modelo:
    def __init__(self):
        self.limites_clases = {
            "Negro": [50, 1220, 50, 310],
            "Rojo": [50, 1220, 315, 580],
            "Amarillo": [50, 1220, 585, 850]
        }
        
        self.clases = []
        self.centros = []
        self.nombres_clases = []
        
        self.clases_rgb = []
        self.centros_rgb = []
        self.covs_rgb = []
        self.inv_covs_rgb = []
        self.det_covs_rgb = []
        
        self.ruta_imagen = None
        self.imagen_array = None

    def establecer_imagen(self, ruta):
        self.ruta_imagen = ruta
        imagen_pil = Image.open(ruta).convert('RGB')
        self.imagen_array = np.array(imagen_pil, dtype=float)

    def inicializar_datos_entrenamiento(self, num_reps, clases_activas=None):
        self.clases.clear()
        self.centros.clear()
        self.nombres_clases.clear()
        self.clases_rgb.clear()

        if clases_activas is None:
            clases_activas = list(self.limites_clases.keys())

        for nombre in clases_activas:
            if nombre in self.limites_clases:
                xmin, xmax, ymin, ymax = self.limites_clases[nombre]
                
                x_coords = np.random.randint(low=int(xmin), high=int(xmax), size=num_reps)
                y_coords = np.random.randint(low=int(ymin), high=int(ymax), size=num_reps)
                
                C_espacial = np.column_stack((x_coords, y_coords))
                self.clases.append(C_espacial)
                self.nombres_clases.append(nombre)
                
                u_espacial = self.centro_gravedad(C_espacial)
                self.centros.append(u_espacial)
                
                C_rgb = self.imagen_array[y_coords, x_coords] 
                self.clases_rgb.append(C_rgb)
                
        # Entrenar con el dataset completo inicialmente
        self.centros_rgb, self.covs_rgb, self.inv_covs_rgb, self.det_covs_rgb = self.entrenar(self.clases_rgb)

    # NUEVO: Función para calcular hiperparámetros de cualquier subconjunto de datos
    def entrenar(self, dataset_rgb):
        centros = []
        covs = []
        inv_covs = []
        det_covs = []
        
        for C_rgb in dataset_rgb:
            u_rgb = self.centro_gravedad(C_rgb)
            centros.append(u_rgb)
            
            cov_rgb, inv_cov_rgb = self.calcular_covarianza_e_inversa(C_rgb, u_rgb)
            covs.append(cov_rgb)
            inv_covs.append(inv_cov_rgb)
            
            det_covs.append(np.linalg.det(cov_rgb))
            
        return centros, covs, inv_covs, det_covs

    def centro_gravedad(self, C):
        return np.mean(C, axis=0)

    def calcular_distancia_euclidiana(self, X, u):
        return np.linalg.norm(X - u)

    def calcular_covarianza_e_inversa(self, C, u):
        N = len(C)
        C_centrado = C - u 
        sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
        sigma += np.eye(3) * 1e-2 
        sigma_inversa = np.linalg.inv(sigma)
        return sigma, sigma_inversa

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(abs(dist_cuadrada))

    def calcular_probabilidad(self, X, u, inv_cov, det_cov):
        n = 3
        distancia_mah = self.calcular_distancia_mahalanobis(X, u, inv_cov)
        mah_sq = distancia_mah ** 2
        denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))
        exponente = np.exp(-0.5 * mah_sq)
        probabilidad = (1 / denominador) * exponente
        return probabilidad

    # NUEVO: Clasificador ligero exclusivo para las evaluaciones
    def clasificar_rgb_eval(self, X_rgb, metodo, centros, inv_covs, det_covs):
        if metodo == "Euclidiana":
            distancias = [self.calcular_distancia_euclidiana(X_rgb, u) for u in centros]
            return np.argmin(distancias)
        elif metodo == "Mahalanobis":
            distancias = [self.calcular_distancia_mahalanobis(X_rgb, c, ic) for c, ic in zip(centros, inv_covs)]
            return np.argmin(distancias)
        elif metodo == "Probabilidad":
            probs = [self.calcular_probabilidad(X_rgb, c, ic, dc) for c, ic, dc in zip(centros, inv_covs, det_covs)]
            return np.argmax(probs)

    # ================= MÉTODOS DE EVALUACIÓN =================

    def evaluar_resustitucion(self, metodo_distancia):
        num_clases = len(self.nombres_clases)
        matriz = np.zeros((num_clases, num_clases), dtype=int)
        
        # Mismo set para entrenar y probar
        for i, C_rgb in enumerate(self.clases_rgb):
            for pixel in C_rgb:
                pred = self.clasificar_rgb_eval(pixel, metodo_distancia, self.centros_rgb, self.inv_covs_rgb, self.det_covs_rgb)
                matriz[i][pred] += 1
        return matriz

    def evaluar_cross_validation(self, metodo_distancia):
        num_clases = len(self.nombres_clases)
        matriz = np.zeros((num_clases, num_clases), dtype=int)
        
        clases_train = []
        clases_test = []
        
        # Dividir a la mitad
        for C_rgb in self.clases_rgb:
            mitad = len(C_rgb) // 2
            clases_train.append(C_rgb[:mitad])
            clases_test.append(C_rgb[mitad:])
            
        # Entrenar con la mitad
        centros, covs, inv_covs, det_covs = self.entrenar(clases_train)
        
        # Probar con la otra mitad
        for i, C_test in enumerate(clases_test):
            for pixel in C_test:
                pred = self.clasificar_rgb_eval(pixel, metodo_distancia, centros, inv_covs, det_covs)
                matriz[i][pred] += 1
        return matriz

    def evaluar_leave_one_out(self, metodo_distancia):
        num_clases = len(self.nombres_clases)
        matriz = np.zeros((num_clases, num_clases), dtype=int)
        
        for i, C_rgb in enumerate(self.clases_rgb):
            n_samples = len(C_rgb)
            for j in range(n_samples):
                clases_train = []
                for k, C_k in enumerate(self.clases_rgb):
                    if k == i:
                        # Elimina 1 muestra para entrenar
                        clases_train.append(np.delete(C_k, j, axis=0))
                    else:
                        clases_train.append(C_k)
                
                # Entrenar temporalmente
                centros, covs, inv_covs, det_covs = self.entrenar(clases_train)
                
                # Probar exclusivamente con la muestra eliminada
                pixel_test = C_rgb[j]
                pred = self.clasificar_rgb_eval(pixel_test, metodo_distancia, centros, inv_covs, det_covs)
                matriz[i][pred] += 1
                
        return matriz

    # ==========================================================

    def clasificar_punto(self, px, py):
        if not self.centros_rgb:
            raise ValueError("Las clases no han sido inicializadas.")

        h, w = self.imagen_array.shape[:2]
        
        if px < 0 or px >= w or py < 0 or py >= h:
            mensaje_fuera = "No pertenece, fuera de la imagen"
            return {
                "Euclidiana": {"ganador": mensaje_fuera, "valor": 0.0},
                "Mahalanobis": {"ganador": mensaje_fuera, "valor": 0.0},
                "Probabilidad": {"ganador": mensaje_fuera, "detalle": ["Coordenada fuera de los límites de la imagen."]},
                "Punto": [px, py]
            }

        px_int, py_int = int(px), int(py)
        X_rgb = self.imagen_array[py_int, px_int]

        # Euclidiana
        dist_euclidianas = [self.calcular_distancia_euclidiana(X_rgb, u) for u in self.centros_rgb]
        min_euclidiana = min(dist_euclidianas)
        idx_euclidiana = dist_euclidianas.index(min_euclidiana)
        res_euclidiana = f"Pertenece a Clase {self.nombres_clases[idx_euclidiana]}" if min_euclidiana < 100 else "No pertenece, es huérfano"

        # Mahalanobis
        dist_mahalanobis = [self.calcular_distancia_mahalanobis(X_rgb, c, ic) for c, ic in zip(self.centros_rgb, self.inv_covs_rgb)]
        min_mahalanobis = min(dist_mahalanobis)
        idx_mahalanobis = dist_mahalanobis.index(min_mahalanobis)
        res_mahalanobis = f"Pertenece a Clase {self.nombres_clases[idx_mahalanobis]}" if min_mahalanobis < 4.0 else "No pertenece, es huérfano"

        # Probabilidad
        probabilidades = [self.calcular_probabilidad(X_rgb, c, ic, dc) for c, ic, dc in zip(self.centros_rgb, self.inv_covs_rgb, self.det_covs_rgb)]
        max_prob = max(probabilidades)
        idx_prob = probabilidades.index(max_prob)
        
        suma_probs = sum(probabilidades)
        porcentajes = [(p / suma_probs) * 100 if suma_probs > 0 else 0.0 for p in probabilidades]
        detalle_proba = []
        
        if max_prob > 1e-15:
            res_prob = f"Pertenece a Clase {self.nombres_clases[idx_prob]}"
            for i, nombre in enumerate(self.nombres_clases):
                estado = "Pertenece" if i == idx_prob else "No pertenece"
                detalle_proba.append(f"{nombre} = {porcentajes[i]:.4f}% - {estado}")
        else:
            res_prob = "No pertenece, es huérfano (Probabilidad casi 0)"
            for nombre in self.nombres_clases:
                detalle_proba.append(f"{nombre} = 0.0000% - No pertenece")

        return {
            "Euclidiana": {"ganador": res_euclidiana, "valor": min_euclidiana},
            "Mahalanobis": {"ganador": res_mahalanobis, "valor": min_mahalanobis},
            "Probabilidad": {"ganador": res_prob, "detalle": detalle_proba},
            "Punto": [px, py]
        }