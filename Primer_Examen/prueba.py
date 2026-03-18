import numpy as np
import matplotlib.pyplot as plt

def generar_imagen_prueba():
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    xx, yy = np.meshgrid(x, y)
    
    imagen = np.zeros((100, 100, 3))
    imagen[:,:,0] = xx  # Gradiente rojo
    imagen[:,:,1] = yy  # Gradiente verde
    imagen[:,:,2] = 0.5 # Azul constante
    return imagen


def cargar_imagen_usuario():
    while True:
        print("\n--- Selección de imagen de entrada ---")
        print("1) Cargar imagen desde archivo")
        print("2) Usar imagen de prueba")
        opcion = input("Elige una opción (1 o 2): ").strip()

        if opcion == "2":
            print("Se usara la imagen sintetica de prueba.")
            return generar_imagen_prueba()

        if opcion == "1":
            ruta = input("Ingrese la ruta de la imagen (ej. ./mi_imagen.jpg): ").strip()
            try:
                imagen = plt.imread(ruta)

                if imagen.ndim == 2:
                    imagen = np.stack((imagen, imagen, imagen), axis=2)
                elif imagen.ndim == 3 and imagen.shape[2] == 4:
                    imagen = imagen[:, :, :3]
                elif imagen.ndim != 3 or imagen.shape[2] < 3:
                    print("Formato de imagen no soportado. Use una imagen RGB.")
                    continue

                imagen = imagen.astype(np.float32)
                if imagen.max() > 1.0:
                    imagen = imagen / 255.0

                print("Imagen cargada correctamente.")
                return imagen
            except FileNotFoundError:
                print("No se encontró la imagen en esa ruta. Intente de nuevo.")
            except Exception as e:
                print(f"No fue posible cargar la imagen: {e}")
        else:
            print("Opción no válida. Intente de nuevo.")



def procesar_imagenes(imagen_original):
    # Clase 1: Solo componente en Rojo
    img_clase1 = imagen_original.copy()
    img_clase1[:,:,1] = 0
    img_clase1[:,:,2] = 0

    # Clase 2: Solo componente en Verde
    img_clase2 = imagen_original.copy()
    img_clase2[:,:,0] = 0
    img_clase2[:,:,2] = 0

    # Clase 3: Solo componente en Azul
    img_clase3 = imagen_original.copy()
    img_clase3[:,:,0] = 0
    img_clase3[:,:,1] = 0

    # Posición 4: Escala de grises (no será clase)
    gris = np.dot(imagen_original[...,:3], [0.2989, 0.5870, 0.1140])
    img_clase4 = np.stack((gris, gris, gris), axis=2) 
    
    return img_clase1, img_clase2, img_clase3, img_clase4

def extraer_representantes(*imagenes):
    # Extraemos 150 píxeles aleatorios
    representantes = {}
    np.random.seed(42) 
    
    for i, img in enumerate(imagenes, 1):
        pixeles_planos = img.reshape(-1, 3)
        indices_aleatorios = np.random.choice(pixeles_planos.shape[0], 150, replace=False)
        representantes[f'Imagen {i}'] = pixeles_planos[indices_aleatorios]
        
    return representantes

def solicitar_vector_usuario():
    while True:
        entrada = input("Con la ventana abierta, ingrese un vector RGB (r,g,b) o presione Enter para tocar la imagen: ").strip()
        if entrada == "":
            return None

        try:
            vector = np.array([float(x.strip()) for x in entrada.split(',')], dtype=np.float32)
            if vector.shape[0] != 3:
                print("Debe ingresar exactamente 3 valores.")
                continue

            if np.any(vector < 0):
                print("Los valores no pueden ser negativos.")
                continue

            if np.any(vector > 1.0):
                if np.any(vector > 255):
                    print("Si usa escala 0-255, los valores deben estar en ese rango.")
                    continue
                vector = vector / 255.0

            return vector
        except ValueError:
            print("Formato inválido. Use el formato r,g,b. Ejemplo: 120,80,255 o 0.5,0.2,1.0")

def clasificar_vector_rgb(vector):
    centroides = {
        "CLASE 1 (Rojo)": np.array([1.0, 0.0, 0.0], dtype=np.float32),
        "CLASE 2 (Verde)": np.array([0.0, 1.0, 0.0], dtype=np.float32),
        "CLASE 3 (Azul)": np.array([0.0, 0.0, 1.0], dtype=np.float32)
    }

    clase_ganadora = min(
        centroides,
        key=lambda nombre: np.linalg.norm(vector - centroides[nombre])
    )
    return clase_ganadora

def main():
    img_orig = cargar_imagen_usuario()  
    c1, c2, c3, c4 = procesar_imagenes(img_orig)
    
    dataset_representantes = extraer_representantes(c1, c2, c3, c4)
    print("Se han extraído 150 representantes de cada imagen.")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.canvas.manager.set_window_title('Problema 2 - Clasificación por Imágenes')

    fila_superior = np.hstack((c1, c2))
    fila_inferior = np.hstack((c3, c4))
    imagen_compuesta = np.vstack((fila_superior, fila_inferior))

    alto, ancho, _ = c1.shape
    ax.imshow(imagen_compuesta)
    ax.set_title('Clasificación por zonas: [Rojo | Verde] / [Azul | Grises]')
    ax.set_xticks([])
    ax.set_yticks([])

    def onclick(event):
        if event.inaxes != ax or event.xdata is None or event.ydata is None:
            return

        x = int(event.xdata)
        y = int(event.ydata)

        if y < alto and x < ancho:
            print(">>> Punto insertado: El vector pertenece a la CLASE 1 (Rojo)")
        elif y < alto and x >= ancho:
            print(">>> Punto insertado: El vector pertenece a la CLASE 2 (Verde)")
        elif y >= alto and x < ancho:
            print(">>> Punto insertado: El vector pertenece a la CLASE 3 (Azul)")
        else:
            print(">>> Punto insertado: El punto NO puede pertenecer a ninguna clase.")

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    print("\n--- INSTRUCCIONES PARA LA PRUEBA ---")
    print("Primero se mostrará la ventana.")
    print("Luego, en consola, puede escribir un vector o presionar Enter para clasificar tocando la imagen.")
    print("Haga clic sobre la imagen compuesta para evaluarlas por zona.")
    print("------------------------------------\n")
    
    plt.tight_layout()
    plt.show(block=False)

    print("\n--- CLASIFICACIÓN POR VECTOR ESCRITO ---")
    vector_usuario = solicitar_vector_usuario()
    if vector_usuario is not None:
        clase_vector = clasificar_vector_rgb(vector_usuario)
        print(f">>> El vector {vector_usuario.tolist()} pertenece a la {clase_vector}")
    else:
        print(">>> Modo clic habilitado: toque dentro de la imagen para clasificar.")

    plt.show()

if __name__ == "__main__":
    main()