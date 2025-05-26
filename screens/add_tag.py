import flet as ft
from services.ai_service import analyze_tag

class ZenColors:
    """Colores zen específicos"""
    # Positivos
    positive_light = "#E8F5E8"
    positive_glow = "#A8EDEA"
    positive_main = "#48BB78"

    # Crecimiento
    growth_light = "#FFF3E0"
    growth_glow = "#FFECD2"
    growth_main = "#ED8936"

    # Base
    background = "#F8FAFC"
    surface = "#FFFFFF"
    text_primary = "#2D3748"
    text_secondary = "#4A5568"
    text_hint = "#A0AEC0"

class DynamicTag:
    def __init__(self, name, context, tag_type, ai_feedback=""):
        self.name = name
        self.context = context
        self.type = tag_type  # "positive" o "growth"
        self.ai_feedback = ai_feedback
        self.emoji = "✨" if tag_type == "positive" else "🌱"

class TagDialog:
    def __init__(self, page, tag_type, on_tag_created=None, on_error=None):
        """
        Clase para manejar el diálogo de añadir etiquetas

        Args:
            page: Objeto page de Flet
            tag_type: "positive" o "growth"
            on_tag_created: Callback cuando se crea un tag (recibe DynamicTag)
            on_error: Callback para mostrar errores (recibe mensaje string)
        """
        self.page = page
        self.tag_type = tag_type
        self.on_tag_created = on_tag_created
        self.on_error = on_error

        # Campos del formulario
        self.name_field = None
        self.context_field = None
        self.dialog = None

        # Configuración de colores según tipo
        self.colors = {
            "positive": {
                "bg": ZenColors.positive_light,
                "main": ZenColors.positive_main,
                "title": "✨ Nuevo Momento Positivo"
            },
            "growth": {
                "bg": ZenColors.growth_light,
                "main": ZenColors.growth_main,
                "title": "🌱 Nueva Área de Crecimiento"
            }
        }

        self.color_scheme = self.colors[tag_type]

    def create_form_fields(self):
        """Crear los campos del formulario"""
        self.name_field = ft.TextField(
            label="Nombre del tag",
            hint_text="Ej: Trabajo, Familia, Ejercicio...",
            border_radius=12,
            autofocus=True,
            border_color="#E2E8F0",
            focused_border_color=self.color_scheme["main"]
        )

        self.context_field = ft.TextField(
            label="¿Qué pasó exactamente?",
            hint_text="Describe la situación específica...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=12,
            border_color="#E2E8F0",
            focused_border_color=self.color_scheme["main"]
        )

    def validate_fields(self):
        """Validar que los campos estén completos"""
        if not self.name_field.value or not self.name_field.value.strip():
            return False, "Escribe un nombre para el tag"

        if not self.context_field.value or not self.context_field.value.strip():
            return False, "Describe qué pasó exactamente"

        return True, ""

    def create_tag(self, e):
        """Crear y guardar el tag"""
        is_valid, error_msg = self.validate_fields()

        if not is_valid:
            if self.on_error:
                self.on_error(error_msg)
            return

        # Crear tag dinámico
        tag = DynamicTag(
            name=self.name_field.value.strip(),
            context=self.context_field.value.strip(),
            tag_type=self.tag_type
        )

        # Callback para notificar que se creó el tag
        if self.on_tag_created:
            self.on_tag_created(tag)

        # Cerrar diálogo
        self.close()

    def ask_ai_advice(self, e):
        """Solicitar consejo a la IA"""
        is_valid, error_msg = self.validate_fields()

        if not is_valid:
            if self.on_error:
                self.on_error("Completa los campos para obtener consejo")
            return

        try:
            # Mostrar loading (opcional)
            self.show_loading_advice()

            # Obtener consejo de IA
            advice = analyze_tag(
                self.name_field.value.strip(),
                self.context_field.value.strip(),
                self.tag_type
            )

            # Mostrar diálogo con el consejo
            self.show_ai_advice_dialog(advice)

        except Exception as ex:
            print(f"Error en IA: {ex}")
            if self.on_error:
                self.on_error("Error obteniendo consejo de IA")

    def show_loading_advice(self):
        """Mostrar estado de carga mientras se obtiene el consejo"""
        # Podrías cambiar el texto del botón temporalmente
        pass

    def show_ai_advice_dialog(self, advice):
        """Mostrar diálogo con el consejo de IA"""
        advice_dialog = ft.AlertDialog(
            title=ft.Text(
                "🤖 Consejo de IA",
                size=18,
                weight=ft.FontWeight.W_500,
                color=self.color_scheme["main"]
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            advice,
                            size=14,
                            color=ZenColors.text_secondary,
                            selectable=True
                        )
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO
                ),
                width=350,
                max_height=300,
                bgcolor=self.color_scheme["bg"],
                padding=ft.padding.all(16),
                border_radius=12,
                border=ft.border.all(1, self.color_scheme["main"])
            ),
            actions=[
                ft.TextButton(
                    "✨ Entendido",
                    on_click=lambda e: self.close_advice_dialog()
                ),
                ft.ElevatedButton(
                    "💾 Guardar con consejo",
                    on_click=lambda e: self.create_tag_with_advice(advice),
                    style=ft.ButtonStyle(
                        bgcolor=self.color_scheme["main"],
                        color="#FFFFFF"
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.page.dialog = advice_dialog
        advice_dialog.open = True
        self.page.update()

    def create_tag_with_advice(self, advice):
        """Crear tag incluyendo el consejo de IA"""
        is_valid, error_msg = self.validate_fields()

        if not is_valid:
            if self.on_error:
                self.on_error(error_msg)
            return

        # Crear tag con consejo incluido
        tag = DynamicTag(
            name=self.name_field.value.strip(),
            context=self.context_field.value.strip(),
            tag_type=self.tag_type,
            ai_feedback=advice
        )

        # Callback para notificar que se creó el tag
        if self.on_tag_created:
            self.on_tag_created(tag)

        # Cerrar todos los diálogos
        self.close_advice_dialog()
        self.close()

    def close_advice_dialog(self):
        """Cerrar diálogo de consejo de IA"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def create_dialog_content(self):
        """Crear el contenido principal del diálogo"""
        return ft.Container(
            content=ft.Column(
                [
                    self.name_field,
                    ft.Container(height=16),
                    self.context_field,
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "🤖 Pedir consejo IA",
                        on_click=self.ask_ai_advice,
                        style=ft.ButtonStyle(
                            bgcolor=self.color_scheme["main"],
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=2
                        ),
                        width=280,
                        height=40
                    )
                ],
                tight=True,
                spacing=0
            ),
            width=320,
            bgcolor=self.color_scheme["bg"],
            padding=ft.padding.all(20),
            border_radius=16,
            border=ft.border.all(1, self.color_scheme["main"])
        )

    def create_dialog_actions(self):
        """Crear los botones de acción del diálogo"""
        return [
            ft.TextButton(
                "❌ Cancelar",
                on_click=lambda e: self.close(),
                style=ft.ButtonStyle(
                    color=ZenColors.text_secondary
                )
            ),
            ft.ElevatedButton(
                "✅ Guardar tag",
                on_click=self.create_tag,
                style=ft.ButtonStyle(
                    bgcolor=self.color_scheme["main"],
                    color="#FFFFFF",
                    elevation=2,
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            )
        ]

    def build(self):
        """Construir el diálogo completo"""
        # Crear campos del formulario
        self.create_form_fields()

        # Crear diálogo principal
        self.dialog = ft.AlertDialog(
            title=ft.Text(
                self.color_scheme["title"],
                size=20,
                weight=ft.FontWeight.W_500,
                color=self.color_scheme["main"]
            ),
            content=self.create_dialog_content(),
            actions=self.create_dialog_actions(),
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            shape=ft.RoundedRectangleBorder(radius=16)
        )

        return self.dialog

    def show(self):
        """Mostrar el diálogo"""
        if not self.dialog:
            self.build()

        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

        # Opcional: enfocar el primer campo
        if self.name_field:
            self.name_field.focus()

    def close(self):
        """Cerrar el diálogo"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def clear_fields(self):
        """Limpiar los campos del formulario"""
        if self.name_field:
            self.name_field.value = ""
        if self.context_field:
            self.context_field.value = ""

# ===== EJEMPLO DE USO =====

class TagDialogExample:
    """Ejemplo de cómo usar la clase TagDialog"""

    def __init__(self, page):
        self.page = page
        self.tags = []

    def on_tag_created(self, tag):
        """Callback cuando se crea un tag"""
        self.tags.append(tag)
        print(f"✅ Tag creado: {tag.name} ({tag.type})")
        if tag.ai_feedback:
            print(f"🤖 Con consejo: {tag.ai_feedback[:50]}...")

        # Aquí actualizarías tu UI principal
        self.show_success(f"Tag {tag.emoji} '{tag.name}' añadido")

    def on_error(self, message):
        """Callback para errores"""
        print(f"❌ Error: {message}")
        # Aquí mostrarías el error en tu UI
        self.show_error(message)

    def show_success(self, message):
        """Mostrar mensaje de éxito"""
        snack = ft.SnackBar(
            content=ft.Text(f"🌸 {message}", color="#FFFFFF"),
            bgcolor="#48BB78"
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def show_error(self, message):
        """Mostrar mensaje de error"""
        snack = ft.SnackBar(
            content=ft.Text(f"⚠️ {message}", color="#FFFFFF"),
            bgcolor="#F56565"
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def open_positive_dialog(self, e):
        """Abrir diálogo para momentos positivos"""
        dialog = TagDialog(
            page=self.page,
            tag_type="positive",
            on_tag_created=self.on_tag_created,
            on_error=self.on_error
        )
        dialog.show()

    def open_growth_dialog(self, e):
        """Abrir diálogo para áreas de crecimiento"""
        dialog = TagDialog(
            page=self.page,
            tag_type="growth",
            on_tag_created=self.on_tag_created,
            on_error=self.on_error
        )
        dialog.show()