"""
📝 Entry Screen CORREGIDA CON DEBUG - ReflectApp
Pantalla principal con logs de debug y funcionamiento correcto
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

    def __str__(self):
        return f"DynamicTag({self.emoji} {self.name} - {self.type})"

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

        # Estado de carga
        self.tags_loaded = False

        print("🏗️ EntryScreen inicializada")

    def set_user(self, user_data):
        """Establecer usuario y cargar datos del día"""
        self.current_user = user_data
        print(f"🙋‍♂️ Usuario establecido: {user_data.get('name', 'Unknown')} (ID: {user_data.get('id')})")

        # NO cargar tags aquí, se hará después de construir la vista
        self.tags_loaded = False

    def update_theme(self):
        """Actualizar tema cuando cambie"""
        old_theme = self.theme.name if self.theme else "none"
        self.theme = get_theme()
        new_theme = self.theme.name

        print(f"🎨 Actualizando tema: {old_theme} → {new_theme}")

        if self.page:
            apply_theme_to_page(self.page)
            self.page.update()

    def load_today_tags(self):
        """Cargar tags del día actual desde la base de datos"""
        print("📅 === INICIANDO CARGA DE TAGS DEL DÍA ===")

        if not self.current_user:
            print("❌ No hay usuario para cargar tags")
            return

        try:
            from services import db
            user_id = self.current_user['id']

            print(f"🔍 Cargando tags para usuario {user_id}")

            entries_today = db.get_user_entries(
                user_id=user_id,
                limit=10,
                offset=0
            )

            print(f"📄 Encontradas {len(entries_today)} entradas totales")

            # Limpiar listas actuales
            old_positive = len(self.positive_tags)
            old_negative = len(self.negative_tags)

            self.positive_tags.clear()
            self.negative_tags.clear()

            # Procesar entradas de hoy
            from datetime import date
            today = date.today().isoformat()
            print(f"📅 Buscando entradas para la fecha: {today}")

            tags_found = False
            for i, entry in enumerate(entries_today):
                entry_date = entry.get('entry_date')
                print(f"📄 Entrada {i+1}: fecha={entry_date}, id={entry.get('id')}")

                if entry_date == today:
                    print(f"✅ ¡Encontrada entrada de hoy! ID: {entry.get('id')}")

                    # Cargar reflexión si existe
                    reflection_text = entry.get('free_reflection', '')
                    if reflection_text and self.reflection_field:
                        self.reflection_field.value = reflection_text
                        print(f"📝 Reflexión cargada: {reflection_text[:50]}...")

                    # Cargar worth_it si existe
                    worth_it_value = entry.get('worth_it')
                    if worth_it_value is not None:
                        self.worth_it = worth_it_value
                        print(f"💭 Worth it cargado: {worth_it_value}")

                    # Cargar tags positivos
                    positive_tags_data = entry.get('positive_tags', [])
                    print(f"➕ Datos de tags positivos: {positive_tags_data}")

                    for j, tag_data in enumerate(positive_tags_data):
                        if isinstance(tag_data, dict):
                            tag = DynamicTag(
                                name=tag_data.get('name', f'Tag {j+1}'),
                                context=tag_data.get('context', ''),
                                tag_type="positive",
                                emoji=tag_data.get('emoji', '✨')
                            )
                            self.positive_tags.append(tag)
                            print(f"  ➕ Tag positivo creado: {tag}")
                        else:
                            print(f"  ⚠️ Tag positivo inválido: {tag_data}")

                    # Cargar tags negativos
                    negative_tags_data = entry.get('negative_tags', [])
                    print(f"➖ Datos de tags negativos: {negative_tags_data}")

                    for j, tag_data in enumerate(negative_tags_data):
                        if isinstance(tag_data, dict):
                            tag = DynamicTag(
                                name=tag_data.get('name', f'Tag {j+1}'),
                                context=tag_data.get('context', ''),
                                tag_type="negative",
                                emoji=tag_data.get('emoji', '💔')
                            )
                            self.negative_tags.append(tag)
                            print(f"  ➖ Tag negativo creado: {tag}")
                        else:
                            print(f"  ⚠️ Tag negativo inválido: {tag_data}")

                    tags_found = True
                    print(f"🎯 TAGS CARGADOS: {len(self.positive_tags)} positivos, {len(self.negative_tags)} negativos")
                    break
                else:
                    print(f"  ⏭️ Entrada de fecha diferente: {entry_date} != {today}")

            if not tags_found:
                print("ℹ️ No se encontraron entradas para hoy - día nuevo")

            print(f"📊 RESUMEN CARGA: {old_positive}→{len(self.positive_tags)} positivos, {old_negative}→{len(self.negative_tags)} negativos")
            self.tags_loaded = True
            print("📅 === FIN CARGA DE TAGS ===")

        except Exception as ex:
            print(f"❌ ERROR CRÍTICO cargando tags del día: {ex}")
            import traceback
            traceback.print_exc()

    def load_and_refresh_tags(self):
        """Cargar tags y refrescar interfaz - método público MEJORADO"""
        print("🔄 === INICIANDO LOAD AND REFRESH TAGS ===")

        if not self.current_user:
            print("❌ No hay usuario actual")
            return

        if not self.positive_tags_container or not self.negative_tags_container:
            print("❌ Contenedores de tags no están inicializados")
            print(f"   positive_tags_container: {self.positive_tags_container}")
            print(f"   negative_tags_container: {self.negative_tags_container}")
            return

        # Cargar datos
        self.load_today_tags()

        # Actualizar worth_it buttons si hay datos
        if self.worth_it is not None:
            print(f"🔘 Actualizando botones worth_it: {self.worth_it}")
            self.update_worth_it_buttons()

        # Refrescar interfaz
        print("🖼️ Iniciando refresh de interfaz...")
        self.force_refresh_tags()

        print(f"✅ === LOAD AND REFRESH COMPLETADO: {len(self.positive_tags)} positivos, {len(self.negative_tags)} negativos ===")

    def update_worth_it_buttons(self):
        """Actualizar botones worth_it con el valor cargado"""
        if not self.worth_it_buttons["yes"] or not self.worth_it_buttons["no"]:
            print("⚠️ Botones worth_it no están inicializados")
            return

        print(f"🔘 Actualizando botones worth_it para valor: {self.worth_it}")

        for btn_key, btn in self.worth_it_buttons.items():
            if (btn_key == "yes" and self.worth_it) or (btn_key == "no" and self.worth_it is False):
                btn.style.bgcolor = self.theme.positive_main if self.worth_it else self.theme.negative_main
                btn.style.color = "#FFFFFF"
                print(f"  ✅ Botón {btn_key} activado")
            else:
                btn.style.bgcolor = self.theme.surface_variant
                btn.style.color = self.theme.text_secondary
                print(f"  ⚪ Botón {btn_key} desactivado")

    def build(self):
        """Construir vista principal zen con temas"""
        print("🏗️ === CONSTRUYENDO ENTRYSCREEN ===")

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

        print(f"📦 Contenedores creados:")
        print(f"   positive_tags_container: {type(self.positive_tags_container)}")
        print(f"   negative_tags_container: {type(self.negative_tags_container)}")

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

        print("🏗️ Vista EntryScreen construida - esperando carga manual de tags")
        return view

    def refresh_positive_tags(self):
        """Actualizar visualización de tags positivos con tema"""
        print(f"🔄 === REFRESH POSITIVE TAGS (Total: {len(self.positive_tags)}) ===")

        if not self.positive_tags_container:
            print("❌ positive_tags_container no existe")
            return

        self.positive_tags_container.controls.clear()

        if not self.positive_tags:
            # Mostrar placeholder cuando no hay tags
            placeholder = ft.Text(
                "Aún no has añadido momentos positivos del día",
                size=12,
                color=self.theme.text_hint,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
            self.positive_tags_container.controls.append(placeholder)
            print("📝 Placeholder positivo añadido")
        else:
            for i, tag in enumerate(self.positive_tags):
                print(f"  ➕ Creando chip para tag {i+1}: {tag}")
                tag_chip = self.create_tag_chip(tag, "positive")
                self.positive_tags_container.controls.append(tag_chip)

        print(f"✅ Tags positivos refrescados: {len(self.positive_tags_container.controls)} controles")

        # Actualizar página si está disponible
        if hasattr(self, 'page') and self.page:
            self.page.update()
            print("🔄 Página actualizada para tags positivos")

    def refresh_negative_tags(self):
        """Actualizar visualización de tags negativos con tema"""
        print(f"🔄 === REFRESH NEGATIVE TAGS (Total: {len(self.negative_tags)}) ===")

        if not self.negative_tags_container:
            print("❌ negative_tags_container no existe")
            return

        self.negative_tags_container.controls.clear()

        if not self.negative_tags:
            # Mostrar placeholder cuando no hay tags
            placeholder = ft.Text(
                "Aún no has añadido momentos negativos del día",
                size=12,
                color=self.theme.text_hint,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
            self.negative_tags_container.controls.append(placeholder)
            print("📝 Placeholder negativo añadido")
        else:
            for i, tag in enumerate(self.negative_tags):
                print(f"  ➖ Creando chip para tag {i+1}: {tag}")
                tag_chip = self.create_tag_chip(tag, "negative")
                self.negative_tags_container.controls.append(tag_chip)

        print(f"✅ Tags negativos refrescados: {len(self.negative_tags_container.controls)} controles")

        # Actualizar página si está disponible
        if hasattr(self, 'page') and self.page:
            self.page.update()
            print("🔄 Página actualizada para tags negativos")

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
        """Callback cuando se crea un tag desde NewTagScreen"""
        print(f"🏷️ === ON_TAG_CREATED LLAMADO ===")
        print(f"📝 Tag recibido: {simple_tag.emoji} {simple_tag.name} ({simple_tag.category})")
        print(f"📝 Reason: {simple_tag.reason}")

        # Convertir SimpleTag a DynamicTag
        tag = DynamicTag.from_simple_tag(simple_tag)
        print(f"🔄 Tag convertido: {tag}")

        # Añadir a la lista correspondiente
        if tag.type == "positive":
            self.positive_tags.append(tag)
            print(f"➕ Añadido a positive_tags. Total actual: {len(self.positive_tags)}")
            print(f"➕ Lista completa positiva: {[str(t) for t in self.positive_tags]}")
        elif tag.type == "negative":
            self.negative_tags.append(tag)
            print(f"➖ Añadido a negative_tags. Total actual: {len(self.negative_tags)}")
            print(f"➖ Lista completa negativa: {[str(t) for t in self.negative_tags]}")

        # Forzar actualización INMEDIATA de la interfaz
        print("🔄 Iniciando force_refresh_tags INMEDIATO...")
        self.force_refresh_tags()

        self.show_success(f"✅ Momento {tag.type} '{tag.name}' añadido")
        print(f"🏷️ === ON_TAG_CREATED COMPLETADO ===")

    def force_refresh_tags(self):
        """Forzar actualización visual de todos los tags"""
        print("🔄 === FORCE REFRESH TAGS ===")

        try:
            print(f"📊 Estado actual: {len(self.positive_tags)} positivos, {len(self.negative_tags)} negativos")

            print("🔄 Refrescando tags positivos...")
            self.refresh_positive_tags()

            print("🔄 Refrescando tags negativos...")
            self.refresh_negative_tags()

            print("✅ === FORCE REFRESH COMPLETADO ===")
        except Exception as e:
            print(f"❌ ERROR en force_refresh_tags: {e}")
            import traceback
            traceback.print_exc()

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
            print(f"✅ Tag eliminado. Quedan {len(self.positive_tags)} tags positivos")

    def remove_negative_tag(self, tag):
        """Eliminar tag negativo"""
        print(f"🗑️ Eliminando tag negativo: {tag}")
        if tag in self.negative_tags:
            self.negative_tags.remove(tag)
            self.refresh_negative_tags()
            print(f"✅ Tag eliminado. Quedan {len(self.negative_tags)} tags negativos")

    def set_worth_it(self, value, e):
        """Establecer si mereció la pena el día"""
        print(f"💭 === SET WORTH IT: {value} ===")
        self.page = e.page
        self.worth_it = value

        # Actualizar estilos de botones con tema
        self.update_worth_it_buttons()

        if self.page:
            self.page.update()

        print(f"💭 Worth it establecido: {value}")

    def save_entry(self, e):
        """Guardar entrada zen"""
        print("💾 === SAVE ENTRY INICIADO ===")
        self.page = e.page

        reflection_text = self.reflection_field.value.strip() if self.reflection_field.value else ""

        print(f"📝 Reflexión a guardar: '{reflection_text[:100]}...'")
        print(f"➕ Tags positivos a guardar: {len(self.positive_tags)}")
        print(f"➖ Tags negativos a guardar: {len(self.negative_tags)}")
        print(f"💭 Worth it a guardar: {self.worth_it}")

        if not reflection_text:
            print("❌ Reflexión vacía")
            self.show_error("Escribe algo en tu reflexión antes de guardar")
            return

        try:
            from services import db

            if self.current_user:
                user_id = self.current_user['id']
                print(f"💾 Guardando entrada para usuario: {user_id}")

                # DEBUG: Mostrar detalles de tags antes de guardar
                for i, tag in enumerate(self.positive_tags):
                    print(f"  ➕ Tag positivo {i+1}: {tag.emoji} {tag.name} - {tag.context[:30]}...")
                for i, tag in enumerate(self.negative_tags):
                    print(f"  ➖ Tag negativo {i+1}: {tag.emoji} {tag.name} - {tag.context[:30]}...")

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
                else:
                    print("❌ Error: entry_id es None")
                    self.show_error("Error al guardar en base de datos")
            else:
                print("❌ Error: No hay usuario actual")
                self.show_error("Usuario no autenticado")

        except Exception as ex:
            print(f"❌ ERROR CRÍTICO guardando: {ex}")
            import traceback
            traceback.print_exc()
            self.show_error("Error del sistema")

        print("💾 === SAVE ENTRY FINALIZADO ===")

    def chat_ai(self, e):
        """Iniciar chat con IA"""
        print("🤖 === CHAT IA INICIADO ===")
        self.page = e.page

        reflection_text = self.reflection_field.value.strip() if self.reflection_field.value else ""

        if not reflection_text:
            print("❌ No hay reflexión para el chat")
            self.show_error("Escribe algo para charlar con la IA")
            return

        try:
            print("🤖 Generando resumen con IA...")
            print(f"📝 Reflexión: {reflection_text[:50]}...")
            print(f"➕ Tags positivos: {len(self.positive_tags)}")
            print(f"➖ Tags negativos: {len(self.negative_tags)}")
            print(f"💭 Worth it: {self.worth_it}")

            summary = get_daily_summary(
                reflection=reflection_text,
                positive_tags=self.positive_tags,
                negative_tags=self.negative_tags,
                worth_it=self.worth_it
            )

            print(f"🤖 Resumen generado: {summary[:100]}...")
            self.show_daily_summary_dialog(summary)

        except Exception as ex:
            print(f"❌ Error en chat IA: {ex}")
            import traceback
            traceback.print_exc()
            self.show_error("Error iniciando chat")

        print("🤖 === CHAT IA FINALIZADO ===")

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
        """Mostrar éxito zen con tema"""
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