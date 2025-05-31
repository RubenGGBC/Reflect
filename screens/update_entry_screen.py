"""
📝 Entry Screen COMPLETA CORREGIDA - ReflectApp
Pantalla principal con sistema de persistencia mejorado, protecciones y chat IA funcional
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

        # Estado de carga y bloqueo - MEJORADO
        self.tags_loaded = False
        self.data_loaded = False
        self.is_saved_today = False  # Para bloquear cambios después de guardar

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
        """Verificar si ya se guardó una entrada hoy - MÉTODO CORREGIDO"""
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
        """Cargar datos de hoy - CORREGIDO PARA NO PERDER TEXTO"""
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

            # ✅ IMPORTANTE: Preservar texto actual si existe
            current_text = self.reflection_field.value if self.reflection_field else ""
            has_current_text = current_text and current_text.strip()

            if not self.data_loaded or not has_current_text:
                # Solo limpiar si no hay datos cargados o no hay texto actual
                self.positive_tags.clear()
                self.negative_tags.clear()
                print("🧹 Limpiando tags (no hay texto actual)")
            else:
                print("🔒 NO limpiando tags - hay texto actual y datos ya cargados")

            # ✅ CARGAR REFLEXIÓN SOLO SI NO HAY TEXTO ACTUAL
            if today_data.get('reflection') and self.reflection_field:
                if not has_current_text:
                    self.reflection_field.value = today_data['reflection']
                    print(f"📝 Reflexión cargada: {today_data['reflection'][:50]}...")
                else:
                    print(f"📝 Reflexión NO sobrescrita - preservando texto actual")

            # Cargar worth_it
            if today_data.get('worth_it') is not None:
                self.worth_it = today_data['worth_it']
                print(f"💭 Worth it cargado: {self.worth_it}")

            # ✅ CARGAR TAGS SOLO SI NO HAY DATOS YA CARGADOS O NO HAY TEXTO
            if not self.data_loaded or not has_current_text:
                positive_tags_data = today_data.get('positive_tags', [])
                for tag_data in positive_tags_data:
                    tag = DynamicTag.from_dict(tag_data)
                    # ✅ Evitar duplicados
                    if not any(existing.name == tag.name and existing.context == tag.context for existing in self.positive_tags):
                        self.positive_tags.append(tag)
                        print(f"  ➕ Tag positivo: {tag}")

                negative_tags_data = today_data.get('negative_tags', [])
                for tag_data in negative_tags_data:
                    tag = DynamicTag.from_dict(tag_data)
                    # ✅ Evitar duplicados
                    if not any(existing.name == tag.name and existing.context == tag.context for existing in self.negative_tags):
                        self.negative_tags.append(tag)
                        print(f"  ➖ Tag negativo: {tag}")
            else:
                print("🔒 NO recargando tags - preservando estado actual")

            print(f"📊 DATOS FINALES: {len(self.positive_tags)} positivos, {len(self.negative_tags)} negativos")
            print(f"🔒 Ya guardó hoy: {self.is_saved_today}")

            self.data_loaded = True

        except Exception as ex:
            print(f"❌ ERROR CRÍTICO cargando datos de hoy: {ex}")
            import traceback
            traceback.print_exc()

    def load_and_refresh_all(self):
        """Cargar todos los datos y refrescar interfaz - MÉTODO PROTEGIDO"""
        print("🔄 === INICIANDO LOAD AND REFRESH ALL ===")

        if not self.current_user:
            print("❌ No hay usuario actual")
            return

        if not self.positive_tags_container or not self.negative_tags_container:
            print("❌ Contenedores de tags no están inicializados")
            return

        # ✅ GUARDAR TEXTO ACTUAL ANTES DE CARGAR
        current_reflection = ""
        if self.reflection_field and self.reflection_field.value:
            current_reflection = self.reflection_field.value
            print(f"💾 Preservando texto actual: {current_reflection[:50]}...")

        # Cargar datos completos
        self.load_today_data()

        # ✅ RESTAURAR TEXTO SI SE PERDIÓ
        if current_reflection and self.reflection_field:
            if not self.reflection_field.value or self.reflection_field.value.strip() != current_reflection.strip():
                self.reflection_field.value = current_reflection
                print(f"🔄 Texto restaurado")

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

                # BOTONES DE ACCIÓN MEJORADOS - LAYOUT CORREGIDO
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
                        )
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

    def on_tag_created(self, simple_tag):
        """Callback cuando se crea un tag - CORREGIDO CONTRA DUPLICADOS"""
        print(f"🏷️ === ON_TAG_CREATED MEJORADO ===")
        print(f"📝 Tag recibido: {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")

        # NUEVO: No permitir si ya guardó hoy
        if self.is_saved_today:
            self.show_error("🔒 No puedes añadir momentos - entrada ya guardada")
            return

        # Convertir SimpleTag a DynamicTag
        tag = DynamicTag.from_simple_tag(simple_tag)
        print(f"🔄 Tag convertido: {tag}")

        # ✅ VERIFICAR DUPLICADOS ANTES DE GUARDAR
        if tag.type == "positive":
            existing = any(existing_tag.name == tag.name and existing_tag.context == tag.context
                           for existing_tag in self.positive_tags)
            if existing:
                self.show_error("⚠️ Este momento ya existe")
                return
        elif tag.type == "negative":
            existing = any(existing_tag.name == tag.name and existing_tag.context == tag.context
                           for existing_tag in self.negative_tags)
            if existing:
                self.show_error("⚠️ Este momento ya existe")
                return

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

    def chat_ai(self, e):
        """Abrir chat con IA - VERSIÓN CORREGIDA que usa integración simple"""
        print("🧠 === ABRIENDO CHAT IA CON INTEGRACIÓN SIMPLE ===")
        self.page = e.page

        if not self.current_user:
            self.show_error("Usuario no autenticado")
            return

        try:
            # PASO 1: Obtener datos REALES del campo y memoria
            print(f"👤 Usuario: {self.current_user.get('name')} (ID: {self.current_user.get('id')})")

            # Obtener reflexión del campo actual
            reflection_from_field = self.reflection_field.value.strip() if self.reflection_field.value else ""

            # Obtener tags de memoria
            positive_tags_data = []
            for tag in self.positive_tags:
                positive_tags_data.append({
                    'name': tag.name,
                    'context': tag.context,
                    'emoji': tag.emoji,
                    'type': 'positive'
                })

            negative_tags_data = []
            for tag in self.negative_tags:
                negative_tags_data.append({
                    'name': tag.name,
                    'context': tag.context,
                    'emoji': tag.emoji,
                    'type': 'negative'
                })

            # Obtener worth_it de memoria
            final_worth_it = self.worth_it

            print(f"📊 DATOS PARA EL CHAT:")
            print(f"   📝 Reflexión: {'SÍ' if reflection_from_field else 'NO'} ({len(reflection_from_field)} chars)")
            print(f"   ➕ Tags positivos: {len(positive_tags_data)}")
            print(f"   ➖ Tags negativos: {len(negative_tags_data)}")
            print(f"   💭 Worth it: {final_worth_it}")

            # PASO 2: Validar que hay contenido mínimo
            total_content = len(reflection_from_field) + len(positive_tags_data) + len(negative_tags_data)

            if total_content == 0:
                self.show_error("No hay contenido del día para analizar. Escribe una reflexión o añade algunos momentos.")
                return

            if len(reflection_from_field) < 10 and total_content < 2:
                self.show_error("Añade más contenido para tener una conversación significativa con la IA.")
                return

            # PASO 3: Preparar contexto usando integración simple
            print("🔗 Preparando contexto con integración simple...")

            try:
                from services.simple_ai_integration import prepare_entry_for_chat

                # Preparar contexto
                chat_context = prepare_entry_for_chat(
                    reflection_text=reflection_from_field,
                    positive_tags=positive_tags_data,
                    negative_tags=negative_tags_data,
                    worth_it=final_worth_it,
                    user_data=self.current_user
                )

                print("✅ Contexto preparado con integración simple")

                # Verificar que el contexto es válido
                if not chat_context.get('has_content', False):
                    error_msg = chat_context.get('error', 'Error preparando contexto')
                    self.show_error(f"Error preparando chat: {error_msg}")
                    return

            except ImportError as e:
                print(f"❌ Error importando integración simple: {e}")
                self.show_error("Servicio de chat no disponible. Verifica la configuración.")
                return
            except Exception as e:
                print(f"❌ Error preparando contexto: {e}")
                self.show_error("Error técnico preparando el chat.")
                return

            # PASO 4: Guardar contexto en la app para que lo use AIChatScreen
            print("💾 Guardando contexto en la app...")

            # Crear contexto compatible con AIChatScreen
            app_chat_context = {
                'reflection': reflection_from_field,
                'positive_tags': positive_tags_data,
                'negative_tags': negative_tags_data,
                'worth_it': final_worth_it,
                'user': self.current_user,
                'prepared_context': chat_context,  # Contexto ya preparado por integración simple
                'timestamp': chat_context.get('timestamp')
            }

            # Guardar en la app
            if hasattr(self.app, 'chat_context'):
                self.app.chat_context = app_chat_context
            else:
                print("⚠️ La app no tiene atributo chat_context")

            print("✅ Contexto guardado en la app")

            # PASO 5: Mostrar resumen al usuario
            try:
                from services.simple_ai_integration import get_chat_summary
                summary = get_chat_summary(chat_context)
                print(f"📊 Resumen del chat: {summary}")
            except:
                summary = f"Reflexión, {len(positive_tags_data)} momentos positivos, {len(negative_tags_data)} momentos negativos"

            # PASO 6: Navegar al chat
            print("🛣️ Navegando a /ai_chat")
            self.page.go("/ai_chat")

            # Mostrar mensaje de éxito
            print("✅ === NAVEGACIÓN AL CHAT COMPLETADA ===")

        except Exception as ex:
            print(f"❌ ERROR CRÍTICO en chat_ai: {ex}")
            import traceback
            traceback.print_exc()
            self.show_error("Error inesperado iniciando el chat. Revisa la consola para más detalles.")

    def debug_chat_data(self):
        """Método helper para debuggear datos del chat - AÑADIR A EntryScreen"""
        print("🔍 === DEBUG DATOS PARA CHAT ===")

        if not self.current_user:
            print("❌ No hay usuario actual")
            return False

        print(f"👤 Usuario: {self.current_user.get('name')} (ID: {self.current_user.get('id')})")

        # Datos del campo
        reflection_text = self.reflection_field.value.strip() if self.reflection_field.value else ""
        print(f"📝 Reflexión en campo: {len(reflection_text)} caracteres")
        if reflection_text:
            print(f"📝 Primeros 100 chars: {reflection_text[:100]}...")

        # Datos de memoria
        print(f"➕ Tags positivos en memoria: {len(self.positive_tags)}")
        for i, tag in enumerate(self.positive_tags):
            print(f"    {i+1}. {tag.emoji} {tag.name}: {tag.context[:50]}...")

        print(f"➖ Tags negativos en memoria: {len(self.negative_tags)}")
        for i, tag in enumerate(self.negative_tags):
            print(f"    {i+1}. {tag.emoji} {tag.name}: {tag.context[:50]}...")

        print(f"💭 Worth it en memoria: {self.worth_it}")

        # Validar contenido mínimo
        total_content = len(reflection_text) + len(self.positive_tags) + len(self.negative_tags)
        print(f"📊 Total de contenido: {total_content}")

        if total_content == 0:
            print("⚠️ NO hay contenido para chat")
            return False
        elif total_content < 2 and len(reflection_text) < 10:
            print("⚠️ Contenido insuficiente para chat significativo")
            return False
        else:
            print("✅ Contenido suficiente para chat")
            return True

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
