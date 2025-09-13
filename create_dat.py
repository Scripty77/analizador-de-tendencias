import os
import pickle

def cargar_estado():
    nombre_archivo = '.estado.dat'
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, 'rb') as archivo:
                estado = pickle.load(archivo)
                return estado['frecuencias'], estado['prohibidas']
        except Exception:
            return {}, set()
    else:
        return {}, set()

def guardar_estado(frecuencias, prohibidas):
    nombre_archivo = '.estado.dat'
    estado_a_guardar = {
        'frecuencias': frecuencias,
        'prohibidas': prohibidas
    }
    with open(nombre_archivo, 'wb') as archivo:
        pickle.dump(estado_a_guardar, archivo)
