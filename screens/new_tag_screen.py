import flet as ft

class ZenColors:
    """Colores zen para la app"""
    # Positivos (verde)
    positive_light = "#E8F5E8"
    positive_main = "#48BB78"
    positive_glow = "#A8EDEA"

    # Negativos (rojo)
    negative_light = "#FEE2E2"
    negative_main = "#EF4444"
    negative_glow = "#FECACA"

    # Base
    background = "#F8FAFC"
    surface = "#FFFFFF"
    text_primary = "#2D3748"
    text_secondary = "#4A5568"

class SimpleTag:
    """Clase simple para representar un tag"""
    def __init__(self, emoji, category, name, reason):
        self.emoji = emoji
        self.category = category  # "positive" o "negative"
        self.name = name
        self.reason = reason
        self.type = category  # Para compatibilidad

class NewTagScreen:
    """Pantalla nueva para crear tags fácilmente"""

    def __init__(self, tag_type="positive", on_tag_created=None, on_cancel=None):
        self.tag_type = tag_type  # "positive" o "negative" - predefinido
        self.on_tag_created = on_tag_created  # Callback cuando se crea tag
        self.on_cancel = on_cancel  # Callback cuando se cancela

        # Campos del formulario
        self.emoji_field = None
        self.name_field = None
        self.reason_field = None

        # Estado
        self.page = None

        # Colores según tipo
        self.colors = {
            "positive": {
                "main": ZenColors.positive_main,
                "light": ZenColors.positive_light,
                "title": "Momento Positivo"
            },
            "negative": {
                "main": ZenColors.negative_main,
                "light": ZenColors.negative_light,
                "title": "Momento Negativo"
            }
        }
        self.color_scheme = self.colors[tag_type]

    def build(self):
        """Construir la vista de la pantalla"""

        # Campo emoji
        self.emoji_field = ft.TextField(
            label="Emoji",
            hint_text="😊 🎉 💪 😔 😰 etc...",
            width=120,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(size=20),
            border_radius=12,
            bgcolor="#FFFFFF"
        )

        # Campo nombre
        self.name_field = ft.TextField(
            label="Nombre del momento",
            hint_text="Ej: Trabajo, Familia, Ejercicio...",
            border_radius=12,
            bgcolor="#FFFFFF",
            expand=True
        )

        # Campo razón/motivo
        self.reason_field = ft.TextField(
            label="Que paso exactamente?",
            hint_text="Describe lo que ocurrió...",
            multiline=True,
            min_lines=3,
            max_lines=6,
            border_radius=12,
            bgcolor="#FFFFFF"
        )

        # Vista principal
        view = ft.View(
            "/new_tag",
            [
                # Header
                ft.Container(
                    content=ft.Row(
                        [
                            ft.TextButton(
                                "← Atras",
                                on_click=self.cancel_click,
                                style=ft.ButtonStyle(color="#FFFFFF")
                            ),
                            ft.Text(
                                "Nuevo " + self.color_scheme["title"],
                                size=20,
                                weight=ft.FontWeight.W_500,
                                color="#FFFFFF",
                                expand=True,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(width=80)  # Espaciador
                        ]
                    ),
                    padding=ft.padding.all(20),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=["#667EEA", "#764BA2"]
                    )
                ),

                # Contenido principal
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=30),

                            # Título
                            ft.Text(
                                f"Crear {self.color_scheme['title'].lower()}",
                                size=24,
                                weight=ft.FontWeight.W_600,
                                color=self.color_scheme["main"],
                                text_align=ft.TextAlign.CENTER
                            ),

                            ft.Container(height=30),

                            # Formulario principal
                            ft.Container(
                                content=ft.Column(
                                    [
                                        # Fila: Emoji + Nombre
                                        ft.Row(
                                            [
                                                self.emoji_field,
                                                ft.Container(width=16),
                                                self.name_field
                                            ]
                                        ),

                                        ft.Container(height=20),

                                        # Campo razón
                                        self.reason_field,

                                        ft.Container(height=30),

                                        # Botones de acción
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "Cancelar",
                                                    width=120,
                                                    height=50,
                                                    on_click=self.cancel_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor="#F1F5F9",
                                                        color=ZenColors.text_secondary,
                                                        shape=ft.RoundedRectangleBorder(radius=12)
                                                    )
                                                ),
                                                ft.Container(expand=True),
                                                ft.ElevatedButton(
                                                    "Guardar Momento",
                                                    width=180,
                                                    height=50,
                                                    on_click=self.save_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=self.color_scheme["main"],
                                                        color="#FFFFFF",
                                                        text_style=ft.TextStyle(
                                                            weight=ft.FontWeight.BOLD,
                                                            size=16
                                                        ),
                                                        shape=ft.RoundedRectangleBorder(radius=12)
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                padding=ft.padding.all(24),
                                bgcolor=ZenColors.surface,
                                border_radius=16,
                                border=ft.border.all(1, "#E2E8F0")
                            ),

                            ft.Container(height=40)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(20),
                    expand=True
                )
            ],
            bgcolor=ZenColors.background,
            padding=0,
            spacing=0
        )

        return view

    def validate_form(self):
        """Validar que todos los campos estén completos"""
        errors = []

        if not self.name_field.value or not self.name_field.value.strip():
            errors.append("Escribe un nombre para el momento")

        if not self.reason_field.value or not self.reason_field.value.strip():
            errors.append("Describe que paso exactamente")

        # El emoji es opcional, si no hay emoji usamos uno por defecto

        return len(errors) == 0, errors

    def save_click(self, e):
        """Guardar el tag"""
        self.page = e.page

        # Validar formulario
        is_valid, errors = self.validate_form()

        if not is_valid:
            self.show_error(errors[0])
            return

        # Crear el tag
        emoji = self.emoji_field.value.strip() if self.emoji_field.value else "⭐"
        if not emoji:
            emoji = "+" if self.tag_type == "positive" else "-"

        tag = SimpleTag(
            emoji=emoji,
            category=self.tag_type,  # Usar el tipo predefinido
            name=self.name_field.value.strip(),
            reason=self.reason_field.value.strip()
        )

        # Llamar callback si existe
        if self.on_tag_created:
            try:
                self.on_tag_created(tag)
                # NO navegar aquí, dejar que el callback maneje la navegación
                self.show_success("Momento creado correctamente")
            except Exception as ex:
                print(f"Error en callback: {ex}")
                self.show_error("Error al crear momento")
        else:
            self.show_success("Momento creado")

    def cancel_click(self, e):
        """Cancelar y volver"""
        if self.on_cancel:
            self.on_cancel()
        else:
            # Volver a la pantalla anterior
            if hasattr(e, 'page'):
                e.page.go("/entry")

    def clear_form(self):
        """Limpiar formulario"""
        self.emoji_field.value = ""
        self.name_field.value = ""
        self.reason_field.value = ""

        if hasattr(self, 'page') and self.page:
            self.page.update()

    def show_error(self, message):
        """Mostrar mensaje de error"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"ERROR: {message}", color="#FFFFFF"),
                bgcolor=ZenColors.negative_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
        else:
            print(f"ERROR: {message}")

    def show_success(self, message):
        """Mostrar mensaje de éxito"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"OK: {message}", color="#FFFFFF"),
                bgcolor=ZenColors.positive_main,
                duration=2000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
        else:
            print(f"OK: {message}")

# ===== EJEMPLO DE USO =====

def ejemplo_uso():
    """Ejemplo de cómo usar NewTagScreen"""

    def on_tag_created(tag):
        print(f"Tag creado: {tag.emoji} {tag.name} ({tag.category})")
        print(f"Razón: {tag.reason}")
        # Aquí añadirías el tag a tu lista

    def on_cancel():
        print("Cancelado por el usuario")
        # Aquí manejarías la cancelación

    # Crear pantalla para momento positivo
    tag_screen = NewTagScreen(
        tag_type="positive",  # o "negative"
        on_tag_created=on_tag_created,
        on_cancel=on_cancel
    )

    return tag_screen.build()

if __name__ == "__main__":
    # Prueba rápida
    def main(page: ft.Page):
        page.title = "Nueva Pantalla de Tags"
        page.window.width = 400
        page.window.height = 720

        def on_tag_created(tag):
            print(f"OK Tag: {tag.emoji} {tag.name}")
            page.go("/")  # Volver al inicio

        screen = NewTagScreen(
            tag_type="positive",
            on_tag_created=on_tag_created
        )
        page.views.append(screen.build())
        page.update()

    ft.app(target=main)