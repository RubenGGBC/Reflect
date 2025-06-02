"""
📝 Entry Screen MEJORADA - ReflectApp
Pantalla principal con layout corregido y persistencia del texto
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

    @classmethod
    def from_dict(cls, tag_dict):
        """Crear DynamicTag desde diccionario"""
        return cls(
            name=tag_dict.get('name', ''),
            context=tag_dict.get('context', ''),
            tag_type=tag_dict.get('type', 'positive'),
            emoji=tag_dict.get('emoji', '+')
        )

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "name": self.name,
            "context": self.context,
            "type": self.type,
            "emoji": self.emoji
        }

    def __str__(self):
        return f"DynamicTag({self.emoji} {self.name} - {self.type})"

class EntryScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.current_user = None
        self.theme = get_theme()

        # Campos principales
        self.reflection_field = None
        self.positive_tags = []
        self.negative_tags = []
        self.worth_it = None

        # Contenedores para tags
        self.positive_tags_container = None
        self.negative_tags_container = None
        self.worth_it_buttons = {"yes": None, "no": None}

        # Estado de carga y bloqueo - NUEVO
        self.tags_loaded = False
        self.data_loaded = False
        self.is_saved_today = False  # NUEVO: Para bloquear cambios después de guardar

        print("🏗️ EntryScreen inicializada con sistema mejorado")

    def set_user(self, user_data):
        """Establecer usuario y marcar datos como no cargados"""
        self.current_user = user_data
        self.data_loaded = False
        self.is_saved_today = False  # Reset del estado de guardado
        print(f"🙋‍♂️ Usuario establecido: {user_data.get('name', 'Unknown')} (ID: {user_data.get('id')})")

    def update_theme(self):
        """Actualizar tema cuando cambie"""
        old_theme = self.theme.name if self.theme else "none"
        self.theme = get_theme()
        new_theme = self.theme.name

        print(f"🎨 Actualizando tema: {old_theme} → {new_theme}")

        if self.page:
            apply_theme_to_page(self.page)
            self.page.update()

    def check_if_saved_today(self):
        """Verificar si ya se guardó una entrada hoy - NUEVO MÉTODO"""
        if not self.current_user:
            return False

        try:
            from services import db
            user_id = self.current_user['id']
            self.is_saved_today = db.has_submitted_today(user_id)
            print(f"📅 ¿Guardado hoy?: {self.is_saved_today}")
            return self.is_saved_today
        except Exception as e:
            print(f"❌ Error verificando si guardó hoy: {e}")
            return False

    def load_today_data(self):
        """Cargar datos de hoy (entrada guardada + tags temporales)"""
        print("📅 === INICIANDO CARGA COMPLETA DE DATOS DE HOY ===")

        if not self.current_user:
            print("❌ No hay usuario para cargar datos")
            return

        try:
            from services import db
            user_id = self.current_user['id']

            print(f"🔍 Cargando datos de hoy para usuario {user_id}")

            # Verificar si ya guardó hoy
            self.check_if_saved_today()

            # Usar nuevo método que combina entrada guardada + tags temporales
            today_data = db.get_today_entry_with_temp_tags(user_id)

            # IMPORTANTE: No limpiar datos si ya están cargados y hay texto en reflexión
            if not self.data_loaded:
                self.positive_tags.clear()
                self.negative_tags.clear()

            # Cargar reflexión SOLO si no hay texto ya escrito (evitar borrar)
            if today_data.get('reflection') and self.reflection_field:
                if not self.reflection_field.value or not self.reflection_field.value.strip():
                    self.reflection_field.value = today_data['reflection']
                    print(f"📝 Reflexión cargada: {today_data['reflection'][:50]}...")
                else:
                    print(f"📝 Reflexión NO sobrescrita - ya hay texto")

            # Cargar worth_it
            if today_data.get('worth_it') is not None:
                self.worth_it = today_data['worth_it']
                print(f"💭 Worth it cargado: {self.worth_it}")

            # Cargar tags positivos (SOLO si no están ya cargados)
            if not self.data_loaded:
                positive_tags_data = today_data.get('positive_tags', [])
                for tag_data in positive_tags_data:
                    tag = DynamicTag.from_dict(tag_data)
                    self.positive_tags.append(tag)
                    print(f"  ➕ Tag positivo: {tag}")

                # Cargar tags negativos
                negative_tags_data = today_data.get('negative_tags', [])
                for tag_data in negative_tags_data:
                    tag = DynamicTag.from_dict(tag_data)
                    self.negative_tags.append(tag)
                    print(f"  ➖ Tag negativo: {tag}")

            print(f"📊 DATOS CARGADOS: {len(self.positive_tags)} positivos, {len(self.negative_tags)} negativos")
            print(f"📊 Estado: Guardado={today_data.get('has_saved_entry', False)}, Temporal={today_data.get('has_temp_tags', False)}")
            print(f"🔒 Ya guardó hoy: {self.is_saved_today}")

            self.data_loaded = True

        except Exception as ex:
            print(f"❌ ERROR CRÍTICO cargando datos de hoy: {ex}")
            import traceback
            traceback.print_exc()

    def build(self):
        """Construir vista principal zen con layout CORREGIDO"""
        print("🏗️ === CONSTRUYENDO ENTRYSCREEN MEJORADA ===")

        # Actualizar tema
        self.theme = get_theme()
        print(f"🎨 Construyendo EntryScreen con tema: {self.theme.display_name}")

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
            label_style=ft.TextStyle(color=self.theme.text_secondary),
            # NUEVO: Hacer readonly si ya guardó hoy
            read_only=self.is_saved_today
        )

        # Contenedores para tags dinámicos
        self.positive_tags_container = ft.Column(spacing=8)
        self.negative_tags_container = ft.Column(spacing=8)

        print(f"📦 Contenedores creados")

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
            height=48,
            disabled=self.is_saved_today  # NUEVO: Deshabilitar si ya guardó
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
            height=48,
            disabled=self.is_saved_today  # NUEVO: Deshabilitar si ya guardó
        )

        # Header con gradiente temático
        back_button = ft.TextButton(
            "← Salir",
            on_click=self.logout_click,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # LAYOUT CORREGIDO: Botones uno al lado del otro
        top_buttons_row = ft.Row(
            [
                ft.TextButton(
                    "🎨",
                    on_click=self.go_to_theme_selector,
                    style=ft.ButtonStyle(color="#FFFFFF"),
                    tooltip="Cambiar tema"
                ),
                ft.TextButton(
                    "📅",
                    on_click=self.go_to_calendar,
                    style=ft.ButtonStyle(color="#FFFFFF"),
                    tooltip="Ver calendario"
                )
            ],
            spacing=0
        )

        user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'
        header = create_gradient_header(
            title=f"Hola, {user_name} 🧘‍♀️",
            left_button=back_button,
            right_button=top_buttons_row,
            theme=self.theme
        )

        # MENSAJE DE ESTADO SI YA GUARDÓ - NUEVO
        status_message = None
        if self.is_saved_today:
            status_message = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.LOCK, color=self.theme.accent_primary, size=20),
                        ft.Text(
                            "✅ Entrada del día guardada. Solo puedes visualizar.",
                            color=self.theme.accent_primary,
                            size=14,
                            weight=ft.FontWeight.W_500
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                bgcolor=self.theme.positive_light,
                padding=ft.padding.all(12),
                border_radius=12,
                border=ft.border.all(1, self.theme.positive_main),
                margin=ft.margin.only(bottom=16)
            )

        # Vista principal zen con tema
        main_content = ft.Column(
            [
                # Mensaje de estado (si aplica)
                status_message,

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
                                    # NUEVO: Solo mostrar botón + si no guardó hoy
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
                                            ),
                                            disabled=self.is_saved_today
                                        ),
                                        bgcolor=self.theme.positive_light,
                                        border_radius=20,
                                        padding=ft.padding.all(4)
                                    ) if not self.is_saved_today else ft.Container()
                                ]
                            ),
                            ft.Container(height=12),
                            self.positive_tags_container
        def build(self):
    """Construir vista principal zen con layout CORREGIDO + Interactive Moments"""
    print("🏗️ === CONSTRUYENDO ENTRYSCREEN MEJORADA ===")

    # Actualizar tema
    self.theme = get_theme()
    print(f"🎨 Construyendo EntryScreen con tema: {self.theme.display_name}")

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
        label_style=ft.TextStyle(color=self.theme.text_secondary),
        # NUEVO: Hacer readonly si ya guardó hoy
        read_only=self.is_saved_today
    )

    # Contenedores para tags dinámicos
    self.positive_tags_container = ft.Column(spacing=8)
    self.negative_tags_container = ft.Column(spacing=8)

    print(f"📦 Contenedores creados")

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
        height=48,
        disabled=self.is_saved_today  # NUEVO: Deshabilitar si ya guardó
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
        height=48,
        disabled=self.is_saved_today  # NUEVO: Deshabilitar si ya guardó
    )

    # Header con gradiente temático
    back_button = ft.TextButton(
        "← Salir",
        on_click=self.logout_click,
        style=ft.ButtonStyle(color="#FFFFFF")
    )

    # LAYOUT CORREGIDO: Botones uno al lado del otro
    top_buttons_row = ft.Row(
        [
            ft.TextButton(
                "🎨",
                on_click=self.go_to_theme_selector,
                style=ft.ButtonStyle(color="#FFFFFF"),
                tooltip="Cambiar tema"
            ),
            ft.TextButton(
                "📅",
                on_click=self.go_to_calendar,
                style=ft.ButtonStyle(color="#FFFFFF"),
                tooltip="Ver calendario"
            )
        ],
        spacing=0
    )

    user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'
    header = create_gradient_header(
        title=f"Hola, {user_name} 🧘‍♀️",
        left_button=back_button,
        right_button=top_buttons_row,
        theme=self.theme
    )

    # MENSAJE DE ESTADO SI YA GUARDÓ - NUEVO
    status_message = None
    if self.is_saved_today:
        status_message = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.LOCK, color=self.theme.accent_primary, size=20),
                    ft.Text(
                        "✅ Entrada del día guardada. Solo puedes visualizar.",
                        color=self.theme.accent_primary,
                        size=14,
                        weight=ft.FontWeight.W_500
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor=self.theme.positive_light,
            padding=ft.padding.all(12),
            border_radius=12,
            border=ft.border.all(1, self.theme.positive_main),
            margin=ft.margin.only(bottom=16)
        )

    # Vista principal zen con tema
    main_content = ft.Column(
        [
            # Mensaje de estado (si aplica)
            status_message,

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
                                # NUEVO: Solo mostrar botón + si no guardó hoy
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
                                        ),
                                        disabled=self.is_saved_today
                                    ),
                                    bgcolor=self.theme.positive_light,
                                    border_radius=20,
                                    padding=ft.padding.all(4)
                                ) if not self.is_saved_today else ft.Container()
                            ]
                        ),
                        ft.Container(height=12),
                        self.positive_tags_container
                    ]
                ),
                theme=self.theme,
                is_surface=False
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
                                # NUEVO: Solo mostrar botón + si no guardó hoy
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
                                        ),
                                        disabled=self.is_saved_today
                                    ),
                                    bgcolor=self.theme.negative_light,
                                    border_radius=20,
                                    padding=ft.padding.all(4)
                                ) if not self.is_saved_today else ft.Container()
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

            # ✨ BOTONES DE ACCIÓN MEJORADOS - CON INTERACTIVE MOMENTS ✨
            ft.Column(
                [
                    # Primera fila: Guardar (solo si no guardó hoy)
                    ft.Row(
                        [
                            create_themed_button(
                                "💾 Guardar Reflexión",
                                self.save_entry,
                                theme=self.theme,
                                button_type="positive",
                                height=56,
                                width=None
                            ) if not self.is_saved_today else ft.Container()
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    ) if not self.is_saved_today else ft.Container(),

                    ft.Container(height=16) if not self.is_saved_today else ft.Container(),

                    # Segunda fila: Chat IA y Calendario
                    ft.Row(
                        [
                            create_themed_button(
                                "🤖 Chat IA",
                                self.chat_ai,
                                theme=self.theme,
                                button_type="primary",
                                height=56
                            ),
                            ft.Container(width=16),
                            create_themed_button(
                                "📅 Calendario",
                                self.go_to_calendar,
                                theme=self.theme,
                                button_type="primary",
                                height=56
                            )
                        ],
                        expand=True
                    ),

                    ft.Container(height=12),

                    # ✨ TERCERA FILA: MOMENTOS INTERACTIVOS - NUEVO ✨
                    ft.Row(
                        [
                            create_themed_button(
                                "🎮 Momentos Interactivos",
                                self.open_interactive_moments,
                                theme=self.theme,
                                button_type="primary",
                                height=50,
                                width=None  # Ocupa todo el ancho
                            ) if not self.is_saved_today else ft.Container()
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    ) if not self.is_saved_today else ft.Container()
                ]
            ),

            ft.Container(height=24)
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=0
    )

    # Filtrar None del contenido principal
    main_content.controls = [control for control in main_content.controls if control is not None]

    view = ft.View(
        "/entry",
        [
            header,
            ft.Container(
                content=main_content,
                padding=ft.padding.all(20),
                expand=True
            )
        ],
        padding=0,
        spacing=0,
        bgcolor=self.theme.primary_bg
    )

    print("🏗️ Vista EntryScreen construida - esperando carga manual")
    return view

# ✨ AÑADIR ESTE MÉTODO AL FINAL DE LA CLASE EntryScreen ✨

def open_interactive_moments(self, e):
    """Abrir pantalla de momentos interactivos - NUEVO MÉTODO"""
    print("🎮 === ABRIENDO MOMENTOS INTERACTIVOS ===")
    self.page = e.page

    if self.is_saved_today:
        self.show_error("🔒 No puedes añadir momentos - entrada ya guardada")
        return

    # Guardar callback para cuando se creen momentos
    def on_moments_created(simple_tags):
        """Callback cuando se crean momentos en la pantalla interactiva"""
        print(f"🎮 Recibidos {len(simple_tags)} momentos interactivos")

        # Procesar cada momento usando el sistema existente
        for simple_tag in simple_tags:
            print(f"   📝 {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")

            # Usar tu sistema existente para añadir el tag
            try:
                self.on_tag_created(simple_tag)
            except Exception as ex:
                print(f"❌ Error procesando tag: {ex}")

        # Mostrar mensaje de éxito
        self.show_success(f"🎮 {len(simple_tags)} momentos interactivos añadidos exitosamente")

    # Guardar contexto en la app para que lo use InteractiveMomentsScreen
    if hasattr(self.app, 'interactive_moments_callback'):
        self.app.interactive_moments_callback = on_moments_created
        print("✅ Callback configurado en app")
    else:
        print("⚠️ App no tiene atributo interactive_moments_callback")

    # Navegar a la nueva pantalla
    print("🛣️ Navegando a /interactive_moments")
    self.page.go("/interactive_moments")
    def load_and_refresh_all(self):
        """Cargar todos los datos y refrescar interfaz - método público"""
        print("🔄 === INICIANDO LOAD AND REFRESH ALL ===")

        if not self.current_user:
            print("❌ No hay usuario actual")
            return

        if not self.positive_tags_container or not self.negative_tags_container:
            print("❌ Contenedores de tags no están inicializados")
            return

        # Cargar datos completos
        self.load_today_data()

        # Actualizar botones worth_it
        if self.worth_it is not None:
            self.update_worth_it_buttons()

        # Refrescar interfaz
        self.force_refresh_all()

        print(f"✅ === LOAD AND REFRESH COMPLETADO ===")

    def save_tag_temporarily(self, tag):
        """Guardar tag temporalmente en base de datos"""
        if not self.current_user:
            print("❌ No hay usuario para guardar tag temporal")
            return False

        # NUEVO: No permitir si ya guardó hoy
        if self.is_saved_today:
            print("🔒 No se puede añadir tag - entrada ya guardada")
            return False

        try:
            from services import db
            user_id = self.current_user['id']

            tag_id = db.save_temp_tag(
                user_id=user_id,
                tag_name=tag.name,
                tag_context=tag.context,
                tag_type=tag.type,
                tag_emoji=tag.emoji
            )

            if tag_id:
                print(f"💾 Tag guardado temporalmente: {tag.emoji} {tag.name} (ID: {tag_id})")
                return True
            else:
                print("❌ Error guardando tag temporal")
                return False

        except Exception as e:
            print(f"❌ Error en save_tag_temporarily: {e}")
            return False

    def on_tag_created(self, simple_tag):
        """Callback cuando se crea un tag desde NewTagScreen - MEJORADO SIN BORRAR TEXTO"""
        print(f"🏷️ === ON_TAG_CREATED MEJORADO ===")
        print(f"📝 Tag recibido: {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")

        # NUEVO: No permitir si ya guardó hoy
        if self.is_saved_today:
            self.show_error("🔒 No puedes añadir momentos - entrada ya guardada")
            return

        # Convertir SimpleTag a DynamicTag
        tag = DynamicTag.from_simple_tag(simple_tag)
        print(f"🔄 Tag convertido: {tag}")

        # Guardar temporalmente en base de datos PRIMERO
        saved_successfully = self.save_tag_temporarily(tag)

        if saved_successfully:
            # Añadir a la lista en memoria
            if tag.type == "positive":
                self.positive_tags.append(tag)
                print(f"➕ Añadido a positive_tags. Total: {len(self.positive_tags)}")
            elif tag.type == "negative":
                self.negative_tags.append(tag)
                print(f"➖ Añadido a negative_tags. Total: {len(self.negative_tags)}")

            # Refrescar interfaz SIN TOCAR EL CAMPO DE REFLEXIÓN
            self.force_refresh_all()
            self.show_success(f"✅ Momento {tag.type} '{tag.name}' añadido")
        else:
            self.show_error("❌ Error guardando el momento")

        print(f"🏷️ === ON_TAG_CREATED COMPLETADO ===")

    def save_entry(self, e):
        """Guardar entrada zen - MEJORADO CON BLOQUEO"""
        print("💾 === SAVE ENTRY MEJORADO ===")
        self.page = e.page

        # NUEVO: Verificar si ya guardó hoy
        if self.is_saved_today:
            self.show_error("🔒 Ya guardaste tu entrada de hoy")
            return

        reflection_text = self.reflection_field.value.strip() if self.reflection_field.value else ""

        print(f"📝 Reflexión: '{reflection_text[:100]}...'")
        print(f"➕ Tags positivos: {len(self.positive_tags)}")
        print(f"➖ Tags negativos: {len(self.negative_tags)}")
        print(f"💭 Worth it: {self.worth_it}")

        if not reflection_text and not self.positive_tags and not self.negative_tags:
            self.show_error("Añade al menos una reflexión o un momento del día")
            return

        try:
            from services import db

            if self.current_user:
                user_id = self.current_user['id']

                entry_id = db.save_daily_entry(
                    user_id=user_id,
                    free_reflection=reflection_text,
                    positive_tags=self.positive_tags,
                    negative_tags=self.negative_tags,
                    worth_it=self.worth_it
                )

                if entry_id:
                    print(f"✅ Entrada guardada con ID: {entry_id}")
                    self.show_success("✨ Reflexión guardada correctamente")

                    # NUEVO: Marcar como guardado y reconstruir vista
                    self.is_saved_today = True
                    self.rebuild_view_with_lock()

                    print("🔒 Entrada bloqueada - no se puede modificar más")
                else:
                    self.show_error("Error al guardar en base de datos")
            else:
                self.show_error("Usuario no autenticado")

        except Exception as ex:
            print(f"❌ ERROR guardando: {ex}")
            import traceback
            traceback.print_exc()
            self.show_error("Error del sistema")

    def rebuild_view_with_lock(self):
        """Reconstruir vista con estado bloqueado - NUEVO MÉTODO"""
        if not self.page:
            return

        try:
            # Limpiar vistas y reconstruir
            if self.page.views:
                self.page.views.clear()

            # Construir nueva vista con estado bloqueado
            new_view = self.build()
            self.page.views.append(new_view)

            # Cargar datos y refrescar
            self.load_and_refresh_all()

            print("🔄 Vista reconstruida con estado bloqueado")

        except Exception as e:
            print(f"❌ Error reconstruyendo vista: {e}")

    # [Resto de métodos iguales que antes: refresh_positive_tags, refresh_negative_tags, etc.]
    def refresh_positive_tags(self):
        """Actualizar visualización de tags positivos con tema"""
        print(f"🔄 REFRESH POSITIVE TAGS (Total: {len(self.positive_tags)})")

        if not self.positive_tags_container:
            print("❌ positive_tags_container no existe")
            return

        self.positive_tags_container.controls.clear()

        if not self.positive_tags:
            placeholder = ft.Text(
                "Aún no has añadido momentos positivos del día",
                size=12,
                color=self.theme.text_hint,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
            self.positive_tags_container.controls.append(placeholder)
        else:
            for i, tag in enumerate(self.positive_tags):
                tag_chip = self.create_tag_chip(tag, "positive")
                self.positive_tags_container.controls.append(tag_chip)

        print(f"✅ Tags positivos refrescados: {len(self.positive_tags_container.controls)} controles")

    def refresh_negative_tags(self):
        """Actualizar visualización de tags negativos con tema"""
        print(f"🔄 REFRESH NEGATIVE TAGS (Total: {len(self.negative_tags)})")

        if not self.negative_tags_container:
            print("❌ negative_tags_container no existe")
            return

        self.negative_tags_container.controls.clear()

        if not self.negative_tags:
            placeholder = ft.Text(
                "Aún no has añadido momentos negativos del día",
                size=12,
                color=self.theme.text_hint,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
            self.negative_tags_container.controls.append(placeholder)
        else:
            for i, tag in enumerate(self.negative_tags):
                tag_chip = self.create_tag_chip(tag, "negative")
                self.negative_tags_container.controls.append(tag_chip)

        print(f"✅ Tags negativos refrescados: {len(self.negative_tags_container.controls)} controles")

    def force_refresh_all(self):
        """Forzar actualización visual completa"""
        print("🔄 === FORCE REFRESH ALL ===")

        try:
            self.refresh_positive_tags()
            self.refresh_negative_tags()

            # Actualizar campo de reflexión
            if hasattr(self, 'page') and self.page:
                self.page.update()
                print("🔄 Página actualizada")

            print("✅ === FORCE REFRESH COMPLETADO ===")
        except Exception as e:
            print(f"❌ ERROR en force_refresh_all: {e}")
            import traceback
            traceback.print_exc()

    def create_tag_chip(self, tag, tag_type):
        """Crear chip visual para un tag"""
        is_positive = tag_type == "positive"
        bg_color = self.theme.positive_light if is_positive else self.theme.negative_light
        border_color = self.theme.positive_main if is_positive else self.theme.negative_main

        # NUEVO: Solo mostrar botón X si no guardó hoy
        remove_button = None
        if not self.is_saved_today:
            remove_callback = self.remove_positive_tag if is_positive else self.remove_negative_tag
            remove_button = ft.TextButton(
                content=ft.Text("×", size=16, color=self.theme.text_secondary),
                on_click=lambda e, t=tag: remove_callback(t),
                style=ft.ButtonStyle(padding=ft.padding.all(4))
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                f"{tag.emoji} {tag.name}",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=self.theme.text_primary,
                                expand=True
                            ),
                            remove_button if remove_button else ft.Container()
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
            bgcolor=bg_color,
            padding=ft.padding.all(12),
            border_radius=16,
            border=ft.border.all(1, border_color),
            margin=ft.margin.only(bottom=8)
        )

    def update_worth_it_buttons(self):
        """Actualizar botones worth_it con el valor cargado"""
        if not self.worth_it_buttons["yes"] or not self.worth_it_buttons["no"]:
            return

        for btn_key, btn in self.worth_it_buttons.items():
            if (btn_key == "yes" and self.worth_it) or (btn_key == "no" and self.worth_it is False):
                btn.style.bgcolor = self.theme.positive_main if self.worth_it else self.theme.negative_main
                btn.style.color = "#FFFFFF"
            else:
                btn.style.bgcolor = self.theme.surface_variant
                btn.style.color = self.theme.text_secondary

    def open_positive_tag_dialog(self, e):
        """Abrir pantalla para añadir momento positivo"""
        if self.is_saved_today:
            self.show_error("🔒 No puedes añadir momentos - entrada ya guardada")
            return

        print("➕ Abriendo diálogo de tag positivo...")
        self.page = e.page
        self.page.go("/new_tag?type=positive")

    def open_negative_tag_dialog(self, e):
        """Abrir pantalla para añadir momento negativo"""
        if self.is_saved_today:
            self.show_error("🔒 No puedes añadir momentos - entrada ya guardada")
            return

        print("➖ Abriendo diálogo de tag negativo...")
        self.page = e.page
        self.page.go("/new_tag?type=negative")

    def remove_positive_tag(self, tag):
        """Eliminar tag positivo"""
        if self.is_saved_today:
            return

        print(f"🗑️ Eliminando tag positivo: {tag}")
        if tag in self.positive_tags:
            self.positive_tags.remove(tag)
            self.refresh_positive_tags()

            if hasattr(self, 'page') and self.page:
                self.page.update()

    def remove_negative_tag(self, tag):
        """Eliminar tag negativo"""
        if self.is_saved_today:
            return

        print(f"🗑️ Eliminando tag negativo: {tag}")
        if tag in self.negative_tags:
            self.negative_tags.remove(tag)
            self.refresh_negative_tags()

            if hasattr(self, 'page') and self.page:
                self.page.update()

    def set_worth_it(self, value, e):
        """Establecer si mereció la pena el día"""
        if self.is_saved_today:
            return

        print(f"💭 SET WORTH IT: {value}")
        self.page = e.page
        self.worth_it = value

        self.update_worth_it_buttons()

        if self.page:
            self.page.update()

    def chat_ai(self, e):
        """Iniciar chat con IA"""
        print("🤖 === CHAT IA ===")
        self.page = e.page

        reflection_text = self.reflection_field.value.strip() if self.reflection_field.value else ""

        if not reflection_text and not self.positive_tags and not self.negative_tags:
            self.show_error("Añade contenido para charlar con la IA")
            return

        try:
            summary = get_daily_summary(
                reflection=reflection_text,
                positive_tags=self.positive_tags,
                negative_tags=self.negative_tags,
                worth_it=self.worth_it
            )

            self.show_daily_summary_dialog(summary)

        except Exception as ex:
            print(f"❌ Error en chat IA: {ex}")
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
        self.close_dialog()
        self.show_success("Chat extendido próximamente")

    def close_dialog(self):
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def go_to_calendar(self, e):
        self.page = e.page
        self.page.go("/calendar")

    def go_to_theme_selector(self, e):
        self.page = e.page
        self.page.go("/theme_selector")

    def logout_click(self, e):
        self.page = e.page
        self.app.navigate_to_login()

    def show_error(self, message):
        print(f"❌ MOSTRAR ERROR: {message}")
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
        print(f"✅ MOSTRAR ÉXITO: {message}")
        if hasattr(self, 'page') and self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"✅ {message}", color="#FFFFFF"),
                bgcolor=self.theme.positive_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()

def open_interactive_moments(self, e):
    """Abrir pantalla de momentos interactivos"""
    print("🎮 === ABRIENDO MOMENTOS INTERACTIVOS ===")
    self.page = e.page

    # Guardar callback para cuando se creen momentos
    def on_moments_created(simple_tags):
        """Callback cuando se crean momentos en la pantalla interactiva"""
        print(f"🎮 Recibidos {len(simple_tags)} momentos interactivos")

        # Procesar cada momento
        for simple_tag in simple_tags:
            print(f"   📝 {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")

            # Usar tu sistema existente
            self.on_tag_created(simple_tag)

    # Guardar contexto en la app para que lo use InteractiveMomentsScreen
    if hasattr(self.app, 'interactive_moments_callback'):
        self.app.interactive_moments_callback = on_moments_created

    # Navegar a la nueva pantalla
    self.page.go("/interactive_moments")