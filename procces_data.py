from concurrent.futures import ThreadPoolExecutor
import os

# Ruta de los archivos
ruta_base = "c:/Users/jean2/Documents/Python_Proyects/data/"

# Función para procesar un solo archivo
def procesar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            return contenido
    except FileNotFoundError:
        return None

# Función para procesar todos los archivos con hilos
def procesar_data(directorio=ruta_base):
    contenido_procesado = []
    try:
        # Obtener la lista de nombres de archivos
        nombres_archivos = os.listdir(directorio)
        # Generar las rutas completas para cada archivo
        rutas_completas = [os.path.join(directorio, nombre) for nombre in nombres_archivos if os.path.isfile(os.path.join(directorio, nombre))]

        # Uso del ThreadPoolExecutor para ejecutar los hilos
        with ThreadPoolExecutor(max_workers=5) as executor:
            resultados = list(executor.map(procesar_archivo, rutas_completas))
        for contenido in resultados:
            if contenido is not None:
                contenido_procesado.append(contenido)
        return contenido_procesado
    except FileNotFoundError:
        print(f"Directorio no encontrado: {directorio}")

# Ejecutar el procesamiento concurrente
print(procesar_data())