"""
🌙 ReflectApp - MAIN.PY COMPLETO Y CORREGIDO
Todas las rutas funcionando correctamente
"""

import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.InteractiveMoments_screen import InteractiveMomentsScreen
from screens.new_tag_screen import NewTagScreen
from screens.calendar_screen import CalendarScreen
from screens.day_details_screen import DailyReviewScreen
from screens.theme_selector_screen import ThemeSelectorScreen

# ✅ IMPORTACIONES MÓVILES PARA NOTIFICACIONES
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
    """Aplicación ReflectApp CON TODAS LAS RUTAS CORREGIDAS"""

    def __init__(self):
        self.current_user = None
        self.theme_manager = ThemeManager()

        # Pantallas
        self.login_screen = None
        self.register_screen = None
        self.interactive_screen = None
        self.new_tag_screen = None
        self.calendar_screen = None
        self.day_details_screen = None
        self.theme_selector_screen = None
        self.mobile_notification_settings_screen = None

        # Estado
        self.current_day_details = None
        self.page = None

        # Sistema de notificaciones móvil
        self.mobile_notification_service = None
        self.notifications_active = False

        print("🚀 ReflectApp inicializada CON TODAS LAS RUTAS CORREGIDAS")

    def main(self, page: ft.Page):
        """Inicializar aplicación principal"""
        self.page = page
        print("🚀 === MAIN APP INICIADA ===")

        # Configuración de la página
        page.title = "ReflectApp - Tu espacio de reflexión"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.padding = 0
        page.spacing = 0
        page.window.width = 390
        page.window.height = 844
        page.window.resizable = False

        # ✅ Inicializar notificaciones móviles
        self.initialize_mobile_notification_system()

        # Aplicar tema inicial
        self.apply_current_theme()

        # Crear instancias de pantallas
        self.initialize_screens()

        # ✅ CONFIGURAR RUTAS CORRECTAMENTE
        page.on_route_change = self.handle_route_change
        page.on_view_pop = self.handle_view_pop
        page.on_window_event = self.handle_window_event

        # Iniciar en login
        print("🔑 Iniciando en LOGIN")
        page.go("/login")

    # ===============================
    # ✅ SISTEMA DE NOTIFICACIONES MÓVIL
    # ===============================

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
                self.mobile_notification_service.send_mobile_notification(
                    title=f"¡Hola {user_name}! 👋",
                    message="🔔 Notificaciones activas. Te recordaremos reflexionar",
                    icon="🌟",
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
            self.mobile_notification_service.send_mobile_notification(
                title="Hasta luego",
                message=f"👋 Nos vemos pronto {user_name}",
                icon="💙",
                priority="low"
            )

    # ===============================
    # ✅ MANEJO DE RUTAS CORREGIDO
    # ===============================

    def handle_route_change(self, route):
        """Manejar cambios de ruta - CORREGIDO COMPLETO"""
        print(f"🛣️ === NAVEGACIÓN A: {self.page.route} ===")
        self.page.views.clear()

        # Aplicar tema actual
        self.apply_current_theme()

        # ✅ RUTAS PRINCIPALES
        if self.page.route == "/login" or self.page.route == "/":
            print("🏠 Navegando a LOGIN")
            self.page.views.append(self.create_themed_login())

        elif self.page.route == "/register":
            print("📝 Navegando a REGISTER")
            self.page.views.append(self.create_themed_register())

        elif self.page.route == "/entry":
            print("🎮 Navegando a INTERACTIVE MOMENTS")
            self.handle_interactive_route()

        # ✅ RUTAS DE TAGS
        elif self.page.route.startswith("/new_tag"):
            print(f"🏷️ Navegando a NEW_TAG: {self.page.route}")
            self.handle_new_tag_route()

        # ✅ RUTA DE CALENDARIO
        elif self.page.route == "/calendar":
            print("📅 Navegando a CALENDAR")
            self.handle_calendar_route()

        # ✅ RUTAS DE DETALLES DE DÍA
        elif self.page.route.startswith("/day_details"):
            print("📊 Navegando a DAY_DETAILS")
            self.handle_day_details_route()

        elif self.page.route == "/daily_review":
            print("📝 Navegando a DAILY_REVIEW")
            self.handle_daily_review_route()

        # ✅ RUTA DE SELECTOR DE TEMAS
        elif self.page.route == "/theme_selector":
            print("🎨 Navegando a THEME_SELECTOR")
            self.handle_theme_selector_route()

        # ✅ RUTA DE CONFIGURACIÓN DE NOTIFICACIONES
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
    # ✅ HANDLERS DE RUTAS ESPECÍFICAS
    # ===============================

    def handle_interactive_route(self):
        """Manejar ruta de InteractiveMoments"""
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

                    # Notificación de éxito
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

        self.interactive_screen = InteractiveMomentsScreen(
            on_moments_created=on_moments_created,
            on_go_back=on_go_back
        )

        self.interactive_screen.page = self.page
        if hasattr(self.interactive_screen, 'set_user'):
            self.interactive_screen.set_user(self.current_user)

        view = self.interactive_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def handle_new_tag_route(self):
        """Manejar ruta de nuevo tag"""
        print("🏷️ === HANDLE NEW TAG ROUTE ===")

        # Determinar tipo según parámetros
        tag_type = "positive"
        if "type=negative" in self.page.route:
            tag_type = "negative"
        elif "type=positive" in self.page.route:
            tag_type = "positive"

        def on_tag_created(tag):
            """Callback para crear tag"""
            print(f"🏷️ Tag creado: {tag.name}")
            self.page.go("/entry")

        def on_cancel():
            """Callback para cancelar"""
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
        """Manejar ruta del calendario - CORREGIDA"""
        print("📅 === HANDLE CALENDAR ROUTE ===")

        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            self.page.go("/login")
            return

        def on_go_to_entry():
            """Ir a entry"""
            self.page.go("/entry")

        def on_view_day(year, month, day, details):
            """Ver detalles de un día específico"""
            print(f"📊 Ver día: {year}-{month}-{day}")
            self.current_day_details = {
                "year": year,
                "month": month,
                "day": day,
                "details": details
            }
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
        """Manejar ruta de detalles del día - REDIRIGIR A DAILY REVIEW"""
        print("📊 === HANDLE DAY DETAILS ROUTE ===")
        # Redirigir a la pantalla de revisión diaria moderna
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
            self.page.go("/calendar")

        self.day_details_screen = DailyReviewScreen(
            app=self,
            user_data=self.current_user,
            on_go_back=on_go_back
        )

        self.day_details_screen.page = self.page
        view = self.day_details_screen.build()
        self.apply_theme_to_view(view)
        self.page.views.append(view)

    def handle_theme_selector_route(self):
        """Manejar ruta del selector de temas - CORREGIDA"""
        print("🎨 === HANDLE THEME SELECTOR ROUTE ===")

        def on_theme_changed(theme_type):
            """Callback cuando cambia el tema"""
            print(f"🎨 Tema cambiado a: {theme_type}")
            self.apply_current_theme()
            self.update_all_screens_theme()
            self.show_theme_change_message(theme_type)

            # Forzar actualización de la página
            if self.page:
                self.page.update()

        def on_go_back():
            """Volver a entry"""
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

        # Importar la pantalla de configuración móvil
        from screens.mobile_notifications_settings_screen import MobileNotificationSettingsScreen

        def on_settings_changed(new_settings):
            """Callback cuando cambian las configuraciones"""
            print(f"📱 Configuración móvil actualizada: {new_settings}")

            if self.mobile_notification_service:
                self.mobile_notification_service.update_settings(new_settings)

        def on_go_back():
            """Volver"""
            self.page.go("/entry")

        def on_test_notification():
            """Probar notificaciones móviles"""
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
    # ✅ MÉTODOS DE NAVEGACIÓN
    # ===============================

    def navigate_to_entry(self, user_data):
        """Navegar a la pantalla de entrada"""
        print(f"🧭 === NAVIGATE TO ENTRY ===")
        print(f"👤 Usuario: {user_data.get('name')} (ID: {user_data.get('id')})")

        self.current_user = user_data

        # Activar notificaciones móviles para este usuario
        self.start_mobile_notifications_for_user(user_data)

        if self.login_screen and hasattr(self.login_screen, 'page'):
            print("🛣️ Navegando desde login a /entry")
            self.login_screen.page.go("/entry")

        print(f"✅ === NAVIGATE TO ENTRY COMPLETADO ===")

    def navigate_to_login(self):
        """Navegar al login"""
        print("🔑 === NAVIGATE TO LOGIN ===")

        # Mensaje de logout móvil
        if self.current_user and self.mobile_notification_service:
            user_name = self.current_user.get('name', 'Viajero')
            self.mobile_notification_service.send_mobile_notification(
                title="Sesión cerrada",
                message=f"👋 Hasta luego {user_name}",
                icon="🚪",
                priority="low"
            )

        self.current_user = None
        if self.page:
            self.page.go("/login")
        print("✅ === NAVIGATE TO LOGIN COMPLETADO ===")

    # ===============================
    # ✅ MÉTODOS AUXILIARES
    # ===============================

    def initialize_screens(self):
        """Inicializar todas las pantallas"""
        print("🏗️ Inicializando pantallas...")
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
    """Crear aplicación con todas las rutas corregidas"""

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

        print("🌙 ReflectApp iniciada CON TODAS LAS RUTAS FUNCIONANDO")
        print(f"🎨 Tema inicial: {get_theme().display_name}")
        print("🔔 Notificaciones móviles: ACTIVAS")
        print("✅ Rutas corregidas: /calendar, /theme_selector, /daily_review")

    return main


if __name__ == "__main__":
    print("🚀 === INICIANDO REFLECTAPP CON RUTAS CORREGIDAS ===")
    print("📋 Rutas disponibles:")
    print("   🏠 /login - Pantalla de inicio de sesión")
    print("   📝 /register - Registro de nuevos usuarios")
    print("   🎮 /entry - Momentos interactivos principales")
    print("   🏷️ /new_tag - Crear nuevos tags")
    print("   📅 /calendar - Calendario con historial")
    print("   📊 /daily_review - Revisión diaria moderna")
    print("   🎨 /theme_selector - Selector de temas")
    print("   🔔 /mobile_notification_settings - Config notificaciones")
    print("=" * 60)

    # Crear y ejecutar aplicación
    app_main = create_improved_app()
    ft.app(target=app_main)