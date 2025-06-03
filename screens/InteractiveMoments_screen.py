"""
🎮 Interactive Moments Screen - CENTRADO PERFECTO Y LAYOUT MÓVIL CORREGIDO
✅ ARREGLADO: Centrado perfecto de emojis y textos en burbujas
✅ ARREGLADO: Padding superior para evitar chocar con barra de notificaciones
✅ ARREGLADO: Espaciado optimizado para móvil
"""

import flet as ft
from datetime import datetime, time
from typing import List, Dict, Any, Optional, Callable
import calendar
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

# ✅ SimpleTag definido localmente para evitar import circular
class SimpleTag:
    """Clase simple para representar un tag"""
    def __init__(self, emoji, category, name, reason):
        self.emoji = emoji
        self.category = category  # "positive" o "negative"
        self.name = name
        self.reason = reason
        self.type = category  # Para compatibilidad

class InteractiveMoment:
    """Clase para representar un momento interactivo"""
    def __init__(self, emoji: str, text: str, moment_type: str,
                 intensity: int = 5, category: str = "general", time_str: Optional[str] = None):
        self.id = int(datetime.now().timestamp() * 1000)  # Timestamp único
        self.emoji = emoji
        self.text = text
        self.type = moment_type  # "positive" o "negative"
        self.intensity = intensity  # 1-10
        self.category = category
        self.time = time_str or datetime.now().strftime("%H:%M")
        self.timestamp = datetime.now()

    def to_simple_tag(self):
        """Convertir a SimpleTag para compatibilidad"""
        return SimpleTag(
            emoji=self.emoji,
            category=self.type,
            name=f"{self.text}",
            reason=f"Momento {self.category} de intensidad {self.intensity} a las {self.time}"
        )

    def to_dict(self):
        """Convertir a diccionario para almacenar en base de datos"""
        return {
            'id': str(self.id),
            'emoji': self.emoji,
            'text': self.text,
            'type': self.type,
            'intensity': self.intensity,
            'category': self.category,
            'time': self.time,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """Crear InteractiveMoment desde diccionario"""
        moment = cls(
            emoji=data.get('emoji', ''),
            text=data.get('text', ''),
            moment_type=data.get('type', 'positive'),
            intensity=int(data.get('intensity', 5)),
            category=data.get('category', 'general'),
            time_str=data.get('time', '00:00')
        )
        moment.id = int(data.get('id', moment.id))
        if 'timestamp' in data:
            try:
                moment.timestamp = datetime.fromisoformat(data['timestamp'])
            except:
                moment.timestamp = datetime.now()
        return moment

class InteractiveMomentsScreen:
    """Pantalla Interactive Moments - CENTRADO PERFECTO Y LAYOUT MÓVIL CORREGIDO"""

    def __init__(self, app=None, on_moments_created: Callable = None, on_go_back: Callable = None):
        self.app = app
        self.on_moments_created = on_moments_created
        self.on_go_back = on_go_back

        # Estado principal
        self.page = None
        self.current_user = None
        self.theme = get_theme()
        self.active_mode = "quick"  # quick, mood, timeline, templates

        # Datos
        self.moments = []

        # Estado de los modos
        self.current_intensity = 5
        self.selected_hour = datetime.now().hour
        self.quick_text_field = None
        self.timeline_text_field = None
        self.intensity_slider = None
        self.intensity_value_text = None  # ✅ Referencia al texto del valor

        # Contenedores
        self.main_container = None
        self.summary_container = None
        self.moments_list_container = None  # ✅ Lista de momentos

        # Estado de persistencia CORREGIDO
        self.data_loaded = False
        self.auto_save_enabled = True

        print("🎮 InteractiveMomentsScreen CENTRADO PERFECTO Y LAYOUT MÓVIL CORREGIDO inicializada")

    def set_user(self, user_data):
        """Establecer usuario actual"""
        self.current_user = user_data
        self.data_loaded = False
        print(f"👤 Usuario establecido: {user_data.get('name')} (ID: {user_data.get('id')})")
        self.load_user_moments()

    def load_user_moments(self):
        """✅ CORREGIDO: Cargar momentos guardados del usuario desde la base de datos"""
        if not self.current_user:
            print("⚠️ No hay usuario para cargar momentos")
            return

        try:
            from services import db
            user_id = self.current_user['id']

            print(f"📚 Cargando momentos interactivos para usuario {user_id}")

            # ✅ Usar método corregido de la clase
            moments_data = db.get_interactive_moments_today(user_id)

            self.moments.clear()
            for moment_dict in moments_data:
                try:
                    moment = InteractiveMoment.from_dict(moment_dict)
                    self.moments.append(moment)
                except Exception as e:
                    print(f"⚠️ Error parseando momento: {e}")
                    continue

            print(f"✅ Cargados {len(self.moments)} momentos interactivos")
            self.data_loaded = True

            if self.page and self.summary_container:
                self.refresh_all_containers()

        except Exception as e:
            print(f"❌ Error cargando momentos del usuario: {e}")
            import traceback
            traceback.print_exc()

    def save_moment_to_db(self, moment):
        """✅ CORREGIDO: Guardar momento individual en la base de datos"""
        if not self.current_user:
            print("⚠️ No hay usuario para guardar momento")
            return False

        try:
            from services import db
            user_id = self.current_user['id']

            moment_id = db.save_interactive_moment(
                user_id=user_id,
                moment_data=moment.to_dict()
            )

            if moment_id:
                print(f"💾 Momento guardado en DB: {moment.emoji} {moment.text} (ID: {moment_id})")
                return True
            else:
                print("❌ Error guardando momento en DB")
                return False

        except Exception as e:
            print(f"❌ Error guardando momento: {e}")
            return False

    def auto_save_moment(self, moment):
        """Auto-guardar momento si está habilitado"""
        if self.auto_save_enabled:
            success = self.save_moment_to_db(moment)
            if success:
                print(f"🔄 Auto-guardado: {moment.emoji} {moment.text}")
            return success
        return True

    def build(self):
        """✅ COMPLETAMENTE CORREGIDO: Layout móvil con padding superior y centrado perfecto"""
        self.theme = get_theme()

        # ✅ CORREGIDO: Header con más espacio superior para móvil
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # ✅ Botones de acción
        action_buttons = ft.Row([
            ft.Container(
                content=ft.Text("🎨", size=16),
                on_click=self.go_to_theme_selector,
                bgcolor="#FFFFFF20",
                border_radius=8,
                padding=ft.padding.all(8),
                tooltip="Temas"
            ),
            ft.Container(
                content=ft.Text("📅", size=16),
                on_click=self.go_to_calendar,
                bgcolor="#FFFFFF20",
                border_radius=8,
                padding=ft.padding.all(8),
                tooltip="Calendario"
            ),
            ft.Container(
                content=ft.Text("🔔", size=16),
                on_click=self.go_to_mobile_notification_settings,
                bgcolor="#FFFFFF20",
                border_radius=8,
                padding=ft.padding.all(8),
                tooltip="Notificaciones"
            )
        ], spacing=8)

        user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'

        # ✅ CORREGIDO: Header con padding superior para evitar barra de notificaciones
        header = ft.Container(
            content=ft.Column([
                # ✅ NUEVO: Espaciador para barra de notificaciones móvil
                ft.Container(height=20),  # Espacio para status bar

                ft.Row([
                    back_button,
                    ft.Column([
                        ft.Text(
                            f"🎮 Momentos",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color="#FFFFFF",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            user_name,
                            size=12,
                            color="#FFFFFF80",
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2, expand=True),
                    action_buttons
                ])
            ]),
            padding=ft.padding.only(left=12, right=12, bottom=12, top=8),  # ✅ CORREGIDO: Menos padding arriba
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=self.theme.gradient_header
            ),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )

        # ✅ Descripción compacta con estadísticas en tiempo real
        self.stats_text_container = ft.Container(
            content=self._build_stats_text(),
            padding=ft.padding.only(top=16, bottom=8),  # ✅ CORREGIDO: Más espacio arriba
            alignment=ft.alignment.center
        )

        # ✅ Selector de modos compacto
        mode_selector = self.build_mode_selector_compact()

        # Contenedor principal dinámico
        self.main_container = ft.Container(
            content=self.build_active_mode(),
            expand=True
        )

        # ✅ Lista de momentos añadidos
        self.moments_list_container = ft.Container(
            content=self.build_moments_list()
        )

        # Resumen de momentos
        self.summary_container = ft.Container(
            content=self.build_moments_summary()
        )

        # ✅ CORREGIDO: Vista completa con padding superior adecuado
        content = ft.Column([
            self.stats_text_container,
            mode_selector,
            ft.Container(height=12),
            self.main_container,
            ft.Container(height=12),
            self.moments_list_container,
            ft.Container(height=12),
            self.summary_container,
            ft.Container(height=20)  # ✅ NUEVO: Espacio inferior para navegación móvil
        ], scroll=ft.ScrollMode.AUTO, spacing=0, expand=True)

        view = ft.View(
            "/interactive_moments",
            [header, ft.Container(content=content, padding=ft.padding.all(12), expand=True)],
            bgcolor=self.theme.primary_bg, padding=0, spacing=0
        )

        return view

    def _build_stats_text(self):
        """✅ Construir texto de estadísticas dinámico"""
        stats_text = ""
        if self.moments:
            positive_count = len([m for m in self.moments if m.type == "positive"])
            negative_count = len([m for m in self.moments if m.type == "negative"])
            stats_text = f" • {positive_count}+ {negative_count}- ({len(self.moments)} total)"

        return ft.Text(
            f"Captura tus momentos{stats_text}",
            size=12,
            color=self.theme.text_secondary,
            text_align=ft.TextAlign.CENTER
        )

    def build_mode_selector_compact(self):
        """✅ Selector de modos compacto para móvil"""
        modes = [
            {"id": "quick", "emoji": "⚡", "name": "Quick"},
            {"id": "mood", "emoji": "🎭", "name": "Mood"},
            {"id": "timeline", "emoji": "⏰", "name": "Timeline"},
            {"id": "templates", "emoji": "🎯", "name": "Templates"}
        ]

        # ✅ En filas de 2 para móvil
        mode_rows = []
        for i in range(0, len(modes), 2):
            row_modes = []
            for j in range(2):
                if i + j < len(modes):
                    mode = modes[i + j]
                    is_active = self.active_mode == mode["id"]

                    button = ft.Container(
                        content=ft.Column([
                            ft.Text(mode["emoji"], size=20),
                            ft.Text(mode["name"], size=12, weight=ft.FontWeight.W_600,
                                    color=self.theme.text_primary)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        width=140,
                        height=70,
                        padding=ft.padding.all(12),
                        border_radius=12,
                        bgcolor=self.theme.accent_primary + "30" if is_active else self.theme.surface,
                        border=ft.border.all(2 if is_active else 1,
                                             self.theme.accent_primary if is_active else self.theme.border_color),
                        on_click=lambda e, mode_id=mode["id"]: self.switch_mode(mode_id)
                    )
                    row_modes.append(button)

            if row_modes:
                mode_rows.append(ft.Row(row_modes, spacing=8, alignment=ft.MainAxisAlignment.CENTER))

        return ft.Column(mode_rows, spacing=8)

    def switch_mode(self, mode_id: str):
        """Cambiar entre modos"""
        print(f"🔄 Cambiando a modo: {mode_id}")
        self.active_mode = mode_id

        if self.main_container:
            self.main_container.content = self.build_active_mode()

        if self.page:
            self.page.update()

    def build_active_mode(self):
        """Construir modo activo"""
        if self.active_mode == "quick":
            return self.build_quick_add_mode()
        elif self.active_mode == "mood":
            return self.build_mood_bubbles_mode()
        elif self.active_mode == "timeline":
            return self.build_timeline_mode()
        elif self.active_mode == "templates":
            return self.build_templates_mode()
        return ft.Container()

    # ===============================
    # MODO 1: QUICK ADD
    # ===============================
    def build_quick_add_mode(self):
        """✅ Modo Quick Add con emojis ampliados"""

        # ✅ Campo de texto mejorado
        self.quick_text_field = ft.TextField(
            hint_text="¿Qué pasó?",
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(12),
            text_style=ft.TextStyle(color=self.theme.text_primary),
            height=50
        )

        # ✅ Más frases rápidas
        quick_phrases = [
            "Me sentí increíble", "Fue genial", "Muy estresante", "Me frustré",
            "Logré algo importante", "Fue relajante", "Me preocupé mucho", "Estaba ansioso"
        ]

        phrase_buttons = []
        for i in range(0, len(quick_phrases), 2):
            row_phrases = []
            for j in range(2):
                if i + j < len(quick_phrases):
                    phrase = quick_phrases[i + j]
                    btn = ft.Container(
                        content=ft.Text(phrase, size=11, color=self.theme.text_secondary,
                                        text_align=ft.TextAlign.CENTER),
                        padding=ft.padding.symmetric(horizontal=8, vertical=6),
                        border_radius=16,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        on_click=lambda e, p=phrase: self.set_quick_text(p),
                        expand=True
                    )
                    row_phrases.append(btn)

            if row_phrases:
                phrase_buttons.append(ft.Row(row_phrases, spacing=6))

        # ✅ Emojis organizados por categorías
        emoji_sections = []

        # ✅ Sección positiva AMPLIADA
        positive_emojis = [
            '😊', '🎉', '💪', '☕', '🎵', '🤗',
            '😄', '🥳', '💖', '🌟', '🚀', '🎯'
        ]
        positive_section = self.build_compact_emoji_section(
            "✨ Positivos", positive_emojis, "positive", self.theme.positive_main
        )
        emoji_sections.append(positive_section)

        # ✅ Sección negativa AMPLIADA
        negative_emojis = [
            '😰', '😔', '😤', '💼', '😫', '🤯',
            '😩', '🙄', '😞', '😣', '🤦', '💔'
        ]
        negative_section = self.build_compact_emoji_section(
            "🌧️ Difíciles", negative_emojis, "negative", self.theme.negative_main
        )
        emoji_sections.append(negative_section)

        return ft.Column([
            # ✅ Campo de texto
            create_themed_container(content=self.quick_text_field, theme=self.theme),

            ft.Container(height=8),

            # ✅ Frases rápidas
            create_themed_container(
                content=ft.Column([
                    ft.Text("⚡ Frases:", size=12, weight=ft.FontWeight.W_500,
                            color=self.theme.text_secondary),
                    ft.Container(height=6),
                    ft.Column(phrase_buttons, spacing=6)
                ]),
                theme=self.theme
            ),

            ft.Container(height=8),

            # ✅ Emojis
            ft.Column(emoji_sections, spacing=8)
        ])

    def build_compact_emoji_section(self, title: str, emojis: List[str], moment_type: str, color: str):
        """✅ CENTRADO PERFECTO: Sección de emojis con alineación correcta"""

        # ✅ Grid de emojis en filas de 6 con CENTRADO PERFECTO
        emoji_rows = []
        for i in range(0, len(emojis), 6):
            row_emojis = []
            for j in range(6):
                if i + j < len(emojis):
                    emoji = emojis[i + j]
                    btn = ft.Container(
                        content=ft.Text(
                            emoji,
                            size=20,
                            text_align=ft.TextAlign.CENTER  # ✅ CENTRADO HORIZONTAL
                        ),
                        width=40,
                        height=40,
                        border_radius=8,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        alignment=ft.alignment.center,  # ✅ CENTRADO TOTAL
                        on_click=lambda e, em=emoji: self.add_quick_moment_safe(em, moment_type, "quick")
                    )
                    row_emojis.append(btn)

            if row_emojis:
                emoji_rows.append(ft.Row(row_emojis, spacing=6, alignment=ft.MainAxisAlignment.CENTER))

        content = ft.Column([
            ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=color),
            ft.Container(height=8),
            ft.Column(emoji_rows, spacing=6)
        ])

        return create_themed_container(content=content, theme=self.theme)

    def set_quick_text(self, text: str):
        """Establecer texto rápido"""
        if self.quick_text_field:
            self.quick_text_field.value = text
            if self.page:
                self.page.update()

    def add_quick_moment_safe(self, emoji: str, moment_type: str, category: str):
        """Añadir momento rápido con verificación"""
        if not self.quick_text_field or not self.quick_text_field.value or not self.quick_text_field.value.strip():
            self.show_message("⚠️ Escribe qué pasó antes de seleccionar emoji", is_error=True)
            return

        self.add_quick_moment(emoji, moment_type, category)

    def add_quick_moment(self, emoji: str, moment_type: str, category: str):
        """✅ CORREGIDO: Añadir momento rápido con actualización completa"""
        moment = InteractiveMoment(
            emoji=emoji, text=self.quick_text_field.value.strip(),
            moment_type=moment_type, intensity=7 if moment_type == "positive" else 6,
            category=category
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.quick_text_field.value = ""
            self.show_message(f"✅ {emoji} {moment.text} añadido")

            # ✅ CORREGIDO: Actualizar TODOS los contenedores
            self.refresh_all_containers()

            if self.page:
                self.page.update()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # MOOD BUBBLES - ✅ CENTRADO PERFECTO CORREGIDO
    # ===============================
    def build_mood_bubbles_mode(self):
        """✅ COMPLETAMENTE CORREGIDO: Modo Mood Bubbles con centrado perfecto"""

        # ✅ Slider de intensidad CORREGIDO
        intensity_section = self.build_compact_intensity_slider()

        # ✅ Más burbujas de humor
        bubble_options = [
            {'emoji': '😊', 'text': 'Alegre', 'type': 'positive'},
            {'emoji': '🎉', 'text': 'Emocionado', 'type': 'positive'},
            {'emoji': '😌', 'text': 'Tranquilo', 'type': 'positive'},
            {'emoji': '💪', 'text': 'Motivado', 'type': 'positive'},
            {'emoji': '🤗', 'text': 'Amoroso', 'type': 'positive'},
            {'emoji': '🌟', 'text': 'Inspirado', 'type': 'positive'},
            {'emoji': '😰', 'text': 'Estresado', 'type': 'negative'},
            {'emoji': '😔', 'text': 'Triste', 'type': 'negative'},
            {'emoji': '😤', 'text': 'Frustrado', 'type': 'negative'},
            {'emoji': '😫', 'text': 'Agotado', 'type': 'negative'},
            {'emoji': '🤯', 'text': 'Abrumado', 'type': 'negative'},
            {'emoji': '😞', 'text': 'Desanimado', 'type': 'negative'}
        ]

        # ✅ CORREGIDO: Grid de burbujas en filas de 2 con CENTRADO PERFECTO
        bubble_rows = []
        for i in range(0, len(bubble_options), 2):
            row_bubbles = []
            for j in range(2):
                if i + j < len(bubble_options):
                    bubble = bubble_options[i + j]
                    bubble_widget = self.create_compact_mood_bubble(bubble)
                    row_bubbles.append(bubble_widget)

            if row_bubbles:
                bubble_rows.append(ft.Row(
                    row_bubbles,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # ✅ CAMBIADO: SPACE_EVENLY para mejor distribución
                    spacing=12
                ))

        bubbles_container = create_themed_container(
            content=ft.Column([
                                  ft.Text("🫧 Toca una emoción", size=14, weight=ft.FontWeight.W_600,
                                          color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                                  ft.Container(height=12)
                              ] + bubble_rows, spacing=12),
            theme=self.theme
        )

        return ft.Column([
            intensity_section,
            ft.Container(height=12),
            bubbles_container
        ])

    def build_compact_intensity_slider(self):
        """✅ COMPLETAMENTE CORREGIDO: Slider de intensidad que SÍ actualiza el número"""
        self.intensity_slider = ft.Slider(
            min=1, max=10, value=self.current_intensity, divisions=9,
            on_change=self.on_intensity_change,  # ✅ CORREGIDO: Callback funcionando
            active_color=self.get_intensity_color(self.current_intensity),
            thumb_color=self.get_intensity_color(self.current_intensity)
        )

        # ✅ NUEVO: Texto del valor con referencia guardada
        self.intensity_value_text = ft.Text(
            f"{int(self.current_intensity)}/10",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=self.get_intensity_color(self.current_intensity),
            text_align=ft.TextAlign.CENTER
        )

        return create_themed_container(
            content=ft.Column([
                ft.Text("🎚️ Intensidad", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                ft.Container(height=8),

                # ✅ Slider compacto
                ft.Row([
                    ft.Text("😐", size=20),
                    ft.Container(content=self.intensity_slider, expand=True),
                    ft.Text("🤯", size=20)
                ]),

                ft.Container(height=8),

                # ✅ CORREGIDO: Valor que SÍ se actualiza
                self.intensity_value_text
            ]), theme=self.theme
        )

    def create_compact_mood_bubble(self, bubble_data):
        """✅ PERFECTO CENTRADO CORREGIDO: Burbuja de emoción con alineación perfecta"""
        is_positive = bubble_data["type"] == "positive"
        base_color = self.theme.positive_main if is_positive else self.theme.negative_main
        light_color = self.theme.positive_light if is_positive else self.theme.negative_light

        bubble = ft.Container(
            content=ft.Column([
                # ✅ CENTRADO PERFECTO: Emoji con todos los tipos de centrado
                ft.Container(
                    content=ft.Text(
                        bubble_data["emoji"],
                        size=28,
                        text_align=ft.TextAlign.CENTER,  # ✅ Centrado horizontal del texto
                        color=self.theme.text_primary
                    ),
                    alignment=ft.alignment.center,  # ✅ Centrado del contenedor
                    height=40  # ✅ Altura fija para consistencia
                ),

                ft.Container(height=4),

                # ✅ CENTRADO PERFECTO: Texto con alineación correcta
                ft.Container(
                    content=ft.Text(
                        bubble_data["text"],
                        size=12,
                        weight=ft.FontWeight.W_500,
                        color=self.theme.text_primary,
                        text_align=ft.TextAlign.CENTER  # ✅ Centrado horizontal del texto
                    ),
                    alignment=ft.alignment.center,  # ✅ Centrado del contenedor
                    height=20  # ✅ Altura fija para consistencia
                ),
            ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # ✅ Centrado horizontal de la columna
                alignment=ft.MainAxisAlignment.CENTER,  # ✅ Centrado vertical de la columna
                spacing=0  # ✅ Sin espacios extra que desalineen
            ),
            width=140,   # ✅ AUMENTADO: Más ancho para que se vea mejor
            height=90,   # ✅ Mantener altura
            padding=ft.padding.all(8),  # ✅ REDUCIDO: Menos padding interno
            border_radius=16,
            bgcolor=light_color,
            border=ft.border.all(2, base_color + "50"),
            on_click=lambda e, bubble=bubble_data: self.create_mood_moment(bubble),
            alignment=ft.alignment.center  # ✅ CENTRADO TOTAL del contenedor
        )

        return bubble

    def on_intensity_change(self, e):
        """✅ COMPLETAMENTE CORREGIDO: Callback cuando cambia intensidad"""
        self.current_intensity = e.control.value
        new_color = self.get_intensity_color(self.current_intensity)

        # ✅ Actualizar colores del slider
        e.control.active_color = new_color
        e.control.thumb_color = new_color

        # ✅ CORREGIDO: Actualizar el texto del valor
        if self.intensity_value_text:
            self.intensity_value_text.value = f"{int(self.current_intensity)}/10"
            self.intensity_value_text.color = new_color

        print(f"🎚️ Intensidad cambiada a: {int(self.current_intensity)}")

        if self.page:
            self.page.update()

    def get_intensity_color(self, intensity):
        """Color según intensidad"""
        if intensity <= 3:
            return self.theme.negative_main
        elif intensity <= 7:
            return "#F59E0B"  # Amarillo/naranja
        else:
            return self.theme.positive_main

    def create_mood_moment(self, bubble_data):
        """✅ CORREGIDO: Crear momento desde burbuja con actualización completa"""
        moment = InteractiveMoment(
            emoji=bubble_data["emoji"], text=bubble_data["text"],
            moment_type=bubble_data["type"], intensity=int(self.current_intensity),
            category="mood"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.show_message(f"✅ {bubble_data['emoji']} {bubble_data['text']} añadido")

            # ✅ CORREGIDO: Actualizar TODOS los contenedores
            self.refresh_all_containers()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # TIMELINE Y TEMPLATES - SIMPLIFICADOS PERO CORREGIDOS
    # ===============================
    def build_timeline_mode(self):
        """✅ Timeline simplificado para móvil"""
        # ✅ Selector de hora simplificado
        current_hour = datetime.now().hour
        hours_around = [max(0, current_hour-2), max(0, current_hour-1), current_hour,
                        min(23, current_hour+1), min(23, current_hour+2)]

        hour_buttons = []
        for hour in hours_around:
            is_selected = hour == self.selected_hour
            btn = ft.Container(
                content=ft.Text(f"{hour:02d}:00", size=12, color=self.theme.text_primary,
                                text_align=ft.TextAlign.CENTER),
                width=60, height=35, border_radius=8,
                bgcolor=self.theme.accent_primary + "30" if is_selected else self.theme.surface,
                border=ft.border.all(1, self.theme.accent_primary if is_selected else self.theme.border_color),
                alignment=ft.alignment.center,
                on_click=lambda e, h=hour: self.select_hour(h)
            )
            hour_buttons.append(btn)

        # ✅ Formulario compacto
        self.timeline_text_field = ft.TextField(
            hint_text="¿Qué pasó en esta hora?",
            border_radius=12, bgcolor=self.theme.surface,
            content_padding=ft.padding.all(12), height=50
        )

        buttons_row = ft.Row([
            ft.ElevatedButton("✨ Positivo", on_click=lambda e: self.add_timeline_moment("positive"),
                              style=ft.ButtonStyle(bgcolor=self.theme.positive_main, color="#FFFFFF"), expand=True),
            ft.Container(width=8),
            ft.ElevatedButton("🌧️ Difícil", on_click=lambda e: self.add_timeline_moment("negative"),
                              style=ft.ButtonStyle(bgcolor=self.theme.negative_main, color="#FFFFFF"), expand=True)
        ])

        return ft.Column([
            create_themed_container(
                content=ft.Column([
                    ft.Text("⏰ Selecciona hora", size=14, weight=ft.FontWeight.W_600, color=self.theme.text_primary),
                    ft.Container(height=8),
                    ft.Row(hour_buttons, spacing=8, alignment=ft.MainAxisAlignment.CENTER)
                ]), theme=self.theme
            ),
            ft.Container(height=12),
            create_themed_container(
                content=ft.Column([
                    self.timeline_text_field,
                    ft.Container(height=12),
                    buttons_row
                ]), theme=self.theme
            )
        ])

    def build_templates_mode(self):
        """✅ Templates simplificados para móvil con CENTRADO CORREGIDO"""
        templates = [
            {"emoji": "💪", "text": "Ejercicio energizante", "type": "positive"},
            {"emoji": "☕", "text": "Café con amigo", "type": "positive"},
            {"emoji": "🎯", "text": "Tarea completada", "type": "positive"},
            {"emoji": "📚", "text": "Aprendizaje nuevo", "type": "positive"},
            {"emoji": "🎵", "text": "Música relajante", "type": "positive"},
            {"emoji": "🌅", "text": "Momento de paz", "type": "positive"},
            {"emoji": "😰", "text": "Estrés laboral", "type": "negative"},
            {"emoji": "😴", "text": "Mala noche", "type": "negative"},
            {"emoji": "🤐", "text": "Conflicto personal", "type": "negative"},
            {"emoji": "💼", "text": "Presión de trabajo", "type": "negative"},
            {"emoji": "🤦", "text": "Error frustrante", "type": "negative"},
            {"emoji": "📱", "text": "Distracción digital", "type": "negative"}
        ]

        template_items = []
        for template in templates:
            is_positive = template["type"] == "positive"
            color = self.theme.positive_main if is_positive else self.theme.negative_main

            item = ft.Container(
                content=ft.Row([
                    ft.Text(template["emoji"], size=20),
                    ft.Text(template["text"], size=13, color=self.theme.text_primary, expand=True),
                    ft.Container(
                        content=ft.Text("+", size=16, color=color, text_align=ft.TextAlign.CENTER),
                        width=30, height=30, border_radius=15,
                        bgcolor=color + "20", alignment=ft.alignment.center
                    )
                ], spacing=12, alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(12), border_radius=12,
                bgcolor=color + "10", border=ft.border.all(1, color + "30"),
                on_click=lambda e, t=template: self.add_template_item(t)
            )
            template_items.append(item)

        return create_themed_container(
            content=ft.Column([
                ft.Text("🎯 Situaciones comunes", size=14, weight=ft.FontWeight.W_600, color=self.theme.text_primary),
                ft.Container(height=12),
                ft.Column(template_items, spacing=8)
            ]), theme=self.theme
        )

    def select_hour(self, hour: int):
        """Seleccionar hora"""
        self.selected_hour = hour
        if self.page:
            self.page.update()

    def add_timeline_moment(self, moment_type: str):
        """✅ CORREGIDO: Añadir momento al timeline con actualización completa"""
        if not self.timeline_text_field or not self.timeline_text_field.value:
            self.show_message("⚠️ Describe qué pasó", is_error=True)
            return

        moment = InteractiveMoment(
            emoji="⭐" if moment_type == "positive" else "🌧️",
            text=self.timeline_text_field.value.strip(), moment_type=moment_type,
            category="timeline", time_str=f"{self.selected_hour:02d}:00"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.timeline_text_field.value = ""
            self.show_message(f"✅ Momento añadido a las {self.selected_hour:02d}:00")

            # ✅ CORREGIDO: Actualizar TODOS los contenedores
            self.refresh_all_containers()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    def add_template_item(self, template: dict):
        """✅ CORREGIDO: Añadir item de template con actualización completa"""
        moment = InteractiveMoment(
            emoji=template["emoji"], text=template["text"], moment_type=template["type"],
            category="template"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.show_message(f"✅ {template['emoji']} {template['text']} añadido")

            # ✅ CORREGIDO: Actualizar TODOS los contenedores
            self.refresh_all_containers()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # ✅ NUEVA SECCIÓN: LISTA DE MOMENTOS AÑADIDOS
    # ===============================
    def build_moments_list(self):
        """✅ NUEVO: Construir lista de momentos añadidos en tiempo real"""
        if not self.moments:
            return ft.Container()  # No mostrar nada si no hay momentos

        # Tomar los últimos 5 momentos
        recent_moments = self.moments[-5:]
        recent_moments.reverse()  # Más reciente primero

        moment_items = []
        for moment in recent_moments:
            # Color del indicador según tipo
            indicator_color = self.theme.positive_main if moment.type == "positive" else self.theme.negative_main

            item = ft.Container(
                content=ft.Row([
                    # Emoji del momento
                    ft.Text(moment.emoji, size=16),

                    # Texto del momento
                    ft.Column([
                        ft.Text(
                            moment.text,
                            size=13,
                            color=self.theme.text_primary,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            max_lines=1
                        ),
                        ft.Text(
                            f"{moment.time} • {moment.category}",
                            size=10,
                            color=self.theme.text_hint
                        )
                    ], spacing=2, expand=True),

                    # Intensidad si existe
                    ft.Text(
                        f"{moment.intensity}/10" if hasattr(moment, 'intensity') and moment.intensity != 5 else "",
                        size=10,
                        color=self.theme.text_hint
                    ),

                    # Indicador de tipo
                    ft.Container(
                        width=4, height=30,
                        bgcolor=indicator_color,
                        border_radius=2
                    )
                ], spacing=8, alignment=ft.CrossAxisAlignment.CENTER),

                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                border_radius=8,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color)
            )
            moment_items.append(item)

        return create_themed_container(
            content=ft.Column([
                ft.Text(
                    f"📝 Momentos añadidos ({len(self.moments)})",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color=self.theme.text_primary
                ),
                ft.Container(height=8),
                ft.Column(moment_items, spacing=6)
            ]),
            theme=self.theme
        )

    # ===============================
    # RESUMEN Y CONTROLES
    # ===============================
    def refresh_all_containers(self):
        """✅ NUEVO: Refrescar TODOS los contenedores"""
        # Actualizar estadísticas en tiempo real
        if self.stats_text_container:
            self.stats_text_container.content = self._build_stats_text()

        # Actualizar lista de momentos
        if self.moments_list_container:
            self.moments_list_container.content = self.build_moments_list()

        # Actualizar resumen
        if self.summary_container:
            self.summary_container.content = self.build_moments_summary()

        if self.page:
            self.page.update()

    def refresh_summary(self):
        """Refrescar resumen - MANTENIDO para compatibilidad"""
        self.refresh_all_containers()

    def build_moments_summary(self):
        """✅ Resumen compacto para móvil"""
        if not self.moments:
            return ft.Container(
                content=ft.Text("No hay momentos añadidos aún",
                                color=self.theme.text_hint, text_align=ft.TextAlign.CENTER, size=12),
                padding=ft.padding.all(16)
            )

        positive_count = len([m for m in self.moments if m.type == "positive"])
        negative_count = len([m for m in self.moments if m.type == "negative"])

        # ✅ Estadísticas compactas
        stats = ft.Row([
            ft.Column([
                ft.Text(str(positive_count), size=20, weight=ft.FontWeight.BOLD, color=self.theme.positive_main),
                ft.Text("Positivos", size=10, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text(str(negative_count), size=20, weight=ft.FontWeight.BOLD, color=self.theme.negative_main),
                ft.Text("Difíciles", size=10, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text(str(len(self.moments)), size=20, weight=ft.FontWeight.BOLD, color=self.theme.accent_primary),
                ft.Text("Total", size=10, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

        # ✅ Botones de acción compactos
        action_buttons = ft.Row([
            ft.ElevatedButton(
                "🗑️ Limpiar", on_click=self.clear_moments,
                style=ft.ButtonStyle(bgcolor=self.theme.negative_main, color="#FFFFFF"),
                height=35, expand=True
            ),
            ft.Container(width=8),
            ft.ElevatedButton(
                "💾 Guardar", on_click=self.save_moments,
                style=ft.ButtonStyle(bgcolor=self.theme.positive_main, color="#FFFFFF"),
                height=35, expand=True
            )
        ])

        return create_themed_container(
            content=ft.Column([
                ft.Text("📈 Resumen", size=14, weight=ft.FontWeight.W_600, color=self.theme.text_primary),
                ft.Container(height=12),
                stats,
                ft.Container(height=16),
                action_buttons
            ]),
            theme=self.theme
        )

    def save_moments(self, e=None):
        """✅ CORREGIDO: Guardar todos los momentos"""
        if not self.moments:
            self.show_message("⚠️ No hay momentos para guardar", is_error=True)
            return

        print(f"💾 Preparando {len(self.moments)} momentos para guardar")

        try:
            from services import db
            user_id = self.current_user['id']

            # ✅ Usar el nuevo método para convertir momentos a entrada diaria
            entry_id = db.save_interactive_moments_as_entry(
                user_id=user_id,
                reflection="Entrada creada desde Momentos Interactivos",
                worth_it=len([m for m in self.moments if m.type == "positive"]) > len([m for m in self.moments if m.type == "negative"])
            )

            if entry_id:
                self.show_message(f"✅ {len(self.moments)} momentos guardados como entrada diaria")

                # ✅ Navegar al calendario para ver el resultado
                if self.page:
                    self.page.go("/calendar")
            else:
                self.show_message("❌ Error guardando momentos", is_error=True)

        except Exception as e:
            print(f"❌ Error guardando momentos: {e}")
            self.show_message("❌ Error guardando momentos", is_error=True)

    def clear_moments(self, e=None):
        """✅ CORREGIDO: Limpiar momentos con actualización completa"""
        if not self.moments:
            self.show_message("ℹ️ No hay momentos para eliminar")
            return

        try:
            from services import db
            user_id = self.current_user['id']

            # ✅ Limpiar de la base de datos también
            db.clear_interactive_moments_today(user_id)

            self.moments.clear()
            self.show_message("🗑️ Momentos eliminados")

            # ✅ CORREGIDO: Actualizar TODOS los contenedores
            self.refresh_all_containers()

        except Exception as e:
            print(f"❌ Error limpiando momentos: {e}")
            self.moments.clear()
            self.show_message("🗑️ Momentos eliminados")
            self.refresh_all_containers()

    # ===============================
    # NAVEGACIÓN Y MENSAJES
    # ===============================
    def go_to_calendar(self, e=None):
        """Ir al calendario"""
        if self.page:
            self.page.go("/calendar")

    def go_to_theme_selector(self, e=None):
        """Ir al selector de temas"""
        if self.page:
            self.page.go("/theme_selector")

    def go_to_mobile_notification_settings(self, e=None):
        """Ir a configuración de notificaciones móviles"""
        if self.page:
            self.page.go("/mobile_notification_settings")
        else:
            print("⚠️ Página no disponible para navegar a notificaciones móviles")

    def go_back(self, e=None):
        """Volver"""
        print("🔙 Volviendo...")
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/calendar")

    def show_message(self, message: str, is_error: bool = False):
        """✅ MEJORADO: Mostrar mensaje como SnackBar más visible"""
        print(f"{'❌' if is_error else '✅'} {message}")
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=3000,
                action="OK",
                action_color="#FFFFFF"
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()