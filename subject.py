from procces_data import procesar_data
from collections import Counter

UMBRAL_TENDENCIA = 100

class MonitorDeTendencias:
    def __init__(self, frecuencias=None, palabras_prohibidas=None):
        self.tendencias = frecuencias if frecuencias is not None else {}
        self.palabras_prohibidas = palabras_prohibidas if palabras_prohibidas is not None else []
        self.observers = []

    def agregar_observer(self, observer):
        self.observers.append(observer)

    def notificar_observers(self, palabra):
        for observer in self.observers:
            observer.actualizar(palabra)

    def procesar_y_actualizar_datos(self):
        contenido_procesado = procesar_data()
        nuevas_frecuencias = Counter()

        if contenido_procesado:
            for contenido in contenido_procesado:
                for palabra in contenido.split():
                    nuevas_frecuencias[palabra] += 1

        for palabra, conteo in nuevas_frecuencias.items():
            if palabra not in self.palabras_prohibidas:
                self.tendencias[palabra] = self.tendencias.get(palabra, 0) + conteo
                if self.tendencias[palabra] >= UMBRAL_TENDENCIA:
                    self.notificar_observers(palabra)

