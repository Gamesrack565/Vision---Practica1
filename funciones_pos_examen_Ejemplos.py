import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# SECCIÓN 1: PROBLEMA 1 (CUBO 3D Y CLASIFICACIÓN)
# =====================================================================

def generar_clases_cubo():
    # Define las coordenadas de los vértices para cada clase en el espacio 3D (R, G, B)
    # MODIFICAR: Si el profesor cambia los colores que pertenecen a cada clase, 
    # actualiza estas coordenadas (1 = 255, 0 = 0).
    clase_rgb = np.array([
        [1, 0, 0],  # Rojo
        [0, 1, 0],  # Verde
        [0, 0, 1]   # Azul
    ])
    
    clase_cmy = np.array([
        [0, 1, 1],  # Cian
        [1, 0, 1],  # Magenta
        [1, 1, 0]   # Amarillo
    ])
    
    clase_grises = np.array([
        [0, 0, 0],  # Negro
        [1, 1, 1]   # Blanco
    ])
    
    return clase_rgb, clase_cmy, clase_grises

def calcular_centroide(clase_puntos):
    # Calcula el centro de gravedad promediando las coordenadas X, Y, Z de la clase
    return np.mean(clase_puntos, axis=0)

def validar_limites_cubo(vector_3d, limite_inf=0.0, limite_sup=1.0):
    # Verifica que el vector ingresado por el profesor no se salga del cubo unitario
    # MODIFICAR: Si el problema cambia de un cubo unitario (0 a 1) a un cubo RGB estándar (0 a 255),
    # cambia el valor de limite_sup al llamar a la función.
    if np.any(vector_3d < limite_inf) or np.any(vector_3d > limite_sup):
        return False
    return True

def clasificar_vector_cubo(vector_profesor, centros):
    # Verifica primero la regla estricta del examen (Punto 4 del examen práctico)
    if not validar_limites_cubo(vector_profesor):
        return "El punto sale de los límites del cubo. No pertenece a ninguna clase."
    
    # Si está dentro, calcula la distancia Euclidiana hacia los centros de cada clase
    # MODIFICAR: Si pide Mahalanobis en lugar de Euclidiana, se debe inyectar la matriz inversa aquí.
    distancias = [np.linalg.norm(vector_profesor - centro) for centro in centros]
    
    # Determina cuál es la distancia más corta
    distancia_min = min(distancias)
    indice_ganador = distancias.index(distancia_min) + 1
    
    # Nombres de las clases para la salida final
    nombres_clases = ["RGB", "CMY", "Blanco y Negro (Grises)"]
    
    return f"El vector pertenece a la Clase {indice_ganador}: {nombres_clases[indice_ganador-1]}"

def graficar_cubo_3d(clases, vector_prueba=None):
    # Emula el comando plot3 de Matlab
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # MODIFICAR: Los colores de visualización en la gráfica.
    colores_plot = ['red', 'cyan', 'black']
    etiquetas = ['Clase 1 (RGB)', 'Clase 2 (CMY)', 'Clase 3 (Grises)']
    
    for i, clase in enumerate(clases):
        ax.scatter(clase[:,0], clase[:,1], clase[:,2], c=colores_plot[i], label=etiquetas[i], s=100)
    
    # Si el profesor dio un vector, lo dibuja en la gráfica como una estrella
    if vector_prueba is not None and validar_limites_cubo(vector_prueba):
        ax.scatter(vector_prueba[0], vector_prueba[1], vector_prueba[2], c='green', marker='*', s=200, label='Vector Profesor')
        
    ax.set_xlabel('Eje X (Rojo)')
    ax.set_ylabel('Eje Y (Verde)')
    ax.set_zlabel('Eje Z (Azul)')
    ax.set_title('Cubo Unitario de Clasificación')
    ax.legend()
    plt.show()

# =====================================================================
# SECCIÓN 2: PROBLEMA 2 (EXPLICACIÓN Y EJEMPLO PARA "LIZ")
# =====================================================================

def generar_letra_L(num_representantes, offset_x, offset_y, dispersion):
    # Una 'L' consiste en una línea vertical y una horizontal.
    # Dividimos los representantes en dos trazos.
    puntos_vertical = num_representantes // 2
    puntos_horizontal = num_representantes - puntos_vertical
    
    # Trazo vertical (X constante, Y varía)
    x_vert = np.ones(puntos_vertical) * offset_x + (np.random.randn(puntos_vertical) * dispersion)
    y_vert = np.linspace(offset_y, offset_y + 5, puntos_vertical) + (np.random.randn(puntos_vertical) * dispersion)
    
    # Trazo horizontal (X varía, Y constante en la base)
    x_horiz = np.linspace(offset_x, offset_x + 3, puntos_horizontal) + (np.random.randn(puntos_horizontal) * dispersion)
    y_horiz = np.ones(puntos_horizontal) * offset_y + (np.random.randn(puntos_horizontal) * dispersion)
    
    # Unimos ambos trazos para formar la clase completa
    x_letra = np.concatenate([x_vert, x_horiz])
    y_letra = np.concatenate([y_vert, y_horiz])
    
    return np.column_stack((x_letra, y_letra))

def generar_letra_I(num_representantes, offset_x, offset_y, dispersion):
    # Una 'I' es solo una línea vertical
    x_letra = np.ones(num_representantes) * offset_x + (np.random.randn(num_representantes) * dispersion)
    y_letra = np.linspace(offset_y, offset_y + 5, num_representantes) + (np.random.randn(num_representantes) * dispersion)
    
    return np.column_stack((x_letra, y_letra))

def generar_letra_Z(num_representantes, offset_x, offset_y, dispersion):
    # Una 'Z' tiene 3 trazos: superior, diagonal, inferior
    puntos_trazo = num_representantes // 3
    
    # Superior (horizontal)
    x_sup = np.linspace(offset_x, offset_x + 3, puntos_trazo) + (np.random.randn(puntos_trazo) * dispersion)
    y_sup = np.ones(puntos_trazo) * (offset_y + 5) + (np.random.randn(puntos_trazo) * dispersion)
    
    # Inferior (horizontal)
    x_inf = np.linspace(offset_x, offset_x + 3, puntos_trazo) + (np.random.randn(puntos_trazo) * dispersion)
    y_inf = np.ones(puntos_trazo) * offset_y + (np.random.randn(puntos_trazo) * dispersion)
    
    # Diagonal
    puntos_restantes = num_representantes - (puntos_trazo * 2)
    x_diag = np.linspace(offset_x + 3, offset_x, puntos_restantes) + (np.random.randn(puntos_restantes) * dispersion)
    y_diag = np.linspace(offset_y + 5, offset_y, puntos_restantes) + (np.random.randn(puntos_restantes) * dispersion)
    
    x_letra = np.concatenate([x_sup, x_diag, x_inf])
    y_letra = np.concatenate([y_sup, y_diag, y_inf])
    
    return np.column_stack((x_letra, y_letra))