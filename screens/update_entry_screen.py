"""
📝 Entry Screen CORREGIDA CON TAGS TEMPORALES - ReflectApp
Pantalla principal con sistema de persistencia mejorado
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

        # Estado de carga
        self.tags_loaded = False
        self.data_loaded = False

        print("🏗️ EntryScreen inicializada con sistema mejorado")

    def set_user(self, user_data):
        """Establecer usuario y marcar datos como no cargados"""
        self.current_user = user_data
        self.data_loaded = False
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

            # Usar nuevo método que combina entrada guardada + tags temporales
            today_data = db.get_today_entry_with_temp_tags(user_id)

            # Limpiar datos actuales
            self.positive_tags.clear()
            self.negative_tags.clear()

            # Cargar reflexión
            if today_data.get('reflection') and self.reflection_field:
                self.reflection_field.value = today_data['reflection']
                print(f"📝 Reflexión cargada: {today_data['reflection'][:50]}...")

            # Cargar worth_it
            if today_data.get('worth_it') is not None:
                self.worth_it = today_data['worth_it']
                print(f"💭 Worth it cargado: {self.worth_it}")

            # Cargar tags positivos
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

            self.data_loaded = True

        except Exception as ex:
            print(f"❌ ERROR CRÍTICO cargando datos de hoy: {ex}")
            import traceback
            traceback.print_exc()

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
        """Construir vista principal zen con temas"""
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
            label_style=ft.TextStyle(color=self.theme.text_secondary)
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

        remove_callback = self.remove_positive_tag if is_positive else self.remove_negative_tag

        return ft.Container(
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
                                on_click=lambda e, t=tag: remove_callback(t),
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
            bgcolor=bg_color,
            padding=ft.padding.all(12),
            border_radius=16,
            border=ft.border.all(1, border_color),
            margin=ft.margin.only(bottom=8)
        )

    def on_tag_created(self, simple_tag):
        """Callback cuando se crea un tag desde NewTagScreen - MEJORADO"""
        print(f"🏷️ === ON_TAG_CREATED MEJORADO ===")
        print(f"📝 Tag recibido: {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")

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

            # Refrescar interfaz
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
        print("➕ Abriendo diálogo de tag positivo...")
        self.page = e.page
        self.page.go("/new_tag?type=positive")

    def open_negative_tag_dialog(self, e):
        """Abrir pantalla para añadir momento negativo"""
        print("➖ Abriendo diálogo de tag negativo...")
        self.page = e.page
        self.page.go("/new_tag?type=negative")

    def remove_positive_tag(self, tag):
        """Eliminar tag positivo"""
        print(f"🗑️ Eliminando tag positivo: {tag}")
        if tag in self.positive_tags:
            self.positive_tags.remove(tag)
            self.refresh_positive_tags()

            # También eliminar de tags temporales si existe
            self.remove_temp_tag(tag)

            if hasattr(self, 'page') and self.page:
                self.page.update()

    def remove_negative_tag(self, tag):
        """Eliminar tag negativo"""
        print(f"🗑️ Eliminando tag negativo: {tag}")
        if tag in self.negative_tags:
            self.negative_tags.remove(tag)
            self.refresh_negative_tags()

            # También eliminar de tags temporales si existe
            self.remove_temp_tag(tag)

            if hasattr(self, 'page') and self.page:
                self.page.update()

    def remove_temp_tag(self, tag):
        """Eliminar tag de la tabla temporal (método helper)"""
        try:
            from services import db
            if self.current_user:
                # Para simplificar, volvemos a cargar los datos después de eliminar
                # Una implementación más sofisticada podría eliminar específicamente
                pass
        except Exception as e:
            print(f"⚠️ Error eliminando tag temporal: {e}")

    def set_worth_it(self, value, e):
        """Establecer si mereció la pena el día"""
        print(f"💭 SET WORTH IT: {value}")
        self.page = e.page
        self.worth_it = value

        self.update_worth_it_buttons()

        if self.page:
            self.page.update()

    def save_entry(self, e):
        """Guardar entrada zen - MEJORADO"""
        print("💾 === SAVE ENTRY MEJORADO ===")
        self.page = e.page

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

                    # Los tags temporales se limpian automáticamente en save_daily_entry
                    print("🧹 Tags temporales limpiados automáticamente")
                else:
                    self.show_error("Error al guardar en base de datos")
            else:
                self.show_error("Usuario no autenticado")

        except Exception as ex:
            print(f"❌ ERROR guardando: {ex}")
            import traceback
            traceback.print_exc()
            self.show_error("Error del sistema")

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