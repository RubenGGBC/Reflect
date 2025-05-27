"""
📝 Entry Screen Actualizada - ReflectApp
Pantalla principal con sistema de temas profesional implementado
"""

import flet as ft
from services.ai_service import analyze_tag, get_daily_summary
from screens.new_tag_screen import NewTagScreen, SimpleTag
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header, zen_colors, apply_theme_to_page
)

class DynamicTag:
    def __init__(self, name, context, tag_type, ai_feedback="", emoji=None):
        self.name = name
        self.context = context
        self.type = tag_type  # "positive" o "negative"
        self.ai_feedback = ai_feedback
        self.emoji = emoji or ("+" if tag_type == "positive" else "-")

    @classmethod
    def from_simple_tag(cls, simple_tag):
        """Crear DynamicTag desde SimpleTag"""
        return cls(
            name=simple_tag.name,
            context=simple_tag.reason,
            tag_type=simple_tag.category,
            emoji=simple_tag.emoji
        )

class EntryScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.current_user = None
        self.theme = get_theme()  # Obtener tema actual

        # Campos principales
        self.reflection_field = None
        self.positive_tags = []
        self.negative_tags = []
        self.worth_it = None  # True, False, o None

        # Contenedores para tags
        self.positive_tags_container = None
        self.negative_tags_container = None
        self.worth_it_buttons = {"yes": None, "no": None}

    def set_user(self, user_data):
        """Establecer usuario y cargar datos del día"""
        self.current_user = user_data
        self.load_today_tags()

    def update_theme(self):
        """Actualizar tema cuando cambie"""
        self.theme = get_theme()
        if self.page:
            apply_theme_to_page(self.page)
            self.page.update()

    def load_today_tags(self):
        """Cargar tags del día actual desde la base de datos"""
        if not self.current_user:
            return

        try:
            from services import db
            entries_today = db.get_user_entries(
                user_id=self.current_user['id'],
                limit=10,
                offset=0
            )

            # Limpiar listas actuales
            self.positive_tags.clear()
            self.negative_tags.clear()

            # Procesar entradas de hoy
            from datetime import date
            today = date.today().isoformat()

            for entry in entries_today:
                if entry.get('entry_date') == today:
                    # Cargar tags positivos
                    for tag_data in entry.get('positive_tags', []):
                        tag = DynamicTag(
                            name=tag_data.get('name', ''),
                            context=tag_data.get('context', ''),
                            tag_type="positive",
                            emoji=tag_data.get('emoji', '+')
                        )
                        self.positive_tags.append(tag)

                    # Cargar tags negativos
                    for tag_data in entry.get('negative_tags', []):
                        tag = DynamicTag(
                            name=tag_data.get('name', ''),
                            context=tag_data.get('context', ''),
                            tag_type="negative",
                            emoji=tag_data.get('emoji', '-')
                        )
                        self.negative_tags.append(tag)

                    # Solo procesamos la primera entrada de hoy
                    break

            print(f"Cargados {len(self.positive_tags)} tags positivos y {len(self.negative_tags)} tags negativos")

        except Exception as ex:
            print(f"Error cargando tags del día: {ex}")

    def build(self):
        """Construir vista principal zen con temas"""
        # Actualizar tema
        self.theme = get_theme()

        # Cargar tags del día al construir la vista
        self.load_today_tags()

        # Campo de reflexión libre zen con tema
        self.reflection_field = ft.TextField(
            label="¿Cómo te ha ido el día?",
            hint_text="Cuéntame sobre tu día... Tómate tu tiempo para reflexionar",
            multiline=True,
            min_lines=4,
            max_lines=8,
            border=ft.InputBorder.OUTLINE,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            border_radius=20,
            content_padding=ft.padding.all(20),
            text_style=ft.TextStyle(size=16, height=1.6, color=self.theme.text_primary),
            cursor_color=self.theme.accent_primary,
            bgcolor=self.theme.surface,
            color=self.theme.text_primary,
            label_style=ft.TextStyle(color=self.theme.text_secondary)
        )

        # Contenedores para tags dinámicos
        self.positive_tags_container = ft.Column(spacing=8)
        self.negative_tags_container = ft.Column(spacing=8)

        # Botones para "¿Mereció la pena?" con tema
        self.worth_it_buttons["yes"] = ft.ElevatedButton(
            "SÍ",
            on_click=lambda e: self.set_worth_it(True, e),
            style=ft.ButtonStyle(
                bgcolor=self.theme.surface_variant,
                color=self.theme.text_secondary,
                elevation=0,
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=20)
            ),
            height=48
        )

        self.worth_it_buttons["no"] = ft.ElevatedButton(
            "NO",
            on_click=lambda e: self.set_worth_it(False, e),
            style=ft.ButtonStyle(
                bgcolor=self.theme.surface_variant,
                color=self.theme.text_secondary,
                elevation=0,
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=20)
            ),
            height=48
        )

        # Header con gradiente temático
        back_button = ft.TextButton(
            "← Salir",
            on_click=self.logout_click,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        calendar_button = ft.TextButton(
            "📅",
            on_click=self.go_to_calendar,
            style=ft.ButtonStyle(color="#FFFFFF"),
            tooltip="Ver calendario"
        )

        # Botón de configuración de temas
        theme_button = ft.TextButton(
            "🎨",
            on_click=self.go_to_theme_selector,
            style=ft.ButtonStyle(color="#FFFFFF"),
            tooltip="Cambiar tema"
        )

        user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'
        header = create_gradient_header(
            title=f"Hola, {user_name} 🧘‍♀️",
            left_button=back_button,
            right_button=ft.Row([theme_button, calendar_button], spacing=0),
            theme=self.theme
        )

        # Vista principal zen con tema
        view = ft.View(
            "/entry",
            [
                header,

                # Contenido principal con scroll zen
                ft.Container(
                    content=ft.Column(
                        [
                            # Campo de reflexión libre
                            create_themed_container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "Reflexión Libre",
                                            size=20,
                                            weight=ft.FontWeight.W_500,
                                            color=self.theme.text_primary
                                        ),
                                        ft.Container(height=16),
                                        self.reflection_field
                                    ]
                                ),
                                theme=self.theme
                            ),

                            ft.Container(height=24),

                            # Sección MOMENTOS POSITIVOS
                            create_themed_container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "+ MOMENTOS POSITIVOS",
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color=self.theme.positive_main,
                                                    expand=True
                                                ),
                                                ft.Container(
                                                    content=ft.TextButton(
                                                        content=ft.Text(
                                                            "+",
                                                            size=20,
                                                            color=self.theme.positive_main,
                                                            weight=ft.FontWeight.BOLD
                                                        ),
                                                        on_click=self.open_positive_tag_dialog,
                                                        style=ft.ButtonStyle(
                                                            bgcolor=self.theme.positive_light,
                                                            shape=ft.CircleBorder(),
                                                            padding=ft.padding.all(8)
                                                        )
                                                    ),
                                                    bgcolor=self.theme.positive_light,
                                                    border_radius=20,
                                                    padding=ft.padding.all(4)
                                                )
                                            ]
                                        ),
                                        ft.Container(height=12),
                                        self.positive_tags_container
                                    ]
                                ),
                                theme=self.theme,
                                is_surface=False  # Usar surface_variant para destacar
                            ),

                            ft.Container(height=16),

                            # Sección MOMENTOS NEGATIVOS
                            create_themed_container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "- MOMENTOS NEGATIVOS",
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color=self.theme.negative_main,
                                                    expand=True
                                                ),
                                                ft.Container(
                                                    content=ft.TextButton(
                                                        content=ft.Text(
                                                            "+",
                                                            size=20,
                                                            color=self.theme.negative_main,
                                                            weight=ft.FontWeight.BOLD
                                                        ),
                                                        on_click=self.open_negative_tag_dialog,
                                                        style=ft.ButtonStyle(
                                                            bgcolor=self.theme.negative_light,
                                                            shape=ft.CircleBorder(),
                                                            padding=ft.padding.all(8)
                                                        )
                                                    ),
                                                    bgcolor=self.theme.negative_light,
                                                    border_radius=20,
                                                    padding=ft.padding.all(4)
                                                )
                                            ]
                                        ),
                                        ft.Container(height=12),
                                        self.negative_tags_container
                                    ]
                                ),
                                theme=self.theme,
                                is_surface=False
                            ),

                            ft.Container(height=24),

                            # Pregunta final zen
                            create_themed_container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "¿Ha merecido la pena tu día?",
                                            size=18,
                                            weight=ft.FontWeight.W_500,
                                            color=self.theme.text_primary,
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.Container(height=20),
                                        ft.Row(
                                            [
                                                self.worth_it_buttons["yes"],
                                                ft.Container(width=16),
                                                self.worth_it_buttons["no"]
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER
                                        )
                                    ]
                                ),
                                theme=self.theme
                            ),

                            ft.Container(height=32),

                            # Botones de acción zen con tema
                            ft.Row(
                                [
                                    create_themed_button(
                                        "💾 Guardar",
                                        self.save_entry,
                                        theme=self.theme,
                                        button_type="positive",
                                        height=56
                                    ),
                                    ft.Container(width=16),
                                    create_themed_button(
                                        "🤖 Chat IA",
                                        self.chat_ai,
                                        theme=self.theme,
                                        button_type="primary",
                                        height=56
                                    )
                                ],
                                expand=True
                            ),

                            ft.Container(height=24)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0
                    ),
                    padding=ft.padding.all(20),
                    expand=True
                )
            ],
            padding=0,
            spacing=0,
            bgcolor=self.theme.primary_bg
        )

        # Refrescar tags después de crear la vista
        self.refresh_positive_tags()
        self.refresh_negative_tags()

        return view

    def refresh_positive_tags(self):
        """Actualizar visualización de tags positivos con tema"""
        if not self.positive_tags_container:
            return

        self.positive_tags_container.controls.clear()

        for i, tag in enumerate(self.positive_tags):
            tag_chip = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    f"{tag.emoji} {tag.name}",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=self.theme.text_primary
                                ),
                                ft.TextButton(
                                    content=ft.Text("×", size=16, color=self.theme.text_secondary),
                                    on_click=lambda e, t=tag: self.remove_positive_tag(t),
                                    style=ft.ButtonStyle(padding=ft.padding.all(4))
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Text(
                            tag.context[:50] + "..." if len(tag.context) > 50 else tag.context,
                            size=12,
                            color=self.theme.text_secondary,
                            italic=True
                        )
                    ],
                    spacing=4,
                    tight=True
                ),
                bgcolor=self.theme.positive_light,
                padding=ft.padding.all(12),
                border_radius=16,
                border=ft.border.all(1, self.theme.positive_main),
                margin=ft.margin.only(bottom=8)
            )
            self.positive_tags_container.controls.append(tag_chip)

    def refresh_negative_tags(self):
        """Actualizar visualización de tags negativos con tema"""
        if not self.negative_tags_container:
            return

        self.negative_tags_container.controls.clear()

        for i, tag in enumerate(self.negative_tags):
            tag_chip = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    f"{tag.emoji} {tag.name}",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=self.theme.text_primary
                                ),
                                ft.TextButton(
                                    content=ft.Text("×", size=16, color=self.theme.text_secondary),
                                    on_click=lambda e, t=tag: self.remove_negative_tag(t),
                                    style=ft.ButtonStyle(padding=ft.padding.all(4))
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Text(
                            tag.context[:50] + "..." if len(tag.context) > 50 else tag.context,
                            size=12,
                            color=self.theme.text_secondary,
                            italic=True
                        )
                    ],
                    spacing=4,
                    tight=True
                ),
                bgcolor=self.theme.negative_light,
                padding=ft.padding.all(12),
                border_radius=16,
                border=ft.border.all(1, self.theme.negative_main),
                margin=ft.margin.only(bottom=8)
            )
            self.negative_tags_container.controls.append(tag_chip)

    def on_tag_created(self, simple_tag):
        """Callback cuando se crea un tag desde NewTagScreen"""
        # Convertir SimpleTag a DynamicTag
        tag = DynamicTag.from_simple_tag(simple_tag)

        # Añadir a la lista correspondiente
        if tag.type == "positive":
            self.positive_tags.append(tag)
        elif tag.type == "negative":
            self.negative_tags.append(tag)

        # Forzar actualización de la interfaz
        self.force_refresh_tags()
        self.show_success(f"Momento {tag.type} '{tag.name}' añadido")

    def force_refresh_tags(self):
        """Forzar actualización visual de todos los tags"""
        self.refresh_positive_tags()
        self.refresh_negative_tags()

        if hasattr(self, 'page') and self.page:
            self.page.update()

    def open_positive_tag_dialog(self, e):
        """Abrir pantalla para añadir momento positivo"""
        self.page = e.page
        self.page.go("/new_tag?type=positive")

    def open_negative_tag_dialog(self, e):
        """Abrir pantalla para añadir momento negativo"""
        self.page = e.page
        self.page.go("/new_tag?type=negative")

    def remove_positive_tag(self, tag):
        """Eliminar tag positivo"""
        self.positive_tags.remove(tag)
        self.refresh_positive_tags()
        if self.page:
            self.page.update()

    def remove_negative_tag(self, tag):
        """Eliminar tag negativo"""
        self.negative_tags.remove(tag)
        self.refresh_negative_tags()
        if self.page:
            self.page.update()

    def set_worth_it(self, value, e):
        """Establecer si mereció la pena el día"""
        self.page = e.page
        self.worth_it = value

        # Actualizar estilos de botones con tema
        for btn_key, btn in self.worth_it_buttons.items():
            if (btn_key == "yes" and value) or (btn_key == "no" and not value):
                btn.style.bgcolor = self.theme.positive_main if value else self.theme.negative_main
                btn.style.color = "#FFFFFF"
            else:
                btn.style.bgcolor = self.theme.surface_variant
                btn.style.color = self.theme.text_secondary

        if self.page:
            self.page.update()

    def save_entry(self, e):
        """Guardar entrada zen"""
        self.page = e.page

        if not self.reflection_field.value or not self.reflection_field.value.strip():
            self.show_error("Escribe algo en tu reflexión antes de guardar")
            return

        try:
            from services import db

            if self.current_user:
                entry_id = db.save_daily_entry(
                    user_id=self.current_user['id'],
                    free_reflection=self.reflection_field.value.strip(),
                    positive_tags=self.positive_tags,
                    negative_tags=self.negative_tags,
                    worth_it=self.worth_it
                )

                if entry_id:
                    self.show_success("✨ Reflexión guardada correctamente")
                else:
                    self.show_error("Error al guardar")
            else:
                self.show_error("Usuario no autenticado")

        except Exception as ex:
            print(f"Error guardando: {ex}")
            self.show_error("Error del sistema")

    def chat_ai(self, e):
        """Iniciar chat con IA"""
        self.page = e.page

        if not self.reflection_field.value or not self.reflection_field.value.strip():
            self.show_error("Escribe algo para charlar con la IA")
            return

        try:
            summary = get_daily_summary(
                reflection=self.reflection_field.value.strip(),
                positive_tags=self.positive_tags,
                negative_tags=self.negative_tags,
                worth_it=self.worth_it
            )

            self.show_daily_summary_dialog(summary)

        except Exception as ex:
            print(f"Error en chat IA: {ex}")
            self.show_error("Error iniciando chat")

    def show_daily_summary_dialog(self, summary):
        """Mostrar resumen diario de IA con tema"""
        dialog_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        summary,
                        size=14,
                        color=self.theme.text_secondary,
                        selectable=True
                    )
                ],
                scroll=ft.ScrollMode.AUTO
            ),
            width=350,
            height=300,
            bgcolor=self.theme.surface,
            padding=ft.padding.all(16),
            border_radius=12,
            border=ft.border.all(1, self.theme.border_color)
        )

        dialog = ft.AlertDialog(
            title=ft.Text(
                "🤖 Resumen de tu día",
                size=18,
                weight=ft.FontWeight.W_500,
                color=self.theme.text_primary
            ),
            content=dialog_content,
            actions=[
                ft.TextButton(
                    "Continuar chat",
                    on_click=lambda e: self.continue_chat(),
                    style=ft.ButtonStyle(color=self.theme.accent_primary)
                ),
                ft.TextButton(
                    "Gracias",
                    on_click=lambda e: self.close_dialog(),
                    style=ft.ButtonStyle(color=self.theme.text_secondary)
                )
            ],
            bgcolor=self.theme.surface
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def continue_chat(self):
        """Continuar chat (funcionalidad futura)"""
        self.close_dialog()
        self.show_success("Chat extendido próximamente")

    def close_dialog(self):
        """Cerrar diálogo"""
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def go_to_calendar(self, e):
        """Navegar al calendario"""
        self.page = e.page
        self.page.go("/calendar")

    def go_to_theme_selector(self, e):
        """Navegar al selector de temas"""
        self.page = e.page
        self.page.go("/theme_selector")

    def logout_click(self, e):
        """Cerrar sesión zen"""
        self.page = e.page
        self.app.navigate_to_login()

    def show_error(self, message):
        """Mostrar error zen con tema"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"❌ {message}", color="#FFFFFF"),
                bgcolor=self.theme.negative_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()

    def show_success(self, message):
        """Mostrar éxito zen con tema"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"✅ {message}", color="#FFFFFF"),
                bgcolor=self.theme.positive_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()