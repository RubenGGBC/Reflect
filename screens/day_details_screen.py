"""
📊 Daily Review Screen CORREGIDA - ReflectApp
✅ ARREGLADO: Muestra datos específicos del día seleccionado (no siempre hoy)
✅ ARREGLADO: Recibe parámetros de fecha correctamente
✅ ARREGLADO: Modo vista vs modo edición
"""

import flet as ft
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Callable
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class DailyReviewScreen:
    """Pantalla para revisar día específico - CORREGIDA"""

    def __init__(self, app=None, user_data=None, on_go_back: Callable = None,
                 target_date: tuple = None, day_details: dict = None):
        self.app = app
        self.user_data = user_data
        self.on_go_back = on_go_back

        # ✅ NUEVO: Datos específicos del día
        self.target_date = target_date  # (year, month, day) o None para hoy
        self.day_details = day_details or {}  # Datos precargados del día

        # Estado
        self.page = None
        self.theme = get_theme()

        # ✅ NUEVO: Determinar si es modo vista o edición
        self.is_today = self._is_target_date_today()
        self.is_view_mode = not self.is_today  # Si no es hoy, es solo vista

        # Datos del día - ✅ CORREGIDO: Usar datos específicos
        self.moments_data = {"positive": [], "negative": []}
        self.reflection_field = None
        self.worth_it_value = None
        self.mood_score = 5

        # UI Components
        self.worth_it_buttons = []
        self.mood_slider = None

        print(f"📊 DailyReviewScreen inicializada - Fecha: {self.target_date}, Modo: {'Vista' if self.is_view_mode else 'Edición'}")

    def _is_target_date_today(self) -> bool:
        """Verificar si la fecha objetivo es hoy"""
        if not self.target_date:
            return True  # Sin fecha específica = hoy

        today = date.today()
        year, month, day = self.target_date
        target = date(year, month, day)

        return target == today

    def build(self):
        """Construir vista principal - CORREGIDA"""
        self.theme = get_theme()

        # ✅ CORREGIDO: Cargar datos del día específico
        self.load_target_day_data()

        # ✅ Header específico según el día
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # ✅ CORREGIDO: Título específico del día
        title = self._get_header_title()

        header = create_gradient_header(
            title=title,
            left_button=back_button,
            theme=self.theme
        )

        # Contenido principal
        content = ft.Column([
            # ✅ Introducción específica del día
            self.build_intro_section(),
            ft.Container(height=16),

            # ✅ Resumen de momentos del día específico
            self.build_moments_summary(),
            ft.Container(height=16),

            # ✅ Reflexión del día (editable solo si es hoy)
            self.build_reflection_section(),
            ft.Container(height=16),

            # ✅ Evaluación del día (solo si es hoy o ya existe)
            self.build_worth_it_section(),
            ft.Container(height=16),

            # ✅ Mood score del día
            self.build_mood_section(),
            ft.Container(height=20),

            # ✅ Botones según el modo
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

    def _get_header_title(self) -> str:
        """✅ NUEVO: Obtener título específico del header"""
        if not self.target_date:
            return "📝 Revisa tu día - Hoy"

        year, month, day = self.target_date
        target_date_obj = date(year, month, day)

        if self.is_today:
            return "📝 Revisa tu día - Hoy"
        else:
            # Formato elegante para días pasados
            formatted_date = target_date_obj.strftime("%d %b %Y")
            return f"📅 {formatted_date}"

    def load_target_day_data(self):
        """✅ CORREGIDO: Cargar datos del día específico (no siempre hoy)"""
        if not self.user_data:
            print("⚠️ No hay datos de usuario")
            return

        try:
            from services import db
            user_id = self.user_data['id']

            if self.target_date:
                year, month, day = self.target_date
                print(f"📚 Cargando datos del día específico: {year}-{month}-{day}")

                # ✅ Usar datos precargados si están disponibles
                if self.day_details:
                    print("📋 Usando datos precargados del día")
                    self._process_day_details(self.day_details)
                else:
                    # Cargar desde base de datos
                    day_entry = db.get_day_entry(user_id, year, month, day)
                    if day_entry:
                        self._process_day_details(day_entry)
                        print(f"📄 Entrada del día cargada desde DB")
                    else:
                        print(f"ℹ️ No hay entrada para el día {year}-{month}-{day}")

                # Cargar momentos interactivos del día específico (si los hay)
                # TODO: Implementar carga de momentos por fecha específica

            else:
                # Es hoy - cargar datos actuales
                print(f"📚 Cargando datos del día actual")

                # Cargar momentos interactivos de hoy
                moments = db.get_interactive_moments_today(user_id)
                self._process_interactive_moments(moments)

                # Cargar entrada existente si existe
                entries = db.get_user_entries(user_id, limit=1)
                if entries and entries[0]['entry_date'] == date.today().isoformat():
                    entry = entries[0]
                    self._process_day_details(entry)
                    print(f"📄 Entrada de hoy cargada")

        except Exception as e:
            print(f"❌ Error cargando datos del día: {e}")
            self._set_empty_day_data()

    def _process_day_details(self, day_details: dict):
        """✅ NUEVO: Procesar detalles del día desde la base de datos"""
        self.reflection_text = day_details.get('reflection', day_details.get('free_reflection', ''))
        self.worth_it_value = day_details.get('worth_it')
        self.mood_score = day_details.get('mood_score', 5)

        # Procesar tags como momentos
        positive_tags = day_details.get('positive_tags', [])
        negative_tags = day_details.get('negative_tags', [])

        self.moments_data = {
            "positive": positive_tags,
            "negative": negative_tags
        }

    def _process_interactive_moments(self, moments: list):
        """✅ NUEVO: Procesar momentos interactivos"""
        self.moments_data = {"positive": [], "negative": []}
        for moment in moments:
            if moment['type'] == 'positive':
                self.moments_data['positive'].append(moment)
            else:
                self.moments_data['negative'].append(moment)

    def _set_empty_day_data(self):
        """✅ NUEVO: Establecer datos vacíos"""
        self.moments_data = {"positive": [], "negative": []}
        self.reflection_text = ""
        self.worth_it_value = None
        self.mood_score = 5

    def build_intro_section(self):
        """✅ CORREGIDO: Sección de introducción específica del día"""
        total_moments = len(self.moments_data['positive']) + len(self.moments_data['negative'])

        if self.is_view_mode:
            # Modo vista (día pasado)
            if total_moments > 0:
                intro_text = f"El {self._get_formatted_date()} registraste {total_moments} momentos."
                intro_emoji = "📖"
            else:
                intro_text = f"No hay momentos registrados para el {self._get_formatted_date()}."
                intro_emoji = "📅"
        else:
            # Modo edición (hoy)
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
                        ft.Text(
                            "Revisión del día" if self.is_view_mode else "Hora de reflexionar",
                            size=18, weight=ft.FontWeight.BOLD, color=self.theme.text_primary
                        ),
                        ft.Text(intro_text, size=14, color=self.theme.text_secondary)
                    ], expand=True)
                ], alignment=ft.CrossAxisAlignment.CENTER)
            ]),
            theme=self.theme
        )

    def _get_formatted_date(self) -> str:
        """✅ NUEVO: Obtener fecha formateada"""
        if not self.target_date:
            return "hoy"

        year, month, day = self.target_date
        target_date_obj = date(year, month, day)
        return target_date_obj.strftime("%d de %B")

    def build_moments_summary(self):
        """✅ CORREGIDO: Resumen visual de momentos del día específico"""
        positive_count = len(self.moments_data['positive'])
        negative_count = len(self.moments_data['negative'])

        if positive_count == 0 and negative_count == 0:
            empty_message = "No hay momentos específicos registrados para este día." if self.is_view_mode else "No hay momentos específicos registrados. Puedes usar la reflexión libre abajo."

            return create_themed_container(
                content=ft.Column([
                    ft.Text("📋 Momentos del día", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=12),
                    ft.Text(empty_message, size=13, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER)
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

        # ✅ NUEVO: Mostrar lista de momentos
        moments_list = self._build_moments_list()

        return create_themed_container(
            content=ft.Column([
                ft.Text("📋 Momentos del día", size=16, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=12),
                stats_row,
                ft.Container(height=16),
                moments_list
            ]),
            theme=self.theme
        )

    def _build_moments_list(self):
        """✅ NUEVO: Construir lista de momentos"""
        moment_items = []

        # Momentos positivos
        for moment in self.moments_data['positive']:
            emoji = moment.get('emoji', '✨')
            text = moment.get('name', moment.get('text', ''))
            time_str = moment.get('time', '')

            item = ft.Row([
                ft.Text(emoji, size=16),
                ft.Text(text, size=13, color=self.theme.text_primary, expand=True),
                ft.Text(time_str, size=11, color=self.theme.text_hint),
                ft.Container(width=4, height=4, border_radius=2, bgcolor=self.theme.positive_main)
            ], spacing=8)
            moment_items.append(item)

        # Momentos negativos
        for moment in self.moments_data['negative']:
            emoji = moment.get('emoji', '🌧️')
            text = moment.get('name', moment.get('text', ''))
            time_str = moment.get('time', '')

            item = ft.Row([
                ft.Text(emoji, size=16),
                ft.Text(text, size=13, color=self.theme.text_primary, expand=True),
                ft.Text(time_str, size=11, color=self.theme.text_hint),
                ft.Container(width=4, height=4, border_radius=2, bgcolor=self.theme.negative_main)
            ], spacing=8)
            moment_items.append(item)

        if not moment_items:
            return ft.Text("Sin momentos específicos", size=12, color=self.theme.text_hint)

        return ft.Column([
            ft.Text("Momentos registrados:", size=13, weight=ft.FontWeight.W_500,
                    color=self.theme.text_secondary),
            ft.Container(height=8),
            ft.Column(moment_items, spacing=6)
        ])

    def build_reflection_section(self):
        """✅ CORREGIDO: Sección de reflexión (editable solo si es hoy)"""
        if self.is_view_mode:
            # Modo vista - solo mostrar reflexión existente
            reflection_text = self.reflection_text or "Sin reflexión registrada para este día"

            return create_themed_container(
                content=ft.Column([
                    ft.Text("💭 Reflexión del día", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Text(
                            reflection_text,
                            size=14,
                            color=self.theme.text_primary,
                            text_align=ft.TextAlign.START
                        ),
                        padding=ft.padding.all(16),
                        border_radius=12,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color)
                    )
                ]),
                theme=self.theme
            )

        else:
            # Modo edición - campo editable
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
        """✅ CORREGIDO: Sección de evaluación final (según modo)"""
        if self.is_view_mode:
            # Modo vista - mostrar evaluación existente
            if self.worth_it_value is not None:
                if self.worth_it_value:
                    icon = "😊"
                    text = "SÍ, mereció la pena"
                    color = self.theme.positive_main
                else:
                    icon = "😔"
                    text = "NO, no mereció la pena"
                    color = self.theme.negative_main
            else:
                icon = "🤷"
                text = "No evaluado"
                color = self.theme.text_hint

            return create_themed_container(
                content=ft.Column([
                    ft.Text("⚖️ ¿Mereció la pena el día?", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Text(icon, size=24),
                        ft.Container(width=12),
                        ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=color)
                    ])
                ]),
                theme=self.theme
            )

        else:
            # Modo edición - controles interactivos
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
        """✅ CORREGIDO: Sección de evaluación de ánimo (según modo)"""
        if self.is_view_mode:
            # Modo vista - mostrar mood existente
            mood_emojis = ["😢", "😔", "😐", "🙂", "😊", "😄", "🤗", "😁", "🥳", "🤩"]
            current_emoji = mood_emojis[min(int(self.mood_score) - 1, 9)]

            return create_themed_container(
                content=ft.Column([
                    ft.Text("🎭 Calificación del día", size=16, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=16),
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

        else:
            # Modo edición - slider interactivo
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
        """✅ CORREGIDO: Botones de acción según el modo"""
        if self.is_view_mode:
            # Modo vista - solo botón de volver al calendario
            return ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("📅", size=16),
                        ft.Container(width=8),
                        ft.Text("Volver al calendario", size=14, weight=ft.FontWeight.W_500)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.go_to_calendar,
                    style=ft.ButtonStyle(
                        bgcolor=self.theme.accent_primary,
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    height=50,
                    expand=True
                )
            ])

        else:
            # Modo edición - botones de guardar y calendario
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
        """Guardar revisión diaria completa - SOLO SI ES HOY"""
        if self.is_view_mode:
            self.show_message("ℹ️ Los días pasados no se pueden editar")
            return

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
                    "name": moment.get('text', moment.get('name', '')),
                    "context": f"Momento {moment.get('category', 'general')} a las {moment.get('time', '')}",
                    "emoji": moment.get('emoji', '✨')
                }
                positive_tags.append(tag)

            for moment in self.moments_data['negative']:
                tag = {
                    "name": moment.get('text', moment.get('name', '')),
                    "context": f"Momento {moment.get('category', 'general')} a las {moment.get('time', '')}",
                    "emoji": moment.get('emoji', '🌧️')
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
            self.page.go("/calendar")

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