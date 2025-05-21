from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button.button import MDButton, MDButtonText
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.chip.chip import MDChip, MDChipText
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.clock import Clock

# Importación simplificada
from services.ai_service import analyze_mock

class EntryScreen(MDScreen):
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
            text="¿Cómo ha sido tu día?",
            font_style="Title",  # Cambiado de H5 a Title
            halign="center",
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)

        # Campo de texto para la entrada
        self.entry_text = MDTextField(
            hint_text="Reflexiona sobre tu día...",
            helper_text="Cuéntame lo bueno, lo malo y tus reflexiones",
            helper_text_mode="on_focus",
            multiline=True,
            size_hint=(1, None),
            height=dp(150)
        )
        layout.add_widget(self.entry_text)

        # Chips para emociones
        emotions_label = MDLabel(
            text="¿Cómo te has sentido hoy?",
            font_style="Body",  # Cambiado de Body1 a Body
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(emotions_label)

        emotions_layout = MDBoxLayout(
            spacing=dp(10),
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )

        emotions = ["Feliz", "Tranquilo", "Triste", "Ansioso", "Productivo"]
        self.selected_emotion = None
        self.emotion_chips = {}

        for emotion in emotions:
            chip = MDChip(
                on_press=lambda x, e=emotion: self.select_emotion(e),
                style="outlined"
            )
            chip.add_widget(MDChipText(text=emotion))
            emotions_layout.add_widget(chip)
            self.emotion_chips[emotion] = chip

        layout.add_widget(emotions_layout)

        # Layout para categorías
        categories_label = MDLabel(
            text="Categoriza tu entrada:",
            font_style="Body",  # Cambiado de Body1 a Body
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(categories_label)

        categories_layout = MDBoxLayout(
            spacing=dp(10),
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )

        categories = ["Trabajo", "Personal", "Salud", "Relaciones", "Crecimiento"]
        self.selected_categories = set()
        self.category_chips = {}

        for category in categories:
            chip = MDChip(
                on_press=lambda x, c=category: self.toggle_category(c),
                style="outlined"
            )
            chip.add_widget(MDChipText(text=category))
            categories_layout.add_widget(chip)
            self.category_chips[category] = chip

        layout.add_widget(categories_layout)

        # Botones de acción
        buttons_layout = MDBoxLayout(
            spacing=dp(10),
            adaptive_height=True,
            padding=[0, 20, 0, 10]
        )

        save_button = MDButton(
            style="elevated",
            on_release=self.save_entry,
            size_hint=(0.7, None),
            height=dp(50)
        )
        save_button.add_widget(MDButtonText(text="Guardar entrada"))
        buttons_layout.add_widget(save_button)

        analyze_button = MDButton(
            style="text",
            on_release=self.analyze_entry,
            size_hint=(0.3, None),
            height=dp(50)
        )
        analyze_button.add_widget(MDButtonText(text="Analizar"))
        buttons_layout.add_widget(analyze_button)

        layout.add_widget(buttons_layout)

        self.add_widget(layout)

        # Dialog para mostrar el análisis
        self.dialog = None

    def select_emotion(self, emotion):
        # Deseleccionar emoción anterior
        if self.selected_emotion and self.selected_emotion in self.emotion_chips:
            # En KivyMD 2.0 la forma de cambiar color es diferente
            self.emotion_chips[self.selected_emotion].style = "outlined"

        # Seleccionar nueva emoción
        self.selected_emotion = emotion
        self.emotion_chips[emotion].style = "filled"
        print(f"Emoción seleccionada: {emotion}")

    def toggle_category(self, category):
        if category in self.selected_categories:
            self.selected_categories.remove(category)
            self.category_chips[category].style = "outlined"
        else:
            self.selected_categories.add(category)
            self.category_chips[category].style = "filled"

        print(f"Categorías seleccionadas: {self.selected_categories}")

    def save_entry(self, instance):
        # Validar entrada
        if not self.entry_text.text:
            self.show_dialog("Error", "Por favor escribe algo antes de guardar")
            return

        # Obtener datos
        text = self.entry_text.text
        emotion = self.selected_emotion or "Sin especificar"
        categories = list(self.selected_categories)

        # TODO: Guardar en la base de datos
        print("\n--- NUEVA ENTRADA ---")
        print(f"Texto: {text}")
        print(f"Emoción: {emotion}")
        print(f"Categorías: {categories}")

        # TODO: Implementar guardado real en Firebase

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
            self.emotion_chips[self.selected_emotion].style = "outlined"
            self.selected_emotion = None

        # Deseleccionar categorías
        for category in self.selected_categories:
            self.category_chips[category].style = "outlined"
        self.selected_categories = set()

    def analyze_entry(self, _):  # Usando _ para indicar que no se usa el parámetro
        # Validar entrada
        if not self.entry_text.text:
            self.show_dialog("Error", "Por favor escribe algo antes de analizar")
            return

        # Obtener texto
        text = self.entry_text.text

        # Usar la función importada de services
        sentiment, insights = analyze_mock(text)

        # Mostrar resultados
        self.show_dialog(
            "Análisis de tu entrada",
            f"Sentimiento detectado: {sentiment}\n\nInsights:\n{insights}",
            size_hint=(0.8, 0.6)
        )

    def show_dialog(self, title, text, auto_dismiss=False, size_hint=(0.8, None)):
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
            size_hint=size_hint,
            buttons=[ok_button]
        )
        self.dialog.open()

        # Auto-cierre después de 3 segundos si es necesario
        if auto_dismiss:
            Clock.schedule_once(lambda dt: self.dialog.dismiss(), 2)