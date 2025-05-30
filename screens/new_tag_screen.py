"""
📝 New Tag Screen - TAMAÑOS CORREGIDOS
Versión optimizada sin scroll
"""

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
    """Pantalla nueva para crear tags - TAMAÑOS OPTIMIZADOS"""

    def __init__(self, tag_type="positive", on_tag_created=None, on_cancel=None):
        self.tag_type = tag_type
        self.on_tag_created = on_tag_created
        self.on_cancel = on_cancel

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
        self.theme = get_theme()

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
        """Construir la vista - TAMAÑOS OPTIMIZADOS"""
        self.setup_tag_config()

        # ✅ CAMPOS MÁS COMPACTOS
        self.emoji_field = ft.TextField(
            label="Emoji",
            hint_text="😊 🎉 💪 😔",
            width=100,  # Era 120 → 100
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(size=18, color=self.theme.text_primary),  # Era 20 → 18
            border_radius=10,  # Era 12 → 10
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.main_color,
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        self.name_field = ft.TextField(
            label="Nombre del momento",
            hint_text="Ej: Trabajo, Familia...",
            border_radius=10,
            bgcolor=self.theme.surface,
            expand=True,
            border_color=self.theme.border_color,
            focused_border_color=self.main_color,
            text_style=ft.TextStyle(color=self.theme.text_primary),
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        # ✅ CAMPO RAZÓN MÁS COMPACTO
        self.reason_field = ft.TextField(
            label="¿Qué pasó?",
            hint_text="Describe brevemente...",
            multiline=True,
            min_lines=2,  # Era 3 → 2
            max_lines=4,  # Era 6 → 4
            border_radius=10,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.main_color,
            text_style=ft.TextStyle(color=self.theme.text_primary),
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        # Header
        back_button = ft.TextButton(
            "← Atrás",
            on_click=self.cancel_click,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        header = create_gradient_header(
            title=f"Nuevo {self.title}",
            left_button=back_button,
            theme=self.theme
        )

        # ✅ VISTA OPTIMIZADA SIN SCROLL
        view = ft.View(
            "/new_tag",
            [
                header,

                # Contenido principal MÁS COMPACTO
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=16),  # Era 30 → 16

                            # Título más compacto
                            ft.Row(
                                [
                                    ft.Text(
                                        self.icon,
                                        size=24,  # Era 32 → 24
                                        color=self.main_color
                                    ),
                                    ft.Container(width=8),  # Era 12 → 8
                                    ft.Text(
                                        f"Crear {self.title.lower()}",
                                        size=20,  # Era 24 → 20
                                        weight=ft.FontWeight.W_600,
                                        color=self.main_color
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),

                            ft.Container(height=20),  # Era 30 → 20

                            # Formulario más compacto
                            create_themed_container(
                                content=ft.Column(
                                    [
                                        # Fila: Emoji + Nombre
                                        ft.Row(
                                            [
                                                self.emoji_field,
                                                ft.Container(width=12),
                                                self.name_field
                                            ]
                                        ),

                                        ft.Container(height=16),  # Era 20 → 16

                                        # Campo razón
                                        self.reason_field,

                                        ft.Container(height=20),  # Era 30 → 20

                                        # Botones más compactos
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "Cancelar",
                                                    width=100,  # Era 120 → 100
                                                    height=44,  # Era 50 → 44
                                                    on_click=self.cancel_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=self.theme.surface_variant,
                                                        color=self.theme.text_secondary,
                                                        shape=ft.RoundedRectangleBorder(radius=10)
                                                    )
                                                ),
                                                ft.Container(expand=True),
                                                ft.ElevatedButton(
                                                    f"{self.icon} Guardar",
                                                    width=160,  # Era 180 → 160
                                                    height=44,  # Era 50 → 44
                                                    on_click=self.save_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=self.main_color,
                                                        color="#FFFFFF",
                                                        text_style=ft.TextStyle(
                                                            weight=ft.FontWeight.BOLD,
                                                            size=14  # Era 16 → 14
                                                        ),
                                                        shape=ft.RoundedRectangleBorder(radius=10),
                                                        elevation=3  # Era 4 → 3
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                theme=self.theme,
                                border_radius=16  # Era 20 → 16
                            ),

                            ft.Container(height=20)  # Era 40 → 20
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(16),  # Era 20 → 16
                    expand=True
                )
            ],
            bgcolor=self.theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    # Resto de métodos igual...
    def validate_form(self):
        """Validar que todos los campos estén completos"""
        errors = []

        if not self.name_field.value or not self.name_field.value.strip():
            errors.append("Escribe un nombre para el momento")

        if not self.reason_field.value or not self.reason_field.value.strip():
            errors.append("Describe qué pasó exactamente")

        return len(errors) == 0, errors

    def save_click(self, e):
        """Guardar el tag"""
        self.page = e.page

        is_valid, errors = self.validate_form()

        if not is_valid:
            self.show_error(errors[0])
            return

        emoji = self.emoji_field.value.strip() if self.emoji_field.value else self.icon
        if not emoji:
            emoji = "✨" if self.tag_type == "positive" else "💔"

        tag = SimpleTag(
            emoji=emoji,
            category=self.tag_type,
            name=self.name_field.value.strip(),
            reason=self.reason_field.value.strip()
        )

        print(f"🏷️ Tag creado: {tag.emoji} {tag.name} ({tag.category})")

        if self.on_tag_created:
            try:
                self.on_tag_created(tag)
                self.show_success("Momento creado correctamente")
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