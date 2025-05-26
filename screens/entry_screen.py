import flet as ft
from services.ai_service import analyze_tag, get_daily_summary
from screens.add_tag import TagDialog, DynamicTag
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

class EntryScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.current_user = None

        # Campos principales
        self.reflection_field = None
        self.positive_tags = []
        self.growth_tags = []
        self.worth_it = None  # True, False, o None

        # Contenedores para tags
        self.positive_tags_container = None
        self.growth_tags_container = None
        self.worth_it_buttons = {"yes": None, "no": None}

    def set_user(self, user_data):
        """Establecer usuario"""
        self.current_user = user_data

    def build(self):
        """Construir vista principal zen"""

        # Campo de reflexión libre zen
        self.reflection_field = ft.TextField(
            label="¿Cómo te ha ido el día?",
            hint_text="Cuéntame sobre tu día... Tómate tu tiempo para reflexionar 🌸",
            multiline=True,
            min_lines=4,
            max_lines=8,
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#667EEA",
            border_radius=20,
            content_padding=ft.padding.all(20),
            text_style=ft.TextStyle(size=16, height=1.6),
            cursor_color="#667EEA"
        )

        # Contenedores para tags dinámicos
        self.positive_tags_container = ft.Column(spacing=8)
        self.growth_tags_container = ft.Column(spacing=8)

        # Botones para "¿Mereció la pena?"
        self.worth_it_buttons["yes"] = ft.ElevatedButton(
            "👍 SÍ",
            on_click=lambda e: self.set_worth_it(True, e),
            style=ft.ButtonStyle(
                bgcolor="#F1F5F9",
                color="#4A5568",
                elevation=0,
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=20)
            ),
            height=48
        )

        self.worth_it_buttons["no"] = ft.ElevatedButton(
            "👎 NO",
            on_click=lambda e: self.set_worth_it(False, e),
            style=ft.ButtonStyle(
                bgcolor="#F1F5F9",
                color="#4A5568",
                elevation=0,
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=20)
            ),
            height=48
        )

        # Vista principal zen
        view = ft.View(
            "/entry",
            [
                # Header zen con gradiente
                ft.Container(
                    content=ft.Row(
                        [
                            ft.TextButton(
                                "← Salir",
                                on_click=self.logout_click,
                                style=ft.ButtonStyle(color="#FFFFFF")
                            ),
                            ft.Text(
                                f"Hola, {self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'} 🧘‍♀️",
                                size=18,
                                weight=ft.FontWeight.W_400,
                                color="#FFFFFF",
                                expand=True,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(width=60)
                        ]
                    ),
                    padding=ft.padding.all(20),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.center_left,
                        end=ft.alignment.center_right,
                        colors=["#667EEA", "#764BA2"]
                    ),
                    border_radius=ft.border_radius.only(bottom_left=24, bottom_right=24)
                ),

                # Contenido principal con scroll zen
                ft.Container(
                    content=ft.Column(
                        [
                            # Campo de reflexión libre
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "✍️ Reflexión Libre",
                                            size=20,
                                            weight=ft.FontWeight.W_500,
                                            color=ZenColors.text_primary
                                        ),
                                        ft.Container(height=16),
                                        self.reflection_field
                                    ]
                                ),
                                padding=ft.padding.all(24),
                                bgcolor=ZenColors.surface,
                                border_radius=20,
                                border=ft.border.all(1, "#E2E8F0")
                            ),

                            ft.Container(height=24),

                            # Sección MOMENTOS POSITIVOS
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "✨ MOMENTOS POSITIVOS",
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ZenColors.positive_main,
                                                    expand=True
                                                ),
                                                ft.TextButton(
                                                    content=ft.Text("＋", size=20, color=ZenColors.positive_main),
                                                    on_click=lambda e: self.open_add_tag_dialog(e),
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ZenColors.positive_light,
                                                        shape=ft.CircleBorder(),
                                                        padding=ft.padding.all(8)
                                                    )
                                                )
                                            ]
                                        ),
                                        ft.Container(height=12),
                                        self.positive_tags_container
                                    ]
                                ),
                                padding=ft.padding.all(20),
                                bgcolor=ZenColors.positive_light,
                                border_radius=16,
                                border=ft.border.all(1, ZenColors.positive_glow)
                            ),

                            ft.Container(height=16),

                            # Sección ÁREAS DE CRECIMIENTO
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "🌱 ÁREAS DE CRECIMIENTO",
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ZenColors.growth_main,
                                                    expand=True
                                                ),
                                                ft.TextButton(
                                                    content=ft.Text("＋", size=20, color=ZenColors.growth_main),
                                                    on_click=lambda e: self.open_add_tag_dialog("growth"),
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ZenColors.growth_light,
                                                        shape=ft.CircleBorder(),
                                                        padding=ft.padding.all(8)
                                                    )
                                                )
                                            ]
                                        ),
                                        ft.Container(height=12),
                                        self.growth_tags_container
                                    ]
                                ),
                                padding=ft.padding.all(20),
                                bgcolor=ZenColors.growth_light,
                                border_radius=16,
                                border=ft.border.all(1, ZenColors.growth_glow)
                            ),

                            ft.Container(height=24),

                            # Pregunta final zen
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "🤔 ¿Ha merecido la pena tu día?",
                                            size=18,
                                            weight=ft.FontWeight.W_500,
                                            color=ZenColors.text_primary,
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
                                padding=ft.padding.all(24),
                                bgcolor=ZenColors.surface,
                                border_radius=16,
                                border=ft.border.all(1, "#E2E8F0")
                            ),

                            ft.Container(height=32),

                            # Botones de acción zen
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "💾 Guardar",
                                        on_click=self.save_entry,
                                        style=ft.ButtonStyle(
                                            bgcolor="#48BB78",
                                            color="#FFFFFF",
                                            elevation=2,
                                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500),
                                            shape=ft.RoundedRectangleBorder(radius=16),
                                            padding=ft.padding.symmetric(vertical=18, horizontal=24)
                                        ),
                                        expand=True,
                                        height=56
                                    ),
                                    ft.Container(width=16),
                                    ft.ElevatedButton(
                                        "🤖 Chat IA",
                                        on_click=self.chat_ai,
                                        style=ft.ButtonStyle(
                                            bgcolor="#667EEA",
                                            color="#FFFFFF",
                                            elevation=2,
                                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_500),
                                            shape=ft.RoundedRectangleBorder(radius=16),
                                            padding=ft.padding.symmetric(vertical=18, horizontal=24)
                                        ),
                                        expand=True,
                                        height=56
                                    )
                                ]
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
            bgcolor=ZenColors.background
        )

        return view

    def add_tag_dialog(self, tag_type, e=None):
        """Mostrar diálogo para crear tag dinámico"""
        print(f"🔍 add_tag_dialog llamado con tag_type: {tag_type}")
        print(f"🔍 Evento e: {e}")
        print(f"🔍 Tiene page?: {hasattr(e, 'page') if e else 'e es None'}")

        # Obtener page del evento
        if not e or not hasattr(e, 'page'):
            print("❌ Error: No se puede acceder al page del evento")
            return

        print(f"🔍 Page obtenido: {e.page}")
        self.page = e.page

        # Campos del diálogo
        name_field = ft.TextField(
            label="Nombre del tag",
            hint_text="Ej: Trabajo, Familia, Ejercicio...",
            border_radius=12,
            autofocus=True
        )

        context_field = ft.TextField(
            label="¿Qué pasó exactamente?",
            hint_text="Describe la situación específica...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=12
        )

        # Colores según tipo
        colors = {
            "positive": {"bg": ZenColors.positive_light, "main": ZenColors.positive_main, "title": "✨ Nuevo Momento Positivo"},
            "growth": {"bg": ZenColors.growth_light, "main": ZenColors.growth_main, "title": "🌱 Nueva Área de Crecimiento"}
        }

        color_scheme = colors[tag_type]

        def create_tag(e):
            if not name_field.value or not context_field.value:
                self.show_error("Completa todos los campos")
                return

            # Crear tag dinámico
            tag = DynamicTag(
                name=name_field.value.strip(),
                context=context_field.value.strip(),
                tag_type=tag_type
            )

            # Añadir a la lista correspondiente
            if tag_type == "positive":
                self.positive_tags.append(tag)
                self.refresh_positive_tags()
            else:
                self.growth_tags.append(tag)
                self.refresh_growth_tags()

            # Cerrar diálogo
            self.page.dialog.open = False
            self.page.update()

            # Mostrar éxito zen
            self.show_success(f"Tag {tag.emoji} añadido")

        def ask_ai(e):
            if not name_field.value or not context_field.value:
                self.show_error("Completa los campos para obtener consejo")
                return

            # Generar consejo de IA
            try:
                advice = analyze_tag(name_field.value, context_field.value, tag_type)
                self.show_ai_advice_dialog(advice, tag_type)
            except Exception as ex:
                print(f"Error en IA: {ex}")
                self.show_error("Error obteniendo consejo")

        # Crear diálogo zen
        dialog = ft.AlertDialog(
            title=ft.Text(
                color_scheme["title"],
                size=20,
                weight=ft.FontWeight.W_500
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        name_field,
                        ft.Container(height=16),
                        context_field,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "🤖 Pedir consejo IA",
                            on_click=ask_ai,
                            style=ft.ButtonStyle(
                                bgcolor=color_scheme["main"],
                                color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=12)
                            ),
                            width=280
                        )
                    ],
                    tight=True
                ),
                width=320,
                bgcolor=color_scheme["bg"],
                padding=ft.padding.all(20),
                border_radius=16
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: self.close_dialog()
                ),
                ft.ElevatedButton(
                    "✅ Guardar tag",
                    on_click=create_tag,
                    style=ft.ButtonStyle(
                        bgcolor=color_scheme["main"],
                        color="#FFFFFF"
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_ai_advice_dialog(self, advice, tag_type):
        """Mostrar consejo de IA"""
        colors = {
            "positive": {"bg": ZenColors.positive_light, "main": ZenColors.positive_main},
            "growth": {"bg": ZenColors.growth_light, "main": ZenColors.growth_main}
        }

        color_scheme = colors[tag_type]

        dialog = ft.AlertDialog(
            title=ft.Text("🤖 Consejo de IA", size=18, weight=ft.FontWeight.W_500),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(advice, size=14, color=ZenColors.text_secondary)
                    ]
                ),
                width=300,
                bgcolor=color_scheme["bg"],
                padding=ft.padding.all(16),
                border_radius=12
            ),
            actions=[
                ft.TextButton(
                    "💬 Seguir charlando",
                    on_click=lambda e: self.continue_chat()
                ),
                ft.TextButton(
                    "✨ Entendido",
                    on_click=lambda e: self.close_dialog()
                )
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def refresh_positive_tags(self):
        """Actualizar visualización de tags positivos"""
        self.positive_tags_container.controls.clear()

        for tag in self.positive_tags:
            tag_chip = ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"{tag.emoji} {tag.name}", size=14, weight=ft.FontWeight.W_500),
                        ft.TextButton(
                            content=ft.Text("×", size=16),
                            on_click=lambda e, t=tag: self.remove_positive_tag(t),
                            style=ft.ButtonStyle(padding=ft.padding.all(4))
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                bgcolor=ZenColors.positive_glow,
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                border_radius=16,
                border=ft.border.all(1, ZenColors.positive_main)
            )
            self.positive_tags_container.controls.append(tag_chip)

        if self.page:
            self.page.update()

    def refresh_growth_tags(self):
        """Actualizar visualización de tags de crecimiento"""
        self.growth_tags_container.controls.clear()

        for tag in self.growth_tags:
            tag_chip = ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"{tag.emoji} {tag.name}", size=14, weight=ft.FontWeight.W_500),
                        ft.TextButton(
                            content=ft.Text("×", size=16),
                            on_click=lambda e, t=tag: self.remove_growth_tag(t),
                            style=ft.ButtonStyle(padding=ft.padding.all(4))
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                bgcolor=ZenColors.growth_glow,
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                border_radius=16,
                border=ft.border.all(1, ZenColors.growth_main)
            )
            self.growth_tags_container.controls.append(tag_chip)

        if self.page:
            self.page.update()

    def remove_positive_tag(self, tag):
        """Eliminar tag positivo"""
        self.positive_tags.remove(tag)
        self.refresh_positive_tags()

    def remove_growth_tag(self, tag):
        """Eliminar tag de crecimiento"""
        self.growth_tags.remove(tag)
        self.refresh_growth_tags()

    def set_worth_it(self, value, e):
        """Establecer si mereció la pena el día"""
        self.page = e.page
        self.worth_it = value

        # Actualizar estilos de botones
        for btn_key, btn in self.worth_it_buttons.items():
            if (btn_key == "yes" and value) or (btn_key == "no" and not value):
                btn.style.bgcolor = "#48BB78" if value else "#ED8936"
                btn.style.color = "#FFFFFF"
            else:
                btn.style.bgcolor = "#F1F5F9"
                btn.style.color = "#4A5568"

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
                    growth_tags=self.growth_tags,
                    worth_it=self.worth_it
                )

                if entry_id:
                    self.show_success("Reflexión guardada con amor 🌸")
                    self.clear_form()
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
            # Generar resumen del día
            summary = get_daily_summary(
                reflection=self.reflection_field.value.strip(),
                positive_tags=self.positive_tags,
                growth_tags=self.growth_tags,
                worth_it=self.worth_it
            )

            self.show_daily_summary_dialog(summary)

        except Exception as ex:
            print(f"Error en chat IA: {ex}")
            self.show_error("Error iniciando chat")

    def show_daily_summary_dialog(self, summary):
        """Mostrar resumen diario de IA"""
        dialog = ft.AlertDialog(
            title=ft.Text("🤖 Resumen de tu día", size=18, weight=ft.FontWeight.W_500),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(summary, size=14, color=ZenColors.text_secondary)
                    ]
                ),
                width=350,
                height=300,
                bgcolor="#F8FAFC",
                padding=ft.padding.all(16),
                border_radius=12
            ),
            actions=[
                ft.TextButton(
                    "💬 Continuar chat",
                    on_click=lambda e: self.continue_chat()
                ),
                ft.TextButton(
                    "🙏 Gracias",
                    on_click=lambda e: self.close_dialog()
                )
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def continue_chat(self):
        """Continuar chat (funcionalidad futura)"""
        self.close_dialog()
        self.show_success("Chat extendido próximamente 🚀")

    def clear_form(self):
        """Limpiar formulario zen"""
        self.reflection_field.value = ""
        self.positive_tags.clear()
        self.growth_tags.clear()
        self.worth_it = None

        # Restablecer botones
        for btn in self.worth_it_buttons.values():
            btn.style.bgcolor = "#F1F5F9"
            btn.style.color = "#4A5568"

        self.refresh_positive_tags()
        self.refresh_growth_tags()

        if self.page:
            self.page.update()

    def close_dialog(self):
        """Cerrar diálogo"""
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def logout_click(self, e):
        """Cerrar sesión zen"""
        self.page = e.page
        self.clear_form()
        self.app.navigate_to_login()

    def show_error(self, message):
        """Mostrar error zen"""
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"⚠️ {message}", color="#FFFFFF"),
                bgcolor="#F56565"
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()

    def show_success(self, message):
        """Mostrar éxito zen"""
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"🌸 {message}", color="#FFFFFF"),
                bgcolor="#48BB78"
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
    def open_positive_tag_dialog(self, e):
        """Abrir diálogo para añadir momento positivo"""
        dialog = TagDialog(
            page=e.page,
            tag_type="positive",
            on_tag_created=self.on_tag_created,
            on_error=self.show_error
        )
        dialog.show()

    def open_growth_tag_dialog(self, e):
    """Abrir diálogo para añadir área de crecimiento"""
         dialog = TagDialog(
            page=e.page,
            tag_type="growth",
            on_tag_created=self.on_tag_created,
            on_error=self.show_error
         )
        dialog.show()