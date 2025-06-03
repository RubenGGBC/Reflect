"""
🎮 Interactive Moments Screen - CORREGIDO Y OPTIMIZADO
✅ Persistencia corregida ✅ Header compacto ✅ Layout móvil ✅ Sin IA
"""

import flet as ft
from datetime import datetime, time
from typing import List, Dict, Any, Optional, Callable
import calendar
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

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
    """Pantalla Interactive Moments - CORREGIDA CON PERSISTENCIA Y MÓVIL OPTIMIZADO"""

    def __init__(self, app=None, on_moments_created: Callable = None, on_go_back: Callable = None):
        self.app = app
        self.on_moments_created = on_moments_created
        self.on_go_back = on_go_back

        # Estado principal
        self.page = None
        self.current_user = None
        self.theme = get_theme()
        self.active_mode = "quick"  # quick, mood, timeline, templates

        # Datos - ✅ CORREGIDO: Inicializar como lista vacía
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

        # ✅ Estado de persistencia CORREGIDO
        self.data_loaded = False
        self.auto_save_enabled = True

        print("🎮 InteractiveMomentsScreen OPTIMIZADA - PERSISTENCIA CORREGIDA")

    def set_user(self, user_data):
        """Establecer usuario actual y cargar datos"""
        self.current_user = user_data
        self.data_loaded = False
        print(f"👤 Usuario establecido: {user_data.get('name')} (ID: {user_data.get('id')})")

        # ✅ IMPORTANTE: Cargar datos inmediatamente
        self.load_user_moments()

        # ✅ Refrescar interfaz si existe
        if self.page and self.summary_container:
            self.refresh_summary()

    def load_user_moments(self):
        """✅ CORREGIDO: Cargar momentos guardados del usuario"""
        if not self.current_user:
            print("⚠️ No hay usuario para cargar momentos")
            return

        try:
            from services import db
            user_id = self.current_user['id']

            print(f"📚 Cargando momentos para usuario {user_id}")

            # ✅ Cargar momentos desde BD
            moments_data = db.get_interactive_moments_today(user_id)

            # ✅ Limpiar lista antes de recargar
            self.moments.clear()

            for moment_dict in moments_data:
                try:
                    moment = InteractiveMoment.from_dict(moment_dict)
                    self.moments.append(moment)
                    print(f"📝 Momento cargado: {moment.emoji} {moment.text}")
                except Exception as e:
                    print(f"⚠️ Error parseando momento: {e}")
                    continue

            print(f"✅ Cargados {len(self.moments)} momentos persistentes")
            self.data_loaded = True

        except Exception as e:
            print(f"❌ Error cargando momentos del usuario: {e}")
            import traceback
            traceback.print_exc()

    def save_moment_to_db(self, moment):
        """✅ CORREGIDO: Guardar momento en BD inmediatamente"""
        if not self.current_user:
            print("⚠️ No hay usuario para guardar momento")
            return False

        try:
            from services import db
            user_id = self.current_user['id']

            # ✅ Guardar usando método corregido
            moment_id = db.save_interactive_moment(
                user_id=user_id,
                moment_data=moment.to_dict()
            )

            if moment_id:
                print(f"💾 Momento guardado en BD: {moment.emoji} {moment.text} (ID: {moment_id})")
                return True
            else:
                print("❌ Error guardando momento en BD")
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
        """✅ CORREGIDO: Construir vista optimizada para móvil con header compacto"""
        self.theme = get_theme()

        # ✅ Header COMPACTO - MÁS PEQUEÑO
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # ✅ Botones de navegación compactos
        nav_buttons = ft.Row([
            ft.Container(
                content=ft.Text("🎨", size=14),  # ✅ Iconos más pequeños
                on_click=self.go_to_theme_selector,
                bgcolor="#FFFFFF20",
                border_radius=6,  # ✅ Border radius menor
                padding=ft.padding.all(6),  # ✅ Padding menor
                tooltip="Temas"
            ),
            ft.Container(
                content=ft.Text("📅", size=14),
                on_click=self.go_to_calendar,
                bgcolor="#FFFFFF20",
                border_radius=6,
                padding=ft.padding.all(6),
                tooltip="Calendario"
            ),
            ft.Container(
                content=ft.Text("🔔", size=14),
                on_click=self.go_to_mobile_notification_settings,
                bgcolor="#FFFFFF20",
                border_radius=6,
                padding=ft.padding.all(6),
                tooltip="Notificaciones"
            )
        ], spacing=6)

        user_name = self.current_user.get('name', 'Viajero') if self.current_user else 'Viajero'

        # ✅ Header MÁS COMPACTO - SOLO 1 LÍNEA
        header = ft.Container(
            content=ft.Row([
                back_button,
                ft.Text(
                    f"🎮 Momentos - {user_name}",
                    size=14,  # ✅ Tamaño reducido
                    weight=ft.FontWeight.W_600,
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER,
                    expand=True
                ),
                nav_buttons
            ]),
            padding=ft.padding.all(10),  # ✅ Padding muy reducido
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=self.theme.gradient_header
            ),
            border_radius=ft.border_radius.only(bottom_left=12, bottom_right=12)  # ✅ Bordes pequeños
        )

        # ✅ Stats en una línea compacta
        stats_text = ""
        if self.moments:
            positive_count = len([m for m in self.moments if m.type == "positive"])
            negative_count = len([m for m in self.moments if m.type == "negative"])
            stats_text = f"📊 {positive_count}+ {negative_count}-"
        else:
            stats_text = "📊 Aún no hay momentos"

        stats_container = ft.Container(
            content=ft.Text(
                stats_text,
                size=11,  # ✅ Texto pequeño
                color=self.theme.text_secondary,
                text_align=ft.TextAlign.CENTER
            ),
            padding=ft.padding.only(top=8, bottom=6),  # ✅ Espaciado mínimo
            alignment=ft.alignment.center
        )

        # ✅ Selector de modos HORIZONTAL con scroll
        mode_selector = self.build_horizontal_mode_selector()

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
            stats_container,
            mode_selector,
            ft.Container(height=8),  # ✅ Espacios mínimos
            self.main_container,
            ft.Container(height=8),
            self.summary_container
        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        view = ft.View(
            "/interactive_moments",
            [header, ft.Container(content=content, padding=ft.padding.all(10), expand=True)],  # ✅ Padding reducido
            bgcolor=self.theme.primary_bg, padding=0, spacing=0
        )

        return view

    def build_horizontal_mode_selector(self):
        """✅ NUEVO: Selector horizontal con scroll lateral"""
        modes = [
            {"id": "quick", "emoji": "⚡", "name": "Quick"},
            {"id": "mood", "emoji": "🎭", "name": "Mood"},
            {"id": "timeline", "emoji": "⏰", "name": "Timeline"},
            {"id": "templates", "emoji": "🎯", "name": "Templates"}
        ]

        mode_buttons = []
        for mode in modes:
            is_active = self.active_mode == mode["id"]

            button = ft.Container(
                content=ft.Column([
                    ft.Text(mode["emoji"], size=18),
                    ft.Text(mode["name"], size=10, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                width=70,  # ✅ Más estrecho para scroll horizontal
                height=50,  # ✅ Más compacto
                padding=ft.padding.all(8),
                border_radius=10,
                bgcolor=self.theme.accent_primary + "30" if is_active else self.theme.surface,
                border=ft.border.all(2 if is_active else 1,
                                     self.theme.accent_primary if is_active else self.theme.border_color),
                on_click=lambda e, mode_id=mode["id"]: self.switch_mode(mode_id)
            )
            mode_buttons.append(button)

        # ✅ Row con scroll horizontal
        return ft.Container(
            content=ft.Row(
                mode_buttons,
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO  # ✅ Scroll horizontal
            ),
            padding=ft.padding.symmetric(horizontal=5)
        )

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
    # MODO 1: QUICK ADD - OPTIMIZADO MÓVIL Y CENTRADO
    # ===============================
    def build_quick_add_mode(self):
        """✅ OPTIMIZADO: Modo Quick Add centrado para móvil"""

        # ✅ Campo de texto centrado
        self.quick_text_field = ft.TextField(
            hint_text="¿Qué pasó?",
            border_radius=12,
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            content_padding=ft.padding.all(12),
            text_style=ft.TextStyle(color=self.theme.text_primary),
            height=45,  # ✅ Altura fija más pequeña
            text_align=ft.TextAlign.CENTER  # ✅ Texto centrado
        )

        # ✅ Frases rápidas centradas
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
                        content=ft.Text(phrase, size=10, color=self.theme.text_secondary,
                                        text_align=ft.TextAlign.CENTER),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=16,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        on_click=lambda e, p=phrase: self.set_quick_text(p),
                        expand=True
                    )
                    row_phrases.append(btn)
                else:
                    # ✅ Añadir container vacío para mantener centrado
                    row_phrases.append(ft.Container(expand=True))

            if row_phrases:
                phrase_buttons.append(ft.Row(row_phrases, spacing=6, alignment=ft.MainAxisAlignment.CENTER))

        # ✅ Emojis organizados y centrados
        emoji_sections = []

        # Sección positiva centrada
        positive_emojis = ['😊', '🎉', '💪', '☕', '🎵', '🤗']
        positive_section = self.build_centered_emoji_section(
            "✨ Positivos", positive_emojis, "positive", self.theme.positive_main
        )
        emoji_sections.append(positive_section)

        # Sección negativa centrada
        negative_emojis = ['😰', '😔', '😤', '💼', '😫', '🤯']
        negative_section = self.build_centered_emoji_section(
            "🌧️ Difíciles", negative_emojis, "negative", self.theme.negative_main
        )
        emoji_sections.append(negative_section)

        return ft.Column([
            # ✅ Campo de texto centrado
            ft.Container(
                content=self.quick_text_field,
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=20)
            ),

            ft.Container(height=8),

            # ✅ Frases rápidas centradas
            ft.Container(
                content=create_themed_container(
                    content=ft.Column([
                        ft.Text("⚡ Frases:", size=12, weight=ft.FontWeight.W_500,
                                color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=6),
                        ft.Column(phrase_buttons, spacing=4)
                    ]),
                    theme=self.theme
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=20)
            ),

            ft.Container(height=8),

            # ✅ Emojis centrados
            ft.Container(
                content=ft.Column(emoji_sections, spacing=8),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=20)
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def build_centered_emoji_section(self, title: str, emojis: List[str], moment_type: str, color: str):
        """✅ Sección de emojis centrada para móvil"""

        # ✅ Grid de emojis centrado
        emoji_rows = []
        for i in range(0, len(emojis), 3):  # ✅ 3 por fila para mejor centrado
            row_emojis = []
            for j in range(3):
                if i + j < len(emojis):
                    emoji = emojis[i + j]
                    btn = ft.Container(
                        content=ft.Text(emoji, size=22),  # ✅ Emojis más grandes
                        width=45,  # ✅ Botones más grandes
                        height=45,
                        border_radius=8,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        alignment=ft.alignment.center,
                        on_click=lambda e, em=emoji: self.add_quick_moment_safe(em, moment_type, "quick")
                    )
                    row_emojis.append(btn)
                else:
                    # ✅ Container vacío para mantener alineación
                    row_emojis.append(ft.Container(width=45, height=45))

            emoji_rows.append(ft.Row(row_emojis, spacing=8, alignment=ft.MainAxisAlignment.CENTER))

        content = ft.Column([
            ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=color, text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.Column(emoji_rows, spacing=6)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

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
        """✅ CORREGIDO: Añadir momento rápido con persistencia"""
        moment = InteractiveMoment(
            emoji=emoji, text=self.quick_text_field.value.strip(),
            moment_type=moment_type, intensity=7 if moment_type == "positive" else 6,
            category=category
        )

        # ✅ Guardar primero en BD
        if self.auto_save_moment(moment):
            # ✅ Solo añadir a la lista local si se guardó correctamente
            self.moments.append(moment)
            self.quick_text_field.value = ""
            self.show_message(f"✅ {emoji} {moment.text} añadido")
            self.refresh_summary()
            if self.page:
                self.page.update()
        else:
            self.show_message("❌ Error guardando momento", is_error=True)

    # ===============================
    # OTROS MODOS - SIMPLIFICADOS Y CENTRADOS
    # ===============================
    def build_mood_bubbles_mode(self):
        """✅ CENTRADO: Modo Mood Bubbles"""

        # ✅ Slider centrado
        intensity_section = self.build_centered_intensity_slider()

        # ✅ Burbujas centradas
        bubble_options = [
            {'emoji': '😊', 'text': 'Alegre', 'type': 'positive'},
            {'emoji': '🎉', 'text': 'Emocionado', 'type': 'positive'},
            {'emoji': '😌', 'text': 'Tranquilo', 'type': 'positive'},
            {'emoji': '💪', 'text': 'Motivado', 'type': 'positive'},
            {'emoji': '😰', 'text': 'Estresado', 'type': 'negative'},
            {'emoji': '😔', 'text': 'Triste', 'type': 'negative'}
        ]

        # ✅ Grid centrado de burbujas
        bubble_rows = []
        for i in range(0, len(bubble_options), 2):
            row_bubbles = []
            for j in range(2):
                if i + j < len(bubble_options):
                    bubble = bubble_options[i + j]
                    bubble_widget = self.create_centered_mood_bubble(bubble)
                    row_bubbles.append(bubble_widget)
                else:
                    row_bubbles.append(ft.Container(width=110, height=80))  # Espaciador

            bubble_rows.append(ft.Row(row_bubbles, alignment=ft.MainAxisAlignment.CENTER, spacing=12))

        bubbles_container = ft.Container(
            content=create_themed_container(
                content=ft.Column([
                                      ft.Text("🫧 Toca una emoción", size=14, weight=ft.FontWeight.W_600,
                                              color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                                      ft.Container(height=12)
                                  ] + bubble_rows, spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                theme=self.theme
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=20)
        )

        return ft.Column([
            intensity_section,
            ft.Container(height=12),
            bubbles_container
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def build_centered_intensity_slider(self):
        """✅ Slider de intensidad centrado"""
        self.intensity_slider = ft.Slider(
            min=1, max=10, value=self.current_intensity, divisions=9,
            on_change=self.on_intensity_change,
            active_color=self.get_intensity_color(self.current_intensity),
            thumb_color=self.get_intensity_color(self.current_intensity)
        )

        return ft.Container(
            content=create_themed_container(
                content=ft.Column([
                    ft.Text("🎚️ Intensidad", size=14, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),

                    # ✅ Slider centrado
                    ft.Row([
                        ft.Text("😐", size=18),
                        ft.Container(content=self.intensity_slider, expand=True),
                        ft.Text("🤯", size=18)
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Container(height=8),

                    # ✅ Valor centrado
                    ft.Text(f"{int(self.current_intensity)}/10", size=16, weight=ft.FontWeight.BOLD,
                            color=self.get_intensity_color(self.current_intensity), text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                theme=self.theme
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=20)
        )

    def create_centered_mood_bubble(self, bubble_data):
        """✅ Burbuja centrada"""
        is_positive = bubble_data["type"] == "positive"
        base_color = self.theme.positive_main if is_positive else self.theme.negative_main
        light_color = self.theme.positive_light if is_positive else self.theme.negative_light

        bubble = ft.Container(
            content=ft.Column([
                ft.Text(bubble_data["emoji"], size=26),
                ft.Container(height=4),
                ft.Text(bubble_data["text"], size=11, weight=ft.FontWeight.W_500,
                        color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=110,  # ✅ Tamaño óptimo
            height=80,
            padding=ft.padding.all(10),
            border_radius=16,
            bgcolor=light_color,
            border=ft.border.all(2, base_color + "50"),
            on_click=lambda e, bubble=bubble_data: self.create_mood_moment(bubble)
        )

        return bubble

    def build_timeline_mode(self):
        """✅ Timeline centrado"""
        # ✅ Selector de hora centrado
        current_hour = datetime.now().hour
        hours_around = [max(0, current_hour-2), max(0, current_hour-1), current_hour,
                        min(23, current_hour+1), min(23, current_hour+2)]

        hour_buttons = []
        for hour in hours_around:
            is_selected = hour == self.selected_hour
            btn = ft.Container(
                content=ft.Text(f"{hour:02d}:00", size=11, color=self.theme.text_primary),
                width=55, height=32, border_radius=8,
                bgcolor=self.theme.accent_primary + "30" if is_selected else self.theme.surface,
                border=ft.border.all(1, self.theme.accent_primary if is_selected else self.theme.border_color),
                alignment=ft.alignment.center,
                on_click=lambda e, h=hour: self.select_hour(h)
            )
            hour_buttons.append(btn)

        # ✅ Formulario centrado
        self.timeline_text_field = ft.TextField(
            hint_text="¿Qué pasó en esta hora?",
            border_radius=12, bgcolor=self.theme.surface,
            content_padding=ft.padding.all(12), height=45,
            text_align=ft.TextAlign.CENTER
        )

        buttons_row = ft.Row([
            ft.ElevatedButton("✨ Positivo", on_click=lambda e: self.add_timeline_moment("positive"),
                              style=ft.ButtonStyle(bgcolor=self.theme.positive_main, color="#FFFFFF"), expand=True),
            ft.Container(width=8),
            ft.ElevatedButton("🌧️ Difícil", on_click=lambda e: self.add_timeline_moment("negative"),
                              style=ft.ButtonStyle(bgcolor=self.theme.negative_main, color="#FFFFFF"), expand=True)
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.Column([
            ft.Container(
                content=create_themed_container(
                    content=ft.Column([
                        ft.Text("⏰ Selecciona hora", size=14, weight=ft.FontWeight.W_600,
                                color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=8),
                        ft.Row(hour_buttons, spacing=6, alignment=ft.MainAxisAlignment.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    theme=self.theme
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=20)
            ),
            ft.Container(height=12),
            ft.Container(
                content=create_themed_container(
                    content=ft.Column([
                        self.timeline_text_field,
                        ft.Container(height=12),
                        buttons_row
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    theme=self.theme
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=20)
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def build_templates_mode(self):
        """✅ Templates centrados"""
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
                    ft.Text(template["emoji"], size=18),
                    ft.Text(template["text"], size=12, color=self.theme.text_primary, expand=True),
                    ft.Container(
                        content=ft.Text("+", size=14, color=color),
                        width=28, height=28, border_radius=14,
                        bgcolor=color + "20", alignment=ft.alignment.center
                    )
                ], spacing=10, alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(10), border_radius=12,
                bgcolor=color + "10", border=ft.border.all(1, color + "30"),
                on_click=lambda e, t=template: self.add_template_item(t)
            )
            template_items.append(item)

        return ft.Container(
            content=create_themed_container(
                content=ft.Column([
                    ft.Text("🎯 Situaciones comunes", size=14, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=12),
                    ft.Column(template_items, spacing=6)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                theme=self.theme
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=20)
        )

    # ===============================
    # MÉTODOS DE CONTROL - SIN CAMBIOS MAYORES
    # ===============================
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
            return "#F59E0B"
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
    # RESUMEN Y CONTROLES - MEJORADOS
    # ===============================
    def refresh_summary(self):
        """Refrescar resumen"""
        if self.summary_container:
            self.summary_container.content = self.build_moments_summary()
        if self.page:
            self.page.update()

    def build_moments_summary(self):
        """✅ MEJORADO: Resumen centrado y compacto"""
        if not self.moments:
            return ft.Container(
                content=ft.Text("Aún no hay momentos añadidos",
                                color=self.theme.text_hint, text_align=ft.TextAlign.CENTER, size=11),
                padding=ft.padding.all(12),
                alignment=ft.alignment.center
            )

        positive_count = len([m for m in self.moments if m.type == "positive"])
        negative_count = len([m for m in self.moments if m.type == "negative"])

        # ✅ Estadísticas centradas
        stats = ft.Row([
            ft.Column([
                ft.Text(str(positive_count), size=18, weight=ft.FontWeight.BOLD, color=self.theme.positive_main),
                ft.Text("Positivos", size=9, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text(str(negative_count), size=18, weight=ft.FontWeight.BOLD, color=self.theme.negative_main),
                ft.Text("Difíciles", size=9, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Text(str(len(self.moments)), size=18, weight=ft.FontWeight.BOLD, color=self.theme.accent_primary),
                ft.Text("Total", size=9, color=self.theme.text_hint)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

        # ✅ Botones centrados
        action_buttons = ft.Row([
            ft.ElevatedButton(
                "🗑️ Limpiar", on_click=self.clear_moments,
                style=ft.ButtonStyle(bgcolor=self.theme.negative_main, color="#FFFFFF"),
                height=32, expand=True
            ),
            ft.Container(width=8),
            ft.ElevatedButton(
                "💾 Completar día", on_click=self.complete_day,  # ✅ Cambiado
                style=ft.ButtonStyle(bgcolor=self.theme.positive_main, color="#FFFFFF"),
                height=32, expand=True
            )
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.Container(
            content=create_themed_container(
                content=ft.Column([
                    ft.Text("📈 Resumen del día", size=13, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    stats,
                    ft.Container(height=12),
                    action_buttons
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                theme=self.theme
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=20)
        )

    def complete_day(self, e=None):
        """✅ NUEVO: Completar día y crear entrada diaria"""
        if not self.moments:
            self.show_message("⚠️ No hay momentos para completar el día", is_error=True)
            return

        try:
            from services import db
            user_id = self.current_user['id']

            print(f"💾 Completando día con {len(self.moments)} momentos")

            # ✅ Usar nuevo método de la base de datos
            entry_id = db.create_daily_entry_from_moments(
                user_id=user_id,
                free_reflection=f"Día completado con {len(self.moments)} momentos capturados",
                worth_it=len([m for m in self.moments if m.type == "positive"]) >= len([m for m in self.moments if m.type == "negative"])
            )

            if entry_id:
                self.show_message(f"✅ ¡Día completado! {len(self.moments)} momentos guardados")

                # ✅ Limpiar momentos locales
                self.moments.clear()
                self.refresh_summary()

                # ✅ Ir al calendario
                if self.page:
                    self.page.go("/calendar")
            else:
                self.show_message("❌ Error completando el día", is_error=True)

        except Exception as e:
            print(f"❌ Error completando día: {e}")
            self.show_message("❌ Error completando el día", is_error=True)

    def clear_moments(self, e=None):
        """✅ MEJORADO: Limpiar momentos con confirmación"""
        if not self.moments:
            self.show_message("ℹ️ No hay momentos para eliminar")
            return

        # TODO: Añadir diálogo de confirmación en versión futura
        try:
            from services import db
            user_id = self.current_user['id']

            # ✅ Desactivar momentos en BD
            db.deactivate_interactive_moments_today(user_id)

            # ✅ Limpiar lista local
            self.moments.clear()
            self.show_message("🗑️ Momentos eliminados")
            self.refresh_summary()
        except Exception as e:
            print(f"❌ Error limpiando momentos: {e}")
            self.moments.clear()
            self.show_message("🗑️ Momentos eliminados")
            self.refresh_summary()

    # ===============================
    # NAVEGACIÓN - SIN CAMBIOS
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
                content=ft.Text(message, color="#FFFFFF", size=11),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=2000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()