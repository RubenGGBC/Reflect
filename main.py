"""
🌙 ReflectApp - MAIN.PY CON SISTEMA DE PERFIL Y SESIONES
✅ NUEVO: Sistema de auto-login y recordar sesión
✅ NUEVO: Pantalla de perfil de usuario con logout
✅ NUEVO: Navegación mejorada con botón de perfil
✅ NUEVO: Emoji de nutria 🦫 en lugar de zen
"""

import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.profile_screen import ProfileScreen
from screens.InteractiveMoments_screen import InteractiveMomentsScreen
from screens.new_tag_screen import NewTagScreen
from screens.calendar_screen import CalendarScreen
from screens.day_details_screen import DailyReviewScreen
from screens.theme_selector_screen import ThemeSelectorScreen

# ✅ NUEVO: Importar sistema de sesiones
from services.session_service import (
    save_user_session, load_user_session, logout_user,
    is_user_logged_in, get_auto_login_data
)

# Importaciones móviles para notificaciones
from services.mobile_notification_service import (
    initialize_mobile_notifications,
    get_mobile_notification_service,
    start_mobile_notifications,
    stop_mobile_notifications,
    send_mobile_notification,
    test_mobile_notifications
)

from services.reflect_themes_system import (
    ThemeManager, ThemeType, get_theme, apply_theme_to_page,
    create_gradient_header, theme_manager
)


