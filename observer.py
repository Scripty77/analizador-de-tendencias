class ConsolaObserver:
    def actualizar(self, palabra):
        print(f"\n¡ALERTA DE TENDENCIA! La palabra '{palabra}' ha superado las 100 apariciones.")

class ArchivoObserver:
    def actualizar(self, palabra):
        nombre_archivo = '.alertas.log'
        with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
            archivo.write(f"ALERTA: La palabra '{palabra}' ha superado las 100 apariciones.\n")
