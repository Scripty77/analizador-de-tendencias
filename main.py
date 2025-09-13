import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk
from collections import Counter
import os
import pickle
from procces_data import procesar_data
from create_dat import cargar_estado, guardar_estado

UMBRAL_TENDENCIA = 100

class ConsolaObserver:
    def actualizar(self, palabra):
        print(f"\n¡ALERTA DE TENDENCIA! La palabra '{palabra}' ha superado las 100 apariciones.")

class ArchivoObserver:
    def actualizar(self, palabra):
        nombre_archivo = '.alertas.log'
        with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
            archivo.write(f"ALERTA: La palabra '{palabra}' ha superado las 100 apariciones.\n")

class MonitorDeTendencias:
    def __init__(self, frecuencias_iniciales, palabras_prohibidas):
        self.tendencias = frecuencias_iniciales
        self.palabras_prohibidas = palabras_prohibidas
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

    def frecuencia_palabra_critica(self, palabra):
        if palabra in self.tendencias and self.tendencias[palabra] > UMBRAL_TENDENCIA:
            return self.tendencias[palabra]
        return 0

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 500)
        self.set_title("Analizador de Tendencias")

        frecuencias, palabras_prohibidas = cargar_estado()

        self.monitor = MonitorDeTendencias(frecuencias, palabras_prohibidas)
        self.monitor.agregar_observer(ConsolaObserver())
        self.monitor.agregar_observer(ArchivoObserver())

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_child(main_box)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_box.set_margin_start(10)
        left_box.set_margin_top(10)
        left_box.set_margin_end(5)
        left_box.add_css_class("main-box")

        label_titulo = Gtk.Label(label="Procesamiento de Datos y Consulta")
        label_titulo.add_css_class("section-title")
        left_box.append(label_titulo)

        self.btn_procesar = Gtk.Button(label="Procesar Nuevos Datos")
        self.btn_procesar.connect("clicked", self.on_procesar_clicked)
        left_box.append(self.btn_procesar)

        label_consulta = Gtk.Label(label="Consultar Frecuencia de Palabra")
        label_consulta.add_css_class("section-title")
        left_box.append(label_consulta)

        self.entrada_palabra = Gtk.Entry()
        self.entrada_palabra.set_placeholder_text("Ingrese una palabra...")
        left_box.append(self.entrada_palabra)

        btn_consultar = Gtk.Button(label="Consultar")
        btn_consultar.connect("clicked", self.on_consultar_clicked)
        left_box.append(btn_consultar)

        self.label_resultado = Gtk.Label(label="Frecuencia: ")
        self.label_resultado.add_css_class("frequency-result")
        left_box.append(self.label_resultado)

        main_box.append(left_box)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        right_box.set_margin_start(5)
        right_box.set_margin_top(10)
        right_box.set_margin_end(10)
        right_box.set_halign(Gtk.Align.CENTER)
        right_box.add_css_class("main-box")

        label_top_10 = Gtk.Label(label="Top 10 de Palabras")
        label_top_10.add_css_class("section-title")
        right_box.append(label_top_10)

        self.label_top_10_list = Gtk.Label()
        self.label_top_10_list.set_xalign(0)
        self.label_top_10_list.set_yalign(0)
        self.label_top_10_list.set_justify(Gtk.Justification.CENTER)
        self.label_top_10_list.set_hexpand(True)
        self.label_top_10_list.set_vexpand(True)
        self.label_top_10_list.add_css_class("top-10-list")
        self.label_top_10_list.set_label("Cargando...")
        right_box.append(self.label_top_10_list)

        main_box.append(right_box)

        self.actualizar_top_10()

    def on_procesar_clicked(self, button):
        print("Iniciando el procesamiento de datos...")
        self.monitor.procesar_y_actualizar_datos()

        guardar_estado(self.monitor.tendencias, self.monitor.palabras_prohibidas)

        self.actualizar_top_10()
        print("Procesamiento de datos completado y estado guardado.")

    def on_consultar_clicked(self, button):
        palabra = self.entrada_palabra.get_text().lower()
        frecuencia = self.monitor.tendencias.get(palabra, 0)
        self.label_resultado.set_label(f"Frecuencia de '{palabra}': {frecuencia}")

    def actualizar_top_10(self):
        top_10 = Counter(self.monitor.tendencias).most_common(10)
        lista_texto = "\n".join([f"{palabra}" for palabra, frecuencia in top_10])
        self.label_top_10_list.set_label(lista_texto)

class App(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.css_provider = Gtk.CssProvider()
        try:
            self.css_provider.load_from_path('style.css')
        except gi.repository.GLib.Error as e:
            print(f"Error al cargar el archivo CSS: {e}")

    def do_activate(self):
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        window = MainWindow(application=self)
        window.present()

if __name__ == "__main__":
    app = App(application_id="org.example.analizador-de-tendencias")
    app.run()
