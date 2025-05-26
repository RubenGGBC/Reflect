import flet as ft
from services.ai_service import analyze_tag, get_daily_summary
from screens.new_tag_screen import NewTagScreen, SimpleTag

# Asegurar que DynamicTag esté definido

class ZenColors:
    """Colores zen específicos"""
    # Positivos
    positive_light = "#E8F5E8"
    positive_glow = "#A8EDEA"
    positive_main = "#48BB78"

    # Negativos (antes growth)
    negative_light = "#FEE2E2"
    negative_glow = "#FECACA"
    negative_main = "#EF4444"

    # Base
    background = "#F8FAFC"
    surface = "#FFFFFF"
    text_primary = "#2D3748"
    text_secondary = "#4A5568"
    text_hint = "#A0AEC0"

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

        # Campos principales
        self.reflection_field = None
        self.positive_tags = []
        self.negative_tags = []  # Cambio de growth_tags
        self.worth_it = None  # True, False, o None

        # Contenedores para tags
        self.positive_tags_container = None
        self.negative_tags_container = None  # Cambio de growth_tags_container
        self.worth_it_buttons = {"yes": None, "no": None}

    def set_user(self, user_data):
        """Establecer usuario y cargar datos del día"""
        self.current_user = user_data
        self.load_today_tags()

    def load_today_tags(self):
        """Cargar tags del día actual desde la base de datos"""
        if not self.current_user:
            return

        try:
            from services import db
            # Obtener entradas de hoy
            entries_today = db.get_user_entries(
                user_id=self.current_user['id'],
                limit=10,  # Entradas recientes
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
        """Construir vista principal zen"""
        # Cargar tags del día al construir la vista
        self.load_today_tags()

        # Resto del código de build() igual...

        # Campo de reflexión libre zen
        self.reflection_field = ft.TextField(
            label="Como te ha ido el dia?",
            hint_text="Cuentame sobre tu dia... Tomate tu tiempo para reflexionar",
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
        self.negative_tags_container = ft.Column(spacing=8)  # Cambio

        # Botones para "¿Mereció la pena?"
        self.worth_it_buttons["yes"] = ft.ElevatedButton(
            "SI",
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
            "NO",
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
                            ft.TextButton(
                                "📅",
                                on_click=self.go_to_calendar,
                                style=ft.ButtonStyle(color="#FFFFFF"),
                                tooltip="Ver calendario"
                            )
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
                                            "Reflexion Libre",
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
                                                    "+ MOMENTOS POSITIVOS",
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ZenColors.positive_main,
                                                    expand=True
                                                ),
                                                ft.TextButton(
                                                    content=ft.Text("+", size=20, color=ZenColors.positive_main, weight=ft.FontWeight.BOLD),
                                                    on_click=self.open_positive_tag_dialog,  # Cambiado
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

                            # Sección MOMENTOS NEGATIVOS (antes growth)
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "- MOMENTOS NEGATIVOS",  # Cambiado
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ZenColors.negative_main,  # Cambiado
                                                    expand=True
                                                ),
                                                ft.TextButton(
                                                    content=ft.Text("+", size=20, color=ZenColors.negative_main, weight=ft.FontWeight.BOLD),
                                                    on_click=self.open_negative_tag_dialog,  # Cambiado
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ZenColors.negative_light,  # Cambiado
                                                        shape=ft.CircleBorder(),
                                                        padding=ft.padding.all(8)
                                                    )
                                                )
                                            ]
                                        ),
                                        ft.Container(height=12),
                                        self.negative_tags_container  # Cambiado
                                    ]
                                ),
                                padding=ft.padding.all(20),
                                bgcolor=ZenColors.negative_light,  # Cambiado
                                border_radius=16,
                                border=ft.border.all(1, ZenColors.negative_glow)  # Cambiado
                            ),

                            ft.Container(height=24),

                            # Pregunta final zen
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "¿Ha merecido la pena tu dia?",
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
                                        "Guardar",
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
                                        "Chat IA",
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

        # Refrescar tags después de crear la vista
        self.refresh_positive_tags()
        self.refresh_negative_tags()

        return view

    def on_tag_created(self, simple_tag):
        """Callback cuando se crea un tag desde NewTagScreen"""
        print(f"Recibido tag: {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")

        # Convertir SimpleTag a DynamicTag
        tag = DynamicTag.from_simple_tag(simple_tag)

        # Añadir a la lista correspondiente
        if tag.type == "positive":
            self.positive_tags.append(tag)
            print(f"Añadido a positive_tags. Total: {len(self.positive_tags)}")
        elif tag.type == "negative":
            self.negative_tags.append(tag)
            print(f"Añadido a negative_tags. Total: {len(self.negative_tags)}")

        # Forzar actualización de la interfaz
        self.force_refresh_tags()

        # Mostrar mensaje de éxito
        self.show_success(f"Momento {tag.type} '{tag.name}' anadido")

    def force_refresh_tags(self):
        """Forzar actualización visual de todos los tags"""
        print("Forzando actualización de tags...")
        self.refresh_positive_tags()
        self.refresh_negative_tags()

        # Si tenemos página, forzar actualización completa
        if hasattr(self, 'page') and self.page:
            self.page.update()
            print("Página actualizada")

    def create_test_tag_with_page(self, tag_type, e):
        """Crear tag de prueba con acceso a página"""
        self.page = e.page
        self.create_test_tag(tag_type)

    def create_test_tag(self, tag_type="positive"):
        """Crear tag de prueba para testing"""
        print(f"Creando tag de prueba: {tag_type}")

        if tag_type == "positive":
            test_tag = DynamicTag(
                name="Prueba Positiva",
                context="Esto es una prueba de momento positivo",
                tag_type="positive",
                emoji="😊"
            )
            self.positive_tags.append(test_tag)
            print(f"Tags positivos totales: {len(self.positive_tags)}")
        else:
            test_tag = DynamicTag(
                name="Prueba Negativa",
                context="Esto es una prueba de momento negativo",
                tag_type="negative",
                emoji="😔"
            )
            self.negative_tags.append(test_tag)
            print(f"Tags negativos totales: {len(self.negative_tags)}")

        # Forzar actualización
        self.force_refresh_tags()

        print(f"Tag de prueba {tag_type} creado y actualizado")

    def open_positive_tag_dialog(self, e):
        """Abrir pantalla para añadir momento positivo"""
        self.page = e.page
        self.page.go("/new_tag?type=positive")

    def open_negative_tag_dialog(self, e):
        """Abrir pantalla para añadir momento negativo"""
        self.page = e.page
        self.page.go("/new_tag?type=negative")

    def refresh_positive_tags(self):
        """Actualizar visualización de tags positivos"""
        print(f"Refreshing positive tags. Total: {len(self.positive_tags)}")

        if not self.positive_tags_container:
            print("ERROR: positive_tags_container no existe")
            return

        self.positive_tags_container.controls.clear()

        for i, tag in enumerate(self.positive_tags):
            print(f"Creando chip para tag {i}: {tag.emoji} {tag.name}")

            tag_chip = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
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
                        ft.Text(
                            tag.context[:50] + "..." if len(tag.context) > 50 else tag.context,
                            size=12,
                            color=ZenColors.text_secondary,
                            italic=True
                        )
                    ],
                    spacing=4,
                    tight=True
                ),
                bgcolor=ZenColors.positive_glow,
                padding=ft.padding.all(12),
                border_radius=16,
                border=ft.border.all(1, ZenColors.positive_main),
                margin=ft.margin.only(bottom=8)
            )
            self.positive_tags_container.controls.append(tag_chip)

        print(f"Chips creados: {len(self.positive_tags_container.controls)}")

    def refresh_negative_tags(self):
        """Actualizar visualización de tags negativos"""
        print(f"Refreshing negative tags. Total: {len(self.negative_tags)}")

        if not self.negative_tags_container:
            print("ERROR: negative_tags_container no existe")
            return

        self.negative_tags_container.controls.clear()

        for i, tag in enumerate(self.negative_tags):
            print(f"Creando chip para tag negativo {i}: {tag.emoji} {tag.name}")

            tag_chip = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(f"{tag.emoji} {tag.name}", size=14, weight=ft.FontWeight.W_500),
                                ft.TextButton(
                                    content=ft.Text("×", size=16),
                                    on_click=lambda e, t=tag: self.remove_negative_tag(t),
                                    style=ft.ButtonStyle(padding=ft.padding.all(4))
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Text(
                            tag.context[:50] + "..." if len(tag.context) > 50 else tag.context,
                            size=12,
                            color=ZenColors.text_secondary,
                            italic=True
                        )
                    ],
                    spacing=4,
                    tight=True
                ),
                bgcolor=ZenColors.negative_glow,
                padding=ft.padding.all(12),
                border_radius=16,
                border=ft.border.all(1, ZenColors.negative_main),
                margin=ft.margin.only(bottom=8)
            )
            self.negative_tags_container.controls.append(tag_chip)

        print(f"Chips negativos creados: {len(self.negative_tags_container.controls)}")

    def remove_positive_tag(self, tag):
        """Eliminar tag positivo"""
        self.positive_tags.remove(tag)
        self.refresh_positive_tags()

    def remove_negative_tag(self, tag):  # Cambiado nombre
        """Eliminar tag negativo"""  # Cambiado texto
        self.negative_tags.remove(tag)  # Cambiado
        self.refresh_negative_tags()  # Cambiado

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
                # Si no hay tags pero sí reflexión, guardar solo la reflexión
                entry_id = db.save_daily_entry(
                    user_id=self.current_user['id'],
                    free_reflection=self.reflection_field.value.strip(),
                    positive_tags=self.positive_tags,
                    negative_tags=self.negative_tags,
                    worth_it=self.worth_it
                )

                if entry_id:
                    self.show_success("Reflexion guardada correctamente")
                    # NO limpiar el formulario aquí para que los tags sigan visibles
                    # self.clear_form()
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
                negative_tags=self.negative_tags,  # Cambiado de growth_tags
                worth_it=self.worth_it
            )

            self.show_daily_summary_dialog(summary)

        except Exception as ex:
            print(f"Error en chat IA: {ex}")
            self.show_error("Error iniciando chat")

    def show_daily_summary_dialog(self, summary):
        """Mostrar resumen diario de IA"""
        dialog = ft.AlertDialog(
            title=ft.Text("IA - Resumen de tu dia", size=18, weight=ft.FontWeight.W_500),
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
                    "Continuar chat",
                    on_click=lambda e: self.continue_chat()
                ),
                ft.TextButton(
                    "Gracias",
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
        self.show_success("Chat extendido proximamente")

    def clear_form(self):
        """Limpiar formulario zen"""
        self.reflection_field.value = ""
        self.positive_tags.clear()
        self.negative_tags.clear()  # Cambiado
        self.worth_it = None

        # Restablecer botones
        for btn in self.worth_it_buttons.values():
            btn.style.bgcolor = "#F1F5F9"
            btn.style.color = "#4A5568"

        self.refresh_positive_tags()
        self.refresh_negative_tags()  # Cambiado

        if hasattr(self, 'page') and self.page:
            self.page.update()

    def close_dialog(self):
        """Cerrar diálogo"""
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def go_to_calendar(self, e):
        """Navegar al calendario"""
        self.page = e.page
        self.page.go("/calendar")

    def logout_click(self, e):
        """Cerrar sesión zen"""
        self.page = e.page
        self.clear_form()
        self.app.navigate_to_login()

    def show_error(self, message):
        """Mostrar error zen"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"ERROR: {message}", color="#FFFFFF"),
                bgcolor="#F56565"
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
        else:
            print(f"ERROR: {message}")

    def show_success(self, message):
        """Mostrar éxito zen"""
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"OK: {message}", color="#FFFFFF"),
                bgcolor="#48BB78"
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()
        else:
            print(f"OK: {message}")