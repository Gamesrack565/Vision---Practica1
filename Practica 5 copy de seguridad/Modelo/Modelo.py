import numpy as np
from PIL import Image

class Modelo:
    def __init__(self):
        self.ruta_imagen = None
        self.imagen_array = None
        
        self.nombres_clases = []
        self.clases_rgb = [] 
        
        self.centros_rgb = []
        self.inv_covs_rgb = []
        self.det_covs_rgb = []

    def establecer_imagen(self, ruta):
        self.ruta_imagen = ruta
        imagen_pil = Image.open(ruta).convert('RGB')
        self.imagen_array = np.array(imagen_pil, dtype=float)

    def limpiar_datos(self):
        self.nombres_clases = []
        self.clases_rgb = []
        self.centros_rgb = []
        self.inv_covs_rgb = []
        self.det_covs_rgb = []

    def cargar_representantes(self, nombres, coordenadas_por_clase):
        self.nombres_clases = nombres
        self.clases_rgb = []
        
        for coords in coordenadas_por_clase:
            colores = [self.imagen_array[int(y), int(x)] for x, y in coords]
            self.clases_rgb.append(np.array(colores))
            
        self.centros_rgb, self.inv_covs_rgb, self.det_covs_rgb = self.entrenar(self.clases_rgb)

    def entrenar(self, dataset_rgb):
        centros = []
        inv_covs = []
        det_covs = []
        
        for C_rgb in dataset_rgb:
            u_rgb = np.mean(C_rgb, axis=0)
            centros.append(u_rgb)
            
            if len(C_rgb) > 1:
                sigma = np.cov(C_rgb, rowvar=False, ddof=0) 
                sigma += np.eye(3) * 1e-4 
            else:
                sigma = np.eye(3) * 1e-4
                
            inv_cov = np.linalg.inv(sigma)
            inv_covs.append(inv_cov)
            det_covs.append(np.linalg.det(sigma))
            
        return centros, inv_covs, det_covs

    def calcular_distancia_euclidiana(self, X, u):
        return np.linalg.norm(X - u)

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(abs(dist_cuadrada))

    def calcular_probabilidad(self, X, u, inv_cov, det_cov):
        n = 3
        mah_sq = self.calcular_distancia_mahalanobis(X, u, inv_cov) ** 2
        denominador = (((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))) + 1e-10
        return (1 / denominador) * np.exp(-0.5 * mah_sq)

    def clasificar_pixel(self, X_rgb, metodo, centros, inv_covs, det_covs):
        if metodo == "Euclidiana":
            distancias = [self.calcular_distancia_euclidiana(X_rgb, u) for u in centros]
            return np.argmin(distancias)
        elif metodo == "Mahalanobis":
            distancias = [self.calcular_distancia_mahalanobis(X_rgb, c, ic) for c, ic in zip(centros, inv_covs)]
            return np.argmin(distancias)
        elif metodo == "Probabilidad":
            probs = [self.calcular_probabilidad(X_rgb, c, ic, dc) for c, ic, dc in zip(centros, inv_covs, det_covs)]
            return np.argmax(probs)

    def evaluar_resustitucion(self, metodo_distancia):
        num_clases = len(self.nombres_clases)
        matriz = np.zeros((num_clases, num_clases), dtype=int)
        
        for i, C_rgb in enumerate(self.clases_rgb):
            for pixel in C_rgb:
                pred = self.clasificar_pixel(pixel, metodo_distancia, self.centros_rgb, self.inv_covs_rgb, self.det_covs_rgb)
                matriz[i][pred] += 1
                
        rendimiento = (np.trace(matriz) / np.sum(matriz)) * 100 if np.sum(matriz) > 0 else 0
        return {"matriz": matriz, "rendimiento": rendimiento}

    def evaluar_leave_one_out(self, metodo_distancia):
        num_clases = len(self.nombres_clases)
        matriz = np.zeros((num_clases, num_clases), dtype=int)
        
        for i, C_rgb in enumerate(self.clases_rgb):
            n_samples = len(C_rgb)
            for j in range(n_samples):
                clases_train = []
                for k, C_k in enumerate(self.clases_rgb):
                    if k == i:
                        clases_train.append(np.delete(C_k, j, axis=0))
                    else:
                        clases_train.append(C_k)
                
                centros, inv_covs, det_covs = self.entrenar(clases_train)
                pixel_test = C_rgb[j]
                pred = self.clasificar_pixel(pixel_test, metodo_distancia, centros, inv_covs, det_covs)
                matriz[i][pred] += 1
                
        rendimiento = (np.trace(matriz) / np.sum(matriz)) * 100 if np.sum(matriz) > 0 else 0
        return {"matriz": matriz, "rendimiento": rendimiento}

    def evaluar_cross_validation(self, metodo_distancia, iteraciones=20):
        num_clases = len(self.nombres_clases)
        resultados_iteraciones = []
        
        for _ in range(iteraciones // 2):
            clases_A = []
            clases_B = []
            
            for C_rgb in self.clases_rgb:
                indices = np.random.permutation(len(C_rgb))
                C_mezclado = C_rgb[indices]
                
                mitad = len(C_mezclado) // 2
                clases_A.append(C_mezclado[:mitad])
                clases_B.append(C_mezclado[mitad:])
                
            matriz_1 = np.zeros((num_clases, num_clases), dtype=int)
            centros_A, inv_covs_A, det_covs_A = self.entrenar(clases_A)
            for i, C_test in enumerate(clases_B):
                for pixel in C_test:
                    pred = self.clasificar_pixel(pixel, metodo_distancia, centros_A, inv_covs_A, det_covs_A)
                    matriz_1[i][pred] += 1
            rendimiento_1 = (np.trace(matriz_1) / np.sum(matriz_1)) * 100 if np.sum(matriz_1) > 0 else 0
            resultados_iteraciones.append({"matriz": matriz_1, "rendimiento": rendimiento_1})
            
            matriz_2 = np.zeros((num_clases, num_clases), dtype=int)
            centros_B, inv_covs_B, det_covs_B = self.entrenar(clases_B)
            for i, C_test in enumerate(clases_A):
                for pixel in C_test:
                    pred = self.clasificar_pixel(pixel, metodo_distancia, centros_B, inv_covs_B, det_covs_B)
                    matriz_2[i][pred] += 1
            rendimiento_2 = (np.trace(matriz_2) / np.sum(matriz_2)) * 100 if np.sum(matriz_2) > 0 else 0
            resultados_iteraciones.append({"matriz": matriz_2, "rendimiento": rendimiento_2})
            
        rendimiento_promedio = np.mean([res["rendimiento"] for res in resultados_iteraciones])
        
        return {
            "iteraciones": resultados_iteraciones, 
            "rendimiento_promedio": rendimiento_promedio
        }