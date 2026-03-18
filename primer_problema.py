import numpy as np
import matplotlib.pyplot as plt

def imprimir_tabla_verdad():
    print("Tabla de Verdad - Espacio de Color RGB")
    print("-" * 55)
    print(f"{'R':<3} | {'G':<3} | {'B':<3} || {'Clase Asignada':<18} | {'Color'}")
    print("-" * 55)
    
    # Clase 1: RGB
    print(f"{1:<3} | {0:<3} | {0:<3} || {'Clase 1 (RGB)':<18} | Rojo")
    print(f"{0:<3} | {1:<3} | {0:<3} || {'Clase 1 (RGB)':<18} | Verde")
    print(f"{0:<3} | {0:<3} | {1:<3} || {'Clase 1 (RGB)':<18} | Azul")
    
    # Clase 2: CMY
    print(f"{0:<3} | {1:<3} | {1:<3} || {'Clase 2 (CMY)':<18} | Cian")
    print(f"{1:<3} | {0:<3} | {1:<3} || {'Clase 2 (CMY)':<18} | Magenta")
    print(f"{1:<3} | {1:<3} | {0:<3} || {'Clase 2 (CMY)':<18} | Amarillo")
    
    # Clase 3: Grises
    print(f"{0:<3} | {0:<3} | {0:<3} || {'Clase 3 (Grises)':<18} | Negro")
    print(f"{1:<3} | {1:<3} | {1:<3} || {'Clase 3 (Grises)':<18} | Blanco")
    print("-" * 55 + "\n")

# Definición de los centroides de las clases (los vértices del cubo)
centroides = {
    "Clase 1 (RGB)": np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    "Clase 2 (CMY)": np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]]),
    "Clase 3 (Grises)": np.array([[0, 0, 0], [1, 1, 1]])
}

def graficar_espacio():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    colores_plot = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'gray']
    puntos = np.vstack(list(centroides.values()))
    
    # Graficar los puntos en el espacio 3D
    ax.scatter(puntos[:, 0], puntos[:, 1], puntos[:, 2], c=colores_plot, s=100)
    
    # Etiquetas y título
    ax.set_xlabel('Rojo (R)')
    ax.set_ylabel('Verde (G)')
    ax.set_zlabel('Azul (B)')
    ax.set_title('Espacio de Color RGB Binario (Cubo)')
    
    # block=False permite que el código siga ejecutándose mientras la gráfica está abierta
    plt.show(block=False) 


def calcular_distancia_euclidiana(X, u):
    return np.sqrt((X[0] - u[0])**2 + (X[1] - u[1])**2 + (X[2] - u[2])**2) 


def clasificar_vector(v_entrada):
    v = np.array(v_entrada)
    

    if np.any(v < 0) or np.any(v > 1):
        return "El vector NO pertenece a ninguna clase (fuera del cubo de color)."
    
    tolerancia_gris = 0.05 
    if np.std(v) <= tolerancia_gris: 
        return "El vector pertenece a la Clase 3 (Grises)"
    
    # 3. Si no es gris, evaluamos Clases 1 y 2
    # Comparamos la distancia solo contra los vértices de color
    vertices_color = {
        "Clase 1 (RGB)": np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        "Clase 2 (CMY)": np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    }
    
    distancia_min = float('inf')
    clase_asignada = None
    
    for nombre_clase, puntos in vertices_color.items():
        for punto in puntos:
            dist = np.linalg.norm(v - punto)
            if dist < distancia_min:
                distancia_min = dist
                clase_asignada = nombre_clase
                
    return f"El vector pertenece a la {clase_asignada}"

if __name__ == "__main__":
    # 1. Imprimir la tabla de verdad
    imprimir_tabla_verdad()
    
    # 2. Generar la gráfica
    graficar_espacio()
    
    print("--- Clasificación de Vectores ---")
    try:
        # 3 y 4. Interacción con el profesor
        entrada = input("Profesor, ingrese un vector 3D separado por comas (ej. 1,0,0) o un vector fuera de rango (ej. 5,8,10): ")
        
        # Convertimos la entrada de texto a una lista de números flotantes
        vector_profesor = [float(x.strip()) for x in entrada.split(',')]
        
        if len(vector_profesor) != 3:
            print("Error: El vector debe tener exactamente 3 componentes (R, G, B).")
        else:
            resultado = clasificar_vector(vector_profesor)
            print(f"\nResultado para el vector {vector_profesor}: \n>>> {resultado}")
            
    except ValueError:
        print("Entrada no válida. Por favor, asegúrese de ingresar solo números separados por comas.")
    
    # Mantiene la ventana de la gráfica abierta hasta que el usuario la cierre manualmente
    plt.show()