import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk
from collections import Counter
from create_dat import cargar_estado, guardar_estado
from observer import ConsolaObserver, ArchivoObserver
from subject import MonitorDeTendencias
import os 

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(1200, 600)  
        self.set_title("Analizador de Tendencias")

        frecuencias, palabras_prohibidas = cargar_estado()

        self.monitor = MonitorDeTendencias(frecuencias, palabras_prohibidas)
        self.monitor.agregar_observer(ConsolaObserver())
        self.monitor.agregar_observer(ArchivoObserver())

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_child(main_box)

        self.create_processing_box(main_box)

        self.create_top10_box(main_box)

        self.create_alerts_log_box(main_box)

        self.actualizar_top_10()
        self.actualizar_alertas_log()

    def create_processing_box(self, parent_box):
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_box.set_margin_start(10)
        left_box.set_margin_top(10)
        left_box.set_margin_end(5)
        left_box.set_hexpand(True)
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

        parent_box.append(left_box)

    def create_top10_box(self, parent_box):
        top10_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        top10_box.set_margin_start(5)
        top10_box.set_margin_top(10)
        top10_box.set_margin_end(5)
        top10_box.set_halign(Gtk.Align.CENTER)
        top10_box.set_hexpand(True)
        top10_box.add_css_class("main-box")
        
        label_top_10 = Gtk.Label(label="Top 10 de Palabras")
        label_top_10.add_css_class("section-title")
        top10_box.append(label_top_10)

        self.label_top_10_list = Gtk.Label()
        self.label_top_10_list.set_xalign(0)
        self.label_top_10_list.set_yalign(0)
        self.label_top_10_list.set_justify(Gtk.Justification.CENTER)
        self.label_top_10_list.set_hexpand(True)
        self.label_top_10_list.set_vexpand(True)
        self.label_top_10_list.add_css_class("top-10-list")
        self.label_top_10_list.set_label("Cargando...")
        top10_box.append(self.label_top_10_list)
        
        parent_box.append(top10_box)

    def create_alerts_log_box(self, parent_box):
        alerts_log_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        alerts_log_box.set_margin_start(5)
        alerts_log_box.set_margin_top(10)
        alerts_log_box.set_margin_end(10)
        alerts_log_box.set_halign(Gtk.Align.CENTER)
        alerts_log_box.set_hexpand(True) 
        alerts_log_box.add_css_class("main-box")

        label_alertaslog = Gtk.Label(label="ALERTAS LOG")
        label_alertaslog.add_css_class("section-title")
        alerts_log_box.append(label_alertaslog)

        self.label_alertaslog_list = Gtk.Label()
        self.label_alertaslog_list.set_xalign(0)
        self.label_alertaslog_list.set_yalign(0)
        self.label_alertaslog_list.set_justify(Gtk.Justification.CENTER)
        self.label_alertaslog_list.set_hexpand(True)
        self.label_alertaslog_list.set_vexpand(True)
        self.label_alertaslog_list.add_css_class("alertas-log-list")
        self.label_alertaslog_list.set_label("Cargando...")
        alerts_log_box.append(self.label_alertaslog_list)

        parent_box.append(alerts_log_box)

    def on_procesar_clicked(self, button):
        print("Iniciando el procesamiento de datos...")
        self.monitor.procesar_y_actualizar_datos()
        guardar_estado(self.monitor.tendencias, self.monitor.palabras_prohibidas)
        self.actualizar_top_10()
        self.actualizar_alertas_log()
        print("Procesamiento de datos completado y estado guardado.")

    def on_consultar_clicked(self, button):
        palabra = self.entrada_palabra.get_text().lower()
        frecuencia = self.monitor.tendencias.get(palabra, 0)
        self.label_resultado.set_label(f"Frecuencia de '{palabra}': {frecuencia}")

    def actualizar_top_10(self):
        top_10 = Counter(self.monitor.tendencias).most_common(10)
        lista_texto = "\n".join([f"{palabra} " for palabra, frecuencia in top_10])
        self.label_top_10_list.set_label(lista_texto)
    
    def actualizar_alertas_log(self):
        nombre_archivo = '.alertas.log'
        if not os.path.exists(nombre_archivo):
            self.label_alertaslog_list.set_label("No hay alertas registradas.")
            return

        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            log_texto = "".join(lineas[-10:])
            self.label_alertaslog_list.set_label(log_texto)

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