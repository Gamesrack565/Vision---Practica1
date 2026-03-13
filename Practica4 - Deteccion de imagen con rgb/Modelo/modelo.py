import numpy as np
from PIL import Image

class Modelo:
    def __init__(self):
        # Límites espaciales (solo para muestrear colores en la imagen)
        self.limites_clases = {
            "Negro": [50, 1220, 50, 310],
            "Rojo": [50, 1220, 315, 580],
            "Amarillo": [50, 1220, 585, 850]
        }
        
        # Variables para la Vista (Gráficas espaciales 2D)
        self.clases = []
        self.centros = []
        self.nombres_clases = []
        
        # Variables para la Matemática (Espacio de Color RGB 3D)
        self.clases_rgb = []
        self.centros_rgb = []
        self.covs_rgb = []
        self.inv_covs_rgb = []
        self.det_covs_rgb = []
        
        self.ruta_imagen = None
        self.imagen_array = None

    def establecer_imagen(self, ruta):
        self.ruta_imagen = ruta
        # Cargamos la imagen a la memoria RAM para poder leer los colores de los píxeles
        imagen_pil = Image.open(ruta).convert('RGB')
        self.imagen_array = np.array(imagen_pil, dtype=float)

    def inicializar_datos_entrenamiento(self, num_reps, clases_activas=None):
        self.clases.clear()
        self.centros.clear()
        self.nombres_clases.clear()
        
        self.clases_rgb.clear()
        self.centros_rgb.clear()
        self.covs_rgb.clear()
        self.inv_covs_rgb.clear()
        self.det_covs_rgb.clear()

        if clases_activas is None:
            clases_activas = list(self.limites_clases.keys())

        for nombre in clases_activas:
            if nombre in self.limites_clases:
                xmin, xmax, ymin, ymax = self.limites_clases[nombre]
                
                # 1. Generar coordenadas enteras aleatorias dentro de los límites
                x_coords = np.random.randint(low=int(xmin), high=int(xmax), size=num_reps)
                y_coords = np.random.randint(low=int(ymin), high=int(ymax), size=num_reps)
                
                # Guardar las coordenadas espaciales para que la Vista pueda dibujar la gráfica 2D
                C_espacial = np.column_stack((x_coords, y_coords))
                self.clases.append(C_espacial)
                self.nombres_clases.append(nombre)
                
                # Centro espacial (solo para dibujar la 'X' en la gráfica)
                u_espacial = self.centro_gravedad(C_espacial)
                self.centros.append(u_espacial)
                
                # 2. Extraer los colores RGB reales de la imagen usando las coordenadas generadas
                # Numpy usa índices [fila, columna] -> [Y, X]
                C_rgb = self.imagen_array[y_coords, x_coords] 
                self.clases_rgb.append(C_rgb)
                
                # 3. Calcular la Matemática en el espacio RGB 3D
                u_rgb = self.centro_gravedad(C_rgb)
                self.centros_rgb.append(u_rgb)
                
                cov_rgb, inv_cov_rgb = self.calcular_covarianza_e_inversa(C_rgb, u_rgb)
                self.covs_rgb.append(cov_rgb)
                self.inv_covs_rgb.append(inv_cov_rgb)
                
                det_cov = np.linalg.det(cov_rgb)
                self.det_covs_rgb.append(det_cov)

    def centro_gravedad(self, C):
        # Sirve tanto para coordenadas 2D como para colores 3D
        return np.mean(C, axis=0)

    def calcular_distancia_euclidiana(self, X, u):
        # Calcula distancia en 3D (R, G, B)
        return np.linalg.norm(X - u)

    def calcular_covarianza_e_inversa(self, C, u):
        N = len(C)
        C_centrado = C - u 
        sigma = (1/N) * np.dot(C_centrado.T, C_centrado)
        # Se agrega una matriz identidad para evitar colapso si un color es absolutamente sólido/constante
        sigma += np.eye(3) * 1e-2 
        sigma_inversa = np.linalg.inv(sigma)
        return sigma, sigma_inversa

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(abs(dist_cuadrada))

    def calcular_probabilidad(self, X, u, inv_cov, det_cov):
        n = 3 # AHORA TRABAJAMOS EN 3 DIMENSIONES (R, G, B), el exponente cambia a 3/2
        distancia_mah = self.calcular_distancia_mahalanobis(X, u, inv_cov)
        mah_sq = distancia_mah ** 2
        denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))
        exponente = np.exp(-0.5 * mah_sq)
        probabilidad = (1 / denominador) * exponente
        return probabilidad

    def clasificar_punto(self, px, py):
        if not self.centros_rgb:
            raise ValueError("Las clases no han sido inicializadas.")

        # Obtenemos el alto (h) y ancho (w) real de la imagen cargada
        h, w = self.imagen_array.shape[:2]
        
        # ================= CANDADO ESPACIAL =================
        # Verificamos si la coordenada ingresada está fuera de la imagen
        if px < 0 or px >= w or py < 0 or py >= h:
            mensaje_fuera = "No pertenece, fuera de la imagen"
            return {
                "Euclidiana": {"ganador": mensaje_fuera, "valor": 0.0},
                "Mahalanobis": {"ganador": mensaje_fuera, "valor": 0.0},
                "Probabilidad": {"ganador": mensaje_fuera, "detalle": ["Coordenada fuera de los límites de la imagen."]},
                "Punto": [px, py]
            }

        # Si pasa el candado, la convertimos a entero para buscar el píxel
        px_int = int(px)
        py_int = int(py)

        # EXTRAEMOS EL COLOR (RGB) DEL PUNTO DESCONOCIDO
        X_rgb = self.imagen_array[py_int, px_int]

        # ================= EUCLIDIANA (En espacio de color) =================
        dist_euclidianas = [self.calcular_distancia_euclidiana(X_rgb, u) for u in self.centros_rgb]
        min_euclidiana = min(dist_euclidianas)
        idx_euclidiana = dist_euclidianas.index(min_euclidiana)
        
        umbral_euclidiana = 100 
        
        if min_euclidiana < umbral_euclidiana:
            res_euclidiana = f"Pertenece a Clase {self.nombres_clases[idx_euclidiana]}"
        else:
            res_euclidiana = "No pertenece, es huérfano"

        # ================= MAHALANOBIS (En espacio de color) =================
        dist_mahalanobis = [self.calcular_distancia_mahalanobis(X_rgb, c, ic) for c, ic in zip(self.centros_rgb, self.inv_covs_rgb)]
        min_mahalanobis = min(dist_mahalanobis)
        idx_mahalanobis = dist_mahalanobis.index(min_mahalanobis)
        
        umbral_mahalanobis = 4.0 
        
        if min_mahalanobis < umbral_mahalanobis:
            res_mahalanobis = f"Pertenece a Clase {self.nombres_clases[idx_mahalanobis]}"
        else:
            res_mahalanobis = "No pertenece, es huérfano"

        # ================= PROBABILIDAD (En espacio de color) =================
        probabilidades = [self.calcular_probabilidad(X_rgb, c, ic, dc) for c, ic, dc in zip(self.centros_rgb, self.inv_covs_rgb, self.det_covs_rgb)]
        max_prob = max(probabilidades)
        idx_prob = probabilidades.index(max_prob)
        
        suma_probs = sum(probabilidades)
        porcentajes = [(p / suma_probs) * 100 if suma_probs > 0 else 0.0 for p in probabilidades]
        
        detalle_proba = []
        umbral_prob = 1e-15 
        
        if max_prob > umbral_prob:
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