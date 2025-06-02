"""
🎮 Interactive Moments Screen - ReflectApp
Pantalla con 4 modos interactivos para capturar momentos
Basada en el diseño React pero adaptada a Flet
"""

import flet as ft
from datetime import datetime, time
from typing import List, Dict, Any, Optional, Callable
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class InteractiveMoment:
    """Clase para representar un momento interactivo"""
    def __init__(self, emoji: str, text: str, moment_type: str,
                 intensity: int = 5, category: str = "general", hour: Optional[int] = None):
        self.emoji = emoji
        self.text = text
        self.type = moment_type  # "positive" o "negative"
        self.intensity = intensity  # 1-10
        self.category = category  # trabajo, social, salud, etc.
        self.hour = hour or datetime.now().hour
        self.timestamp = datetime.now()

    def to_simple_tag(self):
        """Convertir a SimpleTag para compatibilidad"""
        from screens.new_tag_screen import SimpleTag
        return SimpleTag(
            emoji=self.emoji,
            category=self.type,
            name=f"{self.text} (Intensidad: {self.intensity})",
            reason=f"Momento {self.category} a las {self.hour:02d}:00"
        )

class InteractiveMomentsScreen:
    """Pantalla principal con 4 modos interactivos"""

    def __init__(self, on_moments_created: Callable = None, on_go_back: Callable = None):
        self.on_moments_created = on_moments_created
        self.on_go_back = on_go_back

        # Estado
        self.page = None
        self.theme = get_theme()
        self.active_mode = "quick"  # quick, mood, timeline, templates
        self.moments = []  # Lista de InteractiveMoment

        # Contenedores de los modos
        self.main_container = None
        self.modes_content = {}

        print("🎮 InteractiveMomentsScreen inicializada")

    def build(self):
        """Construir vista principal"""
        self.theme = get_theme()

        # Header
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        header = create_gradient_header(
            title="🎮 Momentos Interactivos",
            left_button=back_button,
            theme=self.theme
        )

        # Descripción
        description = ft.Container(
            content=ft.Text(
                "Experimenta diferentes formas de capturar tus momentos del día",
                size=14,
                color=self.theme.text_secondary,
                text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.only(bottom=20),
            alignment=ft.alignment.center
        )

        # Selector de modos
        mode_selector = self.build_mode_selector()

        # Contenedor principal que cambia según el modo
        self.main_container = ft.Container(
            content=self.build_quick_mode(),  # Empezar con quick mode
            expand=True
        )

        # Resumen de momentos
        summary = self.build_moments_summary()

        # Vista completa
        content = ft.Column(
            [
                description,
                mode_selector,
                ft.Container(height=20),
                self.main_container,
                ft.Container(height=20),
                summary
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0
        )

        view = ft.View(
            "/interactive_moments",
            [
                header,
                ft.Container(
                    content=content,
                    padding=ft.padding.all(20),
                    expand=True
                )
            ],
            bgcolor=self.theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def build_mode_selector(self):
        """Construir selector de modos"""
        modes = [
            {"id": "quick", "name": "Quick Add", "emoji": "⚡", "desc": "Emojis rápidos"},
            {"id": "mood", "name": "Mood Bubbles", "emoji": "🎭", "desc": "Burbujas con intensidad"},
            {"id": "timeline", "name": "Timeline", "emoji": "⏰", "desc": "Línea de tiempo"},
            {"id": "templates", "name": "Templates", "emoji": "🎯", "desc": "Situaciones comunes"}
        ]

        mode_buttons = []
        for i, mode in enumerate(modes):
            if i % 2 == 0:  # Crear nueva fila cada 2 botones
                row = ft.Row(spacing=12, alignment=ft.MainAxisAlignment.CENTER)
                mode_buttons.append(row)

            button = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(mode["emoji"], size=28),
                        ft.Text(mode["name"], size=14, weight=ft.FontWeight.W_600,
                                color=self.theme.text_primary),
                        ft.Text(mode["desc"], size=12, color=self.theme.text_secondary)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4
                ),
                width=160,
                height=100,
                padding=ft.padding.all(16),
                border_radius=16,
                bgcolor=self.theme.accent_primary + "20" if self.active_mode == mode["id"] else self.theme.surface,
                border=ft.border.all(
                    2 if self.active_mode == mode["id"] else 1,
                    self.theme.accent_primary if self.active_mode == mode["id"] else self.theme.border_color
                ),
                on_click=lambda e, mode_id=mode["id"]: self.switch_mode(mode_id)
            )

            mode_buttons[-1].controls.append(button)

        return ft.Column(mode_buttons, spacing=12)

    def switch_mode(self, mode_id: str):
        """Cambiar entre modos"""
        print(f"🔄 Cambiando a modo: {mode_id}")
        self.active_mode = mode_id

        # Actualizar contenido principal
        if mode_id == "quick":
            new_content = self.build_quick_mode()
        elif mode_id == "mood":
            new_content = self.build_mood_mode()
        elif mode_id == "timeline":
            new_content = self.build_timeline_mode()
        elif mode_id == "templates":
            new_content = self.build_templates_mode()

        self.main_container.content = new_content

        # Actualizar selector de modos
        if self.page:
            self.page.update()

    def build_quick_mode(self):
        """Construir modo Quick Add"""
        # Entrada de texto rápido
        self.quick_text_field = ft.TextField(
            hint_text="¿Qué pasó? (ej: 'Desayuno delicioso', 'Reunión eterna')",
            border_radius=16,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(16),
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
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color),
                on_click=lambda e, p=phrase: self.set_quick_text(p)
            )
            phrase_buttons.append(btn)

        phrases_container = ft.Wrap(
            children=phrase_buttons,
            spacing=8,
            run_spacing=8
        )

        # Emojis por categorías
        emoji_sections = self.build_emoji_sections()

        return ft.Column(
            [
                ft.Text("⚡ Quick Add", size=20, weight=ft.FontWeight.BOLD,
                        color=self.theme.text_primary),
                ft.Container(height=16),

                # Campo de texto
                create_themed_container(
                    content=self.quick_text_field,
                    theme=self.theme
                ),

                ft.Container(height=16),

                # Frases rápidas
                create_themed_container(
                    content=ft.Column(
                        [
                            ft.Text("⚡ Frases rápidas:", size=14, weight=ft.FontWeight.W_500,
                                    color=self.theme.text_secondary),
                            ft.Container(height=8),
                            phrases_container
                        ]
                    ),
                    theme=self.theme
                ),

                ft.Container(height=16),

                # Secciones de emojis
                emoji_sections
            ],
            scroll=ft.ScrollMode.AUTO
        )

    def build_emoji_sections(self):
        """Construir secciones de emojis para Quick Add"""

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

        sections = []

        # Sección positiva
        positive_section = self.build_emoji_category_section(
            "✨ Momentos Positivos",
            emoji_categories["positive"],
            "positive",
            self.theme.positive_main,
            self.theme.positive_light
        )
        sections.append(positive_section)

        sections.append(ft.Container(height=16))

        # Sección negativa
        negative_section = self.build_emoji_category_section(
            "🌧️ Momentos Difíciles",
            emoji_categories["negative"],
            "negative",
            self.theme.negative_main,
            self.theme.negative_light
        )
        sections.append(negative_section)

        return ft.Column(sections)

    def build_emoji_category_section(self, title: str, categories: Dict, moment_type: str,
                                     main_color: str, light_color: str):
        """Construir una sección de categoría de emojis"""

        category_columns = []

        for category_name, emojis in categories.items():
            # Título de categoría
            category_title = ft.Text(
                category_name.title(),
                size=12,
                color=self.theme.text_hint,
                weight=ft.FontWeight.W_500
            )

            # Botones de emojis
            emoji_buttons = []
            for emoji in emojis:
                btn = ft.Container(
                    content=ft.Text(emoji, size=24),
                    width=50,
                    height=50,
                    border_radius=12,
                    bgcolor=self.theme.surface,
                    border=ft.border.all(1, self.theme.border_color),
                    alignment=ft.alignment.center,
                    on_click=lambda e, em=emoji, cat=category_name: self.add_quick_moment(em, moment_type, cat)
                )
                emoji_buttons.append(btn)

            emoji_grid = ft.Wrap(
                children=emoji_buttons,
                spacing=8,
                run_spacing=8
            )

            category_columns.append(
                ft.Column(
                    [
                        category_title,
                        ft.Container(height=8),
                        emoji_grid
                    ],
                    spacing=0
                )
            )

        content = ft.Column(
            [
                ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=main_color),
                ft.Container(height=12)
            ] + category_columns,
            spacing=12
        )

        return create_themed_container(
            content=content,
            theme=self.theme,
            add_border=True,
            border_radius=16
        )

    def set_quick_text(self, text: str):
        """Establecer texto rápido"""
        if self.quick_text_field:
            self.quick_text_field.value = text
            if self.page:
                self.page.update()

    def add_quick_moment(self, emoji: str, moment_type: str, category: str):
        """Añadir momento rápido"""
        if not hasattr(self, 'quick_text_field') or not self.quick_text_field.value:
            self.show_message("⚠️ Escribe qué pasó antes de seleccionar emoji", is_error=True)
            return

        moment = InteractiveMoment(
            emoji=emoji,
            text=self.quick_text_field.value.strip(),
            moment_type=moment_type,
            intensity=7 if moment_type == "positive" else 6,
            category=category
        )

        self.moments.append(moment)
        self.quick_text_field.value = ""

        self.show_message(f"✅ Momento {moment_type} añadido: {emoji} {moment.text}")
        self.refresh_summary()

    def build_mood_mode(self):
        """Construir modo Mood Bubbles con slider de intensidad"""

        # Estado del slider (inicializar si no existe)
        if not hasattr(self, 'current_intensity'):
            self.current_intensity = 5

        # Slider de intensidad
        intensity_section = self.build_intensity_slider()

        # Burbujas de emociones
        bubbles_section = self.build_mood_bubbles()

        return ft.Column(
            [
                ft.Text("🎭 Mood Bubbles", size=20, weight=ft.FontWeight.BOLD,
                        color=self.theme.text_primary),
                ft.Container(height=16),

                intensity_section,
                ft.Container(height=20),
                bubbles_section
            ],
            scroll=ft.ScrollMode.AUTO
        )

    def build_intensity_slider(self):
        """Construir slider de intensidad visual"""

        # Slider
        self.intensity_slider = ft.Slider(
            min=1,
            max=10,
            value=self.current_intensity,
            divisions=9,
            on_change=self.on_intensity_change,
            active_color=self.get_intensity_color(self.current_intensity),
            thumb_color=self.get_intensity_color(self.current_intensity)
        )

        # Indicadores visuales
        intensity_indicators = []
        for i in range(1, 11):
            size = 8 if i != self.current_intensity else 12
            opacity = 0.3 if i != self.current_intensity else 1.0
            color = self.get_intensity_color(i)

            indicator = ft.Container(
                width=size,
                height=size,
                border_radius=size // 2,
                bgcolor=color,
                opacity=opacity
            )
            intensity_indicators.append(indicator)

        indicators_row = ft.Row(
            intensity_indicators,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text("🎚️ Intensidad del momento", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=12),

                    # Emojis de referencia
                    ft.Row(
                        [
                            ft.Text("😐", size=24),
                            ft.Container(expand=True),
                            ft.Text("🤯", size=24)
                        ]
                    ),
                    ft.Container(height=8),

                    # Slider
                    self.intensity_slider,
                    ft.Container(height=8),

                    # Indicadores
                    indicators_row,
                    ft.Container(height=12),

                    # Valor actual
                    ft.Column(
                        [
                            ft.Text(f"{int(self.current_intensity)}/10",
                                    size=24, weight=ft.FontWeight.BOLD,
                                    color=self.get_intensity_color(self.current_intensity),
                                    text_align=ft.TextAlign.CENTER),
                            ft.Text(self.get_intensity_label(self.current_intensity),
                                    size=14, color=self.theme.text_secondary,
                                    text_align=ft.TextAlign.CENTER)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ]
            ),
            theme=self.theme
        )

    def build_mood_bubbles(self):
        """Construir burbujas de emociones"""

        bubble_options = [
            {"emoji": "😊", "text": "Alegre", "type": "positive"},
            {"emoji": "🎉", "text": "Emocionado", "type": "positive"},
            {"emoji": "😌", "text": "Tranquilo", "type": "positive"},
            {"emoji": "💪", "text": "Motivado", "type": "positive"},
            {"emoji": "😰", "text": "Estresado", "type": "negative"},
            {"emoji": "😔", "text": "Triste", "type": "negative"},
            {"emoji": "😤", "text": "Frustrado", "type": "negative"},
            {"emoji": "😫", "text": "Agotado", "type": "negative"}
        ]

        # Crear burbujas en grid 2x4
        bubble_rows = []
        for i in range(0, len(bubble_options), 2):
            row_bubbles = []
            for j in range(2):
                if i + j < len(bubble_options):
                    bubble = bubble_options[i + j]
                    bubble_widget = self.create_mood_bubble(bubble)
                    row_bubbles.append(bubble_widget)

            if row_bubbles:
                bubble_rows.append(
                    ft.Row(
                        row_bubbles,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        spacing=16
                    )
                )

        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text("🫧 Toca una burbuja de emoción", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=16)
                ] + bubble_rows,
                spacing=16
            ),
            theme=self.theme
        )

    def create_mood_bubble(self, bubble_data):
        """Crear una burbuja de emoción individual"""
        is_positive = bubble_data["type"] == "positive"
        base_color = self.theme.positive_main if is_positive else self.theme.negative_main
        light_color = self.theme.positive_light if is_positive else self.theme.negative_light

        # Crear indicadores de intensidad
        intensity_dots = []
        intensity_level = int(self.current_intensity // 2) + 1  # 1-5 dots
        for i in range(5):
            opacity = 1.0 if i < intensity_level else 0.3
            size = 6 if i < intensity_level else 4

            dot = ft.Container(
                width=size,
                height=size,
                border_radius=size // 2,
                bgcolor=base_color,
                opacity=opacity
            )
            intensity_dots.append(dot)

        dots_row = ft.Row(
            intensity_dots,
            spacing=3,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Crear burbuja
        bubble = ft.Container(
            content=ft.Column(
                [
                    ft.Text(bubble_data["emoji"], size=36),
                    ft.Container(height=8),
                    ft.Text(bubble_data["text"], size=14, weight=ft.FontWeight.W_500,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    dots_row
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            ),
            width=160,
            height=140,
            padding=ft.padding.all(16),
            border_radius=20,
            bgcolor=light_color,
            border=ft.border.all(2, base_color + "50"),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=base_color + "30",
                offset=ft.Offset(0, 4)
            ),
            on_click=lambda e, bubble=bubble_data: self.create_mood_moment(bubble),
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT)
        )

        return bubble

    def on_intensity_change(self, e):
        """Callback cuando cambia la intensidad"""
        self.current_intensity = e.control.value

        # Actualizar color del slider
        new_color = self.get_intensity_color(self.current_intensity)
        e.control.active_color = new_color
        e.control.thumb_color = new_color

        if self.page:
            self.page.update()

    def get_intensity_color(self, intensity):
        """Obtener color según intensidad"""
        if intensity <= 3:
            return self.theme.negative_main
        elif intensity <= 7:
            return "#F59E0B"  # Amarillo/naranja
        else:
            return self.theme.positive_main

    def get_intensity_label(self, intensity):
        """Obtener etiqueta según intensidad"""
        if intensity <= 3:
            return "Suave"
        elif intensity <= 7:
            return "Moderado"
        else:
            return "Intenso"

    def create_mood_moment(self, bubble_data):
        """Crear momento desde burbuja de emoción"""
        moment = InteractiveMoment(
            emoji=bubble_data["emoji"],
            text=f"{bubble_data['text']} (Intensidad {int(self.current_intensity)})",
            moment_type=bubble_data["type"],
            intensity=int(self.current_intensity),
            category="mood"
        )

        self.moments.append(moment)

        # Efecto visual de feedback
        self.show_bubble_feedback(bubble_data["emoji"])

        self.show_message(f"✅ {bubble_data['emoji']} {bubble_data['text']} añadido con intensidad {int(self.current_intensity)}")
        self.refresh_summary()

    def show_bubble_feedback(self, emoji):
        """Mostrar feedback visual cuando se presiona una burbuja"""
        # Por ahora solo mensaje, pero podrías añadir animaciones más elaboradas
        pass

    def build_timeline_mode(self):
        """Construir modo Timeline por horas"""

        # Inicializar hora seleccionada si no existe
        if not hasattr(self, 'selected_hour'):
            self.selected_hour = datetime.now().hour

        # Selector de horas
        hour_selector = self.build_hour_selector()

        # Formulario para añadir momento
        moment_form = self.build_timeline_moment_form()

        # Timeline visual
        timeline_visual = self.build_timeline_visual()

        return ft.Column(
            [
                ft.Text("⏰ Timeline del Día", size=20, weight=ft.FontWeight.BOLD,
                        color=self.theme.text_primary),
                ft.Container(height=16),

                hour_selector,
                ft.Container(height=16),
                moment_form,
                ft.Container(height=16),
                timeline_visual
            ],
            scroll=ft.ScrollMode.AUTO
        )

    def build_hour_selector(self):
        """Construir selector visual de horas"""
        current_hour = datetime.now().hour

        # Crear botones de horas
        hour_buttons = []
        for hour in range(24):
            moment_at_hour = self.get_moment_for_hour(hour)
            is_past = hour < current_hour
            is_current = hour == current_hour
            is_selected = hour == self.selected_hour

            # Determinar estilo del botón
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

            # Opacidad para horas pasadas sin momentos
            opacity = 0.5 if is_past and not moment_at_hour else 1.0

            # Contenido del botón
            if moment_at_hour:
                content = ft.Column(
                    [
                        ft.Text(f"{hour:02d}:00", size=10, color=self.theme.text_secondary),
                        ft.Text(moment_at_hour.emoji, size=16)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            else:
                indicator_color = "#FFA500" if is_current else self.theme.border_color
                content = ft.Column(
                    [
                        ft.Text(f"{hour:02d}:00", size=10, color=self.theme.text_secondary),
                        ft.Container(
                            width=8,
                            height=8,
                            border_radius=4,
                            bgcolor=indicator_color
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )

            button = ft.Container(
                content=content,
                width=60,
                height=50,
                border_radius=8,
                bgcolor=bg_color,
                border=ft.border.all(border_width, border_color),
                opacity=opacity,
                on_click=lambda e, h=hour: self.select_hour(h)
            )

            hour_buttons.append(button)

        # Organizar en filas de 6 horas
        hour_rows = []
        for i in range(0, 24, 6):
            row = ft.Row(
                hour_buttons[i:i+6],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER
            )
            hour_rows.append(row)

        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text("🕐 Selecciona la hora", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=12)
                ] + hour_rows,
                spacing=8
            ),
            theme=self.theme
        )

    def build_timeline_moment_form(self):
        """Construir formulario para añadir momento a hora específica"""

        self.timeline_text_field = ft.TextField(
            hint_text="Describe qué pasó en esta hora...",
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(color=self.theme.text_primary)
        )

        # Botones de tipo de momento
        positive_btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("✨", size=16),
                    ft.Text("Positivo", size=14)
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            on_click=lambda e: self.add_timeline_moment("positive"),
            style=ft.ButtonStyle(
                bgcolor=self.theme.positive_main,
                color="#FFFFFF",
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            height=45,
            expand=True
        )

        negative_btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("🌧️", size=16),
                    ft.Text("Difícil", size=14)
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            on_click=lambda e: self.add_timeline_moment("negative"),
            style=ft.ButtonStyle(
                bgcolor=self.theme.negative_main,
                color="#FFFFFF",
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            height=45,
            expand=True
        )

        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text(f"📝 ¿Qué pasó a las {self.selected_hour:02d}:00?",
                            size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=12),

                    self.timeline_text_field,
                    ft.Container(height=16),

                    ft.Row(
                        [positive_btn, ft.Container(width=12), negative_btn],
                        expand=True
                    )
                ]
            ),
            theme=self.theme
        )

    def build_timeline_visual(self):
        """Construir visualización de timeline"""

        if not self.moments:
            return create_themed_container(
                content=ft.Text(
                    "No hay momentos en el timeline aún",
                    color=self.theme.text_hint,
                    text_align=ft.TextAlign.CENTER
                ),
                theme=self.theme
            )

        # Ordenar momentos por hora
        timeline_moments = sorted(self.moments, key=lambda m: m.hour)

        moment_widgets = []
        for moment in timeline_moments:
            moment_widget = ft.Container(
                content=ft.Row(
                    [
                        # Hora
                        ft.Container(
                            content=ft.Text(f"{moment.hour:02d}:00",
                                            size=12, weight=ft.FontWeight.W_500,
                                            color=self.theme.text_hint),
                            width=60
                        ),

                        # Emoji
                        ft.Text(moment.emoji, size=20),

                        # Texto
                        ft.Text(moment.text, size=14, color=self.theme.text_secondary, expand=True),

                        # Indicador de tipo
                        ft.Container(
                            width=8,
                            height=8,
                            border_radius=4,
                            bgcolor=self.theme.positive_main if moment.type == "positive" else self.theme.negative_main
                        )
                    ],
                    spacing=12,
                    alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8),
                border_radius=8,
                bgcolor=self.theme.surface + "50",
                border=ft.border.all(1, self.theme.border_color)
            )
            moment_widgets.append(moment_widget)

        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text("📊 Tu línea de tiempo", size=14, weight=ft.FontWeight.W_500,
                            color=self.theme.text_secondary),
                    ft.Container(height=12),
                    ft.Column(moment_widgets, spacing=0)
                ]
            ),
            theme=self.theme
        )

    def select_hour(self, hour: int):
        """Seleccionar hora específica"""
        self.selected_hour = hour
        print(f"⏰ Hora seleccionada: {hour:02d}:00")
        if self.page:
            self.page.update()

    def add_timeline_moment(self, moment_type: str):
        """Añadir momento al timeline"""
        if not hasattr(self, 'timeline_text_field') or not self.timeline_text_field.value:
            self.show_message("⚠️ Describe qué pasó antes de añadir", is_error=True)
            return

        # Verificar si ya hay momento en esa hora
        existing_moment = self.get_moment_for_hour(self.selected_hour)
        if existing_moment:
            self.show_message(f"⚠️ Ya hay un momento a las {self.selected_hour:02d}:00", is_error=True)
            return

        moment = InteractiveMoment(
            emoji="⭐" if moment_type == "positive" else "🌧️",
            text=self.timeline_text_field.value.strip(),
            moment_type=moment_type,
            intensity=7 if moment_type == "positive" else 6,
            category="timeline",
            hour=self.selected_hour
        )

        self.moments.append(moment)
        self.timeline_text_field.value = ""

        self.show_message(f"✅ Momento añadido a las {self.selected_hour:02d}:00")
        self.refresh_summary()

    def get_moment_for_hour(self, hour: int):
        """Obtener momento para hora específica"""
        for moment in self.moments:
            if moment.hour == hour:
                return moment
        return None

    def build_templates_mode(self):
        """Construir modo Templates predefinidos"""

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
                    {"emoji": "💻", "text": "Problemas técnicos", "type": "negative"},
                    {"emoji": "😴", "text": "Reunión aburrida", "type": "negative"}
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
                    {"emoji": "📱", "text": "Demasiado tiempo en redes", "type": "negative"},
                    {"emoji": "💔", "text": "Discusión familiar", "type": "negative"}
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
                    {"emoji": "🍔", "text": "Comí mal todo el día", "type": "negative"},
                    {"emoji": "😪", "text": "Muy cansado/a", "type": "negative"}
                ]
            },
            "personal": {
                "title": "🌱 Crecimiento Personal",
                "color": "#8B5CF6",
                "items": [
                    {"emoji": "📚", "text": "Aprendí algo nuevo", "type": "positive"},
                    {"emoji": "✨", "text": "Momento de inspiración", "type": "positive"},
                    {"emoji": "🎨", "text": "Expresé mi creatividad", "type": "positive"},
                    {"emoji": "🙏", "text": "Momento de gratitud", "type": "positive"},
                    {"emoji": "😰", "text": "Me sentí abrumado/a", "type": "negative"},
                    {"emoji": "🤔", "text": "Dudas sobre el futuro", "type": "negative"},
                    {"emoji": "😞", "text": "Baja autoestima", "type": "negative"},
                    {"emoji": "😤", "text": "Frustración conmigo mismo/a", "type": "negative"}
                ]
            }
        }

        template_sections = []
        for category, template in templates.items():
            section = self.build_template_section(category, template)
            template_sections.append(section)
            template_sections.append(ft.Container(height=16))

        return ft.Column(
            [
                ft.Text("🎯 Templates", size=20, weight=ft.FontWeight.BOLD,
                        color=self.theme.text_primary),
                ft.Container(height=8),
                ft.Text("Situaciones comunes organizadas por categorías",
                        size=14, color=self.theme.text_secondary,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=16)
            ] + template_sections[:-1],  # Eliminar último Container
            scroll=ft.ScrollMode.AUTO
        )

    def build_template_section(self, category: str, template: dict):
        """Construir sección de template por categoría"""

        # Header de la sección
        header = ft.Row(
            [
                ft.Text(template["title"], size=16, weight=ft.FontWeight.W_600,
                        color=template["color"]),
                ft.Container(
                    content=ft.Text(f"{len(template['items'])} opciones",
                                    size=12, color=self.theme.text_hint),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                    bgcolor=template["color"] + "20"
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Items del template
        template_items = []
        for item in template["items"]:
            item_widget = self.build_template_item(item, category, template["color"])
            template_items.append(item_widget)

        return create_themed_container(
            content=ft.Column(
                [header, ft.Container(height=12)] + template_items,
                spacing=8
            ),
            theme=self.theme,
            add_border=True,
            border_radius=16
        )

    def build_template_item(self, item: dict, category: str, color: str):
        """Construir item individual de template"""

        is_positive = item["type"] == "positive"
        bg_color = (self.theme.positive_light if is_positive else self.theme.negative_light) + "30"
        border_color = self.theme.positive_main if is_positive else self.theme.negative_main

        return ft.Container(
            content=ft.Row(
                [
                    # Emoji
                    ft.Container(
                        content=ft.Text(item["emoji"], size=20),
                        width=40,
                        alignment=ft.alignment.center
                    ),

                    # Texto
                    ft.Text(item["text"], size=14, color=self.theme.text_primary, expand=True),

                    # Botón de añadir
                    ft.Container(
                        content=ft.Text("+", size=16, weight=ft.FontWeight.BOLD,
                                        color=border_color),
                        width=30,
                        height=30,
                        border_radius=15,
                        bgcolor=bg_color,
                        border=ft.border.all(1, border_color),
                        alignment=ft.alignment.center
                    )
                ],
                spacing=12,
                alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(12),
            border_radius=12,
            bgcolor=bg_color,
            border=ft.border.all(1, border_color + "50"),
            on_click=lambda e, it=item, cat=category: self.add_template_item(item, cat),
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT)
        )

    def add_template_item(self, item: dict, category: str):
        """Añadir item de template como momento"""

        moment = InteractiveMoment(
            emoji=item["emoji"],
            text=item["text"],
            moment_type=item["type"],
            intensity=7 if item["type"] == "positive" else 6,
            category=category
        )

        self.moments.append(moment)

        self.show_message(f"✅ {item['emoji']} {item['text']} añadido")
        self.refresh_summary()

    def build_moments_summary(self):
        """Construir resumen de momentos"""
        if not self.moments:
            return ft.Container(
                content=ft.Text(
                    "No hay momentos añadidos aún",
                    color=self.theme.text_hint,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=ft.padding.all(20)
            )

        positive_count = len([m for m in self.moments if m.type == "positive"])
        negative_count = len([m for m in self.moments if m.type == "negative"])
        avg_intensity = sum(m.intensity for m in self.moments) / len(self.moments)

        # Estadísticas
        stats = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(str(positive_count), size=24, weight=ft.FontWeight.BOLD,
                                color=self.theme.positive_main),
                        ft.Text("Positivos", size=12, color=self.theme.text_hint)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        ft.Text(str(negative_count), size=24, weight=ft.FontWeight.BOLD,
                                color=self.theme.negative_main),
                        ft.Text("Difíciles", size=12, color=self.theme.text_hint)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    [
                        ft.Text(f"{avg_intensity:.1f}", size=24, weight=ft.FontWeight.BOLD,
                                color=self.theme.accent_primary),
                        ft.Text("Intensidad", size=12, color=self.theme.text_hint)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )

        # Lista de momentos recientes
        recent_moments = []
        for moment in self.moments[-3:]:  # Últimos 3
            recent_moments.append(
                ft.Row(
                    [
                        ft.Text(moment.emoji, size=20),
                        ft.Text(moment.text, size=14, color=self.theme.text_secondary, expand=True),
                        ft.Text(f"{moment.hour:02d}:00", size=12, color=self.theme.text_hint)
                    ],
                    spacing=12
                )
            )

        # Botones de acción
        action_buttons = ft.Row(
            [
                create_themed_button(
                    "🗑️ Limpiar",
                    self.clear_moments,
                    theme=self.theme,
                    button_type="negative",
                    width=120,
                    height=40
                ),
                create_themed_button(
                    "✅ Guardar Momentos",
                    self.save_moments,
                    theme=self.theme,
                    button_type="positive",
                    width=180,
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )

        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text("📈 Resumen del día", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=16),
                    stats,
                    ft.Container(height=16),
                    ft.Text("Últimos momentos:", size=14, weight=ft.FontWeight.W_500,
                            color=self.theme.text_secondary),
                    ft.Container(height=8),
                    ft.Column(recent_moments, spacing=8),
                    ft.Container(height=20),
                    action_buttons
                ]
            ),
            theme=self.theme
        )

    def refresh_summary(self):
        """Refrescar resumen de momentos"""
        if self.page:
            self.page.update()

    def clear_moments(self, e=None):
        """Limpiar todos los momentos"""
        self.moments.clear()
        self.show_message("🗑️ Momentos eliminados")
        self.refresh_summary()

    def save_moments(self, e=None):
        """Guardar momentos y volver"""
        if not self.moments:
            self.show_message("⚠️ No hay momentos para guardar", is_error=True)
            return

        if self.on_moments_created:
            # Convertir a SimpleTag para compatibilidad
            simple_tags = [moment.to_simple_tag() for moment in self.moments]
            self.on_moments_created(simple_tags)

        self.show_message(f"✅ {len(self.moments)} momentos guardados")

        # Volver después de un delay
        if self.page:
            def delayed_back():
                if self.on_go_back:
                    self.on_go_back()
                else:
                    self.page.go("/entry")

            # Simular delay
            import threading
            threading.Timer(1.5, delayed_back).start()

    def show_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje al usuario"""
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF"),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=2000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()

    def go_back(self, e=None):
        """Volver a la pantalla anterior"""
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/entry")