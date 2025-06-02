"""
🎮 Interactive Moments Screen - CORREGIDO PARA MÓVIL
✅ Persistencia corregida ✅ Diseño móvil optimizado ✅ Header compacto
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
    """Pantalla Interactive Moments - OPTIMIZADA PARA MÓVIL"""

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

        # Contenedores
        self.main_container = None
        self.summary_container = None

        # Estado de persistencia CORREGIDO
        self.data_loaded = False
        self.auto_save_enabled = True

        print("🎮 InteractiveMomentsScreen OPTIMIZADA PARA MÓVIL inicializada")

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
                self.refresh_summary()

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

            # ✅ Usar método corregido de la clase
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
        """✅ CORREGIDO: Construir vista principal optimizada para móvil"""
        self.theme = get_theme()

        # ✅ Header COMPACTO para móvil
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # ✅ Botones más pequeños y compactos
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
            )
        ], spacing=8)

        user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'

        # ✅ Header más pequeño
        header = ft.Container(
            content=ft.Row([
                back_button,
                ft.Column([
                    ft.Text(
                        f"🎮 Momentos",
                        size=16,  # ✅ Tamaño reducido
                        weight=ft.FontWeight.W_600,
                        color="#FFFFFF",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        user_name,
                        size=12,  # ✅ Subtítulo pequeño
                        color="#FFFFFF80",
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2, expand=True),
                action_buttons
            ]),
            padding=ft.padding.all(12),  # ✅ Padding reducido
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=self.theme.gradient_header
            ),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)  # ✅ Bordes más pequeños
        )

        # ✅ Descripción compacta
        stats_text = ""
        if self.moments:
            positive_count = len([m for m in self.moments if m.type == "positive"])
            negative_count = len([m for m in self.moments if m.type == "negative"])
            stats_text = f" • {positive_count}+ {negative_count}-"

        description = ft.Container(
            content=ft.Text(
                f"Captura tus momentos{stats_text}",
                size=12,  # ✅ Texto más pequeño
                color=self.theme.text_secondary,
                text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.only(top=12, bottom=8),  # ✅ Espaciado reducido
            alignment=ft.alignment.center
        )

        # ✅ Selector de modos compacto
        mode_selector = self.build_mode_selector_compact()

        # Contenedor principal dinámico
        self.main_container = ft.Container(
            content=self.build_active_mode(),
            expand=True
        )

        # Resumen de momentos
        self.summary_container = ft.Container(
            content=self.build_moments_summary()
        )

        # ✅ Vista completa optimizada para móvil
        content = ft.Column([
            description,
            mode_selector,
            ft.Container(height=12),  # ✅ Espacios reducidos
            self.main_container,
            ft.Container(height=12),
            self.summary_container
        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        view = ft.View(
            "/interactive_moments",
            [header, ft.Container(content=content, padding=ft.padding.all(12), expand=True)],  # ✅ Padding reducido
            bgcolor=self.theme.primary_bg, padding=0, spacing=0
        )

        return view

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
                        width=140,  # ✅ Ancho fijo para móvil
                        height=70,  # ✅ Altura reducida
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
    # MODO 1: QUICK ADD - OPTIMIZADO MÓVIL
    # ===============================
    def build_quick_add_mode(self):
        """✅ OPTIMIZADO: Modo Quick Add para móvil"""

        # ✅ Campo de texto más compacto
        self.quick_text_field = ft.TextField(
            hint_text="¿Qué pasó?",
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(12),  # ✅ Padding reducido
            text_style=ft.TextStyle(color=self.theme.text_primary),
            height=50  # ✅ Altura fija más pequeña
        )

        # ✅ Frases rápidas más compactas
        quick_phrases = [
            "Me sentí increíble", "Fue genial", "Muy estresante", "Me frustré"
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

        # ✅ Emojis organizados compactos
        emoji_sections = []

        # Sección positiva compacta
        positive_emojis = ['😊', '🎉', '💪', '☕', '🎵', '🤗']
        positive_section = self.build_compact_emoji_section(
            "✨ Positivos", positive_emojis, "positive", self.theme.positive_main
        )
        emoji_sections.append(positive_section)

        # Sección negativa compacta
        negative_emojis = ['😰', '😔', '😤', '💼', '😫', '🤯']
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

            # ✅ Emojis compactos
            ft.Column(emoji_sections, spacing=8)
        ])

    def build_compact_emoji_section(self, title: str, emojis: List[str], moment_type: str, color: str):
        """✅ Sección de emojis compacta para móvil"""

        # ✅ Grid de emojis en filas de 6
        emoji_rows = []
        for i in range(0, len(emojis), 6):
            row_emojis = []
            for j in range(6):
                if i + j < len(emojis):
                    emoji = emojis[i + j]
                    btn = ft.Container(
                        content=ft.Text(emoji, size=20),
                        width=40,  # ✅ Tamaño reducido
                        height=40,
                        border_radius=8,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        alignment=ft.alignment.center,
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
        """Añadir momento rápido"""
        moment = InteractiveMoment(
            emoji=emoji, text=self.quick_text_field.value.strip(),
            moment_type=moment_type, intensity=7 if moment_type == "positive" else 6,
            category=category
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.quick_text_field.value = ""
            self.show_message(f"✅ {emoji} {moment.text} añadido")
            self.refresh_summary()
            if self.page:
                self.page.update()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # MOOD BUBBLES - OPTIMIZADO MÓVIL
    # ===============================
    def build_mood_bubbles_mode(self):
        """✅ OPTIMIZADO: Modo Mood Bubbles para móvil"""

        # ✅ Slider de intensidad compacto
        intensity_section = self.build_compact_intensity_slider()

        # ✅ Burbujas compactas
        bubble_options = [
            {'emoji': '😊', 'text': 'Alegre', 'type': 'positive'},
            {'emoji': '🎉', 'text': 'Emocionado', 'type': 'positive'},
            {'emoji': '😌', 'text': 'Tranquilo', 'type': 'positive'},
            {'emoji': '💪', 'text': 'Motivado', 'type': 'positive'},
            {'emoji': '😰', 'text': 'Estresado', 'type': 'negative'},
            {'emoji': '😔', 'text': 'Triste', 'type': 'negative'}
        ]

        # ✅ Grid de burbujas en filas de 2
        bubble_rows = []
        for i in range(0, len(bubble_options), 2):
            row_bubbles = []
            for j in range(2):
                if i + j < len(bubble_options):
                    bubble = bubble_options[i + j]
                    bubble_widget = self.create_compact_mood_bubble(bubble)
                    row_bubbles.append(bubble_widget)

            if row_bubbles:
                bubble_rows.append(ft.Row(row_bubbles, alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=12))

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
        """✅ Slider de intensidad compacto"""
        self.intensity_slider = ft.Slider(
            min=1, max=10, value=self.current_intensity, divisions=9,
            on_change=self.on_intensity_change,
            active_color=self.get_intensity_color(self.current_intensity),
            thumb_color=self.get_intensity_color(self.current_intensity)
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

                # ✅ Valor compacto
                ft.Text(f"{int(self.current_intensity)}/10", size=18, weight=ft.FontWeight.BOLD,
                        color=self.get_intensity_color(self.current_intensity), text_align=ft.TextAlign.CENTER)
            ]), theme=self.theme
        )

    def create_compact_mood_bubble(self, bubble_data):
        """✅ Burbuja de emoción compacta"""
        is_positive = bubble_data["type"] == "positive"
        base_color = self.theme.positive_main if is_positive else self.theme.negative_main
        light_color = self.theme.positive_light if is_positive else self.theme.negative_light

        bubble = ft.Container(
            content=ft.Column([
                ft.Text(bubble_data["emoji"], size=28),
                ft.Container(height=4),
                ft.Text(bubble_data["text"], size=12, weight=ft.FontWeight.W_500,
                        color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=120,  # ✅ Tamaño reducido
            height=90,   # ✅ Altura reducida
            padding=ft.padding.all(12),
            border_radius=16,
            bgcolor=light_color,
            border=ft.border.all(2, base_color + "50"),
            on_click=lambda e, bubble=bubble_data: self.create_mood_moment(bubble)
        )

        return bubble

    def on_intensity_change(self, e):
        """Callback cuando cambia intensidad"""
        self.current_intensity = e.control.value
        new_color = self.get_intensity_color(self.current_intensity)
        e.control.active_color = new_color
        e.control.thumb_color = new_color
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
        """Crear momento desde burbuja"""
        moment = InteractiveMoment(
            emoji=bubble_data["emoji"], text=bubble_data["text"],
            moment_type=bubble_data["type"], intensity=int(self.current_intensity),
            category="mood"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.show_message(f"✅ {bubble_data['emoji']} {bubble_data['text']} añadido")
            self.refresh_summary()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # TIMELINE Y TEMPLATES - SIMPLIFICADOS
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
                content=ft.Text(f"{hour:02d}:00", size=12, color=self.theme.text_primary),
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
        """✅ Templates simplificados para móvil"""
        templates = [
            {"emoji": "💪", "text": "Ejercicio energizante", "type": "positive"},
            {"emoji": "☕", "text": "Café con amigo", "type": "positive"},
            {"emoji": "🎯", "text": "Tarea completada", "type": "positive"},
            {"emoji": "😰", "text": "Estrés laboral", "type": "negative"},
            {"emoji": "😴", "text": "Mala noche", "type": "negative"},
            {"emoji": "🤐", "text": "Conflicto personal", "type": "negative"}
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
                        content=ft.Text("+", size=16, color=color),
                        width=30, height=30, border_radius=15,
                        bgcolor=color + "20", alignment=ft.alignment.center
                    )
                ], spacing=12),
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
        """Añadir momento al timeline"""
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
            self.refresh_summary()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    def add_template_item(self, template: dict):
        """Añadir item de template"""
        moment = InteractiveMoment(
            emoji=template["emoji"], text=template["text"], moment_type=template["type"],
            category="template"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.show_message(f"✅ {template['emoji']} {template['text']} añadido")
            self.refresh_summary()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # RESUMEN Y CONTROLES
    # ===============================
    def refresh_summary(self):
        """Refrescar resumen"""
        if self.summary_container:
            self.summary_container.content = self.build_moments_summary()
        if self.page:
            self.page.update()

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
        """✅ CORREGIDO: Guardar todos los momentos usando la nueva integración"""
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
        """Limpiar momentos"""
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
            self.refresh_summary()
        except Exception as e:
            print(f"❌ Error limpiando momentos: {e}")
            self.moments.clear()
            self.show_message("🗑️ Momentos eliminados")
            self.refresh_summary()

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

    def go_back(self, e=None):
        """Volver"""
        print("🔙 Volviendo...")
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/calendar")

    def show_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje"""
        print(f"{'❌' if is_error else '✅'} {message}")
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF", size=12),  # ✅ Texto más pequeño
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=2000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()