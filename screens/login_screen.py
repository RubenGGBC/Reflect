from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button.button import MDButton, MDButtonText
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )

        # Título - Actualizado el font_style
        title = MDLabel(
            text="ReflectApp",
            font_style="Display",  # Cambiado de H4 a Display
            halign="center",
            size_hint_y=None,
            height=dp(80)
        )
        layout.add_widget(title)

        # Subtítulo - Actualizado el font_style
        subtitle = MDLabel(
            text="Tu diario reflexivo con IA",
            font_style="Title",  # Cambiado de Subtitle1 a Title
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(subtitle)

        # Espacio
        spacer = MDBoxLayout(size_hint_y=None, height=dp(40))
        layout.add_widget(spacer)

        # Campo de correo
        self.email = MDTextField(
            hint_text="Correo electrónico",
            helper_text="Introduce tu correo electrónico",
            helper_text_mode="on_focus",
            icon_right="email",
            size_hint_x=None,
            width=dp(300),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.email)

        # Campo de contraseña
        self.password = MDTextField(
            hint_text="Contraseña",
            helper_text="Introduce tu contraseña",
            helper_text_mode="on_focus",
            icon_right="eye-off",
            size_hint_x=None,
            width=dp(300),
            pos_hint={"center_x": 0.5},
            password=True
        )
        layout.add_widget(self.password)

        # Espacio
        spacer2 = MDBoxLayout(size_hint_y=None, height=dp(20))
        layout.add_widget(spacer2)

        # Botón de inicio de sesión
        login_button = MDButton(
            style="elevated",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            on_release=self.login
        )
        login_button.add_widget(MDButtonText(text="Iniciar sesión"))
        layout.add_widget(login_button)

        # Botón de registro
        register_button = MDButton(
            style="text",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            on_release=self.show_register
        )
        register_button.add_widget(MDButtonText(text="¿No tienes cuenta? Regístrate"))
        layout.add_widget(register_button)

        # Espacio restante
        layout.add_widget(MDBoxLayout())

        self.add_widget(layout)

        # Dialog para mensajes
        self.dialog = None

    def login(self, instance):
        """Maneja el proceso de inicio de sesión"""
        # Validación básica
        if not self.email.text or not self.password.text:
            self.show_dialog("Error", "Por favor, completa todos los campos")
            return

        # TODO: Implementar autenticación real con Firebase
        print(f"Intentando iniciar sesión con: {self.email.text}")

        # Simulación de login exitoso
        self.manager.current = "entry"

    def show_register(self, instance):
        """Muestra la pantalla de registro o un diálogo"""
        # TODO: Implementar pantalla de registro
        self.show_dialog(
            "Registro",
            "Funcionalidad de registro próximamente disponible."
        )

    def show_dialog(self, title, text):
        """Muestra un diálogo con el texto proporcionado"""
        if self.dialog:
            self.dialog.dismiss()

        ok_button = MDButton(
            style="text",
            on_release=lambda x: self.dialog.dismiss()
        )
        ok_button.add_widget(MDButtonText(text="OK"))

        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[ok_button]
        )
        self.dialog.open()