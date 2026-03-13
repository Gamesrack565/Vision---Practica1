import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# FUNCIONES GENERADORAS DE LETRAS (150 puntos por clase)
# =====================================================================
def generar_L(offset_x, offset_y, ruido=0.1):
    x_vert = np.full(100, 0.0)
    y_vert = np.linspace(0, 5, 100)
    x_horiz = np.linspace(0, 3, 50)
    y_horiz = np.full(50, 0.0)
    
    x = np.concatenate([x_vert, x_horiz]) + offset_x + np.random.randn(150) * ruido
    y = np.concatenate([y_vert, y_horiz]) + offset_y + np.random.randn(150) * ruido
    return np.column_stack((x, y))

def generar_C(offset_x, offset_y, ruido=0.1):
    x_sup = np.linspace(3, 0, 50)
    y_sup = np.full(50, 5.0)
    x_izq = np.full(50, 0.0)
    y_izq = np.linspace(5, 0, 50)
    x_inf = np.linspace(0, 3, 50)
    y_inf = np.full(50, 0.0)
    
    x = np.concatenate([x_sup, x_izq, x_inf]) + offset_x + np.random.randn(150) * ruido
    y = np.concatenate([y_sup, y_izq, y_inf]) + offset_y + np.random.randn(150) * ruido
    return np.column_stack((x, y))

def generar_S(offset_x, offset_y, ruido=0.1):
    x_1, y_1 = np.linspace(3, 0, 30), np.full(30, 5.0)           
    x_2, y_2 = np.full(30, 0.0), np.linspace(5, 2.5, 30)         
    x_3, y_3 = np.linspace(0, 3, 30), np.full(30, 2.5)           
    x_4, y_4 = np.full(30, 3.0), np.linspace(2.5, 0, 30)         
    x_5, y_5 = np.linspace(3, 0, 30), np.full(30, 0.0)           
    
    x = np.concatenate([x_1, x_2, x_3, x_4, x_5]) + offset_x + np.random.randn(150) * ruido
    y = np.concatenate([y_1, y_2, y_3, y_4, y_5]) + offset_y + np.random.randn(150) * ruido
    return np.column_stack((x, y))

def generar_A(offset_x, offset_y, ruido=0.1):
    x_izq, y_izq = np.linspace(0, 1.5, 60), np.linspace(0, 5, 60)
    x_der, y_der = np.linspace(1.5, 3, 60), np.linspace(5, 0, 60)
    x_mid, y_mid = np.linspace(0.75, 2.25, 30), np.full(30, 2.5)
    
    x = np.concatenate([x_izq, x_der, x_mid]) + offset_x + np.random.randn(150) * ruido
    y = np.concatenate([y_izq, y_der, y_mid]) + offset_y + np.random.randn(150) * ruido
    return np.column_stack((x, y))

# =====================================================================
# FUNCIÓN PARA DIBUJAR LA ESCENA LIMPIA
# =====================================================================
def dibujar_escena(ax, clases, colores, etiquetas):
    ax.clear() # Limpia lo anterior
    for i in range(4):
        ax.scatter(clases[i][:,0], clases[i][:,1], c=colores[i], label=etiquetas[i], s=15)
        
    ax.set_xlim(-2, 26)
    ax.set_ylim(-2, 8)
    ax.set_xticks(np.arange(-2, 27, 1))
    ax.set_yticks(np.arange(-2, 9, 1))
    ax.grid(True, linestyle='--', linewidth=0.5, color='gray')
    ax.set_title("Reconocimiento en 2D (Procedimiento IMREF2D)")

# =====================================================================
# FUNCIÓN PRINCIPAL CON BUCLE INTERACTIVO
# =====================================================================
def main():
    print("="*55)
    print(" EXAMEN PRÁCTICO - PROBLEMA 2 (BUCLE INTERACTIVO)")
    print("="*55)

    # 1. Generar clases
    clases = [
        generar_L(offset_x=1, offset_y=1),
        generar_C(offset_x=6, offset_y=1),
        generar_S(offset_x=11, offset_y=1),
        generar_A(offset_x=20, offset_y=1) # Letra adicional retirada
    ]
    centros = [np.mean(c, axis=0) for c in clases]
    etiquetas = ['Clase 1 (L)', 'Clase 2 (C)', 'Clase 3 (S)', 'Clase 4 (A)']
    colores = ['blue', 'green', 'purple', 'red']

    # 2. Configurar la ventana interactiva
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 5))
    dibujar_escena(ax, clases, colores, etiquetas)
    ax.legend(loc='upper right')
    plt.show(block=False)
    plt.pause(0.5)

    print("\nLa cuadrícula se ha abierto.")

    # 3. Bucle para múltiples vectores
    while True:
        # Pedir datos
        try:
            print("\n" + "-"*55)
            x_val = float(input("Ingresa coordenada X: "))
            y_val = float(input("Ingresa coordenada Y: "))
            vector_prueba = np.array([x_val, y_val])
        except ValueError:
            print("[ERROR] Formato inválido. Por favor ingresa solo números.")
            continue # Vuelve a preguntar sin romper el programa

        # Clasificación
        distancias = [np.linalg.norm(vector_prueba - centro) for centro in centros]
        distancia_min = min(distancias)
        indice_ganador = distancias.index(distancia_min)
        umbral_fondo = 3.5 
        
        # Limpiar y redibujar la escena base
        dibujar_escena(ax, clases, colores, etiquetas)

        # Evaluar y graficar el punto actual
        if distancia_min > umbral_fondo:
            print("RESULTADO: Cayó en el Fondo (Rechazado). No pertenece a ninguna clase.")
            ax.scatter(vector_prueba[0], vector_prueba[1], c='black', marker='X', s=200, label='Fondo (Rechazado)')
        else:
            print(f"RESULTADO: Pertenece a la {etiquetas[indice_ganador]}")
            ax.scatter(vector_prueba[0], vector_prueba[1], c='black', marker='*', s=200, label='Vector Clasificado')

        # Actualizar la gráfica visible
        ax.legend(loc='upper right')
        plt.draw()
        plt.pause(0.1)

        # 4. Preguntar si desea continuar
        respuesta = input("\n¿Quieres intentar otro vector? (si/no): ").strip().lower()
        if respuesta in ['no', 'n', 'nel']:
            print("\n¡Adiós! Cerrando programa...")
            break

    # 5. Cerrar todo al salir del bucle
    plt.ioff()
    plt.close('all')

if __name__ == "__main__":
    main()