class MonitorDeTendencias:
    """Sujeto (Observable) que notifica a los observadores sobre tendencias."""

    def __init__(self):
        self.tendencias = {}
        self.observers = []

    def agregar_observer(self, observer):
        self.observers.append(observer)

    def notificar_observers(self, palabra):
        for observer in self.observers:
            observer.actualizar(palabra)

    def actualizar_tendencia(self, palabra, conteo):
        self.tendencias[palabra] = self.tendencias.get(palabra, 0) + conteo
        if self.tendencias[palabra] >= 100:
            self.notificar_observers(palabra)

    def frecuencia_palabra_critica(self, palabra):
        if palabra in self.tendencias and self.tendencias[palabra] > 100:
            return self.tendencias[palabra]
        return 0
