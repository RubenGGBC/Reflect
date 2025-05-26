import flet as ft
from datetime import datetime

class ZenColors:
    """Colores zen"""
    positive_main = "#48BB78"
    positive_light = "#E8F5E8"
    negative_main = "#EF4444"
    negative_light = "#FEE2E2"
    background = "#F8FAFC"
    surface = "#FFFFFF"
    text_primary = "#2D3748"
    text_secondary = "#4A5568"

class DayDetailsScreen:
    """Pantalla para mostrar detalles de un día específico"""

    def __init__(self, year, month, day, day_details, on_go_back=None):
        self.year = year
        self.month = month
        self.day = day
        self.day_details = day_details  # {"reflection": str, "positive_tags": list, "negative_tags": list, "worth_it": bool}
        self.on_go_back = on_go_back

        # Nombres de meses
        self.month_names = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

    def build(self):
        """Construir vista de detalles del día"""

        month_name = self.month_names[self.month - 1]
        date_str = f"{self.day} de {month_name}, {self.year}"

        # Header
        header = ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        "← Volver",
                        on_click=self.go_back,
                        style=ft.ButtonStyle(color="#FFFFFF")
                    ),
                    ft.Text(
                        date_str,
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color="#FFFFFF",
                        expand=True,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(width=80)
                ]
            ),
            padding=ft.padding.all(20),
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#667EEA", "#764BA2"]
            )
        )

        # Contenido principal
        content = ft.Column(
            [
                # Reflexión del día
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Reflexión del día",
                                size=20,
                                weight=ft.FontWeight.W_500,
                                color=ZenColors.text_primary
                            ),
                            ft.Container(height=12),
                            ft.Container(
                                content=ft.Text(
                                    self.day_details.get("reflection", "Sin reflexión guardada"),
                                    size=14,
                                    color=ZenColors.text_secondary,
                                    selectable=True
                                ),
                                padding=ft.padding.all(16),
                                bgcolor="#F8FAFC",
                                border_radius=12,
                                border=ft.border.all(1, "#E5E7EB")
                            )
                        ]
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ZenColors.surface,
                    border_radius=16,
                    border=ft.border.all(1, "#E2E8F0")
                ),

                ft.Container(height=20),

                # Momentos positivos
                self.build_tags_section("+ MOMENTOS POSITIVOS",
                                        self.day_details.get("positive_tags", []),
                                        ZenColors.positive_main,
                                        ZenColors.positive_light),

                ft.Container(height=16),

                # Momentos negativos
                self.build_tags_section("- MOMENTOS NEGATIVOS",
                                        self.day_details.get("negative_tags", []),
                                        ZenColors.negative_main,
                                        ZenColors.negative_light),

                ft.Container(height=20),

                # ¿Mereció la pena?
                self.build_worth_it_section(),

                ft.Container(height=40)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0
        )

        # Vista completa
        view = ft.View(
            "/day_details",
            [
                header,
                ft.Container(
                    content=content,
                    padding=ft.padding.all(20),
                    expand=True
                )
            ],
            bgcolor=ZenColors.background,
            padding=0,
            spacing=0
        )

        return view

    def build_tags_section(self, title, tags, main_color, light_color):
        """Construir sección de tags"""

        tags_widgets = []
        for tag in tags:
            tag_widget = ft.Container(
                content=ft.Text(
                    f"{tag.get('emoji', '•')} {tag.get('name', 'Sin nombre')}",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=ZenColors.text_primary
                ),
                bgcolor=light_color,
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                border_radius=12,
                border=ft.border.all(1, main_color)
            )
            tags_widgets.append(tag_widget)

        if not tags_widgets:
            tags_widgets = [
                ft.Text(
                    "Sin momentos registrados",
                    size=14,
                    color=ZenColors.text_secondary,
                    italic=True
                )
            ]

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        title,
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=main_color
                    ),
                    ft.Container(height=12),
                    ft.Column(tags_widgets, spacing=8)
                ]
            ),
            padding=ft.padding.all(20),
            bgcolor=light_color,
            border_radius=16,
            border=ft.border.all(1, main_color)
        )

    def build_worth_it_section(self):
        """Construir sección de ¿mereció la pena?"""

        worth_it = self.day_details.get("worth_it", None)

        if worth_it is True:
            response = "SI - El día mereció la pena"
            color = ZenColors.positive_main
            bg_color = ZenColors.positive_light
        elif worth_it is False:
            response = "NO - El día no mereció la pena"
            color = ZenColors.negative_main
            bg_color = ZenColors.negative_light
        else:
            response = "Sin respuesta"
            color = ZenColors.text_secondary
            bg_color = "#F8FAFC"

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "¿Mereció la pena el día?",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=ZenColors.text_primary
                    ),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Text(
                            response,
                            size=16,
                            weight=ft.FontWeight.W_500,
                            color=color,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=ft.padding.all(16),
                        bgcolor=bg_color,
                        border_radius=12,
                        border=ft.border.all(1, color),
                        alignment=ft.alignment.center
                    )
                ]
            ),
            padding=ft.padding.all(20),
            bgcolor=ZenColors.surface,
            border_radius=16,
            border=ft.border.all(1, "#E2E8F0")
        )

    def go_back(self, e):
        """Volver al calendario"""
        if self.on_go_back:
            self.on_go_back()
        elif hasattr(e, 'page'):
            e.page.go("/calendar")

# ====== EJEMPLO DE USO ======

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Detalles del Día"
        page.window.width = 400
        page.window.height = 720

        # Datos de ejemplo
        day_details = {
            "reflection": "Hoy fue un día muy productivo. Terminé varios proyectos importantes y me sentí muy satisfecho con mi trabajo. También tuve tiempo para ejercitarme y relajarme.",
            "positive_tags": [
                {"name": "Trabajo productivo", "emoji": "💼"},
                {"name": "Ejercicio", "emoji": "🏃‍♂️"},
                {"name": "Tiempo personal", "emoji": "🧘‍♀️"}
            ],
            "negative_tags": [
                {"name": "Estrés", "emoji": "😰"}
            ],
            "worth_it": True
        }

        def on_go_back():
            print("Volver al calendario")

        day_screen = DayDetailsScreen(
            year=2024,
            month=3,
            day=15,
            day_details=day_details,
            on_go_back=on_go_back
        )

        page.views.append(day_screen.build())
        page.update()

    ft.app(target=main)