class ReflectApp:
    """Aplicación ReflectApp CON SISTEMA DE PERFIL Y SESIONES"""

    def __init__(self):
        self.current_user = None
        self.theme_manager = ThemeManager()

        # Pantallas
        self.login_screen = None
        self.register_screen = None
        self.profile_screen = None  # ✅ NUEVO
        self.interactive_screen = None
        self.new_tag_screen = None
        self.calendar_screen = None
        self.day_details_screen = None
        self.theme_selector_screen = None
        self.mobile_notification_settings_screen = None

        # Estado para navegación entre días
        self.current_day_details = None
        self.selected_date = None
        self.day_data = None

        self.page = None

        # Sistema de notificaciones móvil
        self.mobile_notification_service = None
        self.notifications_active = False

        print("🚀 ReflectApp inicializada CON SISTEMA DE PERFIL Y SESIONES")

    def main(self, page: ft.Page):
        """Inicializar aplicación principal con auto-login"""
        self.page = page
        print("🚀 === MAIN APP INICIADA CON SESIONES ===")

        # Configuración de la página
        page.title = "ReflectApp - Tu refugio mental 🦫"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.padding = 0
        page.spacing = 0
        page.window.width = 390
        page.window.height = 844
        page.window.resizable = False

        # Inicializar notificaciones móviles
        self.initialize_mobile_notification_system()

        # Aplicar tema inicial
        self.apply_current_theme()

        # Crear instancias de pantallas
        self.initialize_screens()

        # Configurar rutas
        page.on_route_change = self.handle_route_change
        page.on_view_pop = self.handle_view_pop
        page.on_window_event = self.handle_window_event

        # ✅ NUEVO: Verificar auto-login antes de ir a login
        print("🔑 Verificando auto-login...")
        auto_login_data = get_auto_login_data()

        if auto_login_data:
            print(f"🔄 Auto-login disponible para: {auto_login_data.get('email')}")
            # Intentar auto-login
            self.attempt_auto_login(auto_login_data)
        else:
            print("🔑 No hay auto-login, iniciando en LOGIN")
            page.go("/login")

    def attempt_auto_login(self, auto_login_data):
        """✅ NUEVO: Intentar auto-login con datos guardados"""
        try:
            from services import db

            # Obtener datos actualizados del usuario
            email = auto_login_data.get('email')

            # TODO: Necesitamos crear el método get_user_by_email en database_service
            # Por ahora, usar los datos guardados
            user_data = {
                "id": auto_login_data.get('user_id'),
                "email": auto_login_data.get('email'),
                "name": auto_login_data.get('name'),
                "avatar_emoji": auto_login_data.get('avatar_emoji', '🦫')
            }

            if user_data and user_data.get('id'):
                print(f"✅ Auto-login exitoso para: {user_data.get('name')}")

                # Navegar directamente a entry
                self.navigate_to_entry(user_data)
            else:
                print("❌ Auto-login falló, ir a login")
                self.page.go("/login")

        except Exception as e:
            print(f"❌ Error en auto-login: {e}")
            self.page.go("/login")

    def initialize_mobile_notification_system(self):
        """Inicializar sistema de notificaciones móvil"""
        try:
            from services import db
            self.mobile_notification_service = initialize_mobile_notifications(
                page=self.page,
                db_service=db
            )
            print("✅ Sistema de notificaciones móvil inicializado")

        except Exception as e:
            print(f"⚠️ Error inicializando notificaciones móviles: {e}")

    def start_mobile_notifications_for_user(self, user_data):
        """Activar notificaciones para usuario"""
        if not self.mobile_notification_service:
            return

        try:
            if not self.notifications_active:
                self.mobile_notification_service.start_notification_scheduler()
                self.notifications_active = True

                user_name = user_data.get('name', 'Viajero')
                user_emoji = user_data.get('avatar_emoji', '🦫')

                self.mobile_notification_service.send_mobile_notification(
                    title=f"¡Hola {user_name}! 👋",
                    message=f"🔔 {user_emoji} Notificaciones activas. Te recordaremos reflexionar",
                    icon=user_emoji,
                    action_route="/entry",
                    priority="normal"
                )
                print(f"📱 Notificaciones activas para {user_name}")

        except Exception as e:
            print(f"❌ Error activando notificaciones: {e}")

    def handle_window_event(self, e):
        """Manejar eventos de ventana"""
        if e.data == "close" and self.mobile_notification_service and self.current_user:
            user_name = self.current_user.get('name', 'Viajero')
            user_emoji = self.current_user.get('avatar_emoji', '🦫')

            self.mobile_notification_service.send_mobile_notification(
                title="Hasta luego",
                message=f"👋 Nos vemos pronto {user_name}",
                icon=user_emoji,
                priority="low"
            )

    def handle_route_change(self, route):
        """Manejar cambios de ruta con sistema de perfil"""
        print(f"🛣️ === NAVEGACIÓN A: {self.page.route} ===")
        self.page.views.clear()

        # Aplicar tema actual
        self.apply_current_theme()

        # Rutas principales
        if self.page.route == "/login" or self.page.route == "/":
            print("🏠 Navegando a LOGIN")
            self.page.views.append(self.create_themed_login())

        elif self.page.route == "/register":
            print("📝 Navegando a REGISTER")
            self.page.views.append(self.create_themed_register())

        # ✅ NUEVO: Ruta de perfil
        elif self.page.route == "/profile":
            print("👤 Navegando a PROFILE")
            self.handle_profile_route()

        elif self.page.route == "/entry":
            print("🎮 Navegando a INTERACTIVE MOMENTS")
            self.handle_interactive_route()

        # Rutas de tags
        elif self.page.route.startswith("/new_tag"):
            print(f"🏷️ Navegando a NEW_TAG: {self.page.route}")
            self.handle_new_tag_route()

        # Ruta de calendario
        elif self.page.route == "/calendar":
            print("📅 Navegando a CALENDAR")
            self.handle_calendar_route()

        # Rutas de detalles de día
        elif self.page.route.startswith("/day_details"):
            print("📊 Navegando a DAY_DETAILS")
            self.handle_day_details_route()

        elif self.page.route == "/daily_review":
            print("📝 Navegando a DAILY_REVIEW")
            self.handle_daily_review_route()

        # Ruta de selector de temas
        elif self.page.route == "/theme_selector":
            print("🎨 Navegando a THEME_SELECTOR")
            self.handle_theme_selector_route()

        # Ruta de configuración de notificaciones
        elif self.page.route == "/mobile_notification_settings":
            print("🔔 Navegando a MOBILE_NOTIFICATION_SETTINGS")
            self.handle_mobile_notification_settings_route()

        else:
            print(f"❓ Ruta desconocida: {self.page.route} - redirigiendo a login")
            self.page.views.append(self.create_themed_login())

        self.page.update()
        print(f"✅ Navegación a {self.page.route} completada")

    def handle_view_pop(self, view):
        """Manejar navegación hacia atrás"""
        print(f"⬅️ VIEW POP desde {getattr(view, 'route', 'unknown')}")
        self.page.views.pop()
        if len(self.page.views) > 0:
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        else:
            self.page.go("/login")

    # ===============================
    # ✅ NUEVO: HANDLER DE PERFIL
    # ===============================
    def handle_profile_route(self):
        """✅ NUEVO: Manejar ruta de perfil"""
        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            self.page.go("/login")
            return

        def on_logout():
            """Callback para logout desde perfil"""
            print("🚪 Logout desde perfil")
            self.perform_logout()

        def on_go_back():
            """Volver desde perfil"""
            self.page.go("/entry")

        self.profile_screen = ProfileScreen(
            app=self,
            user_data=self.current_user,
            on_logout=on_logout,
            on_go_back=on_go_back
        )

        self.profile_screen.page = self.page
        view = self.profile_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def perform_logout(self):
        """✅ NUEVO: Realizar logout completo"""
        try:
            # Enviar notificación de despedida
            if self.mobile_notification_service and self.current_user:
                user_name = self.current_user.get('name', 'Viajero')
                user_emoji = self.current_user.get('avatar_emoji', '🦫')

                self.mobile_notification_service.send_mobile_notification(
                    title="Sesión cerrada",
                    message=f"{user_emoji} Hasta luego {user_name}",
                    icon="🚪",
                    priority="low"
                )

            # Limpiar sesión del sistema
            logout_user()

            # Limpiar estado de la app
            self.current_user = None
            self.selected_date = None
            self.day_data = None

            # Detener notificaciones
            if self.mobile_notification_service and self.notifications_active:
                self.mobile_notification_service.stop_notification_scheduler()
                self.notifications_active = False

            print("✅ Logout completado")

            # Navegar a login
            if self.page:
                self.page.go("/login")

        except Exception as e:
            print(f"❌ Error en logout: {e}")
            # Forzar navegación a login de todas formas
            if self.page:
                self.page.go("/login")

    # ===============================
    # HANDLERS DE RUTAS EXISTENTES - ACTUALIZADOS
    # ===============================
    def handle_interactive_route(self):
        """Manejar ruta de InteractiveMoments con botón de perfil"""
        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            self.page.go("/login")
            return

        def on_moments_created(simple_tags):
            """Callback cuando se crean momentos"""
            print(f"💾 === GUARDANDO {len(simple_tags)} MOMENTOS ===")

            try:
                from services import db
                user_id = self.current_user['id']

                positive_tags = []
                negative_tags = []

                for tag in simple_tags:
                    tag_dict = {
                        'name': tag.name,
                        'context': tag.reason,
                        'emoji': tag.emoji,
                        'type': tag.category
                    }

                    if tag.category == "positive":
                        positive_tags.append(tag_dict)
                    elif tag.category == "negative":
                        negative_tags.append(tag_dict)

                entry_id = db.save_daily_entry(
                    user_id=user_id,
                    free_reflection="Reflexión creada con Momentos Interactivos",
                    positive_tags=positive_tags,
                    negative_tags=negative_tags,
                    worth_it=True
                )

                if entry_id:
                    print(f"✅ Momentos guardados con ID: {entry_id}")

                    if self.mobile_notification_service:
                        self.mobile_notification_service.send_reflection_saved_notification()

                    self.page.go("/calendar")
                else:
                    print("❌ Error guardando momentos")

            except Exception as e:
                print(f"❌ Error guardando momentos: {e}")

        def on_go_back():
            """Volver"""
            self.page.go("/calendar")

        # ✅ NUEVO: Crear InteractiveMomentsScreen con usuario actualizado
        self.interactive_screen = InteractiveMomentsScreen(
            on_moments_created=on_moments_created,
            on_go_back=on_go_back
        )

        # ✅ NUEVO: Añadir método para ir al perfil
        original_build = self.interactive_screen.build

        def enhanced_build():
            view = original_build()
            # Añadir navegación al perfil en los botones de acción
            self.add_profile_button_to_interactive(view)
            return view

        self.interactive_screen.build = enhanced_build
        self.interactive_screen.page = self.page

        if hasattr(self.interactive_screen, 'set_user'):
            self.interactive_screen.set_user(self.current_user)

        view = self.interactive_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def add_profile_button_to_interactive(self, view):
        """✅ NUEVO: Añadir botón de perfil a la pantalla interactive"""
        try:
            # Buscar el header en la vista
            if hasattr(view, 'controls') and len(view.controls) > 0:
                header_container = view.controls[0]
                if hasattr(header_container, 'content') and hasattr(header_container.content, 'controls'):
                    # Buscar los botones de acción en el header
                    for control in header_container.content.controls:
                        if hasattr(control, 'controls') and isinstance(control.controls, list):
                            for subcontrol in control.controls:
                                if hasattr(subcontrol, 'controls') and len(subcontrol.controls) >= 3:
                                    # Añadir botón de perfil
                                    profile_button = ft.Container(
                                        content=ft.Text(self.current_user.get('avatar_emoji', '🦫'), size=16),
                                        on_click=lambda e: self.page.go("/profile"),
                                        bgcolor="#FFFFFF20",
                                        border_radius=8,
                                        padding=ft.padding.all(8),
                                        tooltip="Mi Perfil"
                                    )
                                    subcontrol.controls.append(profile_button)
                                    break
        except Exception as e:
            print(f"⚠️ Error añadiendo botón de perfil: {e}")

    # Los demás métodos handle_* permanecen igual...
    def handle_new_tag_route(self):
        """Manejar ruta de nuevo tag"""
        print("🏷️ === HANDLE NEW TAG ROUTE ===")

        tag_type = "positive"
        if "type=negative" in self.page.route:
            tag_type = "negative"
        elif "type=positive" in self.page.route:
            tag_type = "positive"

        def on_tag_created(tag):
            print(f"🏷️ Tag creado: {tag.name}")
            self.page.go("/entry")

        def on_cancel():
            self.page.go("/entry")

        self.new_tag_screen = NewTagScreen(
            tag_type=tag_type,
            on_tag_created=on_tag_created,
            on_cancel=on_cancel
        )

        view = self.new_tag_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def handle_calendar_route(self):
        """Manejar ruta del calendario"""
        print("📅 === HANDLE CALENDAR ROUTE ===")

        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            self.page.go("/login")
            return

        def on_go_to_entry():
            """Ir a entry"""
            print("🎮 Navegando a entry desde calendario")
            self.selected_date = None
            self.day_data = None
            self.page.go("/entry")

        def on_view_day(year, month, day, details):
            """Ver detalles de un día específico"""
            print(f"📊 === NAVEGANDO A DÍA ESPECÍFICO ===")
            print(f"📅 Fecha: {year}-{month}-{day}")
            print(f"📋 Detalles: {details}")

            self.selected_date = (year, month, day)
            self.day_data = details

            print(f"💾 Datos guardados - Fecha: {self.selected_date}")

            self.page.go("/daily_review")

        self.calendar_screen = CalendarScreen(
            user_data=self.current_user,
            on_go_to_entry=on_go_to_entry,
            on_view_day=on_view_day
        )

        self.calendar_screen.page = self.page
        if hasattr(self.calendar_screen, 'update_theme'):
            self.calendar_screen.update_theme()

        view = self.calendar_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def handle_day_details_route(self):
        """Manejar ruta de detalles del día"""
        print("📊 === HANDLE DAY DETAILS ROUTE ===")
        self.page.go("/daily_review")

    def handle_daily_review_route(self):
        """Manejar ruta de revisión diaria"""
        print("📝 === HANDLE DAILY REVIEW ROUTE ===")

        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            self.page.go("/login")
            return

        def on_go_back():
            """Volver al calendario"""
            print("🔙 Volviendo al calendario desde daily_review")
            self.page.go("/calendar")

        print(f"🔍 Creando DailyReviewScreen...")
        print(f"📅 Fecha seleccionada: {self.selected_date}")
        print(f"📋 Datos del día: {self.day_data}")

        self.day_details_screen = DailyReviewScreen(
            app=self,
            user_data=self.current_user,
            on_go_back=on_go_back,
            target_date=self.selected_date,
            day_details=self.day_data
        )

        self.day_details_screen.page = self.page
        view = self.day_details_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

        print(f"✅ DailyReviewScreen creada correctamente")

    def handle_theme_selector_route(self):
        """Manejar ruta del selector de temas"""
        print("🎨 === HANDLE THEME SELECTOR ROUTE ===")

        def on_theme_changed(theme_type):
            print(f"🎨 Tema cambiado a: {theme_type}")
            self.apply_current_theme()
            self.update_all_screens_theme()
            self.show_theme_change_message(theme_type)

            if self.page:
                self.page.update()

        def on_go_back():
            self.page.go("/entry")

        self.theme_selector_screen = ThemeSelectorScreen(
            on_theme_changed=on_theme_changed,
            on_go_back=on_go_back
        )

        self.theme_selector_screen.page = self.page
        view = self.theme_selector_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def handle_mobile_notification_settings_route(self):
        """Manejar configuración de notificaciones móvil"""
        print("🔔 === HANDLE MOBILE NOTIFICATION SETTINGS ROUTE ===")

        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            self.page.go("/login")
            return

        from screens.mobile_notifications_settings_screen import MobileNotificationSettingsScreen

        def on_settings_changed(new_settings):
            print(f"📱 Configuración móvil actualizada: {new_settings}")

            if self.mobile_notification_service:
                self.mobile_notification_service.update_settings(new_settings)

        def on_go_back():
            self.page.go("/entry")

        def on_test_notification():
            if self.mobile_notification_service:
                self.mobile_notification_service.test_notification()

        self.mobile_notification_settings_screen = MobileNotificationSettingsScreen(
            user_data=self.current_user,
            notification_service=self.mobile_notification_service,
            on_settings_changed=on_settings_changed,
            on_go_back=on_go_back,
            on_test=on_test_notification
        )

        self.mobile_notification_settings_screen.page = self.page
        view = self.mobile_notification_settings_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    # ===============================
    # MÉTODOS DE NAVEGACIÓN - ACTUALIZADOS
    # ===============================
    def navigate_to_entry(self, user_data):
        """✅ ACTUALIZADO: Navegar con sistema de sesiones"""
        print(f"🧭 === NAVIGATE TO ENTRY CON SESIONES ===")
        print(f"👤 Usuario: {user_data.get('name')} (ID: {user_data.get('id')})")

        self.current_user = user_data

        # Activar notificaciones móviles para este usuario
        self.start_mobile_notifications_for_user(user_data)

        if self.login_screen and hasattr(self.login_screen, 'page'):
            print("🛣️ Navegando desde login a /entry")
            self.login_screen.page.go("/entry")

        print(f"✅ === NAVIGATE TO ENTRY COMPLETADO ===")

    def navigate_to_login(self):
        """Navegar al login con logout completo"""
        print("🔑 === NAVIGATE TO LOGIN CON LOGOUT ===")
        self.perform_logout()

    # ===============================
    # MÉTODOS AUXILIARES - ACTUALIZADOS
    # ===============================
    def initialize_screens(self):
        """Inicializar todas las pantallas"""
        print("🏗️ Inicializando pantallas con sistema de sesiones...")
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        print("✅ Pantallas inicializadas")

    def apply_current_theme(self):
        """Aplicar tema actual a la página"""
        if self.page:
            apply_theme_to_page(self.page)

    def create_themed_login(self):
        """Crear login screen con tema aplicado"""
        view = self.login_screen.build()
        self.apply_theme_to_view(view)
        return view

    def create_themed_register(self):
        """Crear register screen con tema aplicado"""
        view = self.register_screen.build()
        self.apply_theme_to_view(view)
        return view

    def apply_theme_to_view(self, view):
        """Aplicar tema actual a una vista específica"""
        theme = get_theme()
        view.bgcolor = theme.primary_bg

    def update_all_screens_theme(self):
        """Actualizar tema en todas las pantallas existentes"""
        if self.login_screen:
            self.login_screen = LoginScreen(self)
        if self.register_screen:
            self.register_screen = RegisterScreen(self)
        print("✅ Tema actualizado en todas las pantallas")

    def show_theme_change_message(self, theme_type):
        """Mostrar mensaje de cambio de tema"""
        if not self.page:
            return

        theme_names = {
            ThemeType.DEEP_OCEAN: "🌊 Deep Ocean",
            ThemeType.ELECTRIC_DARK: "⚡ Electric Dark",
            ThemeType.SPRING_LIGHT: "🌸 Spring Light",
            ThemeType.SUNSET_WARM: "🌅 Sunset Warm"
        }

        theme_name = theme_names.get(theme_type, "Tema")

        snack = ft.SnackBar(
            content=ft.Text(
                f"✨ {theme_name} aplicado correctamente",
                color="#FFFFFF",
                size=14,
                weight=ft.FontWeight.W_500
            ),
            bgcolor=get_theme().positive_main,
            duration=2500
        )

        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()


