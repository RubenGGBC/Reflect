
import flet as ft
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Callable
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class ModernDailyReviewScreen:
    """Pantalla moderna para revisar el día completo - SIN IA"""

    def __init__(self, app=None, user_data=None, on_go_back: Callable = None, selected_date: date = None):
        self.app = app
        self.user_data = user_data
        self.on_go_back = on_go_back

        # ✅ NUEVO: Fecha específica o día actual
        self.selected_date = selected_date or date.today()
        self.is_today = self.selected_date == date.today()

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
        self.moments_count = {"positive": 0, "negative": 0, "total": 0}

        print(f"📝 ModernDailyReviewScreen inicializada para fecha: {self.selected_date} - SIN IA")

    def build(self):
        """Construir vista principal moderna"""
        self.theme = get_theme()

        # Cargar datos del día específico
        self.load_day_data()

        # Header compacto con fecha
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        user_name = self.user_data.get('name', 'Viajero') if self.user_data else 'Viajero'

        # ✅ NUEVO: Mostrar fecha específica
        date_str = self.selected_date.strftime("%d %b")
        if not self.is_today:
            date_str += f" '{self.selected_date.strftime('%y')}"

        title = f"📝 {'Tu día' if self.is_today else 'Día'} - {date_str}"

        header = create_gradient_header(
            title=title,
            left_button=back_button,
            theme=self.theme
        )

        # Contenido principal con scroll horizontal en secciones
        content = ft.Column([
            # ✅ NUEVO: Banner de fecha si no es hoy
            self.build_date_banner() if not self.is_today else ft.Container(),

            # Introducción moderna
            self.build_modern_intro(),
            ft.Container(height=12),

            # Sección de momentos con scroll horizontal
            self.build_moments_carousel(),
            ft.Container(height=12),

            # Reflexión libre moderna
            self.build_modern_reflection(),
            ft.Container(height=12),

            # Evaluación rápida con sliders
            self.build_quick_evaluation(),
            ft.Container(height=12),

            # Insights automáticos simples
            self.build_simple_insights(),
            ft.Container(height=16),

            # Botones de acción modernos
            self.build_modern_actions(),
            ft.Container(height=20)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        # Vista completa
        view = ft.View(
            "/daily_review",
            [
                header,
                ft.Container(
                    content=content,
                    padding=ft.padding.all(12),
                    expand=True
                )
            ],
            bgcolor=self.theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def build_date_banner(self):
        """✅ NUEVO: Banner para mostrar cuando es una fecha pasada"""
        if self.is_today:
            return ft.Container()

        date_formatted = self.selected_date.strftime("%A, %d de %B de %Y")

        return create_themed_container(
            content=ft.Row([
                ft.Text("📅", size=20),
                ft.Container(width=8),
                ft.Column([
                    ft.Text("Revisando día pasado", size=12, weight=ft.FontWeight.W_500,
                            color=self.theme.text_secondary),
                    ft.Text(date_formatted, size=11, color=self.theme.text_hint)
                ], expand=True)
            ], alignment=ft.CrossAxisAlignment.CENTER),
            theme=self.theme
        )

    def load_day_data(self):
        """✅ MODIFICADO: Cargar datos del día específico (no solo hoy)"""
        if not self.user_data:
            print("⚠️ No hay datos de usuario")
            return

        try:
            from services import db
            user_id = self.user_data['id']
            target_date = self.selected_date.isoformat()

            print(f"📚 Cargando datos del día {target_date} para usuario {user_id}")

            # ✅ NUEVO: Cargar momentos del día específico
            moments = self.get_interactive_moments_by_date(user_id, target_date)

            # Separar por tipo
            self.moments_data = {"positive": [], "negative": []}
            for moment in moments:
                if moment['type'] == 'positive':
                    self.moments_data['positive'].append(moment)
                else:
                    self.moments_data['negative'].append(moment)

            # ✅ NUEVO: Contar momentos del día específico
            self.moments_count = self.count_moments_by_date(user_id, target_date)

            print(f"📊 Cargados: {self.moments_count['positive']} positivos, {self.moments_count['negative']} negativos")

            # ✅ MODIFICADO: Cargar entrada del día específico
            entries = db.get_user_entries(user_id, limit=50)  # Más entradas para buscar
            target_entry = None

            for entry in entries:
                if entry['entry_date'] == target_date:
                    target_entry = entry
                    break

            if target_entry:
                self.reflection_text = target_entry.get('free_reflection', '')
                self.worth_it_value = target_entry.get('worth_it')
                self.mood_score = target_entry.get('mood_score', 5)
                print(f"📄 Entrada del {target_date} cargada")
            else:
                self.reflection_text = ""
                print(f"📄 No hay entrada para {target_date}")

        except Exception as e:
            print(f"❌ Error cargando datos del día: {e}")
            self.moments_data = {"positive": [], "negative": []}
            self.reflection_text = ""
            self.moments_count = {"positive": 0, "negative": 0, "total": 0}

    def get_interactive_moments_by_date(self, user_id: int, target_date: str) -> List[Dict[str, Any]]:
        """✅ NUEVO: Obtener momentos de una fecha específica"""
        try:
            import sqlite3
            from services import db

            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()

                # Verificar si existe la columna is_active
                cursor.execute("PRAGMA table_info(interactive_moments)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                if 'is_active' in column_names:
                    # Versión con is_active
                    cursor.execute("""
                        SELECT moment_id, emoji, text, moment_type, intensity, 
                               category, time_str, created_at
                        FROM interactive_moments 
                        WHERE user_id = ? AND entry_date = ? AND is_active = 1
                        ORDER BY time_str, created_at
                    """, (user_id, target_date))
                else:
                    # Versión sin is_active
                    cursor.execute("""
                        SELECT moment_id, emoji, text, moment_type, intensity, 
                               category, time_str, created_at
                        FROM interactive_moments 
                        WHERE user_id = ? AND entry_date = ?
                        ORDER BY time_str, created_at
                    """, (user_id, target_date))

                results = cursor.fetchall()

                moments = []
                for row in results:
                    moment_dict = {
                        'id': row[0],
                        'emoji': row[1],
                        'text': row[2],
                        'type': row[3],
                        'intensity': row[4],
                        'category': row[5],
                        'time': row[6],
                        'created_at': row[7]
                    }
                    moments.append(moment_dict)

                print(f"📚 Cargados {len(moments)} momentos del {target_date}")
                return moments

        except Exception as e:
            print(f"❌ Error obteniendo momentos de fecha específica: {e}")
            return []

    def count_moments_by_date(self, user_id: int, target_date: str) -> Dict[str, int]:
        """✅ NUEVO: Contar momentos de una fecha específica"""
        try:
            import sqlite3
            from services import db

            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()

                # Verificar si existe la columna is_active
                cursor.execute("PRAGMA table_info(interactive_moments)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                if 'is_active' in column_names:
                    cursor.execute("""
                        SELECT moment_type, COUNT(*) 
                        FROM interactive_moments 
                        WHERE user_id = ? AND entry_date = ? AND is_active = 1
                        GROUP BY moment_type
                    """, (user_id, target_date))
                else:
                    cursor.execute("""
                        SELECT moment_type, COUNT(*) 
                        FROM interactive_moments 
                        WHERE user_id = ? AND entry_date = ?
                        GROUP BY moment_type
                    """, (user_id, target_date))

                results = cursor.fetchall()

                counts = {"positive": 0, "negative": 0}
                for moment_type, count in results:
                    if moment_type in counts:
                        counts[moment_type] = count

                counts["total"] = counts["positive"] + counts["negative"]
                return counts

        except Exception as e:
            print(f"❌ Error contando momentos por fecha: {e}")
            return {"positive": 0, "negative": 0, "total": 0}

    def build_modern_intro(self):
        """✅ MODIFICADO: Introducción moderna con estadísticas para cualquier fecha"""
        total_moments = self.moments_count['total']

        if total_moments > 0:
            day_text = "este día" if not self.is_today else "hoy"
            intro_text = f"Se capturaron {total_moments} momentos {day_text}"
            intro_emoji = "🌟"
            stats_visible = True
        else:
            if self.is_today:
                intro_text = "¿Cómo ha sido tu día? Vamos a reflexionar juntos"
            else:
                intro_text = "No hay momentos específicos registrados este día"
            intro_emoji = "💭"
            stats_visible = total_moments > 0

        # Stats rápidas
        stats_row = ft.Row([
            self.create_stat_bubble(self.moments_count['positive'], "Positivos", self.theme.positive_main, "😊"),
            self.create_stat_bubble(self.moments_count['negative'], "Difíciles", self.theme.negative_main, "🌧️"),
            self.create_stat_bubble(total_moments, "Total", self.theme.accent_primary, "📊")
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND) if stats_visible else ft.Container()

        return create_themed_container(
            content=ft.Column([
                ft.Row([
                    ft.Text(intro_emoji, size=28),
                    ft.Container(width=12),
                    ft.Column([
                        ft.Text("Revisión del día" if not self.is_today else "Hora de reflexionar",
                                size=16, weight=ft.FontWeight.BOLD, color=self.theme.text_primary),
                        ft.Text(intro_text, size=12, color=self.theme.text_secondary)
                    ], expand=True)
                ], alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=12) if stats_visible else ft.Container(),
                stats_row
            ]),
            theme=self.theme
        )

    def create_stat_bubble(self, value: int, label: str, color: str, emoji: str):
        """Crear burbuja de estadística"""
        return ft.Container(
            content=ft.Column([
                ft.Text(emoji, size=16),
                ft.Text(str(value), size=16, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(label, size=9, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            width=70,
            height=60,
            padding=ft.padding.all(8),
            border_radius=12,
            bgcolor=color + "15",
            border=ft.border.all(1, color + "40")
        )

    def build_moments_carousel(self):
        """Carousel horizontal de momentos"""
        if not self.moments_data['positive'] and not self.moments_data['negative']:
            return create_themed_container(
                content=ft.Column([
                    ft.Text("📱 Momentos del día", size=14, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Container(height=8),
                    ft.Text("No hay momentos específicos registrados este día.",
                            size=11, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER)
                ]),
                theme=self.theme
            )

        # Combinar y ordenar momentos por tiempo
        all_moments = self.moments_data['positive'] + self.moments_data['negative']
        all_moments.sort(key=lambda x: x.get('time', '00:00'))

        # Crear cards de momentos
        moment_cards = []
        for moment in all_moments:
            card = self.create_moment_card(moment)
            moment_cards.append(card)

        # Row con scroll horizontal
        moments_scroll = ft.Row(
            moment_cards,
            spacing=8,
            scroll=ft.ScrollMode.AUTO
        )

        return create_themed_container(
            content=ft.Column([
                ft.Text("📱 Momentos del día", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=8),
                ft.Container(
                    content=moments_scroll,
                    height=80
                )
            ]),
            theme=self.theme
        )

    def create_moment_card(self, moment):
        """Crear card de momento individual"""
        is_positive = moment['type'] == 'positive'
        color = self.theme.positive_main if is_positive else self.theme.negative_main

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(moment['emoji'], size=16),
                    ft.Text(moment['time'], size=8, color=self.theme.text_hint)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=4),
                ft.Text(
                    moment['text'][:20] + "..." if len(moment['text']) > 20 else moment['text'],
                    size=10,
                    color=self.theme.text_primary,
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=90,
            height=70,
            padding=ft.padding.all(8),
            border_radius=12,
            bgcolor=color + "15",
            border=ft.border.all(1, color + "40")
        )

    def build_modern_reflection(self):
        """✅ MODIFICADO: Reflexión libre moderna - solo editable si es hoy"""
        self.reflection_field = ft.TextField(
            label="💭 ¿Cómo fue tu día? Reflexiona libremente..." if self.is_today else "💭 Reflexión del día",
            multiline=True,
            min_lines=3,
            max_lines=5,
            value=getattr(self, 'reflection_text', ''),
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(12),
            text_style=ft.TextStyle(color=self.theme.text_primary),
            read_only=not self.is_today  # ✅ Solo editable si es hoy
        )

        # Prompts solo si es hoy
        if self.is_today:
            prompts = [
                "¿Qué aprendiste?", "¿Qué te hizo sonreír?", "¿Qué cambiarías?",
                "¿Cómo te sientes?", "¿Qué te sorprendió?", "¿De qué estás agradecido?"
            ]

            prompt_chips = []
            for prompt in prompts:
                chip = ft.Container(
                    content=ft.Text(prompt, size=10, color=self.theme.text_secondary,
                                    text_align=ft.TextAlign.CENTER),
                    padding=ft.padding.symmetric(horizontal=10, vertical=6),
                    border_radius=16,
                    bgcolor=self.theme.surface,
                    border=ft.border.all(1, self.theme.border_color),
                    on_click=lambda e, p=prompt: self.add_prompt_to_reflection(p)
                )
                prompt_chips.append(chip)

            prompts_scroll = ft.Row(
                prompt_chips,
                spacing=6,
                scroll=ft.ScrollMode.AUTO
            )

            return create_themed_container(
                content=ft.Column([
                    self.reflection_field,
                    ft.Container(height=10),
                    ft.Text("💡 Toca para añadir:", size=11, weight=ft.FontWeight.W_500,
                            color=self.theme.text_secondary),
                    ft.Container(height=6),
                    ft.Container(content=prompts_scroll, height=35)
                ]),
                theme=self.theme
            )
        else:
            return create_themed_container(
                content=self.reflection_field,
                theme=self.theme
            )

    def build_quick_evaluation(self):
        """✅ MODIFICADO: Evaluación rápida - solo editable si es hoy"""
        # Slider de mood
        self.mood_slider = ft.Slider(
            min=1, max=10, value=self.mood_score, divisions=9,
            on_change=self.on_mood_change if self.is_today else None,
            active_color=self.get_mood_color(self.mood_score),
            thumb_color=self.get_mood_color(self.mood_score),
            disabled=not self.is_today  # ✅ Solo editable si es hoy
        )

        # Worth it como toggle buttons modernos
        worth_it_section = self.build_modern_worth_it()

        return create_themed_container(
            content=ft.Column([
                # Mood slider
                ft.Text("🎭 Calificación del día", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=8),

                ft.Row([
                    ft.Text("😢", size=16),
                    ft.Container(content=self.mood_slider, expand=True),
                    ft.Text("🤩", size=16)
                ]),

                ft.Container(height=6),

                # Valor actual centrado
                ft.Text(f"{int(self.mood_score)}/10 - {self.get_mood_label(self.mood_score)}",
                        size=12, weight=ft.FontWeight.BOLD,
                        color=self.get_mood_color(self.mood_score),
                        text_align=ft.TextAlign.CENTER),

                ft.Container(height=16),

                # Worth it section
                worth_it_section
            ]),
            theme=self.theme
        )

    def build_modern_worth_it(self):
        """✅ MODIFICADO: Worth it moderna - solo editable si es hoy"""
        options = [
            {"value": True,"text": "Valió la pena", "color": self.theme.positive_main},
            {"value": False, "text": "No valió la pena", "color": self.theme.negative_main},
            {"value": None,  "text": "No estoy seguro", "color": self.theme.text_hint}
        ]

        self.worth_it_buttons = []
        button_widgets = []

        for option in options:
            is_selected = self.worth_it_value == option["value"]

            btn = ft.Container(
                content=ft.Row([
                    ft.Container(width=6),
                    ft.Text(option["text"], size=11, weight=ft.FontWeight.W_500,
                            color="#FFFFFF" if is_selected else self.theme.text_primary)
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                border_radius=8,
                bgcolor=option["color"] if is_selected else self.theme.surface,
                border=ft.border.all(1, option["color"]),
                on_click=lambda e, val=option["value"]: self.set_worth_it(val) if self.is_today else None,
                expand=True,
                opacity=1.0 if self.is_today else 0.7  # ✅ Visual para días pasados
            )

            self.worth_it_buttons.append(btn)
            button_widgets.append(btn)

        return ft.Column([
            ft.Text("⚖️ ¿Mereció la pena el día?", size=14, weight=ft.FontWeight.W_600,
                    color=self.theme.text_primary),
            ft.Container(height=8),
            ft.Row(button_widgets, spacing=6)
        ])

    def build_simple_insights(self):
        """Insights automáticos simples (sin IA externa)"""
        insights = self.generate_simple_insights()

        if not insights:
            return ft.Container()

        insight_chips = []
        for insight in insights:
            chip = ft.Container(
                content=ft.Text(insight, size=10, color=self.theme.text_primary,
                                text_align=ft.TextAlign.CENTER),
                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                border_radius=12,
                bgcolor=self.theme.accent_primary + "20",
                border=ft.border.all(1, self.theme.accent_primary + "40")
            )
            insight_chips.append(chip)

        # Create rows of chips (2 per row max)
        chip_rows = []
        current_row = []

        for i, chip in enumerate(insight_chips):
            current_row.append(chip)
            if len(current_row) == 2 or i == len(insight_chips) - 1:
                # Create row with current chips
                row = ft.Row(
                    controls=current_row.copy(),
                    spacing=6,
                    alignment=ft.MainAxisAlignment.CENTER
                )
                chip_rows.append(row)
                current_row = []

        return create_themed_container(
            content=ft.Column([
                ft.Text("✨ Observaciones del día", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=8),
                ft.Column(
                    controls=chip_rows,
                    spacing=6
                )
            ]),
            theme=self.theme
        )

    def generate_simple_insights(self):
        """Generar insights simples basados en datos (sin IA externa)"""
        insights = []

        positive_count = self.moments_count['positive']
        negative_count = self.moments_count['negative']
        total_count = self.moments_count['total']

        # Insights basados en balance
        if positive_count > negative_count and positive_count > 0:
            insights.append(f"🌟 Día mayormente positivo ({positive_count} vs {negative_count})")
        elif negative_count > positive_count and negative_count > 0:
            insights.append(f"🌧️ Día con desafíos ({negative_count} vs {positive_count})")
        elif positive_count == negative_count and total_count > 0:
            insights.append("⚖️ Día equilibrado entre altos y bajos")

        # Insights sobre actividad
        if total_count > 5:
            insights.append("📈 Día muy activo emocionalmente")
        elif total_count == 0:
            insights.append("🕯️ Día tranquilo y sereno")

        # Insights sobre mood
        if self.mood_score >= 8:
            insights.append("😄 Excelente estado de ánimo")
        elif self.mood_score <= 3:
            insights.append("💙 Día desafiante, pero valiente")

        # Insights sobre reflexión
        reflection_length = len(getattr(self, 'reflection_text', ''))
        if reflection_length > 100:
            insights.append("📝 Reflexión profunda y detallada")

        return insights[:3]  # Máximo 3 insights

    def build_modern_actions(self):
        """✅ MODIFICADO: Botones de acción modernos - adaptados según fecha"""
        if self.is_today:
            # Botones para día actual
            return ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("💾", size=14),
                        ft.Container(width=6),
                        ft.Text("Completar día", size=12, weight=ft.FontWeight.W_500)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.save_daily_review,
                    style=ft.ButtonStyle(
                        bgcolor=self.theme.positive_main,
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    height=45,
                    expand=True
                ),
                ft.Container(width=10),
                ft.OutlinedButton(
                    content=ft.Row([
                        ft.Text("📅", size=14),
                        ft.Container(width=6),
                        ft.Text("Calendario", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.go_to_calendar,
                    style=ft.ButtonStyle(
                        color=self.theme.accent_primary,
                        side=ft.BorderSide(2, self.theme.accent_primary),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    height=45,
                    expand=True
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        else:
            # Botones para días pasados
            return ft.Row([
                ft.OutlinedButton(
                    content=ft.Row([
                        ft.Text("📅", size=14),
                        ft.Container(width=6),
                        ft.Text("Volver al calendario", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.go_to_calendar,
                    style=ft.ButtonStyle(
                        color=self.theme.accent_primary,
                        side=ft.BorderSide(2, self.theme.accent_primary),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    height=45,
                    expand=True
                )
            ], alignment=ft.MainAxisAlignment.CENTER)

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
        """✅ CORREGIDO: Guardar revisión diaria sin IA"""
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

            # Convertir momentos a tags si existen
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

            # ✅ Guardar entrada diaria SIN IA
            entry_id = db.save_daily_entry(
                user_id=user_id,
                free_reflection=reflection,
                positive_tags=positive_tags,
                negative_tags=negative_tags,
                worth_it=self.worth_it_value,
                mood_score=int(self.mood_score)
            )

            if entry_id:
                # ✅ Desactivar momentos después de guardar
                if self.moments_data['positive'] or self.moments_data['negative']:
                    db.deactivate_interactive_moments_today(user_id)

                self.show_message("✅ Día completado y guardado correctamente")

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
                content=ft.Text(message, color="#FFFFFF", size=12),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()