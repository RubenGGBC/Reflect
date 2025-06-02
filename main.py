"""
🌙 ReflectApp - VERSIÓN CORREGIDA CON TAGS TEMPORALES
Aplicación principal con sistema mejorado de persistencia
"""

import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.update_entry_screen import EntryScreen  # Usar versión corregida
from screens.new_tag_screen import NewTagScreen
from screens.calendar_screen import CalendarScreen
from screens.day_details_screen import DayDetailsScreen
from screens.theme_selector_screen import ThemeSelectorScreen
from services.reflect_themes_system import (
    ThemeManager, ThemeType, get_theme, apply_theme_to_page,
    create_gradient_header, theme_manager
)


class ReflectApp:
    """Aplicación principal CORREGIDA con sistema de tags temporales"""

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
        self.ai_chat_screen = None
        self.chat_context = None  #

        # Estado
        self.current_day_details = None
        self.page = None

        print("🚀 ReflectApp CORREGIDA inicializada")

    def main(self, page: ft.Page):
        """Inicializar aplicación principal"""
        self.page = page
        print("🚀 === MAIN APP CORREGIDA INICIADA ===")

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
                print("📖 Navegando a ENTRY")
                self.handle_entry_route(page)

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
            elif page.route=="/ai_chat":
                self.handle_ai_chat_route(page)

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
        self.entry_screen = EntryScreen(self)  # Usar versión corregida
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

        # Actualizar gradientes en la vista
        for control in view.controls:
            self.update_control_theme(control, theme)

    def update_control_theme(self, control, theme):
        """Actualizar tema de un control recursivamente"""
        # Actualizar gradientes
        if hasattr(control, 'gradient') and control.gradient:
            control.gradient.colors = theme.gradient_header

        # Actualizar colores de fondo
        if hasattr(control, 'bgcolor'):
            if control.bgcolor in ["#F8FAFC", "#FFFFFF"]:
                control.bgcolor = theme.surface
            elif control.bgcolor in ["#E8F5E8"]:
                control.bgcolor = theme.positive_light
            elif control.bgcolor in ["#FEE2E2"]:
                control.bgcolor = theme.negative_light

        # Actualizar colores de texto
        if hasattr(control, 'color'):
            if control.color in ["#2D3748"]:
                control.color = theme.text_primary
            elif control.color in ["#4A5568"]:
                control.color = theme.text_secondary

        # Recursión para controles contenedores
        if hasattr(control, 'controls'):
            for child in control.controls:
                self.update_control_theme(child, theme)
        elif hasattr(control, 'content'):
            if control.content:
                self.update_control_theme(control.content, theme)

    def handle_entry_route(self, page):
        """Manejar ruta de entry CORREGIDA"""
        print("📖 === HANDLE ENTRY ROUTE CORREGIDA ===")

        if not self.entry_screen:
            print("🏗️ Creando nueva EntryScreen")
            self.entry_screen = EntryScreen(self)
        else:
            print("♻️ Reutilizando EntryScreen existente")

        self.entry_screen.page = page
        self.entry_screen.update_theme()

        # Si hay usuario, establecerlo
        if self.current_user:
            print(f"👤 Estableciendo usuario: {self.current_user.get('name')} (ID: {self.current_user.get('id')})")
            self.entry_screen.set_user(self.current_user)
        else:
            print("⚠️ No hay usuario actual")

        print("🏗️ Construyendo vista...")
        view = self.entry_screen.build()
        page.views.append(view)
        page.update()  # Renderizar primero
        print("✅ Vista construida y renderizada")

        # NUEVO SISTEMA: Cargar datos después del renderizado
        if self.current_user:
            try:
                print("📅 === CARGANDO DATOS DE HOY ===")
                # Usar el nuevo método que carga entrada + tags temporales
                self.entry_screen.load_and_refresh_all()
                print("✅ === CARGA DE DATOS COMPLETADA ===")
            except Exception as e:
                print(f"❌ ERROR CRÍTICO cargando datos: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠️ No se cargan datos: sin usuario")

    def handle_new_tag_route(self, page):
        """Manejar ruta de nuevo tag"""
        print("🏷️ === HANDLE NEW TAG ROUTE ===")

        # Determinar tipo según parámetros
        tag_type = "positive"
        if "type=negative" in page.route:
            tag_type = "negative"
        elif "type=positive" in page.route:
            tag_type = "positive"

        print(f"🏷️ Tipo de tag: {tag_type}")

        def on_tag_created_with_navigation(tag):
            """Callback para crear tag con navegación"""
            print(f"🏷️ === CALLBACK TAG CREATED ===")
            print(f"📝 Tag recibido: {tag.emoji} {tag.name} ({tag.category})")

            if self.entry_screen:
                print("📤 Enviando tag a EntryScreen...")
                self.entry_screen.page = page
                self.entry_screen.on_tag_created(tag)
                print("✅ Tag enviado a EntryScreen")
            else:
                print("❌ No hay EntryScreen disponible")

            print("🛣️ Navegando de vuelta a /entry")
            page.go("/entry")

        def on_cancel():
            """Callback para cancelar"""
            print("❌ Creación de tag cancelada")
            page.go("/entry")

        # Crear nueva instancia con tema actual
        print("🏗️ Creando NewTagScreen...")
        self.new_tag_screen = NewTagScreen(
            tag_type=tag_type,
            on_tag_created=on_tag_created_with_navigation,
            on_cancel=on_cancel
        )

        view = self.new_tag_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)
        print(f"✅ NewTagScreen creada para tipo: {tag_type}")

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

        self.update_calendar_theme()

        view = self.calendar_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)

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

            view = self.day_details_screen.build()
            self.apply_theme_to_view(view)
            page.views.append(view)

    def handle_theme_selector_route(self, page):
        """Manejar ruta del selector de temas"""
        def on_theme_changed(theme_type):
            """Callback cuando cambia el tema"""
            print(f"🎨 Tema cambiado a: {theme_type}")

            # Aplicar nuevo tema a la página
            self.apply_current_theme()

            # Actualizar TODAS las pantallas existentes
            self.update_all_screens_theme()

            # Mostrar mensaje de éxito
            self.show_theme_change_message(theme_type)

            # Forzar actualización completa de la página
            self.force_page_refresh()

        def on_go_back():
            """Volver a entry"""
            page.go("/entry")

        self.theme_selector_screen = ThemeSelectorScreen(
            on_theme_changed=on_theme_changed,
            on_go_back=on_go_back
        )
        self.theme_selector_screen.page = page

        page.views.append(self.theme_selector_screen.build())

    def update_all_screens_theme(self):
        """Actualizar tema en todas las pantallas existentes"""
        # Actualizar entry_screen si existe
        if self.entry_screen:
            self.entry_screen.update_theme()

        # Recrear otras pantallas para que tomen el nuevo tema
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
        if hasattr(self.calendar_screen, 'ZenColors'):
            theme = get_theme()
            self.calendar_screen.ZenColors.positive_main = theme.positive_main
            self.calendar_screen.ZenColors.negative_main = theme.negative_main
            self.calendar_screen.ZenColors.background = theme.primary_bg
            self.calendar_screen.ZenColors.surface = theme.surface
            self.calendar_screen.ZenColors.text_primary = theme.text_primary
            self.calendar_screen.ZenColors.text_secondary = theme.text_secondary

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
        print(f"🧭 === NAVIGATE TO ENTRY CORREGIDA ===")
        print(f"👤 Usuario: {user_data.get('name')} (ID: {user_data.get('id')})")

        self.current_user = user_data

        if self.entry_screen:
            print("📤 Estableciendo usuario en EntryScreen existente")
            self.entry_screen.set_user(user_data)
        else:
            print("ℹ️ No hay EntryScreen aún - se creará en la navegación")

        if self.login_screen and hasattr(self.login_screen, 'page'):
            print("🛣️ Navegando desde login a /entry")
            self.login_screen.page.go("/entry")

        print(f"✅ === NAVIGATE TO ENTRY COMPLETADO ===")
    def handle_ai_chat_route(self, page):
        """Manejar ruta del chat con IA"""
        print("🧠 === HANDLE AI CHAT ROUTE ===")

        # Crear nueva instancia del chat
        self.ai_chat_screen.page = page

        # Si hay contexto guardado, pasarlo al chat
        if hasattr(self, 'chat_context') and self.chat_context:
            print(f"📋 Pasando contexto al chat:")
            print(f"   Usuario: {self.chat_context.get('user', {}).get('name', 'Unknown')}")
            print(f"   Reflexión: {len(self.chat_context.get('reflection', ''))} caracteres")
            print(f"   Tags: +{len(self.chat_context.get('positive_tags', []))} -{len(self.chat_context.get('negative_tags', []))}")

            self.ai_chat_screen.set_initial_context(
                reflection_text=self.chat_context.get('reflection', ''),
                positive_tags=self.chat_context.get('positive_tags', []),
                negative_tags=self.chat_context.get('negative_tags', []),
                worth_it=self.chat_context.get('worth_it')
            )

            # Limpiar contexto después de usarlo
            self.chat_context = None
        else:
            print("⚠️ No hay contexto para el chat - iniciando chat vacío")

        # Construir y mostrar vista
        view = self.ai_chat_screen.build()
        self.apply_theme_to_view(view)
        page.views.append(view)

        print("✅ Chat IA inicializado correctamente")
    def navigate_to_login(self):
        """Navegar al login"""
        print("🔑 === NAVIGATE TO LOGIN ===")
        self.current_user = None
        if hasattr(self.entry_screen, 'page') and self.entry_screen.page:
            self.entry_screen.page.go("/login")
        print("✅ === NAVIGATE TO LOGIN COMPLETADO ===")

def create_improved_app():
    """Crear aplicación CORREGIDA con sistema mejorado"""

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

        print("🌙 ReflectApp CORREGIDA iniciada con sistema mejorado")
        print(f"🎨 Tema inicial: {get_theme().display_name}")

    return main

if __name__ == "__main__":
    # Crear y ejecutar aplicación corregida
    app_main = create_improved_app()
    ft.app(target=app_main)