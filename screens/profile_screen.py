"""
👤 Profile Screen CORREGIDA - ReflectApp
✅ ARREGLADO: Removidos todos los iconos ft.Icon y ft.icons
✅ ARREGLADO: Funciones de Flet verificadas
✅ ARREGLADO: Usando solo emojis y texto
"""

import flet as ft
from datetime import datetime, date, timedelta
from typing import Dict, Any, Callable, Optional
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class ProfileScreen:
    """Pantalla de perfil de usuario con diseño moderno SIN ICONOS"""

    def __init__(self, app=None, user_data=None, on_logout: Callable = None, on_go_back: Callable = None):
        self.app = app
        self.user_data = user_data or {}
        self.on_logout = on_logout
        self.on_go_back = on_go_back

        # Estado
        self.page = None
        self.theme = get_theme()

        # Campos editables
        self.name_field = None
        self.selected_avatar = self.user_data.get('avatar_emoji', '🦫')

        # Estadísticas del usuario
        self.user_stats = {}

        print(f"👤 ProfileScreen inicializada para: {self.user_data.get('name', 'Usuario')}")

    def build(self):
        """Construir vista de perfil SIN ICONOS"""
        self.theme = get_theme()

        # Cargar estadísticas del usuario
        self.load_user_statistics()

        # Header con gradient y botón volver
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        # Botón de configuración
        settings_button = ft.Container(
            content=ft.Text("⚙️", size=18),
            on_click=self.go_to_settings,
            bgcolor="#FFFFFF20",
            border_radius=8,
            padding=ft.padding.all(8),
            tooltip="Configuración"
        )

        header = create_gradient_header(
            title="👤 Mi Perfil",
            left_button=back_button,
            right_button=settings_button,
            theme=self.theme
        )

        # Contenido principal
        content = ft.Column([
            # Sección de información personal
            self.build_profile_info_section(),
            ft.Container(height=16),

            # Estadísticas del usuario
            self.build_statistics_section(),
            ft.Container(height=16),

            # Configuración de la cuenta
            self.build_account_settings_section(),
            ft.Container(height=16),

            # Botón de logout
            self.build_logout_section(),
            ft.Container(height=20)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        # Vista completa
        view = ft.View(
            "/profile",
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

    def build_profile_info_section(self):
        """Sección de información personal del usuario SIN ICONOS"""
        user_name = self.user_data.get('name', 'Usuario Zen')
        user_email = self.user_data.get('email', 'email@ejemplo.com')
        join_date = self.user_data.get('created_at', datetime.now().isoformat())

        # Formatear fecha de registro
        try:
            if isinstance(join_date, str):
                join_datetime = datetime.fromisoformat(join_date.replace('Z', '+00:00'))
            else:
                join_datetime = join_date
            formatted_date = join_datetime.strftime("%B %Y")
        except:
            formatted_date = "Hace tiempo"

        # Avatar grande con selector
        avatar_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    self.selected_avatar,
                    size=60,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.TextButton(
                    "Cambiar",
                    on_click=self.show_avatar_picker,
                    style=ft.ButtonStyle(
                        color=self.theme.accent_primary
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            width=120,
            height=120,
            bgcolor=self.theme.surface,
            border_radius=60,
            border=ft.border.all(3, self.theme.accent_primary),
            alignment=ft.alignment.center
        )

        # Campo de nombre editable SIN ICONO
        self.name_field = ft.TextField(
            value=user_name,
            hint_text="Tu nombre",
            border=ft.InputBorder.OUTLINE,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            border_radius=12,
            filled=True,
            bgcolor=self.theme.surface,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(color=self.theme.text_primary, size=16)
        )

        # Información del usuario SIN ICONOS
        info_section = ft.Column([
            self.name_field,
            ft.Container(height=12),

            # Email (no editable por seguridad) - SIN ICONO
            ft.Container(
                content=ft.Row([
                    ft.Text("📧", size=20, color=self.theme.text_secondary),
                    ft.Container(width=12),
                    ft.Text(user_email, size=14, color=self.theme.text_secondary)
                ]),
                padding=ft.padding.all(16),
                border_radius=12,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color)
            ),

            ft.Container(height=12),

            # Fecha de registro - SIN ICONO
            ft.Container(
                content=ft.Row([
                    ft.Text("📅", size=20, color=self.theme.text_secondary),
                    ft.Container(width=12),
                    ft.Text(f"Miembro desde {formatted_date}", size=14, color=self.theme.text_secondary)
                ]),
                padding=ft.padding.all(16),
                border_radius=12,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color)
            )
        ])

        # Layout principal de perfil
        profile_layout = ft.Row([
            avatar_container,
            ft.Container(width=20),
            ft.Column([info_section], expand=True)
        ], alignment=ft.CrossAxisAlignment.START)

        # Botón guardar cambios
        save_button = create_themed_button(
            "💾 Guardar Cambios",
            self.save_profile_changes,
            theme=self.theme,
            button_type="positive",
            width=200,
            height=45
        )

        return create_themed_container(
            content=ft.Column([
                ft.Text(
                    "Información Personal",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme.text_primary
                ),
                ft.Container(height=16),
                profile_layout,
                ft.Container(height=20),
                ft.Row([save_button], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            theme=self.theme
        )

    def build_statistics_section(self):
        """Sección de estadísticas del usuario"""
        stats = [
            {
                "icon": "📝",
                "value": str(self.user_stats.get('total_entries', 0)),
                "label": "Reflexiones",
                "color": self.theme.accent_primary
            },
            {
                "icon": "🔥",
                "value": str(self.user_stats.get('streak_days', 0)),
                "label": "Días seguidos",
                "color": self.theme.positive_main
            },
            {
                "icon": "⭐",
                "value": str(self.user_stats.get('positive_count', 0)),
                "label": "Momentos +",
                "color": self.theme.positive_main
            },
            {
                "icon": "🌧️",
                "value": str(self.user_stats.get('negative_count', 0)),
                "label": "Momentos -",
                "color": self.theme.negative_main
            }
        ]

        # Crear cards de estadísticas
        stat_cards = []
        for i in range(0, len(stats), 2):
            row_stats = []
            for j in range(2):
                if i + j < len(stats):
                    stat = stats[i + j]
                    card = ft.Container(
                        content=ft.Column([
                            ft.Text(stat["icon"], size=24, text_align=ft.TextAlign.CENTER),
                            ft.Text(
                                stat["value"],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=stat["color"],
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                stat["label"],
                                size=12,
                                color=self.theme.text_secondary,
                                text_align=ft.TextAlign.CENTER
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                        width=140,
                        height=100,
                        padding=ft.padding.all(16),
                        border_radius=16,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(1, self.theme.border_color),
                        expand=True
                    )
                    row_stats.append(card)

            if row_stats:
                stat_cards.append(ft.Row(row_stats, spacing=12))

        return create_themed_container(
            content=ft.Column([
                ft.Text(
                    "📊 Tus Estadísticas",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme.text_primary
                ),
                ft.Container(height=16),
                ft.Column(stat_cards, spacing=12)
            ]),
            theme=self.theme
        )

    def build_account_settings_section(self):
        """Sección de configuración de cuenta SIN ICONOS"""
        settings_options = [
            {
                "icon": "🎨",
                "title": "Temas",
                "subtitle": "Personalizar apariencia",
                "action": self.go_to_themes
            },
            {
                "icon": "🔔",
                "title": "Notificaciones",
                "subtitle": "Configurar recordatorios",
                "action": self.go_to_notifications
            },
            {
                "icon": "📊",
                "title": "Exportar Datos",
                "subtitle": "Descargar mis reflexiones",
                "action": self.export_user_data
            },
            {
                "icon": "🔒",
                "title": "Privacidad",
                "subtitle": "Configuración de privacidad",
                "action": self.show_privacy_options
            }
        ]

        option_widgets = []
        for option in settings_options:
            widget = ft.Container(
                content=ft.Row([
                    ft.Text(option["icon"], size=24),
                    ft.Container(width=16),
                    ft.Column([
                        ft.Text(
                            option["title"],
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=self.theme.text_primary
                        ),
                        ft.Text(
                            option["subtitle"],
                            size=12,
                            color=self.theme.text_secondary
                        )
                    ], expand=True, spacing=2),
                    ft.Text("→", size=20, color=self.theme.text_hint)  # EMOJI en lugar de icono
                ], alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(16),
                border_radius=12,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color),
                on_click=lambda e, action=option["action"]: action()
            )
            option_widgets.append(widget)

        return create_themed_container(
            content=ft.Column([
                ft.Text(
                    "⚙️ Configuración",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme.text_primary
                ),
                ft.Container(height=16),
                ft.Column(option_widgets, spacing=8)
            ]),
            theme=self.theme
        )

    def build_logout_section(self):
        """Sección de logout con confirmación SIN ICONOS"""
        return create_themed_container(
            content=ft.Column([
                ft.Text(
                    "Sesión",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme.text_primary
                ),
                ft.Container(height=16),

                # Información de sesión SIN ICONO
                ft.Container(
                    content=ft.Row([
                        ft.Text("🔐", size=20, color=self.theme.positive_main),
                        ft.Container(width=12),
                        ft.Text(
                            "Sesión activa",
                            size=14,
                            color=self.theme.text_primary,
                            expand=True
                        ),
                        ft.Text(
                            "🟢",
                            size=16
                        )
                    ]),
                    padding=ft.padding.all(16),
                    border_radius=12,
                    bgcolor=self.theme.positive_light,
                    border=ft.border.all(1, self.theme.positive_main + "30")
                ),

                ft.Container(height=16),

                # Botón de logout SIN ICONO
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("🚪", size=20),
                        ft.Container(width=8),
                        ft.Text(
                            "Cerrar Sesión",
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color="#FFFFFF"
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.confirm_logout,
                    style=ft.ButtonStyle(
                        bgcolor=self.theme.negative_main,
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=4
                    ),
                    width=200,
                    height=50
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            theme=self.theme
        )

    # ===============================
    # MÉTODOS DE ACCIÓN
    # ===============================

    def load_user_statistics(self):
        """Cargar estadísticas del usuario desde la base de datos"""
        if not self.user_data.get('id'):
            self.user_stats = {}
            return

        try:
            from services import db
            user_id = self.user_data['id']

            # Obtener estadísticas básicas
            total_entries = db.get_entry_count(user_id)

            # Obtener entradas del usuario para calcular más estadísticas
            entries = db.get_user_entries(user_id, limit=100)

            positive_count = 0
            negative_count = 0

            for entry in entries:
                positive_count += len(entry.get('positive_tags', []))
                negative_count += len(entry.get('negative_tags', []))

            # Calcular racha de días consecutivos
            streak_days = self.calculate_streak_days(entries)

            self.user_stats = {
                'total_entries': total_entries,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'streak_days': streak_days
            }

            print(f"📊 Estadísticas cargadas: {self.user_stats}")

        except Exception as e:
            print(f"❌ Error cargando estadísticas: {e}")
            self.user_stats = {}

    def calculate_streak_days(self, entries):
        """Calcular días consecutivos de reflexión"""
        if not entries:
            return 0

        # Ordenar entradas por fecha
        sorted_entries = sorted(entries, key=lambda x: x.get('entry_date', ''), reverse=True)

        streak = 0
        current_date = date.today()

        for entry in sorted_entries:
            try:
                entry_date = datetime.strptime(entry['entry_date'], '%Y-%m-%d').date()

                if entry_date == current_date:
                    streak += 1
                    current_date -= timedelta(days=1)
                else:
                    break

            except:
                continue

        return streak

    def show_avatar_picker(self, e=None):
        """Mostrar selector de avatar"""
        avatar_options = ['🦫', '🧘‍♀️', '🧘‍♂️', '😊', '🌟', '🎯', '🦋', '🌸', '🌿', '⭐', '🔮', '🕊️']

        def select_avatar(emoji):
            self.selected_avatar = emoji
            if self.page:
                # Actualizar el display del avatar
                self.page.update()
            # Cerrar diálogo
            dialog.open = False
            self.page.update()

        # Crear grid de avatares
        avatar_grid = []
        for i in range(0, len(avatar_options), 4):
            row = []
            for j in range(4):
                if i + j < len(avatar_options):
                    emoji = avatar_options[i + j]
                    btn = ft.Container(
                        content=ft.Text(emoji, size=32, text_align=ft.TextAlign.CENTER),
                        width=60,
                        height=60,
                        border_radius=30,
                        bgcolor=self.theme.surface,
                        border=ft.border.all(2, self.theme.accent_primary if emoji == self.selected_avatar else self.theme.border_color),
                        alignment=ft.alignment.center,
                        on_click=lambda e, em=emoji: select_avatar(em)
                    )
                    row.append(btn)
            avatar_grid.append(ft.Row(row, spacing=12, alignment=ft.MainAxisAlignment.CENTER))

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Elige tu avatar", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(avatar_grid, spacing=12),
                width=300,
                height=200
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(dialog))
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """Cerrar diálogo"""
        dialog.open = False
        self.page.update()

    def save_profile_changes(self, e=None):
        """Guardar cambios en el perfil"""
        if not self.name_field or not self.name_field.value.strip():
            self.show_message("⚠️ El nombre no puede estar vacío", is_error=True)
            return

        try:
            from services import db

            # Actualizar datos en la base de datos
            user_id = self.user_data['id']
            new_name = self.name_field.value.strip()

            # Actualizar datos usando el método del servicio de base de datos
            success = db.update_user_profile(
                user_id=user_id,
                name=new_name,
                avatar_emoji=self.selected_avatar
            )

            if success:
                # Actualizar datos locales
                self.user_data['name'] = new_name
                self.user_data['avatar_emoji'] = self.selected_avatar
                self.show_message("✅ Perfil actualizado correctamente")
            else:
                self.show_message("❌ Error actualizando perfil", is_error=True)

        except Exception as e:
            print(f"❌ Error guardando perfil: {e}")
            self.show_message("❌ Error guardando cambios", is_error=True)

    def confirm_logout(self, e=None):
        """Confirmar logout con diálogo"""
        def do_logout(e):
            dialog.open = False
            self.page.update()
            self.perform_logout()

        def cancel_logout(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Text("🚪", size=20),
                ft.Container(width=8),
                ft.Text("Cerrar Sesión", size=18, weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Text(
                "¿Estás seguro de que quieres cerrar sesión?\n\nTus datos se mantendrán seguros.",
                size=14
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_logout),
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    on_click=do_logout,
                    style=ft.ButtonStyle(
                        bgcolor=self.theme.negative_main,
                        color="#FFFFFF"
                    )
                )
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def perform_logout(self):
        """Realizar logout del usuario"""
        try:
            # Limpiar sesión
            from services.session_service import logout_user
            logout_user()

            self.show_message("👋 Sesión cerrada correctamente")

            # Llamar callback de logout
            if self.on_logout:
                self.on_logout()

        except Exception as e:
            print(f"❌ Error en logout: {e}")
            self.show_message("❌ Error cerrando sesión", is_error=True)

    # Métodos de navegación
    def go_to_themes(self):
        """Ir a configuración de temas"""
        if self.page:
            self.page.go("/theme_selector")

    def go_to_notifications(self):
        """Ir a configuración de notificaciones"""
        if self.page:
            self.page.go("/mobile_notification_settings")

    def go_to_settings(self, e=None):
        """Ir a configuración general"""
        self.show_message("ℹ️ Configuración en desarrollo")

    def export_user_data(self):
        """Exportar datos del usuario"""
        self.show_message("📊 Exportación en desarrollo")

    def show_privacy_options(self):
        """Mostrar opciones de privacidad"""
        self.show_message("🔒 Configuración de privacidad en desarrollo")

    def go_back(self, e=None):
        """Volver a la pantalla anterior"""
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