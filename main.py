from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# Ajustar tamaño de ventana para pruebas de escritorio
Window.size = (375, 667)  # Tamaño aproximado de un smartphone

# Importar pantallas
from screens.entry_screen import EntryScreen
from screens.login_screen import LoginScreen
class ReflectApp(MDApp):
    def build(self):
        # Configurar tema
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Purple"
        self.theme_cls.theme_style = "Light"  # "Dark" para tema oscuro

        # Crear administrador de pantallas
        self.sm = ScreenManager()

        # Añadir pantallas
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(EntryScreen(name="entry"))

        return self.sm

    def on_start(self):
        # Inicialización cuando arranca la app
        print("Aplicación iniciada")

        # Aquí puedes cargar configuraciones, verificar login, etc.
        pass


if __name__ == "__main__":
    ReflectApp().run()