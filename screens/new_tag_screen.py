import flet as ft
from services.reflect_themes_system import get_theme, create_themed_container, create_gradient_header

class SimpleTag:
    """Clase simple para representar un tag"""
    def __init__(self, emoji, category, name, reason):
        self.emoji = emoji
        self.category = category  # "positive" o "negative"
        self.name = name
        self.reason = reason
        self.type = category  # Para compatibilidad

class NewTagScreen:
    """Pantalla nueva para crear tags fácilmente CON TEMAS"""

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
        self.theme = get_theme()

        # Configuración según tipo de tag
        self.setup_tag_config()

    def setup_tag_config(self):
        """Configurar colores y textos según tipo de tag"""
        self.theme = get_theme()  # Actualizar tema

        if self.tag_type == "positive":
            self.main_color = self.theme.positive_main
            self.light_color = self.theme.positive_light
            self.title = "Momento Positivo"
            self.icon = "✨"
        else:  # negative
            self.main_color = self.theme.negative_main
            self.light_color = self.theme.negative_light
            self.title = "Momento Negativo"
            self.icon = "💔"

    def build(self):
        """Construir la vista de la pantalla CON TEMAS"""
        # Actualizar configuración con tema actual
        self.setup_tag_config()

        # Campo emoji con tema
        self.emoji_field = ft.TextField(
            label="Emoji",
            hint_text="😊 🎉 💪 😔 😰 etc...",
            width=120,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(size=20, color=self.theme.text_primary),
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.main_color,
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        # Campo nombre con tema
        self.name_field = ft.TextField(
            label="Nombre del momento",
            hint_text="Ej: Trabajo, Familia, Ejercicio...",
            border_radius=12,
            bgcolor=self.theme.surface,
            expand=True,
            border_color=self.theme.border_color,
            focused_border_color=self.main_color,
            text_style=ft.TextStyle(color=self.theme.text_primary),
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        # Campo razón/motivo con tema
        self.reason_field = ft.TextField(
            label="¿Qué pasó exactamente?",
            hint_text="Describe lo que ocurrió...",
            multiline=True,
            min_lines=3,
            max_lines=6,
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.main_color,
            text_style=ft.TextStyle(color=self.theme.text_primary),
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        # Botón volver para header
        back_button = ft.TextButton(
            "← Atrás",
            on_click=self.cancel_click,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # Header con gradiente temático
        header = create_gradient_header(
            title=f"Nuevo {self.title}",
            left_button=back_button,
            theme=self.theme
        )

        # Vista principal
        view = ft.View(
            "/new_tag",
            [
                header,

                # Contenido principal con tema
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=30),

                            # Título con icono temático
                            ft.Row(
                                [
                                    ft.Text(
                                        self.icon,
                                        size=32,
                                        color=self.main_color
                                    ),
                                    ft.Container(width=12),
                                    ft.Text(
                                        f"Crear {self.title.lower()}",
                                        size=24,
                                        weight=ft.FontWeight.W_600,
                                        color=self.main_color
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),

                            ft.Container(height=30),

                            # Formulario principal con tema
                            create_themed_container(
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
                                                        bgcolor=self.theme.surface_variant,
                                                        color=self.theme.text_secondary,
                                                        shape=ft.RoundedRectangleBorder(radius=12)
                                                    )
                                                ),
                                                ft.Container(expand=True),
                                                ft.ElevatedButton(
                                                    f"{self.icon} Guardar Momento",
                                                    width=180,
                                                    height=50,
                                                    on_click=self.save_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=self.main_color,
                                                        color="#FFFFFF",
                                                        text_style=ft.TextStyle(
                                                            weight=ft.FontWeight.BOLD,
                                                            size=16
                                                        ),
                                                        shape=ft.RoundedRectangleBorder(radius=12),
                                                        elevation=4
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                theme=self.theme,
                                border_radius=20
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
            bgcolor=self.theme.primary_bg,
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
            errors.append("Describe qué pasó exactamente")

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
        emoji = self.emoji_field.value.strip() if self.emoji_field.value else self.icon
        if not emoji:
            emoji = "✨" if self.tag_type == "positive" else "💔"

        tag = SimpleTag(
            emoji=emoji,
            category=self.tag_type,  # Usar el tipo predefinido
            name=self.name_field.value.strip(),
            reason=self.reason_field.value.strip()
        )

        print(f"🏷️ Tag creado: {tag.emoji} {tag.name} ({tag.category})")

        # Llamar callback si existe
        if self.on_tag_created:
            try:
                self.on_tag_created(tag)
                self.show_success("Momento creado correctamente")
                # Limpiar formulario
                self.clear_form()
            except Exception as ex:
                print(f"Error en callback: {ex}")
                import traceback
                traceback.print_exc()
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
        """Mostrar mensaje de error con tema"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"❌ {message}", color="#FFFFFF"),
                bgcolor=self.theme.negative_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
        else:
            print(f"ERROR: {message}")

    def show_success(self, message):
        """Mostrar mensaje de éxito con tema"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"✅ {message}", color="#FFFFFF"),
                bgcolor=self.theme.positive_main,
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