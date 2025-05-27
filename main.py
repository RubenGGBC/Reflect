"""
🌙 ReflectApp - Sistema de Temas Profesional
Aplicación principal con soporte completo para temas de modo noche
"""

import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.update_entry_screen import EntryScreen  # Versión actualizada
from screens.new_tag_screen import NewTagScreen
from screens.calendar_screen import CalendarScreen
from screens.day_details_screen import DayDetailsScreen
from screens.theme_selector_screen import ThemeSelectorScreen
from services.reflect_themes_system import (
    ThemeManager, ThemeType, get_theme, apply_theme_to_page,
    create_gradient_header, theme_manager
)

class ReflectApp:
    """Aplicación principal con sistema de temas profesional"""

    def __init__(self):
        self.current_user = None
        self.theme_manager = ThemeManager()

        # Pantallas (se crearán dinámicamente)
        self.login_screen = None
        self.register_screen = None
        self.entry_screen = None
        self.new_tag_screen = None
        self.calendar_screen = None
        self.day_details_screen = None
        self.theme_selector_screen = None

        # Estado
        self.current_day_details = None
        self.page = None

    def main(self, page: ft.Page):
        """Inicializar aplicación principal"""
        self.page = page

        # Configuración zen de la página
        page.title = "ReflectApp - Tu espacio de reflexión"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.spacing = 0
        page.window.width = 400
        page.window.height = 720
        page.window.resizable = False

        # Aplicar tema inicial
        self.apply_current_theme()

        # Crear instancias de las pantallas
        self.initialize_screens()

        # Sistema de navegación
        def route_change(route):
            """Manejar cambios de ruta"""
            page.views.clear()

            # Aplicar tema actual antes de crear vistas
            self.apply_current_theme()

            if page.route == "/login" or page.route == "/":
                page.views.append(self.login_screen.build())

            elif page.route == "/register":
                page.views.append(self.register_screen.build())

            elif page.route == "/entry":
                self.entry_screen.page = page
                self.entry_screen.update_theme()  # Actualizar tema
                page.views.append(self.entry_screen.build())

            elif page.route.startswith("/new_tag"):
                self.handle_new_tag_route(page)


            elif page.route == "/calendar":
                self.handle_calendar_route(page)

            elif page.route.startswith("/day_details"):
                self.handle_day_details_route(page)

            elif page.route == "/theme_selector":
                self.handle_theme_selector_route(page)

            page.update()

        def view_pop(view):
            """Manejar navegación hacia atrás"""
            page.views.pop()
            if len(page.views) > 0:
                top_view = page.views[-1]
                page.go(top_view.route)
            else:
                page.go("/login")

        page.on_route_change = route_change
        page.on_view_pop = view_pop

        # Iniciar en login
        page.go("/login")

    def initialize_screens(self):
        """Inicializar todas las pantallas"""
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.entry_screen = EntryScreen(self)

    def apply_current_theme(self):
        """Aplicar tema actual a la página"""
        if self.page:
            apply_theme_to_page(self.page)

    def handle_new_tag_route(self, page):
        """Manejar ruta de nuevo tag"""
        # Determinar tipo según parámetros
        tag_type = "positive"
        if "type=negative" in page.route:
            tag_type = "negative"
        elif "type=positive" in page.route:
            tag_type = "positive"

        def on_tag_created_with_navigation(tag):
            """Callback para crear tag con navegación"""
            self.entry_screen.page = page
            self.entry_screen.on_tag_created(tag)
            page.go("/entry")

        def on_cancel():
            """Callback para cancelar"""
            page.go("/entry")

        # Crear nueva instancia con tema actual
        self.new_tag_screen = NewTagScreen(
            tag_type=tag_type,
            on_tag_created=on_tag_created_with_navigation,
            on_cancel=on_cancel
        )

        # Aplicar tema a la nueva pantalla
        view = self.new_tag_screen.build()
        page.views.append(view)

    def handle_calendar_route(self, page):
        """Manejar ruta del calendario"""
        def on_go_to_entry():
            page.go("/entry")

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

        # Actualizar colores del calendario con tema actual
        self.update_calendar_theme()

        page.views.append(self.calendar_screen.build())

    def handle_day_details_route(self, page):
        """Manejar ruta de detalles del día"""
        if self.current_day_details:
            details = self.current_day_details

            def on_go_back():
                page.go("/calendar")

            self.day_details_screen = DayDetailsScreen(
                year=details["year"],
                month=details["month"],
                day=details["day"],
                day_details=details["details"],
                on_go_back=on_go_back
            )

            # Actualizar tema de la pantalla de detalles
            view = self.day_details_screen.build()
            self.update_day_details_theme(view)

            page.views.append(view)

    def handle_theme_selector_route(self, page):
        """Manejar ruta del selector de temas"""
        def on_theme_changed(theme_type):
            """Callback cuando cambia el tema"""
            print(f"🎨 Tema cambiado a: {theme_type}")

            # Aplicar nuevo tema a la página
            self.apply_current_theme()

            # Actualizar entry_screen si existe
            if self.entry_screen:
                self.entry_screen.update_theme()

            # Mostrar mensaje de éxito
            self.show_theme_change_message(theme_type)

        def on_go_back():
            """Volver a entry"""
            page.go("/entry")

        self.theme_selector_screen = ThemeSelectorScreen(
            on_theme_changed=on_theme_changed,
            on_go_back=on_go_back
        )
        self.theme_selector_screen.page = page

        page.views.append(self.theme_selector_screen.build())

    def update_calendar_theme(self):
        """Actualizar tema del calendario"""
        if hasattr(self.calendar_screen, 'ZenColors'):
            theme = get_theme()
            # Actualizar colores del calendario
            self.calendar_screen.ZenColors.positive_main = theme.positive_main
            self.calendar_screen.ZenColors.negative_main = theme.negative_main
            self.calendar_screen.ZenColors.background = theme.primary_bg
            self.calendar_screen.ZenColors.surface = theme.surface
            self.calendar_screen.ZenColors.text_primary = theme.text_primary
            self.calendar_screen.ZenColors.text_secondary = theme.text_secondary

    def update_day_details_theme(self, view):
        """Actualizar tema de la pantalla de detalles del día"""
        theme = get_theme()
        view.bgcolor = theme.primary_bg

        # Actualizar colores de los controles si es necesario
        for control in view.controls:
            if hasattr(control, 'bgcolor'):
                if control.bgcolor == "#F8FAFC":  # Color anterior
                    control.bgcolor = theme.primary_bg

    def show_theme_change_message(self, theme_type):
        """Mostrar mensaje de cambio de tema"""
        if not self.page:
            return

        theme_names = {
            ThemeType.DEEP_OCEAN: "🌊 Deep Ocean",
            ThemeType.MIDNIGHT_PROFESSIONAL: "💼 Midnight Pro",
            ThemeType.NORDIC_NIGHT: "🏔️ Nordic Night",
            ThemeType.ELECTRIC_DARK: "⚡ Electric Dark"
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
        """Navegar a la pantalla de entrada"""
        self.current_user = user_data
        if self.entry_screen:
            self.entry_screen.set_user(user_data)
        if self.login_screen and hasattr(self.login_screen, 'page'):
            self.login_screen.page.go("/entry")

    def navigate_to_login(self):
        """Navegar al login"""
        self.current_user = None
        if hasattr(self.entry_screen, 'page') and self.entry_screen.page:
            self.entry_screen.page.go("/login")

class ThemedLoginScreen(LoginScreen):
    """Login screen con soporte de temas"""

    def build(self):
        """Construir vista con tema aplicado"""
        view = super().build()
        theme = get_theme()

        # Actualizar colores principales
        view.bgcolor = theme.primary_bg

        # Buscar y actualizar gradientes
        for control in view.controls:
            if hasattr(control, 'gradient') and control.gradient:
                # Actualizar gradiente del header
                control.gradient.colors = theme.gradient_header

        return view

class ThemedRegisterScreen(RegisterScreen):
    """Register screen con soporte de temas"""

    def build(self):
        """Construir vista con tema aplicado"""
        view = super().build()
        theme = get_theme()

        # Actualizar colores principales
        view.bgcolor = theme.primary_bg

        return view

def create_themed_app():
    """Crear aplicación con temas profesionales"""

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

        print("🌙 ReflectApp iniciada con sistema de temas profesional")
        print(f"🎨 Tema inicial: {get_theme().display_name}")

    return main

def create_theme_demo():
    """Crear demo de temas para testing"""

    def demo_main(page: ft.Page):
        page.title = "Demo de Temas - ReflectApp"
        page.window.width = 500
        page.window.height = 800

        # Aplicar tema inicial
        apply_theme_to_page(page)

        def change_theme(theme_type):
            """Cambiar tema en el demo"""
            theme_manager.set_theme(theme_type)
            apply_theme_to_page(page)
            page.update()

        # Botones para cada tema
        theme_buttons = ft.Column(
            [
                ft.ElevatedButton(
                    "🌊 Deep Ocean",
                    on_click=lambda e: change_theme(ThemeType.DEEP_OCEAN),
                    width=200
                ),
                ft.ElevatedButton(
                    "💼 Midnight Pro",
                    on_click=lambda e: change_theme(ThemeType.MIDNIGHT_PROFESSIONAL),
                    width=200
                ),
                ft.ElevatedButton(
                    "🏔️ Nordic Night",
                    on_click=lambda e: change_theme(ThemeType.NORDIC_NIGHT),
                    width=200
                ),
                ft.ElevatedButton(
                    "⚡ Electric Dark",
                    on_click=lambda e: change_theme(ThemeType.ELECTRIC_DARK),
                    width=200
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Header de demo
        header = create_gradient_header("🎨 Demo de Temas")

        # Contenido de demo
        demo_content = ft.Column(
            [
                ft.Container(height=20),
                ft.Text(
                    "Prueba los diferentes temas:",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=get_theme().text_primary,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                theme_buttons
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(header, demo_content)

    return demo_main

if __name__ == "__main__":
    # Crear y ejecutar aplicación
    app_main = create_themed_app()
    ft.app(target=app_main)

    # Para demo de temas, usar:
    # demo_main = create_theme_demo()
    # ft.app(target=demo_main)