import numpy as np

class Modelo:
    def __init__(self):
        self.nombres_clases = [] 
        self.clases_rgb = []     
        self.puntos_xy = []      
        self.centros_rgb = []    
        self.covs = []
        self.inv_covs = []
        self.det_covs = []
        
    def limpiar_modelo(self):
        self.nombres_clases.clear()
        self.clases_rgb.clear()
        self.puntos_xy.clear()
        self.centros_rgb.clear()
        self.covs.clear()
        self.inv_covs.clear()
        self.det_covs.clear()

    # NUEVO: El modelo provee los datos de las clases, no la vista
    def obtener_clases_predefinidas(self, alto, ancho):
        return [
            ("Pato Blanco", 1200, 2000, 250, 1100),     
            ("Patitos Amarillos", 100, 2413, 800, 1455),     
            ("Pasto Verde", 0, 2600, 50, 1500),       
            ("Flores Rojas", 0, 2500, 80, 1200),      
            ("Cielo Azul", 0, 2600, 0, 500),        
        ]

    def agregar_clase_desde_rangos(self, nombre, xmin, xmax, ymin, ymax, num_reps, imagen_matriz):
        alto, ancho = imagen_matriz.shape[0], imagen_matriz.shape[1]
        
        # Proteger los límites
        xmin, xmax = max(0, min(xmin, ancho-1)), max(0, min(xmax, ancho-1))
        ymin, ymax = max(0, min(ymin, alto-1)), max(0, min(ymax, alto-1))
        
        # 1. Extraer solo el cuadro (ROI) de la imagen
        roi = imagen_matriz[ymin:ymax+1, xmin:xmax+1, :3].astype(float)
        R = roi[:, :, 0]
        G = roi[:, :, 1]
        B = roi[:, :, 2]
        
        # 2. Crear una máscara de color dependiendo de la clase que estamos buscando
        mascara = np.zeros(R.shape, dtype=bool)
        nombre_lower = nombre.lower()
        
        if "blanco" in nombre_lower:
            # El blanco necesita que TODOS los canales estén altísimos (cerca del 255)
            mascara = (R > 200) & (G > 200) & (B > 200)
        elif "amarillo" in nombre_lower:
            # El amarillo tiene rojo y verde altos, pero el azul debe estar bloqueado
            mascara = (R > 180) & (G > 170) & (B < 100)
        elif "verde" in nombre_lower:
            # El verde debe dominar por un buen margen sobre los otros dos
            mascara = (G > R + 30) & (G > B + 30)
        elif "roja" in nombre_lower or "rojo" in nombre_lower:
            # Aislamos el rojo puro: R alto, pero bloqueamos G y B para que no agarre amarillos, naranjas ni blancos cálidos
            mascara = (R > 150) & (G < 100) & (B < 100)
        elif "azul" in nombre_lower:
            # El azul domina sobre el rojo y verde
            mascara = (B > R + 30) & (B > G + 30) & (B > 100)
        else:
            mascara = np.ones(R.shape, dtype=bool)
            
        # 3. Obtener las coordenadas relativas al cuadro donde el color SÍ coincide
        y_roi, x_roi = np.where(mascara)
        
        # Protección: Si en ese cuadro gigante no hay ni un solo píxel de ese color, agarramos todo
        if len(x_roi) == 0:
            y_roi, x_roi = np.where(np.ones(R.shape, dtype=bool))
            
        # 4. Transformar las coordenadas relativas del cuadro a coordenadas globales de la imagen real
        y_validos = y_roi + ymin
        x_validos = x_roi + xmin
        
        # 5. Seleccionar aleatoriamente 'num_reps' (ej. 1000) de los píxeles ya filtrados
        if len(x_validos) < num_reps:
            # Si hay muy poquitos píxeles de ese color, agarramos los que haya
            indices = np.arange(len(x_validos))
        else:
            # Seleccionamos al azar de la bolsa de píxeles filtrados
            indices = np.random.choice(len(x_validos), size=num_reps, replace=False)
            
        x_coords = x_validos[indices]
        y_coords = y_validos[indices]
        
        # 6. Guardar los puntos y entrenar el modelo (como lo tenías originalmente)
        puntos = np.column_stack((x_coords, y_coords))
        self.puntos_xy.append(puntos)
        
        colores = imagen_matriz[y_coords, x_coords, :3] 
        self.clases_rgb.append(colores)
        self.nombres_clases.append(nombre)
        
        u_rgb = self.centro_gravedad(colores)
        self.centros_rgb.append(u_rgb)
        
        cov, inv_cov, det_cov = self.calcular_estadisticas(colores)
        self.covs.append(cov)
        self.inv_covs.append(inv_cov)
        self.det_covs.append(det_cov)

    def agregar_clase_desde_clic(self, nombre, cx, cy, num_reps, disp, imagen_matriz):
        base_color = imagen_matriz[cy, cx, :3]
        img_rgb = imagen_matriz[:, :, :3].astype(float)
        
        distancias = np.linalg.norm(img_rgb - base_color, axis=2)
        y_validos, x_validos = np.where(distancias <= disp)

        if len(x_validos) < num_reps:
            indices_planos = np.argsort(distancias, axis=None)[:num_reps]
            y_validos, x_validos = np.unravel_index(indices_planos, distancias.shape)
        else:
            indices_aleatorios = np.random.choice(len(x_validos), size=num_reps, replace=False)
            y_validos = y_validos[indices_aleatorios]
            x_validos = x_validos[indices_aleatorios]

        puntos = np.column_stack((x_validos, y_validos))
        self.puntos_xy.append(puntos)
        
        colores = imagen_matriz[y_validos, x_validos, :3]
        self.clases_rgb.append(colores)
        self.nombres_clases.append(nombre)
        
        u_rgb = self.centro_gravedad(colores)
        self.centros_rgb.append(u_rgb)
        
        cov, inv_cov, det_cov = self.calcular_estadisticas(colores)
        self.covs.append(cov)
        self.inv_covs.append(inv_cov)
        self.det_covs.append(det_cov)

    def centro_gravedad(self, C):
        return np.mean(C, axis=0)

    def calcular_estadisticas(self, C):
        n_dims = C.shape[1] 
        cov = np.cov(C, rowvar=False, bias=True) 
        cov += np.eye(n_dims) * 1e-4 
        
        inv_cov = np.linalg.inv(cov)
        det_cov = np.linalg.det(cov)
        if det_cov == 0: det_cov = 1e-6 
        
        return cov, inv_cov, det_cov

    # --- FUNCIONES MATEMÁTICAS EXPLÍCITAS ---
    def calcular_distancia_euclidiana(self, X, u):
        # Distancia en 3 dimensiones (R, G, B)
        return np.sqrt(np.sum((X - u)**2))

    def calcular_distancia_mahalanobis(self, X, u, inv_cov):
        v = X - u 
        dist_cuadrada = np.dot(np.dot(v, inv_cov), v.T)
        return np.sqrt(abs(dist_cuadrada))

    def calcular_probabilidad(self, X, u, inv_cov, det_cov):
        n = 3 # n=3 porque analizamos 3 canales (R, G, B)
        distancia_mah = self.calcular_distancia_mahalanobis(X, u, inv_cov)
        mah_sq = distancia_mah ** 2
        
        denominador = ((2 * np.pi) ** (n / 2)) * np.sqrt(abs(det_cov))
        exponente = np.exp(-0.5 * mah_sq)
        probabilidad = (1 / denominador) * exponente
        return probabilidad

    # --- CLASIFICADOR ACTUALIZADO ---
    def clasificar(self, color_rgb, metodo="ninguna"):
        if not self.centros_rgb: return "No hay clases entrenadas."
        if metodo == "ninguna": return "Selecciona un método válido."

        # Convertimos el color a float por seguridad matemática
        color_rgb = np.array(color_rgb, dtype=float)

        if metodo == "euclidiana":
            distancias = [self.calcular_distancia_euclidiana(color_rgb, u) for u in self.centros_rgb]
            dist_min = min(distancias)
            indice_ganador = distancias.index(dist_min)
            
            # Un umbral de 150 unidades de color para decidir si es huérfano
            if dist_min < 150:
                return f"{self.nombres_clases[indice_ganador]} (Euc)"
            else:
                return "Huérfano (No se parece a nada)"
                
        elif metodo == "mahalanobis":
            distancias = [self.calcular_distancia_mahalanobis(color_rgb, c, ic) for c, ic in zip(self.centros_rgb, self.inv_covs)]
            suma_distancias = sum(distancias)
            dist_normalizada = [(d / suma_distancias) * 100 for d in distancias]
            
            minimo_norm = min(dist_normalizada)
            indice_ganador = dist_normalizada.index(minimo_norm)
            
            return f"{self.nombres_clases[indice_ganador]} (Mah: {minimo_norm:.2f}%)"
                
        elif "probabilidad" in metodo:
            probabilidades = [self.calcular_probabilidad(color_rgb, c, ic, dc) for c, ic, dc, in zip(self.centros_rgb, self.inv_covs, self.det_covs)]
            
            max_prob = max(probabilidades)
            indice_ganador = probabilidades.index(max_prob)
            suma_probs = sum(probabilidades)
            
            prob_norm = (max_prob / suma_probs) * 100 if suma_probs > 0 else 0.0
            
            if max_prob > 1e-25: # Umbral de probabilidad extremadamente bajo para RGB
                return f"{self.nombres_clases[indice_ganador]} (Prob: {prob_norm:.2f}%)"
            else:
                return "Huérfano (Probabilidad casi nula)"

