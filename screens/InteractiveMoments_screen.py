"""
🎮 Interactive Moments Screen - CLASE COMPLETA
Implementación completa de los 4 modos: Quick Add, Mood Bubbles, Timeline, Templates
"""

import flet as ft
from datetime import datetime, time
from typing import List, Dict, Any, Optional, Callable
import calendar
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

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
        """Convertir a SimpleTag para compatibilidad con EntryScreen"""
        from screens.new_tag_screen import SimpleTag
        return SimpleTag(
            emoji=self.emoji,
            category=self.type,
            name=f"{self.text}",
            reason=f"Momento {self.category} de intensidad {self.intensity} a las {self.time}"
        )

    def to_dict(self):
        """Convertir a diccionario para almacenar en base de datos"""
        return {
            'id': self.id,
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
            emoji=data['emoji'],
            text=data['text'],
            moment_type=data['type'],
            intensity=data['intensity'],
            category=data['category'],
            time_str=data['time']
        )
        moment.id = data['id']
        if 'timestamp' in data:
            moment.timestamp = datetime.fromisoformat(data['timestamp'])
        return moment

    def __str__(self):
        return f"{self.emoji} {self.text} ({self.type}) - {self.intensity}/10"

class InteractiveMomentsScreen:
    """Pantalla Interactive Moments - CLASE COMPLETA"""

    def __init__(self, app, on_moments_created: Callable = None, on_go_back: Callable = None):
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

        # Contenedores
        self.main_container = None
        self.summary_container = None

        # Estado de persistencia
        self.data_loaded = False
        self.auto_save_enabled = True

        print("🎮 InteractiveMomentsScreen COMPLETA inicializada")

    def set_user(self, user_data):
        """Establecer usuario actual"""
        self.current_user = user_data
        self.data_loaded = False
        print(f"👤 Usuario establecido: {user_data.get('name')} (ID: {user_data.get('id')})")
        self.load_user_moments()

    def load_user_moments(self):
        """Cargar momentos guardados del usuario desde la base de datos"""
        if not self.current_user:
            print("⚠️ No hay usuario para cargar momentos")
            return

        try:
            from services import db
            user_id = self.current_user['id']

            print(f"📚 Cargando momentos interactivos para usuario {user_id}")

            moments_data = db.get_interactive_moments_today(user_id)

            self.moments.clear()
            for moment_dict in moments_data:
                moment = InteractiveMoment.from_dict(moment_dict)
                self.moments.append(moment)

            print(f"✅ Cargados {len(self.moments)} momentos interactivos")
            self.data_loaded = True

            if self.page:
                self.refresh_summary()

        except Exception as e:
            print(f"❌ Error cargando momentos del usuario: {e}")
            import traceback
            traceback.print_exc()

    def save_moment_to_db(self, moment):
        """Guardar momento individual en la base de datos"""
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
        """Construir vista principal"""
        self.theme = get_theme()

        # Header
        back_button = ft.TextButton(
            "← Entry",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        additional_buttons = ft.Row([
            ft.TextButton("🎨", on_click=self.go_to_theme_selector,
                          style=ft.ButtonStyle(color="#FFFFFF"), tooltip="Temas"),
            ft.TextButton("📅", on_click=self.go_to_calendar,
                          style=ft.ButtonStyle(color="#FFFFFF"), tooltip="Calendario"),
            ft.TextButton("⚙️", on_click=self.show_settings_dialog,
                          style=ft.ButtonStyle(color="#FFFFFF"), tooltip="Configuración")
        ], spacing=0)

        user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'
        header = create_gradient_header(
            title=f"🎮 Momentos - {user_name}",
            left_button=back_button,
            right_button=additional_buttons,
            theme=self.theme
        )

        # Descripción con estadísticas
        stats_text = ""
        if self.moments:
            positive_count = len([m for m in self.moments if m.type == "positive"])
            negative_count = len([m for m in self.moments if m.type == "negative"])
            stats_text = f" • {positive_count}+ {negative_count}- momentos de hoy"

        description = ft.Container(
            content=ft.Text(
                f"Experimenta diferentes formas de capturar tus momentos{stats_text}",
                size=14, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.only(bottom=20), alignment=ft.alignment.center
        )

        # Selector de modos
        mode_selector = self.build_mode_selector()

        # Contenedor principal dinámico
        self.main_container = ft.Container(
            content=self.build_active_mode(),
            expand=True
        )

        # Resumen de momentos
        self.summary_container = ft.Container(
            content=self.build_moments_summary()
        )

        # Vista completa
        content = ft.Column([
            description,
            mode_selector,
            ft.Container(height=20),
            self.main_container,
            ft.Container(height=20),
            self.summary_container
        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        view = ft.View(
            "/interactive_moments",
            [header, ft.Container(content=content, padding=ft.padding.all(20), expand=True)],
            bgcolor=self.theme.primary_bg, padding=0, spacing=0
        )

        return view

    def build_mode_selector(self):
        """Selector de modos"""
        modes = [
            {"id": "quick", "name": "Quick Add", "emoji": "⚡", "desc": "Añadir rápido con emojis"},
            {"id": "mood", "name": "Mood Bubbles", "emoji": "🎭", "desc": "Burbujas de intensidad"},
            {"id": "timeline", "name": "Timeline", "emoji": "⏰", "desc": "Línea de tiempo del día"},
            {"id": "templates", "name": "Templates", "emoji": "🎯", "desc": "Situaciones comunes"}
        ]

        mode_buttons = []
        for i, mode in enumerate(modes):
            if i % 2 == 0:
                row = ft.Row(spacing=12, alignment=ft.MainAxisAlignment.CENTER)
                mode_buttons.append(row)

            is_active = self.active_mode == mode["id"]
            button = ft.Container(
                content=ft.Column([
                    ft.Text(mode["emoji"], size=28),
                    ft.Text(mode["name"], size=14, weight=ft.FontWeight.W_600, color=self.theme.text_primary),
                    ft.Text(mode["desc"], size=12, color=self.theme.text_secondary)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                width=160, height=100, padding=ft.padding.all(16), border_radius=16,
                bgcolor=self.theme.accent_primary + "20" if is_active else self.theme.surface,
                border=ft.border.all(2 if is_active else 1,
                                     self.theme.accent_primary if is_active else self.theme.border_color),
                on_click=lambda e, mode_id=mode["id"]: self.switch_mode(mode_id)
            )
            mode_buttons[-1].controls.append(button)

        return ft.Column(mode_buttons, spacing=12)

    def switch_mode(self, mode_id: str):
        """Cambiar entre modos"""
        print(f"🔄 Cambiando a modo: {mode_id}")
        self.active_mode = mode_id
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
    # MODO 1: QUICK ADD COMPLETO
    # ===============================
    def build_quick_add_mode(self):
        """Modo Quick Add - IMPLEMENTACIÓN COMPLETA"""

        # Campo de texto principal
        self.quick_text_field = ft.TextField(
            hint_text="¿Qué pasó? (ej: 'Desayuno delicioso', 'Reunión eterna')",
            border_radius=16, bgcolor=self.theme.surface, border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary, content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(color=self.theme.text_primary)
        )

        # Frases rápidas
        quick_phrases = [
            "Me sentí increíble", "Fue genial", "Perfecto momento", "Me encantó",
            "Muy estresante", "Me frustré", "Fue difícil", "Me agotó"
        ]

        phrase_buttons = []
        for phrase in quick_phrases:
            btn = ft.Container(
                content=ft.Text(phrase, size=12, color=self.theme.text_secondary),
                padding=ft.padding.symmetric(horizontal=12, vertical=6), border_radius=20,
                bgcolor=self.theme.surface, border=ft.border.all(1, self.theme.border_color),
                on_click=lambda e, p=phrase: self.set_quick_text(p)
            )
            phrase_buttons.append(btn)

        phrases_container = ft.Wrap(children=phrase_buttons, spacing=8, run_spacing=8)

        # Categorías de emojis organizadas
        emoji_categories = {
            "positive": {
                "simple": ['😊', '😍', '🥰', '😌', '😎', '🤗'],
                "achievement": ['🎉', '🏆', '⭐', '💪', '🚀', '✨'],
                "activities": ['☕', '🍕', '📚', '🎵', '🎨', '🏃‍♂️'],
                "social": ['👫', '💕', '🤝', '🎭', '💬', '🎈']
            },
            "negative": {
                "stress": ['😰', '😫', '🤯', '😤', '😮‍💨', '🥴'],
                "sadness": ['😢', '😔', '💔', '😞', '😿', '⛈️'],
                "work": ['💼', '📊', '⏰', '🔥', '📉', '💻'],
                "health": ['🤒', '😷', '🤕', '😵', '🥱', '😪']
            }
        }

        # Construir secciones de emojis
        emoji_sections = []

        # Sección positiva
        positive_section = self.build_emoji_category_section(
            "✨ Momentos Positivos", emoji_categories["positive"], "positive",
            self.theme.positive_main, self.theme.positive_light
        )
        emoji_sections.append(positive_section)
        emoji_sections.append(ft.Container(height=16))

        # Sección negativa
        negative_section = self.build_emoji_category_section(
            "🌧️ Momentos Difíciles", emoji_categories["negative"], "negative",
            self.theme.negative_main, self.theme.negative_light
        )
        emoji_sections.append(negative_section)

        return ft.Column([
            ft.Text("⚡ Quick Add", size=20, weight=ft.FontWeight.BOLD, color=self.theme.text_primary),
            ft.Container(height=16),

            # Campo de texto
            create_themed_container(content=self.quick_text_field, theme=self.theme),
            ft.Container(height=16),

            # Frases rápidas
            create_themed_container(
                content=ft.Column([
                    ft.Text("⚡ Frases rápidas:", size=14, weight=ft.FontWeight.W_500, color=self.theme.text_secondary),
                    ft.Container(height=8),
                    phrases_container
                ]), theme=self.theme
            ),
            ft.Container(height=16),

            # Secciones de emojis
            ft.Column(emoji_sections)
        ])

    def build_emoji_category_section(self, title: str, categories: Dict, moment_type: str,
                                     main_color: str, light_color: str):
        """Construir sección de categoría de emojis"""
        category_columns = []

        for category_name, emojis in categories.items():
            # Título de categoría
            category_title = ft.Text(category_name.title(), size=12, color=self.theme.text_hint,
                                     weight=ft.FontWeight.W_500)

            # Botones de emojis
            emoji_buttons = []
            for emoji in emojis:
                btn = ft.Container(
                    content=ft.Text(emoji, size=24), width=50, height=50, border_radius=12,
                    bgcolor=self.theme.surface, border=ft.border.all(1, self.theme.border_color),
                    alignment=ft.alignment.center,
                    on_click=lambda e, em=emoji, cat=category_name: self.add_quick_moment(em, moment_type, cat)
                )
                emoji_buttons.append(btn)

            emoji_grid = ft.Wrap(children=emoji_buttons, spacing=8, run_spacing=8)

            category_columns.append(ft.Column([
                category_title, ft.Container(height=8), emoji_grid
            ], spacing=0))

        content = ft.Column([
                                ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=main_color),
                                ft.Container(height=12)
                            ] + category_columns, spacing=12)

        return create_themed_container(content=content, theme=self.theme, border_radius=16)

    def set_quick_text(self, text: str):
        """Establecer texto rápido"""
        if self.quick_text_field:
            self.quick_text_field.value = text
            if self.page:
                self.page.update()

    def add_quick_moment(self, emoji: str, moment_type: str, category: str):
        """Añadir momento rápido"""
        if not self.quick_text_field or not self.quick_text_field.value:
            self.show_message("⚠️ Escribe qué pasó antes de seleccionar emoji", is_error=True)
            return

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
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===================================
    # MODO 2: MOOD BUBBLES COMPLETO
    # ===================================
    def build_mood_bubbles_mode(self):
        """Modo Mood Bubbles - IMPLEMENTACIÓN COMPLETA"""

        # Slider de intensidad avanzado
        intensity_section = self.build_intensity_slider()

        # Burbujas de emociones
        bubble_options = [
            {'emoji': '😊', 'text': 'Alegre', 'type': 'positive'},
            {'emoji': '🎉', 'text': 'Emocionado', 'type': 'positive'},
            {'emoji': '😌', 'text': 'Tranquilo', 'type': 'positive'},
            {'emoji': '💪', 'text': 'Motivado', 'type': 'positive'},
            {'emoji': '😰', 'text': 'Estresado', 'type': 'negative'},
            {'emoji': '😔', 'text': 'Triste', 'type': 'negative'},
            {'emoji': '😤', 'text': 'Frustrado', 'type': 'negative'},
            {'emoji': '😫', 'text': 'Agotado', 'type': 'negative'}
        ]

        # Crear grid de burbujas
        bubble_rows = []
        for i in range(0, len(bubble_options), 2):
            row_bubbles = []
            for j in range(2):
                if i + j < len(bubble_options):
                    bubble = bubble_options[i + j]
                    bubble_widget = self.create_mood_bubble(bubble)
                    row_bubbles.append(bubble_widget)

            if row_bubbles:
                bubble_rows.append(ft.Row(row_bubbles, alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=16))

        bubbles_container = create_themed_container(
            content=ft.Column([
                                  ft.Text("🫧 Toca una burbuja de emoción", size=16, weight=ft.FontWeight.W_600,
                                          color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                                  ft.Container(height=16)
                              ] + bubble_rows, spacing=16),
            theme=self.theme
        )

        return ft.Column([
            ft.Text("🎭 Mood Bubbles", size=20, weight=ft.FontWeight.BOLD, color=self.theme.text_primary),
            ft.Container(height=16),
            intensity_section,
            ft.Container(height=20),
            bubbles_container
        ])

    def build_intensity_slider(self):
        """Slider de intensidad visual mejorado"""
        # Slider principal
        self.intensity_slider = ft.Slider(
            min=1, max=10, value=self.current_intensity, divisions=9,
            on_change=self.on_intensity_change,
            active_color=self.get_intensity_color(self.current_intensity),
            thumb_color=self.get_intensity_color(self.current_intensity)
        )

        # Indicadores visuales de intensidad
        intensity_indicators = []
        for i in range(1, 11):
            size = 8 if i != self.current_intensity else 12
            opacity = 0.3 if i != self.current_intensity else 1.0
            color = self.get_intensity_color(i)

            indicator = ft.Container(
                width=size, height=size, border_radius=size // 2,
                bgcolor=color, opacity=opacity
            )
            intensity_indicators.append(indicator)

        indicators_row = ft.Row(intensity_indicators, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return create_themed_container(
            content=ft.Column([
                ft.Text("🎚️ Intensidad del momento", size=16, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                ft.Container(height=12),

                # Emojis de referencia
                ft.Row([ft.Text("😐", size=24), ft.Container(expand=True), ft.Text("🤯", size=24)]),
                ft.Container(height=8),

                # Slider
                self.intensity_slider,
                ft.Container(height=8),

                # Indicadores
                indicators_row,
                ft.Container(height=12),

                # Valor actual
                ft.Column([
                    ft.Text(f"{int(self.current_intensity)}/10", size=24, weight=ft.FontWeight.BOLD,
                            color=self.get_intensity_color(self.current_intensity), text_align=ft.TextAlign.CENTER),
                    ft.Text(self.get_intensity_label(self.current_intensity), size=14,
                            color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ]), theme=self.theme
        )

    def create_mood_bubble(self, bubble_data):
        """Crear burbuja de emoción individual mejorada"""
        is_positive = bubble_data["type"] == "positive"
        base_color = self.theme.positive_main if is_positive else self.theme.negative_main
        light_color = self.theme.positive_light if is_positive else self.theme.negative_light

        # Indicadores de intensidad
        intensity_level = int(self.current_intensity // 2) + 1  # 1-5 dots
        intensity_dots = []
        for i in range(5):
            opacity = 1.0 if i < intensity_level else 0.3
            size = 6 if i < intensity_level else 4
            dot = ft.Container(width=size, height=size, border_radius=size // 2,
                               bgcolor=base_color, opacity=opacity)
            intensity_dots.append(dot)

        dots_row = ft.Row(intensity_dots, spacing=3, alignment=ft.MainAxisAlignment.CENTER)

        # Burbuja principal
        bubble = ft.Container(
            content=ft.Column([
                ft.Text(bubble_data["emoji"], size=36),
                ft.Container(height=8),
                ft.Text(bubble_data["text"], size=14, weight=ft.FontWeight.W_500,
                        color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                ft.Container(height=8),
                dots_row
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            width=160, height=140, padding=ft.padding.all(16), border_radius=20,
            bgcolor=light_color, border=ft.border.all(2, base_color + "50"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=base_color + "30", offset=ft.Offset(0, 4)),
            on_click=lambda e, bubble=bubble_data: self.create_mood_moment(bubble),
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT)
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

    def get_intensity_label(self, intensity):
        """Etiqueta según intensidad"""
        if intensity <= 3:
            return "Suave"
        elif intensity <= 7:
            return "Moderado"
        else:
            return "Intenso"

    def create_mood_moment(self, bubble_data):
        """Crear momento desde burbuja"""
        moment = InteractiveMoment(
            emoji=bubble_data["emoji"], text=bubble_data["text"],
            moment_type=bubble_data["type"], intensity=int(self.current_intensity),
            category="mood"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.show_message(f"✅ {bubble_data['emoji']} {bubble_data['text']} añadido con intensidad {int(self.current_intensity)}")
            self.refresh_summary()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # MODO 3: TIMELINE COMPLETO
    # ===============================
    def build_timeline_mode(self):
        """Modo Timeline - IMPLEMENTACIÓN COMPLETA"""

        # Selector de horas visual
        hour_selector = self.build_hour_selector()

        # Formulario para añadir momento
        moment_form = self.build_timeline_moment_form()

        # Vista de timeline
        timeline_visual = self.build_timeline_visual()

        return ft.Column([
            ft.Text("⏰ Timeline del Día", size=20, weight=ft.FontWeight.BOLD, color=self.theme.text_primary),
            ft.Container(height=16),
            hour_selector,
            ft.Container(height=16),
            moment_form,
            ft.Container(height=16),
            timeline_visual
        ])

    def build_hour_selector(self):
        """Selector visual de horas completo"""
        current_hour = datetime.now().hour

        # Crear botones de horas en filas de 6
        hour_rows = []
        for row_start in range(0, 24, 6):
            hour_buttons = []

            for hour in range(row_start, min(row_start + 6, 24)):
                moment_at_hour = self.get_moment_for_hour(hour)
                is_past = hour < current_hour
                is_current = hour == current_hour
                is_selected = hour == self.selected_hour

                # Determinar estilo
                if is_selected:
                    bg_color = self.theme.accent_primary + "50"
                    border_color = self.theme.accent_primary
                    border_width = 2
                elif moment_at_hour:
                    color = self.theme.positive_main if moment_at_hour.type == "positive" else self.theme.negative_main
                    bg_color = color + "30"
                    border_color = color
                    border_width = 2
                else:
                    bg_color = self.theme.surface
                    border_color = self.theme.border_color
                    border_width = 1

                opacity = 0.5 if is_past and not moment_at_hour else 1.0

                # Contenido del botón
                if moment_at_hour:
                    content = ft.Column([
                        ft.Text(f"{hour:02d}:00", size=10, color=self.theme.text_secondary),
                        ft.Text(moment_at_hour.emoji, size=16)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)
                else:
                    indicator_color = "#FFA500" if is_current else self.theme.border_color
                    content = ft.Column([
                        ft.Text(f"{hour:02d}:00", size=10, color=self.theme.text_secondary),
                        ft.Container(width=8, height=8, border_radius=4, bgcolor=indicator_color)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)

                button = ft.Container(
                    content=content, width=60, height=50, border_radius=8,
                    bgcolor=bg_color, border=ft.border.all(border_width, border_color),
                    opacity=opacity, on_click=lambda e, h=hour: self.select_hour(h)
                )
                hour_buttons.append(button)

            hour_rows.append(ft.Row(hour_buttons, spacing=8, alignment=ft.MainAxisAlignment.CENTER))

        return create_themed_container(
            content=ft.Column([
                                  ft.Text("🕐 Selecciona la hora", size=16, weight=ft.FontWeight.W_600,
                                          color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                                  ft.Container(height=12)
                              ] + hour_rows, spacing=8), theme=self.theme
        )

    def build_timeline_moment_form(self):
        """Formulario para añadir momento al timeline"""
        self.timeline_text_field = ft.TextField(
            hint_text="Describe qué pasó en esta hora...", border_radius=12,
            bgcolor=self.theme.surface, border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary, content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(color=self.theme.text_primary)
        )

        positive_btn = ft.ElevatedButton(
            content=ft.Row([ft.Text("✨", size=16), ft.Text("Positivo", size=14)],
                           spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            on_click=lambda e: self.add_timeline_moment("positive"),
            style=ft.ButtonStyle(bgcolor=self.theme.positive_main, color="#FFFFFF",
                                 shape=ft.RoundedRectangleBorder(radius=12)),
            height=45, expand=True
        )

        negative_btn = ft.ElevatedButton(
            content=ft.Row([ft.Text("🌧️", size=16), ft.Text("Difícil", size=14)],
                           spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            on_click=lambda e: self.add_timeline_moment("negative"),
            style=ft.ButtonStyle(bgcolor=self.theme.negative_main, color="#FFFFFF",
                                 shape=ft.RoundedRectangleBorder(radius=12)),
            height=45, expand=True
        )

        return create_themed_container(
            content=ft.Column([
                ft.Text(f"📝 ¿Qué pasó a las {self.selected_hour:02d}:00?", size=16,
                        weight=ft.FontWeight.W_600, color=self.theme.text_primary),
                ft.Container(height=12),
                self.timeline_text_field,
                ft.Container(height=16),
                ft.Row([positive_btn, ft.Container(width=12), negative_btn], expand=True)
            ]), theme=self.theme
        )

    def build_timeline_visual(self):
        """Vista visual del timeline"""
        if not self.moments:
            return create_themed_container(
                content=ft.Text("No hay momentos en el timeline aún", color=self.theme.text_hint,
                                text_align=ft.TextAlign.CENTER), theme=self.theme
            )

        # Ordenar momentos por hora
        timeline_moments = sorted(self.moments, key=lambda m: m.time)

        moment_widgets = []
        for moment in timeline_moments:
            moment_widget = ft.Container(
                content=ft.Row([
                    # Hora
                    ft.Container(
                        content=ft.Text(moment.time, size=12, weight=ft.FontWeight.W_500,
                                        color=self.theme.text_hint), width=60
                    ),
                    # Emoji
                    ft.Text(moment.emoji, size=20),
                    # Texto
                    ft.Text(moment.text, size=14, color=self.theme.text_secondary, expand=True),
                    # Indicador
                    ft.Container(width=8, height=8, border_radius=4,
                                 bgcolor=self.theme.positive_main if moment.type == "positive"
                                 else self.theme.negative_main)
                ], spacing=12, alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(12), margin=ft.margin.only(bottom=8),
                border_radius=8, bgcolor=self.theme.surface + "50",
                border=ft.border.all(1, self.theme.border_color)
            )
            moment_widgets.append(moment_widget)

        return create_themed_container(
            content=ft.Column([
                ft.Text("📊 Tu línea de tiempo", size=14, weight=ft.FontWeight.W_500,
                        color=self.theme.text_secondary),
                ft.Container(height=12),
                ft.Column(moment_widgets, spacing=0)
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
            self.show_message("⚠️ Describe qué pasó antes de añadir", is_error=True)
            return

        # Verificar si ya hay momento en esa hora
        existing_moment = self.get_moment_for_hour(self.selected_hour)
        if existing_moment:
            self.show_message(f"⚠️ Ya hay un momento a las {self.selected_hour:02d}:00", is_error=True)
            return

        moment = InteractiveMoment(
            emoji="⭐" if moment_type == "positive" else "🌧️",
            text=self.timeline_text_field.value.strip(), moment_type=moment_type,
            intensity=7 if moment_type == "positive" else 6, category="timeline",
            time_str=f"{self.selected_hour:02d}:00"
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.timeline_text_field.value = ""
            self.show_message(f"✅ Momento añadido a las {self.selected_hour:02d}:00")
            self.refresh_summary()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    def get_moment_for_hour(self, hour: int):
        """Obtener momento para hora específica"""
        for moment in self.moments:
            if moment.time.startswith(f"{hour:02d}:"):
                return moment
        return None

    # ===============================
    # MODO 4: TEMPLATES COMPLETO
    # ===============================
    def build_templates_mode(self):
        """Modo Templates - IMPLEMENTACIÓN COMPLETA"""

        templates = {
            "work": {
                "title": "💼 Trabajo",
                "color": self.theme.accent_primary,
                "items": [
                    {"emoji": "🎯", "text": "Completé una tarea importante", "type": "positive"},
                    {"emoji": "🤝", "text": "Buena reunión de equipo", "type": "positive"},
                    {"emoji": "📊", "text": "Presentación exitosa", "type": "positive"},
                    {"emoji": "💡", "text": "Tuve una gran idea", "type": "positive"},
                    {"emoji": "⏰", "text": "Deadline estresante", "type": "negative"},
                    {"emoji": "🤯", "text": "Demasiadas reuniones", "type": "negative"},
                    {"emoji": "💻", "text": "Problemas técnicos", "type": "negative"}
                ]
            },
            "social": {
                "title": "👥 Social & Familia",
                "color": self.theme.positive_main,
                "items": [
                    {"emoji": "☕", "text": "Café con un amigo", "type": "positive"},
                    {"emoji": "🎉", "text": "Celebración familiar", "type": "positive"},
                    {"emoji": "💬", "text": "Conversación profunda", "type": "positive"},
                    {"emoji": "🤗", "text": "Abrazo reconfortante", "type": "positive"},
                    {"emoji": "😔", "text": "Me sentí solo/a", "type": "negative"},
                    {"emoji": "🤐", "text": "Conflicto con alguien", "type": "negative"},
                    {"emoji": "📱", "text": "Demasiado tiempo en redes", "type": "negative"}
                ]
            },
            "health": {
                "title": "🏃‍♂️ Bienestar & Salud",
                "color": "#F59E0B",
                "items": [
                    {"emoji": "💪", "text": "Ejercicio energizante", "type": "positive"},
                    {"emoji": "🧘‍♀️", "text": "Meditación relajante", "type": "positive"},
                    {"emoji": "🥗", "text": "Comida saludable", "type": "positive"},
                    {"emoji": "😊", "text": "Me siento en forma", "type": "positive"},
                    {"emoji": "😴", "text": "No dormí bien", "type": "negative"},
                    {"emoji": "🤒", "text": "Me siento enfermo/a", "type": "negative"},
                    {"emoji": "🍔", "text": "Comí mal todo el día", "type": "negative"}
                ]
            }
        }

        template_sections = []
        for category, template in templates.items():
            section = self.build_template_section(category, template)
            template_sections.append(section)
            template_sections.append(ft.Container(height=16))

        return ft.Column([
                             ft.Text("🎯 Templates", size=20, weight=ft.FontWeight.BOLD, color=self.theme.text_primary),
                             ft.Container(height=8),
                             ft.Text("Situaciones comunes organizadas por categorías", size=14,
                                     color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER),
                             ft.Container(height=16)
                         ] + template_sections[:-1])

    def build_template_section(self, category: str, template: dict):
        """Sección de template por categoría"""
        # Header
        header = ft.Row([
            ft.Text(template["title"], size=16, weight=ft.FontWeight.W_600, color=template["color"]),
            ft.Container(
                content=ft.Text(f"{len(template['items'])} opciones", size=12, color=self.theme.text_hint),
                padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=12,
                bgcolor=template["color"] + "20"
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Items
        template_items = []
        for item in template["items"]:
            item_widget = self.build_template_item(item, category, template["color"])
            template_items.append(item_widget)

        return create_themed_container(
            content=ft.Column([header, ft.Container(height=12)] + template_items, spacing=8),
            theme=self.theme, border_radius=16
        )

    def build_template_item(self, item: dict, category: str, color: str):
        """Item individual de template"""
        is_positive = item["type"] == "positive"
        bg_color = (self.theme.positive_light if is_positive else self.theme.negative_light) + "30"
        border_color = self.theme.positive_main if is_positive else self.theme.negative_main

        return ft.Container(
            content=ft.Row([
                # Emoji
                ft.Container(content=ft.Text(item["emoji"], size=20), width=40, alignment=ft.alignment.center),
                # Texto
                ft.Text(item["text"], size=14, color=self.theme.text_primary, expand=True),
                # Botón añadir
                ft.Container(
                    content=ft.Text("+", size=16, weight=ft.FontWeight.BOLD, color=border_color),
                    width=30, height=30, border_radius=15, bgcolor=bg_color,
                    border=ft.border.all(1, border_color), alignment=ft.alignment.center
                )
            ], spacing=12, alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(12), border_radius=12, bgcolor=bg_color,
            border=ft.border.all(1, border_color + "50"),
            on_click=lambda e, it=item, cat=category: self.add_template_item(item, cat),
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT)
        )

    def add_template_item(self, item: dict, category: str):
        """Añadir item de template"""
        moment = InteractiveMoment(
            emoji=item["emoji"], text=item["text"], moment_type=item["type"],
            intensity=7 if item["type"] == "positive" else 6, category=category
        )

        if self.auto_save_moment(moment):
            self.moments.append(moment)
            self.show_message(f"✅ {item['emoji']} {item['text']} añadido")
            self.refresh_summary()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # RESUMEN DE MOMENTOS COMPLETO
    # ===============================
    def build_moments_summary(self):
        """Resumen completo de momentos"""
        if not self.moments:
            return ft.Container(
                content=ft.Text("No hay momentos añadidos aún. ¡Empieza añadiendo algunos!",
                                color=self.theme.text_hint, text_align=ft.TextAlign.CENTER),
                padding=ft.padding.all(20)
            )

        positive_count = len([m for m in self.moments if m.type == "positive"])
        negative_count = len([m for m in self.moments if m.type == "negative"])
        avg_intensity = sum(m.intensity for m in self.moments) / len(self.moments)

        # Estadísticas principales
        stats = ft.Row([
            ft.Column([
                ft.Text(str(positive_count), size=24, weight=ft.FontWeight.BOLD, color=self.theme.positive_main),
                ft.Text("Positivos", size=12, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text(str(negative_count), size=24, weight=ft.FontWeight.BOLD, color=self.theme.negative_main),
                ft.Text("Difíciles", size=12, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text(f"{avg_intensity:.1f}", size=24, weight=ft.FontWeight.BOLD, color=self.theme.accent_primary),
                ft.Text("Intensidad", size=12, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

        # Últimos momentos
        recent_moments = []
        for moment in self.moments[-3:]:
            recent_moments.append(ft.Row([
                ft.Text(moment.emoji, size=20),
                ft.Text(moment.text, size=14, color=self.theme.text_secondary, expand=True),
                ft.Text(moment.time, size=12, color=self.theme.text_hint)
            ], spacing=12))

        # Botones de acción
        action_buttons = ft.Row([
            create_themed_button("🗑️ Limpiar", self.clear_moments, theme=self.theme,
                                 button_type="negative", width=120, height=40),
            create_themed_button("💾 Guardar Momentos", self.save_moments, theme=self.theme,
                                 button_type="positive", width=180, height=40)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

        return create_themed_container(
            content=ft.Column([
                ft.Text("📈 Resumen del día", size=16, weight=ft.FontWeight.W_600, color=self.theme.text_primary),
                ft.Container(height=16), stats, ft.Container(height=16),
                ft.Text("Últimos momentos:", size=14, weight=ft.FontWeight.W_500, color=self.theme.text_secondary),
                ft.Container(height=8), ft.Column(recent_moments, spacing=8),
                ft.Container(height=20), action_buttons
            ]), theme=self.theme
        )

    # ===============================
    # MÉTODOS DE CONFIGURACIÓN
    # ===============================
    def show_settings_dialog(self, e):
        """Mostrar diálogo de configuración"""
        settings_dialog = ft.AlertDialog(
            title=ft.Text("⚙️ Configuración", size=18, weight=ft.FontWeight.W_500),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Auto-guardar momentos:", size=14, expand=True),
                        ft.Switch(
                            value=self.auto_save_enabled,
                            on_change=self.toggle_auto_save
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Text(
                        "Cuando está activo, cada momento se guarda automáticamente",
                        size=12, color=self.theme.text_hint
                    ),
                    ft.Container(height=16),
                    ft.Row([
                        ft.Text(f"Momentos de hoy: {len(self.moments)}", size=14),
                        ft.Container(expand=True),
                        ft.TextButton(
                            "🗑️ Limpiar todo",
                            on_click=self.confirm_clear_all
                        )
                    ])
                ], tight=True),
                width=300
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=lambda e: self.close_dialog()
                )
            ]
        )

        self.page.dialog = settings_dialog
        settings_dialog.open = True
        self.page.update()

    def toggle_auto_save(self, e):
        """Alternar auto-guardado"""
        self.auto_save_enabled = e.control.value
        status = "activado" if self.auto_save_enabled else "desactivado"
        print(f"🔄 Auto-guardado {status}")

    def close_dialog(self):
        """Cerrar diálogo"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def confirm_clear_all(self, e):
        """Confirmar limpiar todos los momentos"""
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar", color=self.theme.negative_main),
            content=ft.Text("¿Estás seguro de que quieres eliminar TODOS los momentos de hoy?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog()),
                ft.ElevatedButton(
                    "Sí, eliminar todo",
                    on_click=self.clear_all_moments_confirmed,
                    style=ft.ButtonStyle(bgcolor=self.theme.negative_main, color="#FFFFFF")
                )
            ]
        )

        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def clear_all_moments_confirmed(self, e):
        """Eliminar todos los momentos confirmado"""
        try:
            from services import db
            if self.current_user:
                user_id = self.current_user['id']
                success = db.clear_interactive_moments_today(user_id)

                if success:
                    self.moments.clear()
                    self.show_message("🗑️ Todos los momentos eliminados")
                    self.refresh_summary()
                else:
                    self.show_message("❌ Error eliminando momentos", is_error=True)

            self.close_dialog()

        except Exception as ex:
            print(f"❌ Error eliminando momentos: {ex}")
            self.show_message("❌ Error del sistema", is_error=True)
            self.close_dialog()

    # ===============================
    # MÉTODOS DE CONTROL
    # ===============================
    def save_moments(self, e=None):
        """Guardar todos los momentos"""
        if not self.moments:
            self.show_message("⚠️ No hay momentos para guardar", is_error=True)
            return

        print(f"💾 Preparando {len(self.moments)} momentos para entry")

        if self.on_moments_created:
            # Convertir a SimpleTag para compatibilidad con EntryScreen
            simple_tags = [moment.to_simple_tag() for moment in self.moments]
            self.on_moments_created(simple_tags)
            self.show_message(f"✅ {len(self.moments)} momentos enviados a Entry")
        else:
            # Solo confirmación de guardado
            self.show_message(f"✅ {len(self.moments)} momentos guardados")

    def clear_moments(self, e=None):
        """Limpiar momentos"""
        if not self.moments:
            self.show_message("ℹ️ No hay momentos para eliminar")
            return

        # Mostrar diálogo de confirmación
        self.confirm_clear_all(e)

    def refresh_summary(self):
        """Refrescar resumen"""
        if self.summary_container:
            self.summary_container.content = self.build_moments_summary()
        if self.page:
            self.page.update()

    def go_to_calendar(self, e=None):
        """Ir al calendario"""
        if self.page:
            self.page.go("/calendar")

    def go_to_theme_selector(self, e=None):
        """Ir al selector de temas"""
        if self.page:
            self.page.go("/theme_selector")

    def go_back(self, e=None):
        """Volver a Entry"""
        print("🔙 Volviendo a EntryScreen")
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/entry")

    def show_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje"""
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=2000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()