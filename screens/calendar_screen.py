import flet as ft
from datetime import datetime, date, timedelta
import calendar
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class CalendarScreen:

    def __init__(self, user_data=None, on_go_to_entry=None, on_view_day=None):
        self.user_data = user_data
        self.on_go_to_entry = on_go_to_entry      # Callback para ir a entry
        self.on_view_day = on_view_day            # Callback para ver día específico

        # Estado de la vista
        self.current_view = "months"  # "months" o "days"
        self.selected_year = datetime.now().year
        self.selected_month = None    # None = vista de meses, int = vista de días

        # Datos del calendario (se llenarán con métodos de negocio)
        self.months_data = {}         # {month: {"positive": int, "negative": int, "total": int}}
        self.days_data = {}           # {day: {"positive": int, "negative": int, "submitted": bool}}

        # UI Components
        self.page = None
        self.main_container = None
        self.theme = get_theme()  # NUEVO: Tema actual

    def update_theme(self):
        """Actualizar tema - NUEVO MÉTODO"""
        self.theme = get_theme()
        print(f"🎨 Calendar: Tema actualizado a {self.theme.display_name}")

    # ====== MÉTODOS DE NEGOCIO (SIN CAMBIOS) ======

    def load_year_data(self, year):
        try:
            from services import db

            if not self.user_data:
                print("⚠️ Sin datos de usuario para cargar año")
                return self._get_empty_year_data()

            user_id = self.user_data.get('id')
            if not user_id:
                print("⚠️ ID de usuario no encontrado")
                return self._get_empty_year_data()

            print(f"🔍 Cargando datos del año {year} para usuario {user_id}")

            year_data = db.get_year_summary(user_id, year)

            print(f"✅ Datos del año cargados: {year_data}")
            return year_data

        except Exception as e:
            print(f"❌ Error cargando datos del año {year}: {e}")
            return self._get_empty_year_data()

    def _get_empty_year_data(self):
        """Retornar estructura vacía para el año"""
        empty_data = {}
        for month in range(1, 13):
            empty_data[month] = {"positive": 0, "negative": 0, "total": 0}
        return empty_data

    def load_month_data(self, year, month):
        try:
            from services import db

            if not self.user_data:
                print("⚠️ Sin datos de usuario para cargar mes")
                return {}

            user_id = self.user_data.get('id')
            if not user_id:
                print("⚠️ ID de usuario no encontrado")
                return {}

            print(f"🔍 Cargando datos del mes {year}-{month} para usuario {user_id}")

            month_data = db.get_month_summary(user_id, year, month)

            print(f"✅ Datos del mes cargados: {month_data}")
            return month_data

        except Exception as e:
            print(f"❌ Error cargando datos del mes {year}-{month}: {e}")
            return {}

    def get_day_details(self, year, month, day):
        try:
            from services import db

            if not self.user_data:
                print("⚠️ Sin datos de usuario para obtener detalles del día")
                return self._get_empty_day_details()

            user_id = self.user_data.get('id')
            if not user_id:
                print("⚠️ ID de usuario no encontrado")
                return self._get_empty_day_details()

            print(f"🔍 Obteniendo detalles del día {year}-{month}-{day}")

            day_entry = db.get_day_entry(user_id, year, month, day)

            if not day_entry:
                print(f"ℹ️ No hay datos para el día {year}-{month}-{day}")
                return self._get_empty_day_details()

            print(f"✅ Detalles del día obtenidos: {day_entry}")
            return day_entry

        except Exception as e:
            print(f"❌ Error obteniendo detalles del día {year}-{month}-{day}: {e}")
            return self._get_empty_day_details()

    def _get_empty_day_details(self):
        return {
            "reflection": "Sin reflexión guardada para este día",
            "positive_tags": [],
            "negative_tags": [],
            "worth_it": None,
            "mood_score": 5,
            "ai_summary": ""
        }

    def is_current_day(self, year, month, day):
        """Verificar si es el día actual"""
        today = date.today()
        return year == today.year and month == today.month and day == today.day

    def is_future_day(self, year, month, day):
        """Verificar si es un día futuro"""
        today = date.today()
        check_date = date(year, month, day)
        return check_date > today

    def calculate_month_color(self, month_data):
        if month_data["total"] == 0:
            return self.theme.surface_variant  # CAMBIADO: Usar tema

        if month_data["positive"] > month_data["negative"]:
            return self.theme.positive_main
        elif month_data["negative"] > month_data["positive"]:
            return self.theme.negative_main
        else:
            return self.theme.surface_variant  # CAMBIADO: Usar tema

    def calculate_day_color(self, day_data, year, month, day):
        # Día futuro = surface
        if self.is_future_day(year, month, day):
            return self.theme.surface  # CAMBIADO: Usar tema

        # Día actual sin submitear = accent secundario
        if self.is_current_day(year, month, day) and not day_data.get("submitted", False):
            return self.theme.accent_secondary  # CAMBIADO: Usar tema

        # Día con datos = color según balance
        if day_data.get("submitted", False):
            if day_data["positive"] > day_data["negative"]:
                return self.theme.positive_main
            elif day_data["negative"] > day_data["positive"]:
                return self.theme.negative_main
            else:
                return self.theme.surface_variant  # CAMBIADO: Usar tema

        # Sin datos = surface variant
        return self.theme.surface_variant  # CAMBIADO: Usar tema

    # ====== UI METHODS ACTUALIZADOS CON TEMAS ======

    def build(self):
        """Construir vista principal del calendario CON TEMAS"""
        # Actualizar tema
        self.update_theme()

        # Cargar datos iniciales del año
        print(f"🔄 Cargando datos iniciales para el año {self.selected_year}")
        self.months_data = self.load_year_data(self.selected_year)

        # Header con tema
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        header = create_gradient_header(
            title="📅 Calendario Zen",
            left_button=back_button,
            theme=self.theme
        )

        # Contenedor principal que cambiará según la vista
        self.main_container = ft.Container(
            content=self.build_months_view(),  # Empezar con vista de meses
            expand=True,
            padding=ft.padding.all(20)
        )

        # Vista completa CON TEMA
        view = ft.View(
            "/calendar",
            [
                header,
                self.main_container
            ],
            bgcolor=self.theme.primary_bg,  # CAMBIADO: Usar tema
            padding=0,
            spacing=0
        )

        return view

    def build_months_view(self):
        """Construir vista de meses del año CON TEMAS"""

        # Título del año con navegación TEMÁTICA
        year_header = ft.Row(
            [
                create_themed_button(
                    "<",
                    lambda e: self.change_year(-1),
                    theme=self.theme,
                    button_type="primary",
                    width=50,
                    height=50
                ),
                ft.Text(
                    str(self.selected_year),
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme.text_primary,  # CAMBIADO: Usar tema
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
                create_themed_button(
                    ">",
                    lambda e: self.change_year(1),
                    theme=self.theme,
                    button_type="primary",
                    width=50,
                    height=50
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Grid de meses (3x4)
        months_grid = ft.Column(
            [
                ft.Row([
                    self.create_month_card(1, "Enero"),
                    self.create_month_card(2, "Febrero"),
                    self.create_month_card(3, "Marzo")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    self.create_month_card(4, "Abril"),
                    self.create_month_card(5, "Mayo"),
                    self.create_month_card(6, "Junio")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    self.create_month_card(7, "Julio"),
                    self.create_month_card(8, "Agosto"),
                    self.create_month_card(9, "Septiembre")
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    self.create_month_card(10, "Octubre"),
                    self.create_month_card(11, "Noviembre"),
                    self.create_month_card(12, "Diciembre")
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        return ft.Column(
            [
                year_header,
                ft.Container(height=30),
                months_grid,
                ft.Container(height=30),
                self.build_legend()
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

    def create_month_card(self, month_num, month_name):
        """Crear tarjeta de mes CON TEMAS"""

        # Obtener datos REALES del mes
        if hasattr(self, 'months_data') and self.months_data:
            month_data = self.months_data.get(month_num, {"positive": 0, "negative": 0, "total": 0})
        else:
            # Cargar datos si no están disponibles
            self.months_data = self.load_year_data(self.selected_year)
            month_data = self.months_data.get(month_num, {"positive": 0, "negative": 0, "total": 0})

        month_color = self.calculate_month_color(month_data)

        # Determinar si es el mes actual
        current_month = datetime.now().month
        current_year = datetime.now().year
        is_current = month_num == current_month and self.selected_year == current_year

        # Color de fondo y texto CON TEMAS
        if is_current and month_data["total"] == 0:
            bg_color = self.theme.accent_secondary
            text_color = "#FFFFFF" if self.theme.is_dark else self.theme.text_primary
        else:
            bg_color = month_color
            text_color = "#FFFFFF" if month_color in [self.theme.positive_main, self.theme.negative_main] else self.theme.text_primary

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        month_name[:3].upper(),  # ENE, FEB, MAR
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"{month_data['total']}",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"+{month_data['positive']} -{month_data['negative']}",
                        size=10,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4
            ),
            width=100,
            height=80,
            bgcolor=bg_color,
            border_radius=12,
            padding=ft.padding.all(8),
            on_click=lambda e, m=month_num: self.select_month(m),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=self.theme.shadow_color,  # CAMBIADO: Usar tema
                offset=ft.Offset(0, 2)
            )
        )

    def build_days_view(self):
        """Construir vista de días del mes seleccionado CON TEMAS"""

        month_name = calendar.month_name[self.selected_month]

        # Header del mes CON BOTÓN TEMÁTICO
        month_header = ft.Row(
            [
                create_themed_button(
                    "← Meses",
                    lambda e: self.go_to_months_view(),
                    theme=self.theme,
                    button_type="primary",
                    width=100,
                    height=40
                ),
                ft.Text(
                    f"{month_name} {self.selected_year}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=self.theme.text_primary,  # CAMBIADO: Usar tema
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(width=100)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Días de la semana CON TEMA
        weekdays = ft.Row(
            [
                ft.Text("L", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
                ft.Text("M", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
                ft.Text("X", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
                ft.Text("J", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
                ft.Text("V", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
                ft.Text("S", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
                ft.Text("D", size=12, weight=ft.FontWeight.BOLD, color=self.theme.text_secondary, text_align=ft.TextAlign.CENTER, width=40),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Grid de días
        days_grid = self.build_days_grid()

        return ft.Column(
            [
                month_header,
                ft.Container(height=20),
                weekdays,
                ft.Container(height=10),
                days_grid,
                ft.Container(height=30),
                self.build_legend()
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

    def build_days_grid(self):
        """Construir grid de días del mes"""

        # Obtener datos del calendario
        cal = calendar.monthcalendar(self.selected_year, self.selected_month)

        rows = []
        for week in cal:
            day_cells = []
            for day in week:
                if day == 0:
                    # Día vacío
                    day_cells.append(ft.Container(width=40, height=40))
                else:
                    day_cells.append(self.create_day_cell(day))

            rows.append(ft.Row(day_cells, alignment=ft.MainAxisAlignment.CENTER))

        return ft.Column(rows, spacing=8)

    def create_day_cell(self, day):
        """Crear celda de día individual CON TEMAS"""

        # Obtener datos REALES del día
        if hasattr(self, 'days_data') and self.days_data:
            day_data = self.days_data.get(day, {"positive": 0, "negative": 0, "submitted": False})
        else:
            # Cargar datos si no están disponibles
            self.days_data = self.load_month_data(self.selected_year, self.selected_month)
            day_data = self.days_data.get(day, {"positive": 0, "negative": 0, "submitted": False})

        day_color = self.calculate_day_color(day_data, self.selected_year, self.selected_month, day)

        # Determinar si es clickeable
        is_future = self.is_future_day(self.selected_year, self.selected_month, day)
        is_current = self.is_current_day(self.selected_year, self.selected_month, day)

        # Color del texto CON TEMA
        if day_color == self.theme.surface:
            text_color = self.theme.text_hint
        elif day_color in [self.theme.positive_main, self.theme.negative_main]:
            text_color = "#FFFFFF"
        else:
            text_color = self.theme.text_primary

        # Callback de click
        on_click_handler = None
        if not is_future:
            if is_current:
                on_click_handler = lambda e, d=day: self.go_to_current_day()
            else:
                on_click_handler = lambda e, d=day: self.view_past_day(d)

        # Border para día actual CON TEMA
        border = None
        if is_current:
            border = ft.border.all(2, self.theme.accent_primary)

        return ft.Container(
            content=ft.Text(
                str(day),
                size=14,
                weight=ft.FontWeight.W_500,
                color=text_color,
                text_align=ft.TextAlign.CENTER
            ),
            width=40,
            height=40,
            bgcolor=day_color,
            border_radius=8,
            alignment=ft.alignment.center,
            on_click=on_click_handler,
            border=border
        )

    def build_legend(self):
        """Construir leyenda de colores CON TEMAS"""
        return create_themed_container(
            content=ft.Column(
                [
                    ft.Text(
                        "Leyenda:",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=self.theme.text_primary
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            self.create_legend_item(self.theme.positive_main, "Días positivos"),
                            self.create_legend_item(self.theme.negative_main, "Días negativos"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            self.create_legend_item(self.theme.accent_secondary, "Día actual"),
                            self.create_legend_item(self.theme.surface, "Días futuros"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            theme=self.theme,
            border_radius=12
        )

    def create_legend_item(self, color, label):
        """Crear item de leyenda CON TEMAS"""
        return ft.Row(
            [
                ft.Container(width=16, height=16, bgcolor=color, border_radius=4),
                ft.Container(width=8),
                ft.Text(label, size=12, color=self.theme.text_secondary)
            ],
            spacing=0
        )

    # ====== EVENT HANDLERS ACTUALIZADOS ======

    def change_year(self, direction):
        """Cambiar año (+1 o -1)"""
        self.selected_year += direction
        print(f"📅 Cambiando a año {self.selected_year}")

        # Recargar datos del año
        self.months_data = self.load_year_data(self.selected_year)

        # Actualizar vista
        if self.page:
            self.main_container.content = self.build_months_view()
            self.page.update()

    def select_month(self, month):
        """Seleccionar mes para ver días"""
        self.selected_month = month
        self.current_view = "days"
        print(f"📅 Seleccionando mes {month} del año {self.selected_year}")

        # Cargar datos del mes
        self.days_data = self.load_month_data(self.selected_year, month)

        # Cambiar a vista de días
        if self.page:
            self.main_container.content = self.build_days_view()
            self.page.update()

    def go_to_months_view(self):
        """Volver a vista de meses"""
        self.selected_month = None
        self.current_view = "months"
        if self.page:
            self.main_container.content = self.build_months_view()
            self.page.update()

    def go_to_current_day(self):
        """Ir al día actual (entry screen)"""
        print("Ir a entry screen del día actual")
        if self.on_go_to_entry:
            self.on_go_to_entry()

    def view_past_day(self, day):
        """Ver detalles de un día pasado"""
        print(f"Ver día pasado: {self.selected_year}-{self.selected_month}-{day}")
        if self.on_view_day:
            day_details = self.get_day_details(self.selected_year, self.selected_month, day)
            self.on_view_day(self.selected_year, self.selected_month, day, day_details)

    def go_back(self, e):
        """Volver a la pantalla anterior"""
        if hasattr(e, 'page'):
            e.page.go("/entry")

    # ====== MÉTODO DE PRUEBA ======

    def test_calendar_data(self):
        """Método para probar que la carga de datos funciona"""
        print("🧪 TESTING - Probando carga de datos del calendario")

        if not self.user_data:
            print("❌ No hay datos de usuario para probar")
            return

        user_id = self.user_data.get('id')
        print(f"👤 Usuario ID: {user_id}")

        # Test 1: Datos del año actual
        current_year = datetime.now().year
        year_data = self.load_year_data(current_year)
        print(f"📅 Datos del año {current_year}: {year_data}")

        # Test 2: Datos del mes actual
        current_month = datetime.now().month
        month_data = self.load_month_data(current_year, current_month)
        print(f"📆 Datos del mes {current_month}: {month_data}")

        # Test 3: Verificar si submiteó hoy
        try:
            from services import db
            submitted_today = db.has_submitted_today(user_id)
            print(f"✅ ¿Submiteó hoy?: {submitted_today}")
        except Exception as e:
            print(f"❌ Error verificando submisión de hoy: {e}")

        print("🧪 TESTING - Pruebas completadas")

# ====== EJEMPLO DE USO ======