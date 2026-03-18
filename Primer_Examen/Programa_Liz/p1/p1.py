import numpy as np
import matplotlib.pyplot as plt

def dibujar_caras_cubo(ax):
    """Dibuja el esqueleto del cubo unitario (límites de 0 a 1)"""
    estilo = {'color': 'gray', 'linestyle': '--', 'linewidth': 1.5, 'alpha': 0.5}
    # Base y Techo
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], **estilo)
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [1, 1, 1, 1, 1], **estilo)
    # Postes
    for x, y in zip([0, 1, 1, 0], [0, 0, 1, 1]):
        ax.plot([x, x], [y, y], [0, 1], **estilo)

def dibujar_escena_base(ax, clase_rgb, clase_cmy, clase_gris, etiquetas):
    """Limpia y redibuja la estructura base del cubo y sus clases"""
    ax.clear()
    dibujar_caras_cubo(ax)
    
    ax.scatter(clase_rgb[:,0], clase_rgb[:,1], clase_rgb[:,2], c='red', s=100, label='Clase 1 (RGB)')
    ax.scatter(clase_cmy[:,0], clase_cmy[:,1], clase_cmy[:,2], c='cyan', s=100, label='Clase 2 (CMY)')
    ax.scatter(clase_gris[:,0], clase_gris[:,1], clase_gris[:,2], c='black', s=100, label='Clase 3 (Gris)')

    # Etiquetas de texto
    for coord, nombre in etiquetas.items():
        ax.text(coord[0], coord[1], coord[2] + 0.05, nombre, fontsize=9, fontweight='bold')

    # Estética de la gráfica
    ax.set_xlim([-0.2, 1.2])
    ax.set_ylim([-0.2, 1.2])
    ax.set_zlim([-0.2, 1.2])
    ax.set_xlabel('Eje X (Rojo)')
    ax.set_ylabel('Eje Y (Verde)')
    ax.set_zlabel('Eje Z (Azul)')
    ax.view_init(elev=25, azim=-50)

def main():
    print("="*50)
    print(" EXAMEN PRÁCTICO - PROBLEMA 1 (BUCLE INTERACTIVO)")
    print("="*50)

    # 1. Definición de las clases
    clase_rgb = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    clase_cmy = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    clase_gris = np.array([[0, 0, 0], [1, 1, 1]])

    etiquetas = {
        (0,0,0): "Negro", (1,1,1): "Blanco", (1,0,0): "Rojo", (0,1,0): "Verde",
        (0,0,1): "Azul", (0,1,1): "Cian", (1,0,1): "Magenta", (1,1,0): "Amarillo"
    }

    # Calculamos los centros de gravedad una sola vez
    centro_rgb = np.mean(clase_rgb, axis=0)
    centro_cmy = np.mean(clase_cmy, axis=0)
    centro_gris = np.mean(clase_gris, axis=0)

    # 2. Abrir gráfica al inicio
    plt.ion()
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    dibujar_escena_base(ax, clase_rgb, clase_cmy, clase_gris, etiquetas)
    ax.legend()
    plt.show(block=False)
    plt.pause(0.5)

    print("\nLa gráfica base se ha abierto.")

    # 3. Bucle interactivo
    while True:
        print("\n" + "-"*50)
        try:
            r = float(input("Ingresa el valor para X (Rojo)   [0.0 a 1.0]: "))
            g = float(input("Ingresa el valor para Y (Verde)  [0.0 a 1.0]: "))
            b = float(input("Ingresa el valor para Z (Azul)   [0.0 a 1.0]: "))
            vector_profesor = np.array([r, g, b])
        except ValueError:
            print("[ERROR] Por favor ingresa solo valores numéricos.")
            continue # Vuelve a preguntar sin cerrar el programa

        # Clasificación y Validación
        fuera_de_limites = np.any(vector_profesor < 0.0) or np.any(vector_profesor > 1.0)
        
        # Redibuja el cubo limpio antes de colocar el nuevo punto
        dibujar_escena_base(ax, clase_rgb, clase_cmy, clase_gris, etiquetas)

        print("\n" + "-"*50)
        if fuera_de_limites:
            print("RESULTADO: El punto sale de los límites del cubo.")
            print("           No pertenece a ninguna clase.")
            ax.scatter(vector_profesor[0], vector_profesor[1], vector_profesor[2], 
                       c='red', marker='X', s=200, label='Fuera de límite')
        else:
            distancias = [
                np.linalg.norm(vector_profesor - centro_rgb),
                np.linalg.norm(vector_profesor - centro_cmy),
                np.linalg.norm(vector_profesor - centro_gris)
            ]
            
            indice_ganador = np.argmin(distancias)
            nombres = ["Clase 1 (RGB)", "Clase 2 (CMY)", "Clase 3 (Grises)"]
            print(f"RESULTADO: El vector pertenece a la {nombres[indice_ganador]}")
            
            ax.scatter(vector_profesor[0], vector_profesor[1], vector_profesor[2], 
                       c='lime', marker='*', s=300, edgecolor='black', label='Vector Evaluado')
            
        print("-"*50 + "\n")

        ax.legend()
        plt.draw()
        plt.pause(0.1)

        # 4. Condición de salida
        respuesta = input("¿Quieres intentar otro vector? (si/no): ").strip().lower()
        if respuesta in ['no', 'n', 'nel']:
            print("\nCerrando programa...")
            break

    plt.ioff()
    plt.close('all')

if __name__ == "__main__":
    main()