def create_improved_app():
    """Crear aplicación con sistema de perfil y sesiones"""

    def main(page: ft.Page):
        """Función principal de la aplicación"""
        app = ReflectApp()

        # Configurar página base
        page.theme = ft.Theme(
            color_scheme_seed="#667EEA",
            visual_density=ft.VisualDensity.COMFORTABLE
        )

        apply_theme_to_page(page)
        app.main(page)

        print("🦫 ReflectApp iniciada CON SISTEMA DE PERFIL Y SESIONES")
        print(f"🎨 Tema inicial: {get_theme().display_name}")
        print("🔔 Notificaciones móviles: ACTIVAS")
        print("✅ NUEVAS CARACTERÍSTICAS:")
        print("   👤 Sistema de perfil de usuario")
        print("   🔐 Auto-login y recordar sesión")
        print("   🚪 Logout completo con confirmación")
        print("   🦫 Emoji de nutria en lugar de zen")

    return main


if __name__ == "__main__":
    print("🚀 === INICIANDO REFLECTAPP CON PERFIL Y SESIONES ===")
    print("📋 NUEVAS CARACTERÍSTICAS IMPLEMENTADAS:")
    print("   ✅ Sistema de auto-login con 'Recordarme'")
    print("   ✅ Pantalla de perfil completa con estadísticas")
    print("   ✅ Logout seguro con confirmación")
    print("   ✅ Login screen mejorada con mejor diseño")
    print("   ✅ Emoji de nutria 🦫 en lugar de zen 🧘‍♀️")
    print("   ✅ Navegación fluida entre perfil y otras pantallas")
    print("=" * 70)

    # Crear y ejecutar aplicación
    app_main = create_improved_app()
    ft.app(target=app_main)