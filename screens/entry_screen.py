from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.clock import Clock

# Importación simplificada
from services.ai_service import analyze_mock

class EntryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        self.layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20)
        )

        # Configurar UI
        self._setup_ui()

        # Añadir layout a la pantalla
        self.add_widget(self.layout)

        # Inicializar diálogo
        self.dialog = None

        # Inicializar variables
        self.selected_emotion = None
        self.selected_categories = set()

    def _setup_ui(self):
        """Configurar todos los elementos de la UI"""
        # Título
        title = MDLabel(
            text="¿Cómo ha sido tu día?",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)
        )
        self.layout.add_widget(title)

        # Campo de texto
        self.entry_text = MDTextField(
            hint_text="Reflexiona sobre tu día...",
            helper_text="Cuéntame lo bueno, lo malo y tus reflexiones",
            helper_text_mode="on_focus",
            multiline=True,
            size_hint=(1, None),
            height=dp(150)
        )
        self.layout.add_widget(self.entry_text)

        # Sección de emociones
        emotions_label = MDLabel(
            text="¿Cómo te has sentido hoy?",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )
        self.layout.add_widget(emotions_label)

        # Layout para botones de emociones (en lugar de chips)
        self.emotions_layout = MDBoxLayout(
            spacing=dp(10),
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )

        # Crear botones para emociones
        emotions = ["Feliz", "Tranquilo", "Triste", "Ansioso", "Productivo"]
        self.emotion_buttons = {}

        for emotion in emotions:
            button = MDFlatButton(
                text=emotion,
                size_hint=(None, None),
                height=dp(40),
                on_release=lambda x, e=emotion: self.select_emotion(e)
            )
            self.emotions_layout.add_widget(button)
            self.emotion_buttons[emotion] = button

        self.layout.add_widget(self.emotions_layout)

        # Sección de categorías
        categories_label = MDLabel(
            text="Categoriza tu entrada:",
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )
        self.layout.add_widget(categories_label)

        # Layout para botones de categorías
        self.categories_layout = MDBoxLayout(
            spacing=dp(10),
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )

        # Crear botones para categorías
        categories = ["Trabajo", "Personal", "Salud", "Relaciones", "Crecimiento"]
        self.category_buttons = {}

        for category in categories:
            button = MDFlatButton(
                text=category,
                size_hint=(None, None),
                height=dp(40),
                on_release=lambda x, c=category: self.toggle_category(c)
            )
            self.categories_layout.add_widget(button)
            self.category_buttons[category] = button

        self.layout.add_widget(self.categories_layout)

        # Botones de acción
        buttons_layout = MDBoxLayout(
            spacing=dp(10),
            adaptive_height=True,
            padding=[0, 20, 0, 10]
        )

        save_button = MDRaisedButton(
            text="Guardar entrada",
            on_release=self.save_entry,
            size_hint=(0.7, None),
            height=dp(50)
        )
        buttons_layout.add_widget(save_button)

        analyze_button = MDFlatButton(
            text="Analizar",
            on_release=self.analyze_entry,
            size_hint=(0.3, None),
            height=dp(50)
        )
        buttons_layout.add_widget(analyze_button)

        self.layout.add_widget(buttons_layout)

    def select_emotion(self, emotion):
        """Seleccionar una emoción"""
        # Deseleccionar emoción anterior
        if self.selected_emotion and self.selected_emotion in self.emotion_buttons:
            old_button = self.emotion_buttons[self.selected_emotion]
            old_button.md_bg_color = (0, 0, 0, 0)  # Color normal, transparente

        # Seleccionar nueva emoción
        self.selected_emotion = emotion
        button = self.emotion_buttons[emotion]
        button.md_bg_color = self.theme_cls.primary_light  # Color seleccionado
        print(f"Emoción seleccionada: {emotion}")

    def toggle_category(self, category):
        """Alternar selección de categoría"""
        button = self.category_buttons[category]

        if category in self.selected_categories:
            # Deseleccionar
            self.selected_categories.remove(category)
            button.md_bg_color = (0, 0, 0, 0)  # Color normal, transparente
        else:
            # Seleccionar
            self.selected_categories.add(category)
            button.md_bg_color = self.theme_cls.primary_light  # Color seleccionado

        print(f"Categorías seleccionadas: {self.selected_categories}")

    def save_entry(self, instance):
        """Guardar la entrada"""
        # Validar entrada
        if not self.entry_text.text:
            self.show_dialog("Error", "Por favor escribe algo antes de guardar")
            return

        # Obtener datos
        text = self.entry_text.text
        emotion = self.selected_emotion or "Sin especificar"
        categories = list(self.selected_categories)

        # Mostrar en consola (simulación)
        print("\n--- NUEVA ENTRADA ---")
        print(f"Texto: {text}")
        print(f"Emoción: {emotion}")
        print(f"Categorías: {categories}")

        # Mostrar confirmación
        self.show_dialog(
            "Entrada guardada",
            "Tu reflexión se ha guardado correctamente.",
            auto_dismiss=True
        )

        # Limpiar formulario
        self.entry_text.text = ""

        # Deseleccionar emoción
        if self.selected_emotion:
            button = self.emotion_buttons[self.selected_emotion]
            button.md_bg_color = (0, 0, 0, 0)  # Color normal, transparente
            self.selected_emotion = None

        # Deseleccionar categorías
        for category in self.selected_categories:
            button = self.category_buttons[category]
            button.md_bg_color = (0, 0, 0, 0)  # Color normal, transparente
        self.selected_categories = set()

    def analyze_entry(self, instance):
        """Analizar entrada con IA"""
        # Validar entrada
        if not self.entry_text.text:
            self.show_dialog("Error", "Por favor escribe algo antes de analizar")
            return

        # Obtener texto
        text = self.entry_text.text

        # Usar servicio de análisis
        sentiment, insights = analyze_mock(text)

        # Mostrar resultados
        self.show_dialog(
            "Análisis de tu entrada",
            f"Sentimiento detectado: {sentiment}\n\nInsights:\n{insights}"
        )

    def show_dialog(self, title, text, auto_dismiss=False):
        """Mostrar diálogo informativo"""
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, None),
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

        # Auto-cierre después de 2 segundos si es necesario
        if auto_dismiss:
            Clock.schedule_once(lambda dt: self.dialog.dismiss(), 2)