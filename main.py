import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.entry_screen import EntryScreen
from screens.new_tag_screen import NewTagScreen
from screens.calendar_screen import CalendarScreen
from screens.day_details_screen import DayDetailsScreen

class ZenColors:
    """Paleta de colores zen y relajantes"""
    # Gradientes principales
    gradient_start = "#667EEA"
    gradient_end = "#764BA2"

    # Sección positiva
    positive_light = "#E8F5E8"
    positive_accent = "#FED6E3"
    positive_glow = "#A8EDEA"
    positive_main = "#48BB78"

    # Sección negativa (antes growth)
    negative_light = "#FEE2E2"
    negative_accent = "#FCB69F"
    negative_glow = "#FECACA"
    negative_main = "#EF4444"

    # Base zen
    background = "#F8FAFC"
    surface = "#FFFFFF"
    surface_variant = "#F1F5F9"

    # Textos zen
    text_primary = "#2D3748"
    text_secondary = "#4A5568"
    text_hint = "#A0AEC0"

    # Estados
    success = "#48BB78"
    warning = "#ED8936"
    error = "#F56565"
    info = "#4299E1"

class ReflectApp:
    def __init__(self):
        self.current_user = None
        self.login_screen = None
        self.register_screen = None
        self.entry_screen = None
        self.new_tag_screen = None
        self.calendar_screen = None
        self.day_details_screen = None
        self.current_day_details = None  # Para pasar datos a la pantalla de detalles

    def main(self, page: ft.Page):
        # Configuración zen de la página
        page.title = "ReflectApp - Tu espacio de reflexion"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.spacing = 0
        page.window.width = 400
        page.window.height = 720
        page.window.resizable = False
        page.bgcolor = ZenColors.background

        # Tema zen personalizado
        page.theme = ft.Theme(
            color_scheme_seed=ZenColors.gradient_start,
            visual_density=ft.VisualDensity.COMFORTABLE
        )

        # Crear instancias de las pantallas
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.entry_screen = EntryScreen(self)

        # Sistema de navegación
        def route_change(route):
            page.views.clear()

            if page.route == "/login" or page.route == "/":
                page.views.append(self.login_screen.build())
            elif page.route == "/register":
                page.views.append(self.register_screen.build())
            elif page.route == "/entry":
                # Establecer página en entry_screen
                self.entry_screen.page = page
                page.views.append(self.entry_screen.build())
            elif page.route.startswith("/new_tag"):
                # Determinar tipo según parámetros o defecto
                tag_type = "positive"  # por defecto
                if "type=negative" in page.route:
                    tag_type = "negative"
                elif "type=positive" in page.route:
                    tag_type = "positive"

                # Crear nueva instancia de NewTagScreen con tipo específico
                def on_tag_created_with_navigation(tag):
                    # Establecer página en entry_screen antes de llamar callback
                    self.entry_screen.page = page
                    # Llamar al método original
                    self.entry_screen.on_tag_created(tag)
                    # Navegar de vuelta a entry
                    page.go("/entry")

                self.new_tag_screen = NewTagScreen(
                    tag_type=tag_type,
                    on_tag_created=on_tag_created_with_navigation,
                    on_cancel=lambda: page.go("/entry")
                )
                page.views.append(self.new_tag_screen.build())
            elif page.route == "/calendar":
                # Crear instancia de CalendarScreen
                def on_go_to_entry():
                    page.go("/entry")

                def on_view_day(year, month, day, details):
                    # Navegar a pantalla de detalles del día
                    page.go(f"/day_details?year={year}&month={month}&day={day}")
                    # Guardar los detalles para la próxima carga
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
                page.views.append(self.calendar_screen.build())
            elif page.route.startswith("/day_details"):
                # Crear instancia de DayDetailsScreen
                if self.current_day_details:
                    details = self.current_day_details
                    self.day_details_screen = DayDetailsScreen(
                        year=details["year"],
                        month=details["month"],
                        day=details["day"],
                        day_details=details["details"],
                        on_go_back=lambda: page.go("/calendar")
                    )
                    page.views.append(self.day_details_screen.build())

            page.update()

        def view_pop(view):
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

    def navigate_to_entry(self, user_data):
        """Navegar a la pantalla de entrada"""
        self.current_user = user_data
        self.entry_screen.set_user(user_data)
        self.login_screen.page.go("/entry")

    def navigate_to_login(self):
        """Navegar al login"""
        self.current_user = None
        if hasattr(self.entry_screen, 'page') and self.entry_screen.page:
            self.entry_screen.page.go("/login")

def main(page: ft.Page):
    app = ReflectApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)