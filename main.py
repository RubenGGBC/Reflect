"""
🌙 ReflectApp - CAMBIO SIMPLE
Solo cambiar /entry para que vaya a InteractiveMomentsScreen
"""

import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
# CAMBIO 1: Importar InteractiveMomentsScreen en lugar de EntryScreen
from screens.InteractiveMoments_screen import InteractiveMomentsScreen
from screens.new_tag_screen import NewTagScreen
from screens.calendar_screen import CalendarScreen
from screens.day_details_screen import DailyReviewScreen
from screens.theme_selector_screen import ThemeSelectorScreen
from services.reflect_themes_system import (
    ThemeManager, ThemeType, get_theme, apply_theme_to_page,
    create_gradient_header, theme_manager
)


class ReflectApp:
    """Aplicación principal - SOLO CAMBIO DE RUTA /entry"""

    def __init__(self):
        self.current_user = None
        self.theme_manager = ThemeManager()

        # Pantallas (se crearán dinámicamente)
        self.login_screen = None
        self.register_screen = None
        # CAMBIO 2: Variable para InteractiveMomentsScreen en lugar de EntryScreen
        self.interactive_screen = None
        self.new_tag_screen = None
        self.calendar_screen = None
        self.day_details_screen = None
        self.theme_selector_screen = None
        self.ai_chat_screen = None
        self.chat_context = None

        # Estado
        self.current_day_details = None
        self.page = None

        print("🚀 ReflectApp inicializada con InteractiveMoments")

    def main(self, page: ft.Page):
        """Inicializar aplicación principal"""
        self.page = page
        print("🚀 === MAIN APP INICIADA ===")

        # Configuración zen de la página
        page.title = "ReflectApp - Tu espacio de reflexión"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.spacing = 0
        page.window.width = 380
        page.window.height = 640
        page.window.resizable = False

        # Aplicar tema inicial
        self.apply_current_theme()

        # Crear instancias de las pantallas
        self.initialize_screens()

        # Sistema de navegación
        def route_change(route):
            """Manejar cambios de ruta"""
            print(f"🛣️ === NAVEGACIÓN A: {page.route} ===")
            page.views.clear()

            # Aplicar tema actual antes de crear vistas
            self.apply_current_theme()

            if page.route == "/login" or page.route == "/":
                print("🏠 Navegando a LOGIN")
                page.views.append(self.create_themed_login())

            elif page.route == "/register":
                print("📝 Navegando a REGISTER")
                page.views.append(self.create_themed_register())

            elif page.route == "/entry":
                # CAMBIO 3: Esta ruta ahora va a InteractiveMomentsScreen
                print("🎮 Navegando a INTERACTIVE MOMENTS (nueva /entry)")
                self.handle_interactive_route(page)

            elif page.route.startswith("/new_tag"):
                print(f"🏷️ Navegando a NEW_TAG: {page.route}")
                self.handle_new_tag_route(page)

            elif page.route == "/calendar":
                print("📅 Navegando a CALENDAR")
                self.handle_calendar_route(page)

            elif page.route.startswith("/day_details"):
                print("📊 Navegando a DAY_DETAILS")
                self.handle_day_details_route(page)

            elif page.route == "/theme_selector":
                print("🎨 Navegando a THEME_SELECTOR")
                self.handle_theme_selector_route(page)

            elif page.route == "/ai_chat":
                print("🧠 Navegando a AI_CHAT")
                self.handle_ai_chat_route(page)

            elif page.route == "/daily_review":
                print("📝 Navegando a DAILY_REVIEW")
                self.handle_daily_review_route(page)

            page.update()
            print(f"✅ Navegación a {page.route} completada")

        def view_pop(view):
            """Manejar navegación hacia atrás"""
            print(f"⬅️ VIEW POP desde {view.route if hasattr(view, 'route') else 'unknown'}")
            page.views.pop()
            if len(page.views) > 0:
                top_view = page.views[-1]
                page.go(top_view.route)
            else:
                page.go("/login")

        page.on_route_change = route_change
        page.on_view_pop = view_pop

        # Iniciar en login
        print("🔑 Iniciando en LOGIN")
        page.go("/login")

    def initialize_screens(self):
        """Inicializar todas las pantallas"""
        print("🏗️ Inicializando pantallas...")
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        # NOTA: interactive_screen se crea dinámicamente
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

    def update_control_theme(self, control, theme):
        """Actualizar tema de un control recursivamente"""
        # Actualizar gradientes
        if hasattr(control, 'gradient') and control.gradient:
            control.gradient.colors = theme.gradient_header

        # Recursión para controles contenedores
        if hasattr(control, 'controls'):
            for child in control.controls:
                self.update_control_theme(child, theme)
        elif hasattr(control, 'content'):
            if control.content:
                self.update_control_theme(control.content, theme)

    def handle_interactive_route(self, page):
        """NUEVO: Manejar ruta de InteractiveMomentsScreen en /entry"""
        print("🎮 === HANDLE INTERACTIVE ROUTE ===")

        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            page.go("/login")
            return

        # Callback cuando se guardan momentos
        def on_moments_created(simple_tags):
            """Callback cuando se crean momentos"""
            print(f"💾 === GUARDANDO {len(simple_tags)} MOMENTOS ===")

            try:
                from services import db
                user_id = self.current_user['id']

                # Convertir SimpleTag a formato de BD
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

                print(f"➕ Tags positivos: {len(positive_tags)}")
                print(f"➖ Tags negativos: {len(negative_tags)}")

                # Guardar en BD
                entry_id = db.save_daily_entry(
                    user_id=user_id,
                    free_reflection="Reflexión creada con Momentos Interactivos",
                    positive_tags=positive_tags,
                    negative_tags=negative_tags,
                    worth_it=True
                )

                if entry_id:
                    print(f"✅ Momentos guardados con ID: {entry_id}")
                    # Mostrar mensaje de éxito y ir al calendario
                    page.go("/calendar")
                else:
                    print("❌ Error guardando momentos")

            except Exception as e:
                print(f"❌ Error guardando momentos: {e}")

        # Callback para volver
        def on_go_back():
            """Volver (logout o calendario)"""
            page.go("/calendar")

        # Crear InteractiveMomentsScreen
        self.interactive_screen = InteractiveMomentsScreen(
            on_moments_created=on_moments_created,
            on_go_back=on_go_back
        )

        # Establecer página y usuario
        self.interactive_screen.page = page
        if hasattr(self.interactive_screen, 'set_user'):
            self.interactive_screen.set_user(self.current_user)

        # Construir vista
        view = self.interactive_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)

        print("✅ InteractiveMomentsScreen creada en /entry")

    def handle_new_tag_route(self, page):
        """Manejar ruta de nuevo tag (mantener igual)"""
        print("🏷️ === HANDLE NEW TAG ROUTE ===")

        # Determinar tipo según parámetros
        tag_type = "positive"
        if "type=negative" in page.route:
            tag_type = "negative"
        elif "type=positive" in page.route:
            tag_type = "positive"

        def on_tag_created_with_navigation(tag):
            """Callback para crear tag"""
            print(f"🏷️ Tag creado: {tag.name}")
            page.go("/entry")  # Volver a Interactive Moments

        def on_cancel():
            """Callback para cancelar"""
            page.go("/entry")

        # Crear nueva instancia
        self.new_tag_screen = NewTagScreen(
            tag_type=tag_type,
            on_tag_created=on_tag_created_with_navigation,
            on_cancel=on_cancel
        )

        view = self.new_tag_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)

    def handle_calendar_route(self, page):
        """Manejar ruta del calendario (mantener igual)"""
        def on_go_to_entry():
            page.go("/entry")  # Ahora va a Interactive Moments

        def on_view_day(year, month, day, details):
            page.go(f"/day_details?year={year}&month={month}&day={day}")
            self.current_day_details = {
                "year": year,
                "month": month,
                "day": day,
                "details": details
            }

        self.calendar_screen = CalendarScreen(
            user_data=self.current_user,
            on_go_to_entry=on_go_to_entry,
            on_view_day=on_view_day
        )
        self.calendar_screen.page = page
        self.update_calendar_theme()

        view = self.calendar_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)

    def handle_day_details_route(self, page):
        """Manejar ruta de detalles del día - CORREGIDO"""
        print("📊 === HANDLE DAY DETAILS ROUTE ===")

        # Redirigir a la pantalla de revisión diaria moderna
        page.go("/daily_review")

    def handle_daily_review_route(self, page):
        """Manejar ruta de la revisión diaria - NUEVO"""
        print("📝 === HANDLE DAILY REVIEW ROUTE ===")

        if not self.current_user:
            print("❌ No hay usuario - redirigiendo a login")
            page.go("/login")
            return

        def on_go_back():
            """Callback para volver"""
            page.go("/calendar")

        # Crear DailyReviewScreen con los parámetros correctos
        self.day_details_screen = DailyReviewScreen(
            app=self,
            user_data=self.current_user,
            on_go_back=on_go_back
        )

        # Establecer página
        self.day_details_screen.page = page

        # Construir vista
        view = self.day_details_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)

        print("✅ DailyReviewScreen creada")

    def handle_theme_selector_route(self, page):
        """Manejar ruta del selector de temas (mantener igual)"""
        def on_theme_changed(theme_type):
            """Callback cuando cambia el tema"""
            print(f"🎨 Tema cambiado a: {theme_type}")
            self.apply_current_theme()
            self.update_all_screens_theme()
            self.show_theme_change_message(theme_type)
            self.force_page_refresh()

        def on_go_back():
            page.go("/entry")  # Volver a Interactive Moments

        self.theme_selector_screen = ThemeSelectorScreen(
            on_theme_changed=on_theme_changed,
            on_go_back=on_go_back
        )
        self.theme_selector_screen.page = page
        page.views.append(self.theme_selector_screen.build())

    def handle_ai_chat_route(self, page):
        """Manejar ruta del chat con IA (placeholder)"""
        print("🧠 === HANDLE AI CHAT ROUTE ===")
        # Por ahora redirigir a interactive
        page.go("/entry")

    def update_all_screens_theme(self):
        """Actualizar tema en todas las pantallas existentes"""
        if self.login_screen:
            self.login_screen = LoginScreen(self)
        if self.register_screen:
            self.register_screen = RegisterScreen(self)
        print("✅ Tema actualizado en todas las pantallas")

    def force_page_refresh(self):
        """Forzar refresh completo de la página"""
        if self.page:
            self.apply_current_theme()
            self.page.update()

    def update_calendar_theme(self):
        """Actualizar tema del calendario"""
        if hasattr(self.calendar_screen, 'update_theme'):
            self.calendar_screen.update_theme()

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

    def navigate_to_entry(self, user_data):
        """Navegar a la pantalla de entrada (ahora InteractiveMoments)"""
        print(f"🧭 === NAVIGATE TO ENTRY (INTERACTIVE) ===")
        print(f"👤 Usuario: {user_data.get('name')} (ID: {user_data.get('id')})")

        self.current_user = user_data

        if self.login_screen and hasattr(self.login_screen, 'page'):
            print("🛣️ Navegando desde login a /entry (InteractiveMoments)")
            self.login_screen.page.go("/entry")

        print(f"✅ === NAVIGATE TO ENTRY COMPLETADO ===")

    def navigate_to_login(self):
        """Navegar al login"""
        print("🔑 === NAVIGATE TO LOGIN ===")
        self.current_user = None
        if self.page:
            self.page.go("/login")
        print("✅ === NAVIGATE TO LOGIN COMPLETADO ===")


def create_improved_app():
    """Crear aplicación con InteractiveMoments en /entry"""

    def main(page: ft.Page):
        """Función principal de la aplicación"""
        app = ReflectApp()

        # Configurar página base
        page.theme = ft.Theme(
            color_scheme_seed="#667EEA",
            visual_density=ft.VisualDensity.COMFORTABLE
        )

        # Aplicar tema inicial antes de inicializar
        apply_theme_to_page(page)

        # Inicializar aplicación
        app.main(page)

        print("🌙 ReflectApp iniciada con InteractiveMoments en /entry")
        print(f"🎨 Tema inicial: {get_theme().display_name}")

    return main


if __name__ == "__main__":
    # Crear y ejecutar aplicación
    app_main = create_improved_app()
    ft.app(target=app_main)