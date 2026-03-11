import numpy as np

class Modelo:
    def __init__(self):
        self.clases_datos = []
        self.nombres_clases = []
        self.centros = []
        self.covs = []
        self.inv_covs = []
        self.det_covs = []

    def entrenar_con_pixeles(self, datos_rgb_por_clase, nombres):
        self.clases_datos.clear()
        self.centros.clear()
        self.covs.clear()
        self.inv_covs.clear()
        self.det_covs.clear()
        self.nombres_clases = nombres

        for C in datos_rgb_por_clase:
            # Convertimos la lista de colores a una matriz matemática
            C = np.array(C, dtype=float)
            self.clases_datos.append(C)
            
            # Centro de gravedad (Media de los colores RGB)
            u = np.mean(C, axis=0)
            self.centros.append(u)
            
            # Covarianza e Inversa
            N = len(C)
            C_centrado = C - u 
            # Sumamos np.eye * 1e-5 para evitar matrices singulares si los pixeles son idénticos
            cov = (1/N) * np.dot(C_centrado.T, C_centrado) + (np.eye(C.shape[1]) * 1e-5)
            self.covs.append(cov)
            
            inv_cov = np.linalg.inv(cov)
            self.inv_covs.append(inv_cov)
            
            det_cov = np.linalg.det(cov)
            self.det_covs.append(det_cov)

    def calcular_distancia_euclidiana(self, X, u):
        return np.linalg.norm(X - u)

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(abs(dist_cuadrada))

    def calcular_probabilidad(self, X, u, inv_cov, det_cov):
        n = len(X) # Ahora n=3 porque usamos RGB en lugar de coordenadas XY
        distancia_mah = self.calcular_distancia_mahalanobis(X, u, inv_cov)
        mah_sq = distancia_mah ** 2
        denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))
        exponente = np.exp(-0.5 * mah_sq)
        probabilidad = (1 / denominador) * exponente
        return probabilidad

    def clasificar(self, X, umbral=1000):
        # Euclidiana
        dist_euc = [self.calcular_distancia_euclidiana(X, u) for u in self.centros]
        min_euc = min(dist_euc)
        ganador_euc = self.nombres_clases[dist_euc.index(min_euc)]

        # Mahalanobis
        dist_mah = [self.calcular_distancia_mahalanobis(X, c, ic) for c, ic in zip(self.centros, self.inv_covs)]
        min_mah = min(dist_mah)
        ganador_mah = self.nombres_clases[dist_mah.index(min_mah)]

        # Probabilidad (Bayes)
        probs = [self.calcular_probabilidad(X, c, ic, dc) for c, ic, dc in zip(self.centros, self.inv_covs, self.det_covs)]
        max_prob = max(probs)
        ganador_prob = self.nombres_clases[probs.index(max_prob)]

        return {
            "Euclidiana": ganador_euc if min_euc < umbral else "Huérfano",
            "Mahalanobis": ganador_mah if min_mah < umbral else "Huérfano",
            "Probabilidad": ganador_prob if max_prob > 1e-15 else "Huérfano"
        }