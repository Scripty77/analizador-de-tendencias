from concurrent.futures import ThreadPoolExecutor
import os

ruta_base = r"C:\Users\raiku\Documents\analizador-de-tendencias\data"

def procesar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            return contenido
    except FileNotFoundError:
        return None

def procesar_data(directorio=ruta_base):
    contenido_procesado = []
    try:
        #lista de nombres de archivos
        nombres_archivos = os.listdir(directorio)
        #rutas completas para cada archivo
        rutas_completas = [os.path.join(directorio, nombre) for nombre in nombres_archivos if os.path.isfile(os.path.join(directorio, nombre))]

        # Uso del ThreadPoolExecutor para ejecutar los hilos
        with ThreadPoolExecutor(max_workers=5) as executor:
            resultados = list(executor.map(procesar_archivo, rutas_completas))
        for contenido in resultados:
            if contenido is not None:
                contenido_lower = contenido.lower()
                contenido_procesado.append(contenido_lower)
        return contenido_procesado
    except FileNotFoundError:
        print(f"Directorio no encontrado: {directorio}")

def buscar_tendencia(contenido_procesado):
    palabras_repetidas = {}
    for contenido in contenido_procesado:
        palabras = contenido.split()
        for palabra in palabras:
            if palabra in palabras_repetidas:
                palabras_repetidas[palabra] += 1
            else:
                palabras_repetidas[palabra] = 1

    if not palabras_repetidas:
        return 0
    palabra_mas_repetida = max(palabras_repetidas, key=palabras_repetidas.get)
    palabra_prohibida = "GITHUB"
    if palabra_mas_repetida == palabra_prohibida:
        return 0
    else:
        return palabra_mas_repetida

def transformar_data_a_dat(palabra_mas_repetida):
    contenido_bat = []
    contenido_bat = "".join(f"Palabra en tendencia: {palabra_mas_repetida}")
    nombre_archivo = 'estado.dat'
    with open(nombre_archivo, 'w') as archivo:
        archivo.write((contenido_bat))
        return print(f"Archivo {nombre_archivo} creado exitosamente.")
