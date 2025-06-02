"""
📝 Daily Review Screen - NUEVA PANTALLA MODERNA
Pantalla para revisar y completar el día con reflexión y evaluación final
"""

import flet as ft
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Callable
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class DailyReviewScreen:
    """Pantalla moderna para revisar el día completo"""

    def __init__(self, app=None, user_data=None, on_go_back: Callable = None):
        self.app = app
        self.user_data = user_data
        self.on_go_back = on_go_back

        # Estado
        self.page = None
        self.theme = get_theme()

        # Datos del día
        self.moments_data = {"positive": [], "negative": []}
        self.reflection_field = None
        self.worth_it_value = None
        self.mood_score = 5

        # UI Components
        self.worth_it_buttons = []
        self.mood_slider = None

        print("📝 DailyReviewScreen inicializada")

    def build(self):
        """Construir vista principal"""
        self.theme = get_theme()

        # Cargar datos del día
        self.load_today_data()

        # Header
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        user_name = self.user_data.get('name', 'Viajero') if self.user_data else 'Viajero'
        today_str = date.today().strftime("%d %b")

        header = create_gradient_header(
            title=f"📝 Revisa tu día - {today_str}",
            left_button=back_button,
            theme=self.theme
        )

        # Contenido principal
        content = ft.Column([
            # Introducción
            self.build_intro_section(),
            ft.Container(height=16),

            # Resumen de momentos
            self.build_moments_summary(),
            ft.Container(height=16),

            # Reflexión libre
            self.build_reflection_section(),
            ft.Container(height=16),

            # Evaluación del día
            self.build_worth_it_section(),
            ft.Container(height=16),

            # Mood score
            self.build_mood_section(),
            ft.Container(height=20),

            # Botones de acción
            self.build_action_buttons(),
            ft.Container(height=20)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        # Vista completa
        view = ft.View(
            "/daily_review",
            [
                header,
                ft.Container(
                    content=content,
                    padding=ft.padding.all(16),
                    expand=True
                )
            ],
            bgcolor=self.theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def load_today_data(self):
        """Cargar datos del día actual"""
        if not self.user_data:
            print("⚠️ No hay datos de usuario")
            return

        try:
            from services import db
            user_id = self.user_data['id']

            print(f"📚 Cargando datos del día para usuario {user_id}")

            # Cargar momentos interactivos
            moments = db.get_interactive_moments_today(user_id)

            # Separar por tipo
            self.moments_data = {"positive": [], "negative": []}
            for moment in moments:
                if moment['type'] == 'positive':
                    self.moments_data['positive'].append(moment)
                else:
                    self.moments_data['negative'].append(moment)

            print(f"📊 Cargados: {len(self.moments_data['positive'])} positivos, {len(self.moments_data['negative'])} negativos")

            # Cargar entrada existente si existe
            entries = db.get_user_entries(user_id, limit=1)
            if entries and entries[0]['entry_date'] == date.today().isoformat():
                entry = entries[0]
                self.reflection_text = entry.get('free_reflection', '')
                self.worth_it_value = entry.get('worth_it')
                self.mood_score = entry.get('mood_score', 5)
                print(f"📄 Entrada existente cargada")
            else:
                self.reflection_text = ""
                print(f"📄 No hay entrada previa")

        except Exception as e:
            print(f"❌ Error cargando datos del día: {e}")
            self.moments_data = {"positive": [], "negative": []}
            self.reflection_text = ""

    def build_intro_section(self):
        """Sección de introducción"""
        total_moments = len(self.moments_data['positive']) + len(self.moments_data['negative'])

        if total_moments > 0:
            intro_text = f"Has registrado {total_moments} momentos hoy. Es hora de reflexionar sobre tu día completo."
            intro_emoji = "🌟"
        else:
            intro_text = "Aún no has registrado momentos específicos, pero puedes reflexionar sobre tu día."
            intro_emoji = "💭"

        return create_themed_container(
            content=ft.Column([
                ft.Row([
                    ft.Text(intro_emoji, size=32),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text("Hora de reflexionar", size=18, weight=ft.FontWeight.BOLD,
                                color=self.theme.text_primary),
                        ft.Text(intro_text, size=14, color=self.theme.text_secondary)
                    ], expand=True)
                ], alignment=ft.CrossAxisAlignment.CENTER)
            ]),
            theme=self.theme
        )

    def build_moments_summary(self):
        """Resumen visual de momentos del día"""
        positive_count = len(self.moments_data['positive'])
        negative_count = len(self.moments_data['negative'])

        if positive_count == 0 and negative_count == 0:
            return create_themed_container(
                content=ft.Column([
                    ft.Text("📋 Momentos del día", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=12),
                    ft.Text("No hay momentos específicos registrados. Puedes usar la reflexión libre abajo.",
                            size=13, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER)
                ]),
                theme=self.theme
            )

        # Estadísticas
        stats_row = ft.Row([
            ft.Column([
                ft.Text(str(positive_count), size=24, weight=ft.FontWeight.BOLD,
                        color=self.theme.positive_main),
                ft.Text("Positivos", size=12, color=self.theme.text_secondary)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

            ft.Container(width=2, height=40, bgcolor=self.theme.border_color),

            ft.Column([
                ft.Text(str(negative_count), size=24, weight=ft.FontWeight.BOLD,
                        color=self.theme.negative_main),
                ft.Text("Difíciles", size=12, color=self.theme.text_secondary)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

        # Muestra de momentos recientes
        recent_moments = []
        all_moments = self.moments_data['positive'] + self.moments_data['negative']

        # Ordenar por tiempo y tomar los últimos 3
        sorted_moments = sorted(all_moments, key=lambda x: x.get('time', '00:00'), reverse=True)[:3]

        for moment in sorted_moments:
            color = self.theme.positive_main if moment['type'] == 'positive' else self.theme.negative_main
            recent_moments.append(
                ft.Row([
                    ft.Text(moment['emoji'], size=16),
                    ft.Text(moment['text'], size=13, color=self.theme.text_secondary, expand=True),
                    ft.Text(moment['time'], size=11, color=self.theme.text_hint),
                    ft.Container(width=4, height=4, border_radius=2, bgcolor=color)
                ], spacing=8)
            )

        return create_themed_container(
            content=ft.Column([
                ft.Text("📋 Momentos del día", size=16, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=12),
                stats_row,
                ft.Container(height=16),
                ft.Text("Últimos momentos:", size=13, weight=ft.FontWeight.W_500,
                        color=self.theme.text_secondary),
                ft.Container(height=8),
                ft.Column(recent_moments, spacing=6) if recent_moments else ft.Text("Sin momentos recientes",
                                                                                    size=12, color=self.theme.text_hint)
            ]),
            theme=self.theme
        )

    def build_reflection_section(self):
        """Sección de reflexión libre"""
        self.reflection_field = ft.TextField(
            label="¿Cómo fue tu día? Reflexiona libremente...",
            multiline=True,
            min_lines=4,
            max_lines=6,
            value=getattr(self, 'reflection_text', ''),
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(color=self.theme.text_primary)
        )

        # Prompts de ayuda
        prompts = [
            "¿Qué aprendiste hoy?",
            "¿Qué te hizo sonreír?",
            "¿Qué cambiarías?",
            "¿Cómo te sientes ahora?"
        ]

        prompt_buttons = []
        for i in range(0, len(prompts), 2):
            row = []
            for j in range(2):
                if i + j < len(prompts):
                    prompt = prompts[i + j]
                    btn = ft.Container(
                        content=ft.Text(prompt, size=11, color=self.theme.text_secondary,
                                        text_align=ft.TextAlign.CENTER),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        border_radius=16,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        on_click=lambda e, p=prompt: self.add_prompt_to_reflection(p),
                        expand=True
                    )
                    row.append(btn)
            if row:
                prompt_buttons.append(ft.Row(row, spacing=8))

        return create_themed_container(
            content=ft.Column([
                ft.Text("💭 Reflexión libre", size=16, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=12),
                self.reflection_field,
                ft.Container(height=12),
                ft.Text("💡 Ideas para reflexionar:", size=13, weight=ft.FontWeight.W_500,
                        color=self.theme.text_secondary),
                ft.Container(height=8),
                ft.Column(prompt_buttons, spacing=6)
            ]),
            theme=self.theme
        )

    def build_worth_it_section(self):
        """Sección de evaluación final del día"""
        self.worth_it_buttons = []

        # Opciones
        options = [
            {"value": True, "emoji": "😊", "text": "SÍ, mereció la pena", "color": self.theme.positive_main},
            {"value": False, "emoji": "😔", "text": "NO, no mereció la pena", "color": self.theme.negative_main},
            {"value": None, "emoji": "🤷", "text": "No estoy seguro/a", "color": self.theme.text_hint}
        ]

        option_widgets = []
        for option in options:
            is_selected = self.worth_it_value == option["value"]

            btn = ft.Container(
                content=ft.Row([
                    ft.Text(option["emoji"], size=24),
                    ft.Container(width=12),
                    ft.Text(option["text"], size=14, weight=ft.FontWeight.W_500,
                            color=self.theme.text_primary, expand=True),
                    ft.Container(
                        width=20, height=20, border_radius=10,
                        bgcolor=option["color"] if is_selected else "transparent",
                        border=ft.border.all(2, option["color"])
                    )
                ], alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16),
                border_radius=12,
                bgcolor=option["color"] + "15" if is_selected else self.theme.surface,
                border=ft.border.all(2 if is_selected else 1,
                                     option["color"] if is_selected else self.theme.border_color),
                on_click=lambda e, val=option["value"]: self.set_worth_it(val)
            )

            self.worth_it_buttons.append(btn)
            option_widgets.append(btn)

        return create_themed_container(
            content=ft.Column([
                ft.Text("⚖️ ¿Mereció la pena el día?", size=16, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=12),
                ft.Column(option_widgets, spacing=8)
            ]),
            theme=self.theme
        )

    def build_mood_section(self):
        """Sección de evaluación de ánimo"""
        self.mood_slider = ft.Slider(
            min=1, max=10, value=self.mood_score, divisions=9,
            on_change=self.on_mood_change,
            active_color=self.get_mood_color(self.mood_score),
            thumb_color=self.get_mood_color(self.mood_score)
        )

        mood_emojis = ["😢", "😔", "😐", "🙂", "😊", "😄", "🤗", "😁", "🥳", "🤩"]
        current_emoji = mood_emojis[min(int(self.mood_score) - 1, 9)]

        return create_themed_container(
            content=ft.Column([
                ft.Text("🎭 ¿Cómo calificas tu día?", size=16, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=16),

                # Slider visual
                ft.Row([
                    ft.Text("😢", size=20),
                    ft.Container(content=self.mood_slider, expand=True),
                    ft.Text("🤩", size=20)
                ]),

                ft.Container(height=16),

                # Valor actual
                ft.Row([
                    ft.Text(current_emoji, size=32),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(f"{int(self.mood_score)}/10", size=24, weight=ft.FontWeight.BOLD,
                                color=self.get_mood_color(self.mood_score)),
                        ft.Text(self.get_mood_label(self.mood_score), size=14,
                                color=self.theme.text_secondary)
                    ])
                ], alignment=ft.CrossAxisAlignment.CENTER)
            ]),
            theme=self.theme
        )

    def build_action_buttons(self):
        """Botones de acción final"""
        return ft.Row([
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Text("💾", size=16),
                    ft.Container(width=8),
                    ft.Text("Guardar día", size=14, weight=ft.FontWeight.W_500)
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=self.save_daily_review,
                style=ft.ButtonStyle(
                    bgcolor=self.theme.positive_main,
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                height=50,
                expand=True
            ),
            ft.Container(width=12),
            ft.OutlinedButton(
                content=ft.Row([
                    ft.Text("📅", size=16),
                    ft.Container(width=8),
                    ft.Text("Ver calendario", size=14)
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=self.go_to_calendar,
                style=ft.ButtonStyle(
                    color=self.theme.accent_primary,
                    side=ft.BorderSide(2, self.theme.accent_primary),
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                height=50,
                expand=True
            )
        ])

    # ===============================
    # MÉTODOS DE CONTROL
    # ===============================
    def add_prompt_to_reflection(self, prompt: str):
        """Añadir prompt a la reflexión"""
        if self.reflection_field:
            current = self.reflection_field.value or ""
            if current and not current.endswith('\n'):
                current += '\n\n'
            self.reflection_field.value = current + prompt + ' '
            if self.page:
                self.page.update()

    def set_worth_it(self, value):
        """Establecer valor de 'worth it'"""
        self.worth_it_value = value
        print(f"⚖️ Worth it establecido: {value}")
        if self.page:
            self.page.update()

    def on_mood_change(self, e):
        """Callback cuando cambia el mood"""
        self.mood_score = e.control.value
        new_color = self.get_mood_color(self.mood_score)
        e.control.active_color = new_color
        e.control.thumb_color = new_color
        if self.page:
            self.page.update()

    def get_mood_color(self, mood):
        """Color según mood score"""
        if mood <= 3:
            return self.theme.negative_main
        elif mood <= 6:
            return "#F59E0B"  # Amarillo
        else:
            return self.theme.positive_main

    def get_mood_label(self, mood):
        """Etiqueta según mood score"""
        if mood <= 2:
            return "Muy difícil"
        elif mood <= 4:
            return "Difícil"
        elif mood <= 6:
            return "Regular"
        elif mood <= 8:
            return "Bueno"
        else:
            return "Excelente"

    def save_daily_review(self, e=None):
        """Guardar revisión diaria completa"""
        if not self.user_data:
            self.show_message("❌ Error: No hay datos de usuario", is_error=True)
            return

        if not self.reflection_field or not self.reflection_field.value.strip():
            self.show_message("⚠️ Añade una reflexión antes de guardar", is_error=True)
            return

        try:
            from services import db
            user_id = self.user_data['id']

            print(f"💾 Guardando revisión diaria para usuario {user_id}")

            # Preparar datos
            reflection = self.reflection_field.value.strip()

            # Convertir momentos a tags
            positive_tags = []
            negative_tags = []

            for moment in self.moments_data['positive']:
                tag = {
                    "name": moment['text'],
                    "context": f"Momento {moment['category']} a las {moment['time']}",
                    "emoji": moment['emoji']
                }
                positive_tags.append(tag)

            for moment in self.moments_data['negative']:
                tag = {
                    "name": moment['text'],
                    "context": f"Momento {moment['category']} a las {moment['time']}",
                    "emoji": moment['emoji']
                }
                negative_tags.append(tag)

            # Guardar entrada completa
            entry_id = db.save_daily_entry(
                user_id=user_id,
                free_reflection=reflection,
                positive_tags=positive_tags,
                negative_tags=negative_tags,
                worth_it=self.worth_it_value
            )

            if entry_id:
                self.show_message("✅ Día guardado correctamente")

                # Navegar al calendario después de un momento
                if self.page:
                    def delayed_navigation():
                        if self.page:
                            self.page.go("/calendar")

                    import threading
                    timer = threading.Timer(1.5, delayed_navigation)
                    timer.start()
            else:
                self.show_message("❌ Error guardando el día", is_error=True)

        except Exception as e:
            print(f"❌ Error guardando revisión diaria: {e}")
            self.show_message("❌ Error guardando el día", is_error=True)

    def go_to_calendar(self, e=None):
        """Ir al calendario"""
        if self.page:
            self.page.go("/calendar")

    def go_back(self, e=None):
        """Volver"""
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/entry")

    def show_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje al usuario"""
        print(f"{'❌' if is_error else '✅'} {message}")
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF", size=14),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()