"""
🎨 Selector de Temas Elegante - ReflectApp
Pantalla para elegir entre los diferentes temas profesionales
"""

import flet as ft
from services.reflect_themes_system import (
    ThemeManager, ThemeType, ReflectTheme, get_theme,
    create_themed_container, create_themed_button,
    create_gradient_header, apply_theme_to_page
)

class ThemeSelectorScreen:
    """Pantalla elegante para seleccionar temas"""

    def __init__(self, on_theme_changed=None, on_go_back=None):
        self.theme_manager = ThemeManager()
        self.on_theme_changed = on_theme_changed
        self.on_go_back = on_go_back
        self.page = None

        # Estado
        self.current_selection = None
        self.preview_cards = {}

    def build(self) -> ft.View:
        """Construir vista del selector de temas"""

        # Header con gradiente
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        header = create_gradient_header(
            title="🎨 Selector de Temas",
            left_button=back_button
        )

        # Contenido principal
        content = ft.Column(
            [
                # Introducción
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Elige tu tema favorito",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=get_theme().text_primary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "Cada tema tiene su propia personalidad y ambiente único",
                                size=14,
                                color=get_theme().text_secondary,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(top=30, bottom=20, left=20, right=20)
                ),

                # Grid de temas
                ft.Container(
                    content=ft.Column(
                        [
                            # Fila 1: Deep Ocean y Midnight Pro
                            ft.Row(
                                [
                                    self.create_theme_card(ThemeType.DEEP_OCEAN),
                                    ft.Container(width=16),
                                    self.create_theme_card(ThemeType.MIDNIGHT_PROFESSIONAL)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Container(height=20),
                            # Fila 2: Nordic y Electric
                            ft.Row(
                                [
                                    self.create_theme_card(ThemeType.NORDIC_NIGHT),
                                    ft.Container(width=16),
                                    self.create_theme_card(ThemeType.ELECTRIC_DARK)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ]
                    ),
                    padding=ft.padding.symmetric(horizontal=20)
                ),

                ft.Container(height=30),

                # Botón de aplicar
                ft.Container(
                    content=ft.ElevatedButton(
                        "✨ Aplicar Tema Seleccionado",
                        on_click=self.apply_selected_theme,
                        width=280,
                        height=55,
                        style=ft.ButtonStyle(
                            bgcolor=get_theme().accent_primary,
                            color="#FFFFFF",
                            elevation=8,
                            text_style=ft.TextStyle(
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            shape=ft.RoundedRectangleBorder(radius=16)
                        )
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=30)
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0
        )

        # Vista completa
        view = ft.View(
            "/theme_selector",
            [
                header,
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=get_theme().primary_bg
                )
            ],
            bgcolor=get_theme().primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def create_theme_card(self, theme_type: ThemeType) -> ft.Container:
        """Crear tarjeta de preview de tema"""
        theme = self.theme_manager.themes[theme_type]
        is_current = self.theme_manager.get_current_theme().name == theme.name

        # Determinar si está seleccionado
        is_selected = self.current_selection == theme_type

        # Crear preview mini
        mini_preview = self.create_mini_preview(theme)

        # Título y descripción
        header_content = ft.Column(
            [
                ft.Text(
                    theme.display_name,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=get_theme().text_primary,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    theme.description,
                    size=12,
                    color=get_theme().text_secondary,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        )

        # Badge si es el tema actual
        current_badge = None
        if is_current:
            current_badge = ft.Container(
                content=ft.Text(
                    "ACTUAL",
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF"
                ),
                bgcolor=get_theme().positive_main,
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=8,
                alignment=ft.alignment.center
            )

        # Contenido de la tarjeta
        card_content = ft.Column(
            [
                header_content,
                ft.Container(height=12),
                mini_preview,
                ft.Container(height=12),
                current_badge if current_badge else ft.Container(height=24)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        # Contenedor principal con efectos
        border_color = theme.accent_primary if is_selected else get_theme().border_color
        border_width = 3 if is_selected else 1

        card = ft.Container(
            content=card_content,
            width=160,
            height=200,
            bgcolor=get_theme().surface,
            border=ft.border.all(border_width, border_color),
            border_radius=16,
            padding=ft.padding.all(16),
            on_click=lambda e, t=theme_type: self.select_theme(t),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12 if is_selected else 6,
                color=get_theme().shadow_color,
                offset=ft.Offset(0, 4 if is_selected else 2)
            )
        )

        return card

    def create_mini_preview(self, theme: ReflectTheme) -> ft.Container:
        """Crear mini preview del tema"""

        # Simular elementos de la UI con los colores del tema
        mini_header = ft.Container(
            content=ft.Text(
                "Header",
                size=8,
                color="#FFFFFF",
                text_align=ft.TextAlign.CENTER
            ),
            width=120,
            height=20,
            bgcolor=theme.accent_primary,
            border_radius=4,
            alignment=ft.alignment.center
        )

        # Cards de ejemplo
        positive_card = ft.Container(
            content=ft.Text(
                "+ Positivo",
                size=7,
                color="#FFFFFF",
                text_align=ft.TextAlign.CENTER
            ),
            width=55,
            height=16,
            bgcolor=theme.positive_main,
            border_radius=3,
            alignment=ft.alignment.center
        )

        negative_card = ft.Container(
            content=ft.Text(
                "- Negativo",
                size=7,
                color="#FFFFFF",
                text_align=ft.TextAlign.CENTER
            ),
            width=55,
            height=16,
            bgcolor=theme.negative_main,
            border_radius=3,
            alignment=ft.alignment.center
        )

        # Surface de ejemplo
        surface_demo = ft.Container(
            content=ft.Text(
                "Surface",
                size=7,
                color=theme.text_secondary,
                text_align=ft.TextAlign.CENTER
            ),
            width=120,
            height=20,
            bgcolor=theme.surface_variant,
            border_radius=4,
            alignment=ft.alignment.center,
            border=ft.border.all(1, theme.border_color)
        )

        # Layout del preview
        preview_content = ft.Column(
            [
                mini_header,
                ft.Container(height=4),
                ft.Row(
                    [positive_card, negative_card],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4
                ),
                ft.Container(height=4),
                surface_demo
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        return ft.Container(
            content=preview_content,
            width=130,
            height=80,
            bgcolor=theme.primary_bg,
            border_radius=8,
            padding=ft.padding.all(6),
            border=ft.border.all(1, theme.border_color)
        )

    def select_theme(self, theme_type: ThemeType):
        """Seleccionar tema"""
        self.current_selection = theme_type
        print(f"Tema seleccionado: {self.theme_manager.themes[theme_type].display_name}")

        if self.page:
            self.page.update()

    def apply_selected_theme(self, e):
        """Aplicar tema seleccionado"""
        if not self.current_selection:
            self.show_message("Selecciona un tema primero", is_error=True)
            return

        # Cambiar tema
        success = self.theme_manager.set_theme(self.current_selection)

        if success:
            theme_name = self.theme_manager.themes[self.current_selection].display_name
            self.show_message(f"✨ Tema {theme_name} aplicado correctamente")

            # Aplicar a la página actual
            if self.page:
                apply_theme_to_page(self.page)

            # Callback si existe
            if self.on_theme_changed:
                self.on_theme_changed(self.current_selection)

            # Volver después de un delay
            # self.page.after(2000, self.go_back)

        else:
            self.show_message("Error aplicando tema", is_error=True)

    def show_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje al usuario"""
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(
                    message,
                    color="#FFFFFF",
                    size=14,
                    weight=ft.FontWeight.W_500
                ),
                bgcolor=get_theme().negative_main if is_error else get_theme().positive_main,
                duration=3000
            )
            self.page.overlay.append(snack)
            snack.open = True
            self.page.update()

    def go_back(self, e=None):
        """Volver a la pantalla anterior"""
        if self.on_go_back:
            self.on_go_back()
        elif self.page:
            self.page.go("/entry")

class ThemeAwareComponent:
    """Clase base para componentes que reaccionan a cambios de tema"""

    def __init__(self):
        self.theme = get_theme()
        self.components = []  # Lista de componentes a actualizar

    def update_theme(self):
        """Actualizar tema y refrescar componentes"""
        self.theme = get_theme()
        self.refresh_components()

    def refresh_components(self):
        """Refrescar todos los componentes registrados"""
        for component in self.components:
            if hasattr(component, 'bgcolor'):
                component.bgcolor = self.theme.surface
            if hasattr(component, 'color'):
                component.color = self.theme.text_primary
            # Añadir más propiedades según necesidad

# Ejemplo de uso avanzado con animaciones
def create_animated_theme_preview(theme: ReflectTheme, width: int = 200, height: int = 120) -> ft.Container:
    """Crear preview animado de tema"""

    # Elementos animados
    animated_circle = ft.Container(
        width=20,
        height=20,
        bgcolor=theme.positive_main,
        border_radius=10,
        # Añadir animación de rotación si es necesario
    )

    gradient_bg = ft.Container(
        width=width - 20,
        height=height - 20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[theme.primary_bg, theme.surface, theme.surface_variant]
        ),
        border_radius=12,
        content=ft.Column(
            [
                ft.Text(
                    theme.display_name,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=theme.text_primary,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=8),
                ft.Row(
                    [
                        ft.Container(
                            width=30,
                            height=8,
                            bgcolor=theme.positive_main,
                            border_radius=4
                        ),
                        ft.Container(width=4),
                        ft.Container(
                            width=30,
                            height=8,
                            bgcolor=theme.negative_main,
                            border_radius=4
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=8),
                animated_circle
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10)
    )

    return ft.Container(
        content=gradient_bg,
        width=width,
        height=height,
        bgcolor=theme.surface,
        border_radius=16,
        border=ft.border.all(2, theme.border_color),
        padding=ft.padding.all(10),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=theme.shadow_color,
            offset=ft.Offset(0, 4)
        )
    )

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Selector de Temas - ReflectApp"
        page.window.width = 400
        page.window.height = 720

        def on_theme_changed(theme_type):
            print(f"Tema cambiado a: {theme_type}")
            # Aquí recargarías toda la app con el nuevo tema

            selector = ThemeSelectorScreen(on_theme_changed=on_theme_changed)
            selector.page = page

        # Aplicar tema inicial
            apply_theme_to_page(page)

            page.views.append(selector.build())
            page.update()

    ft.app(target=main)