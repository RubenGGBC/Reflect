"""
📱 Configuración de Notificaciones Móvil - ReflectApp CORREGIDA
Pantalla optimizada para dispositivos móviles Android/iOS - SIN ERRORES
"""

import flet as ft
from datetime import datetime, time
from typing import Dict, Callable, Optional
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class MobileNotificationSettingsScreen:
    """Configuración de notificaciones optimizada para móvil - CORREGIDA"""

    def __init__(self, user_data=None, notification_service=None,
                 on_settings_changed: Callable = None, on_go_back: Callable = None,
                 on_test: Callable = None):
        self.user_data = user_data
        self.notification_service = notification_service
        self.on_settings_changed = on_settings_changed
        self.on_go_back = on_go_back
        self.on_test = on_test

        # Configuración móvil
        self.settings = {
            "daily_reminder_enabled": True,
            "daily_reminder_time": "20:00",
            "morning_motivation_enabled": True,
            "morning_motivation_time": "09:00",
            "goodnight_enabled": True,
            "goodnight_time": "22:30",
            "wellbeing_checks_enabled": True,
            "notification_sound": True,
            "notification_vibration": True,
            "priority_mode": "normal"  # low, normal, high
        }

        # Estado móvil
        self.page = None
        self.theme = get_theme()
        self.switches = {}
        self.time_fields = {}

        print("📱 MobileNotificationSettingsScreen inicializada - CORREGIDA")

    def build(self):
        """Construir interfaz móvil optimizada - CORREGIDA"""
        self.theme = get_theme()
        self.load_current_settings()

        # ✅ Header móvil compacto
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        test_button = ft.Container(
            content=ft.Text("🧪", size=18),
            on_click=self.test_mobile_notifications,
            bgcolor="#FFFFFF20",
            border_radius=8,
            padding=ft.padding.all(8),
            tooltip="Probar"
        )

        header = create_gradient_header(
            title="🔔 Notificaciones",
            left_button=back_button,
            right_button=test_button,
            theme=self.theme
        )

        # ✅ Contenido móvil con scroll
        content = ft.Column([
            # Estado del sistema móvil
            self.build_mobile_status(),
            ft.Container(height=12),

            # Configuración rápida
            self.build_quick_settings_mobile(),
            ft.Container(height=12),

            # Horarios móvil
            self.build_mobile_schedule(),
            ft.Container(height=12),

            # Configuración avanzada móvil - CORREGIDA
            self.build_mobile_advanced(),
            ft.Container(height=16),

            # Botones de acción móvil
            self.build_mobile_actions(),
            ft.Container(height=20)

        ], scroll=ft.ScrollMode.AUTO, spacing=0)

        # ✅ Vista móvil optimizada
        view = ft.View(
            "/mobile_notification_settings",
            [
                header,
                ft.Container(
                    content=content,
                    padding=ft.padding.all(12),  # Padding reducido para móvil
                    expand=True
                )
            ],
            bgcolor=self.theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def load_current_settings(self):
        """Cargar configuración actual móvil"""
        if self.notification_service and self.user_data:
            try:
                saved_settings = self.notification_service.get_settings()
                self.settings.update(saved_settings)
                print(f"📱 Configuración móvil cargada")
            except Exception as e:
                print(f"⚠️ Error cargando configuración móvil: {e}")

    def build_mobile_status(self):
        """Estado del sistema de notificaciones móvil"""
        system_active = self.notification_service is not None

        status_color = self.theme.positive_main if system_active else self.theme.negative_main
        status_icon = "📱" if system_active else "📵"
        status_text = "Notificaciones Activas" if system_active else "Sistema Inactivo"
        status_detail = "Funcionando en segundo plano" if system_active else "Revisa la configuración"

        return create_themed_container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(status_icon, size=24),
                    width=40, height=40, border_radius=20,
                    bgcolor=status_color + "20",
                    alignment=ft.alignment.center
                ),
                ft.Container(width=12),
                ft.Column([
                    ft.Text(status_text, size=14, weight=ft.FontWeight.W_600,
                            color=self.theme.text_primary),
                    ft.Text(status_detail, size=12,
                            color=self.theme.text_secondary)
                ], expand=True)
            ], alignment=ft.CrossAxisAlignment.CENTER),
            theme=self.theme
        )

    def build_quick_settings_mobile(self):
        """Configuración rápida móvil con switches"""

        # ✅ Switches móviles optimizados
        daily_switch = ft.Switch(
            value=self.settings.get("daily_reminder_enabled", True),
            active_color=self.theme.positive_main,
            scale=0.8,  # Más pequeño para móvil
            on_change=lambda e: self.update_setting("daily_reminder_enabled", e.control.value)
        )
        self.switches["daily"] = daily_switch

        morning_switch = ft.Switch(
            value=self.settings.get("morning_motivation_enabled", True),
            active_color=self.theme.positive_main,
            scale=0.8,
            on_change=lambda e: self.update_setting("morning_motivation_enabled", e.control.value)
        )
        self.switches["morning"] = morning_switch

        goodnight_switch = ft.Switch(
            value=self.settings.get("goodnight_enabled", True),
            active_color=self.theme.positive_main,
            scale=0.8,
            on_change=lambda e: self.update_setting("goodnight_enabled", e.control.value)
        )
        self.switches["goodnight"] = goodnight_switch

        wellbeing_switch = ft.Switch(
            value=self.settings.get("wellbeing_checks_enabled", True),
            active_color=self.theme.positive_main,
            scale=0.8,
            on_change=lambda e: self.update_setting("wellbeing_checks_enabled", e.control.value)
        )
        self.switches["wellbeing"] = wellbeing_switch

        # ✅ Lista compacta para móvil
        settings_mobile = [
            {"icon": "📝", "title": "Recordatorio diario", "switch": daily_switch},
            {"icon": "🌅", "title": "Motivación matutina", "switch": morning_switch},
            {"icon": "🌙", "title": "Buenas noches", "switch": goodnight_switch},
            {"icon": "💚", "title": "Verificación bienestar", "switch": wellbeing_switch}
        ]

        setting_widgets = []
        for item in settings_mobile:
            widget = ft.Container(
                content=ft.Row([
                    ft.Text(item["icon"], size=20),
                    ft.Container(width=8),
                    ft.Text(item["title"], size=13, weight=ft.FontWeight.W_500,
                            color=self.theme.text_primary, expand=True),
                    item["switch"]
                ], alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),  # Más compacto
                border_radius=8,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color)
            )
            setting_widgets.append(widget)

        return create_themed_container(
            content=ft.Column([
                ft.Text("⚙️ Tipos de Notificaciones", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=8),
                ft.Column(setting_widgets, spacing=6)  # Espaciado reducido
            ]),
            theme=self.theme
        )

    def build_mobile_schedule(self):
        """Configuración de horarios móvil"""

        # ✅ Campos de tiempo móvil compactos - CORREGIDOS
        morning_time = ft.TextField(
            value=self.settings.get("morning_motivation_time", "09:00"),
            hint_text="09:00",
            width=70,
            border_radius=6,
            text_align=ft.TextAlign.CENTER,
            content_padding=ft.padding.all(6),
            # ✅ CORREGIDO: Removido text_size y height inválidos
            on_change=lambda e: self.update_setting("morning_motivation_time", e.control.value)
        )

        daily_time = ft.TextField(
            value=self.settings.get("daily_reminder_time", "20:00"),
            hint_text="20:00",
            width=70,
            border_radius=6,
            text_align=ft.TextAlign.CENTER,
            content_padding=ft.padding.all(6),
            on_change=lambda e: self.update_setting("daily_reminder_time", e.control.value)
        )

        goodnight_time = ft.TextField(
            value=self.settings.get("goodnight_time", "22:30"),
            hint_text="22:30",
            width=70,
            border_radius=6,
            text_align=ft.TextAlign.CENTER,
            content_padding=ft.padding.all(6),
            on_change=lambda e: self.update_setting("goodnight_time", e.control.value)
        )

        # ✅ Presets móvil optimizados
        mobile_presets = [
            {"name": "Temprano", "morning": "07:00", "daily": "19:00", "goodnight": "21:30"},
            {"name": "Normal", "morning": "09:00", "daily": "20:00", "goodnight": "22:30"},
            {"name": "Tardío", "morning": "10:30", "daily": "21:30", "goodnight": "23:45"}
        ]

        preset_buttons = []
        for preset in mobile_presets:
            btn = ft.Container(
                content=ft.Text(preset["name"], size=11, color=self.theme.text_primary,
                                text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500),
                padding=ft.padding.symmetric(horizontal=8, vertical=6),
                border_radius=12,
                bgcolor=self.theme.surface,
                border=ft.border.all(1, self.theme.border_color),
                on_click=lambda e, p=preset: self.apply_mobile_preset(p),
                expand=True
            )
            preset_buttons.append(btn)

        return create_themed_container(
            content=ft.Column([
                ft.Text("⏰ Horarios", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=8),

                # ✅ Horarios compactos
                ft.Column([
                    ft.Row([
                        ft.Text("🌅", size=16),
                        ft.Container(width=6),
                        ft.Text("Motivación", size=12, color=self.theme.text_secondary, expand=True),
                        morning_time
                    ], alignment=ft.CrossAxisAlignment.CENTER),

                    ft.Container(height=6),

                    ft.Row([
                        ft.Text("📝", size=16),
                        ft.Container(width=6),
                        ft.Text("Reflexión", size=12, color=self.theme.text_secondary, expand=True),
                        daily_time
                    ], alignment=ft.CrossAxisAlignment.CENTER),

                    ft.Container(height=6),

                    ft.Row([
                        ft.Text("🌙", size=16),
                        ft.Container(width=6),
                        ft.Text("Buenas noches", size=12, color=self.theme.text_secondary, expand=True),
                        goodnight_time
                    ], alignment=ft.CrossAxisAlignment.CENTER)
                ]),

                ft.Container(height=12),

                # ✅ Presets móvil
                ft.Text("🎯 Presets:", size=12, weight=ft.FontWeight.W_500,
                        color=self.theme.text_secondary),
                ft.Container(height=6),
                ft.Row(preset_buttons, spacing=6)
            ]),
            theme=self.theme
        )

    def build_mobile_advanced(self):
        """Configuración avanzada móvil - CORREGIDA"""

        # ✅ Sonido móvil
        sound_switch = ft.Switch(
            value=self.settings.get("notification_sound", True),
            active_color=self.theme.positive_main,
            scale=0.8,
            on_change=lambda e: self.update_setting("notification_sound", e.control.value)
        )

        # ✅ Vibración móvil
        vibration_switch = ft.Switch(
            value=self.settings.get("notification_vibration", True),
            active_color=self.theme.positive_main,
            scale=0.8,
            on_change=lambda e: self.update_setting("notification_vibration", e.control.value)
        )

        # ✅ Prioridad móvil - CORREGIDO: Sin height ni text_size inválidos
        priority_dropdown = ft.Dropdown(
            value=self.settings.get("priority_mode", "normal"),
            options=[
                ft.dropdown.Option("low", "🔕 Silencioso"),
                ft.dropdown.Option("normal", "🔔 Normal"),
                ft.dropdown.Option("high", "📢 Alta prioridad")
            ],
            width=140,
            # ✅ CORREGIDO: Removidos height, text_size y content_padding inválidos
            on_change=lambda e: self.update_setting("priority_mode", e.control.value)
        )

        return create_themed_container(
            content=ft.Column([
                ft.Text("🔧 Configuración Avanzada", size=14, weight=ft.FontWeight.W_600,
                        color=self.theme.text_primary),
                ft.Container(height=8),

                # ✅ Configuraciones compactas móvil
                ft.Column([
                    ft.Row([
                        ft.Text("🔊", size=16),
                        ft.Container(width=8),
                        ft.Text("Sonido", size=12, color=self.theme.text_secondary, expand=True),
                        sound_switch
                    ], alignment=ft.CrossAxisAlignment.CENTER),

                    ft.Container(height=8),

                    ft.Row([
                        ft.Text("📳", size=16),
                        ft.Container(width=8),
                        ft.Text("Vibración", size=12, color=self.theme.text_secondary, expand=True),
                        vibration_switch
                    ], alignment=ft.CrossAxisAlignment.CENTER),

                    ft.Container(height=8),

                    ft.Row([
                        ft.Text("📊", size=16),
                        ft.Container(width=8),
                        ft.Text("Prioridad", size=12, color=self.theme.text_secondary, expand=True),
                        priority_dropdown
                    ], alignment=ft.CrossAxisAlignment.CENTER)
                ])
            ]),
            theme=self.theme
        )

    def build_mobile_actions(self):
        """Botones de acción móvil"""
        return ft.Column([
            # ✅ Botón principal móvil
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Text("💾", size=16),
                    ft.Container(width=8),
                    ft.Text("Guardar Configuración", size=14, weight=ft.FontWeight.W_500)
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=self.save_mobile_settings,
                style=ft.ButtonStyle(
                    bgcolor=self.theme.positive_main,
                    color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                height=45,
                width=280
            ),

            ft.Container(height=8),

            # ✅ Botones secundarios móvil
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("🧪", size=14),
                        ft.Container(width=4),
                        ft.Text("Probar", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.test_mobile_notifications,
                    style=ft.ButtonStyle(
                        bgcolor=self.theme.accent_primary,
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    height=40,
                    expand=True
                ),

                ft.Container(width=8),

                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("🗑️", size=14),
                        ft.Container(width=4),
                        ft.Text("Reset", size=12)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.reset_mobile_settings,
                    style=ft.ButtonStyle(
                        bgcolor=self.theme.negative_main,
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    height=40,
                    expand=True
                )
            ])
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # ===============================
    # MÉTODOS DE CONTROL MÓVIL
    # ===============================

    def update_setting(self, key: str, value):
        """Actualizar configuración móvil"""
        self.settings[key] = value
        print(f"📱 Configuración móvil actualizada: {key} = {value}")

    def apply_mobile_preset(self, preset: Dict):
        """Aplicar preset móvil"""
        self.settings["morning_motivation_time"] = preset["morning"]
        self.settings["daily_reminder_time"] = preset["daily"]
        self.settings["goodnight_time"] = preset["goodnight"]

        # Actualizar campos visuales
        if self.page:
            self.page.update()

        self.show_mobile_message(f"⏰ Preset '{preset['name']}' aplicado")

    def save_mobile_settings(self, e=None):
        """Guardar configuración móvil"""
        try:
            if self.notification_service:
                self.notification_service.update_settings(self.settings)

            if self.on_settings_changed:
                self.on_settings_changed(self.settings)

            self.show_mobile_message("✅ Configuración guardada")
            print(f"📱 Configuración móvil guardada: {self.settings}")

        except Exception as e:
            print(f"❌ Error guardando configuración móvil: {e}")
            self.show_mobile_message("❌ Error guardando", is_error=True)

    def reset_mobile_settings(self, e=None):
        """Resetear configuración móvil"""
        default_settings = {
            "daily_reminder_enabled": True,
            "daily_reminder_time": "20:00",
            "morning_motivation_enabled": True,
            "morning_motivation_time": "09:00",
            "goodnight_enabled": True,
            "goodnight_time": "22:30",
            "wellbeing_checks_enabled": True,
            "notification_sound": True,
            "notification_vibration": True,
            "priority_mode": "normal"
        }

        self.settings.update(default_settings)

        if self.page:
            self.page.update()

        self.show_mobile_message("🔄 Configuración restablecida")

    def test_mobile_notifications(self, e=None):
        """Probar notificaciones móviles"""
        if self.on_test:
            self.on_test()
            self.show_mobile_message("🧪 Notificación de prueba enviada")
        else:
            self.show_mobile_message("⚠️ Pruebas no disponibles", is_error=True)

    def go_back(self, e=None):
        """Volver móvil"""
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/entry")

    def show_mobile_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje optimizado para móvil"""
        print(f"📱 {'❌' if is_error else '✅'} {message}")
        if self.page:
            # ✅ SnackBar más pequeño para móvil
            snack = ft.SnackBar(
                content=ft.Text(message, color="#FFFFFF", size=13),
                bgcolor=self.theme.negative_main if is_error else self.theme.positive_main,
                duration=2500  # Más corto para móvil
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()