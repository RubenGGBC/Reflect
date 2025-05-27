"""
🎨 Selector de Temas CORREGIDO - ReflectApp
Pantalla para elegir entre los diferentes temas profesionales con funcionamiento correcto
"""

import flet as ft
from services.reflect_themes_system import (
    ThemeManager, ThemeType, ReflectTheme, get_theme,
    create_themed_container, create_themed_button,
    create_gradient_header, apply_theme_to_page, theme_manager
)

class ThemeSelectorScreen:
    """Pantalla elegante para seleccionar temas CORREGIDA"""

    def __init__(self, on_theme_changed=None, on_go_back=None):
        self.theme_manager = theme_manager  # Usar instancia global
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
        theme_name = self.theme_manager.themes[theme_type].display_name
        print(f"🎯 Tema seleccionado: {theme_name}")

        if self.page:
            self.page.update()

    def apply_selected_theme(self, e):
        """Aplicar tema seleccionado CORREGIDO"""
        if not self.current_selection:
            self.show_message("⚠️ Selecciona un tema primero", is_error=True)
            return

        # PASO 1: Cambiar tema en el manager (esto notificará automáticamente)
        success = self.theme_manager.set_theme(self.current_selection)

        if success:
            theme_name = self.theme_manager.themes[self.current_selection].display_name
            print(f"✅ Tema {theme_name} aplicado correctamente")

            # PASO 2: Aplicar inmediatamente a la página actual
            if self.page:
                apply_theme_to_page(self.page)
                self.page.update()

            # PASO 3: Mostrar mensaje de éxito
            self.show_message(f"✨ Tema {theme_name} aplicado")

            # PASO 4: Callback externo si existe
            if self.on_theme_changed:
                try:
                    self.on_theme_changed(self.current_selection)
                except Exception as ex:
                    print(f"❌ Error en callback externo: {ex}")

            # PASO 5: Limpiar selección
            self.current_selection = None

        else:
            self.show_message("❌ Error aplicando tema", is_error=True)

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

# Clase helper para componentes que reaccionan a cambios de tema
class ThemeAwareComponent:
    """Clase base para componentes que reaccionan a cambios de tema"""

    def __init__(self):
        self.theme = get_theme()
        self.components = []  # Lista de componentes a actualizar

        # Registrarse para recibir notificaciones de cambio de tema
        from services.reflect_themes_system import register_theme_callback
        register_theme_callback(self.on_theme_changed)

    def on_theme_changed(self, theme_type):
        """Callback cuando cambia el tema"""
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

# Demo avanzado del selector de temas
def create_theme_demo_advanced():
    """Crear demo avanzado con cambio en tiempo real"""

    def demo_main(page: ft.Page):
        page.title = "Demo Avanzado - Selector de Temas"
        page.window.width = 500
        page.window.height = 800

        # Aplicar tema inicial
        apply_theme_to_page(page)

        # Componentes de demo que cambiarán con el tema
        demo_title = ft.Text(
            "🎨 Demo de Temas en Tiempo Real",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=get_theme().text_primary,
            text_align=ft.TextAlign.CENTER
        )

        demo_container = create_themed_container(
            content=ft.Column(
                [
                    ft.Text("Este contenedor cambia con el tema", color=get_theme().text_secondary),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Container(width=50, height=30, bgcolor=get_theme().positive_main, border_radius=5),
                            ft.Container(width=50, height=30, bgcolor=get_theme().negative_main, border_radius=5),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    )
                ]
            )
        )

        def on_theme_changed_demo(theme_type):
            """Callback para demo - actualizar componentes"""
            print(f"🔄 Demo: Actualizando por cambio de tema a {theme_type}")

            # Actualizar título
            demo_title.color = get_theme().text_primary

            # Recrear container con nuevo tema
            demo_container.bgcolor = get_theme().surface
            demo_container.border = ft.border.all(1, get_theme().border_color)

            # Aplicar tema a página
            apply_theme_to_page(page)

            # Actualizar página
            page.update()

        # Crear selector de temas
        selector = ThemeSelectorScreen(
            on_theme_changed=on_theme_changed_demo
        )
        selector.page = page

        # Layout principal
        main_content = ft.Column(
            [
                demo_title,
                ft.Container(height=20),
                demo_container,
                ft.Container(height=30),
                ft.Text("Prueba cambiar el tema:", color=get_theme().text_secondary),
                ft.Container(height=20),
                # Botones de cambio rápido
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "🌊 Ocean",
                            on_click=lambda e: selector.theme_manager.set_theme(ThemeType.DEEP_OCEAN)
                        ),
                        ft.ElevatedButton(
                            "💼 Pro",
                            on_click=lambda e: selector.theme_manager.set_theme(ThemeType.MIDNIGHT_PROFESSIONAL)
                        ),
                        ft.ElevatedButton(
                            "🏔️ Nordic",
                            on_click=lambda e: selector.theme_manager.set_theme(ThemeType.NORDIC_NIGHT)
                        ),
                        ft.ElevatedButton(
                            "⚡ Electric",
                            on_click=lambda e: selector.theme_manager.set_theme(ThemeType.ELECTRIC_DARK)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        page.add(main_content)

    return demo_main

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Selector de Temas - ReflectApp"
        page.window.width = 400
        page.window.height = 720

        def on_theme_changed(theme_type):
            print(f"Tema cambiado a: {theme_type}")

        # Aplicar tema inicial
        apply_theme_to_page(page)

        selector = ThemeSelectorScreen(on_theme_changed=on_theme_changed)
        selector.page = page

        page.views.append(selector.build())
        page.update()

    # Usar demo normal o avanzado
    ft.app(target=main)
    # Para demo avanzado: ft.app(target=create_theme_demo_advanced())