"""
🎨 Selector de Temas ACTUALIZADO - ReflectApp
Pantalla para elegir entre temas oscuros y claros con preview dinámico
"""

import flet as ft
from services.reflect_themes_system import (
    ThemeManager, ThemeType, ReflectTheme, get_theme,
    create_themed_container, create_themed_button,
    create_gradient_header, apply_theme_to_page, theme_manager
)

class ThemeSelectorScreen:
    """Pantalla elegante para seleccionar temas ACTUALIZADA"""

    def __init__(self, on_theme_changed=None, on_go_back=None):
        self.theme_manager = theme_manager
        self.on_theme_changed = on_theme_changed
        self.on_go_back = on_go_back
        self.page = None

        # Estado
        self.current_selection = None
        self.preview_cards = {}

    def build(self) -> ft.View:
        """Construir vista del selector de temas ACTUALIZADA"""
        current_theme = get_theme()

        # Header con gradiente del tema actual
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        header = create_gradient_header(
            title="🎨 Selector de Temas",
            left_button=back_button,
            theme=current_theme
        )

        # Contenido principal que cambia según el tema actual
        content = ft.Column(
            [
                # Introducción con colores del tema actual
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Elige tu tema favorito",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=current_theme.text_primary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "Cada tema tiene su propia personalidad y ambiente único",
                                size=14,
                                color=current_theme.text_secondary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                f"📱 Tema actual: {current_theme.display_name}",
                                size=12,
                                color=current_theme.accent_primary,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.W_500
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.only(top=30, bottom=20, left=20, right=20)
                ),

                # Sección de temas oscuros
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "🌙 TEMAS OSCUROS",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=current_theme.text_primary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=16),
                            ft.Row(
                                [
                                    self.create_theme_card(ThemeType.DEEP_OCEAN),
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

                # Sección de temas claros - NUEVA
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "☀️ TEMAS CLAROS",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=current_theme.text_primary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=16),
                            ft.Row(
                                [
                                    self.create_theme_card(ThemeType.SPRING_LIGHT),
                                    ft.Container(width=16),
                                    self.create_theme_card(ThemeType.SUNSET_WARM)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ]
                    ),
                    padding=ft.padding.symmetric(horizontal=20)
                ),

                ft.Container(height=30),

                # Botón de aplicar con tema actual
                ft.Container(
                    content=create_themed_button(
                        "✨ Aplicar Tema Seleccionado",
                        self.apply_selected_theme,
                        theme=current_theme,
                        button_type="primary",
                        width=280,
                        height=55
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=30)
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=0
        )

        # Vista completa con tema actual
        view = ft.View(
            "/theme_selector",
            [
                header,
                ft.Container(
                    content=content,
                    expand=True,
                    bgcolor=current_theme.primary_bg
                )
            ],
            bgcolor=current_theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def create_theme_card(self, theme_type: ThemeType) -> ft.Container:
        """Crear tarjeta de preview de tema MEJORADA"""
        theme = self.theme_manager.themes[theme_type]
        current_theme = get_theme()
        is_current = self.theme_manager.get_current_theme().name == theme.name

        # Determinar si está seleccionado
        is_selected = self.current_selection == theme_type

        # Crear preview mini
        mini_preview = self.create_mini_preview(theme)

        # Título y descripción con colores del tema actual
        header_content = ft.Column(
            [
                ft.Text(
                    theme.display_name,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=current_theme.text_primary,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    theme.description,
                    size=12,
                    color=current_theme.text_secondary,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        )

        # Badge si es el tema actual - con colores del tema actual
        current_badge = None
        if is_current:
            current_badge = ft.Container(
                content=ft.Text(
                    "ACTUAL",
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF"
                ),
                bgcolor=current_theme.positive_main,
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                border_radius=8,
                alignment=ft.alignment.center
            )

        # Badge de tipo (Oscuro/Claro) - NUEVO
        type_badge = ft.Container(
            content=ft.Text(
                "CLARO" if not theme.is_dark else "OSCURO",
                size=8,
                weight=ft.FontWeight.BOLD,
                color=theme.text_primary if not theme.is_dark else "#FFFFFF"
            ),
            bgcolor="#FFFFFF" if not theme.is_dark else "#000000",
            padding=ft.padding.symmetric(horizontal=6, vertical=2),
            border_radius=6,
            alignment=ft.alignment.center
        )

        # Contenido de la tarjeta
        card_content = ft.Column(
            [
                ft.Row(
                    [type_badge],
                    alignment=ft.MainAxisAlignment.END
                ),
                header_content,
                ft.Container(height=8),
                mini_preview,
                ft.Container(height=8),
                current_badge if current_badge else ft.Container(height=20)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        # Contenedor principal con efectos - usando colores del tema actual
        border_color = theme.accent_primary if is_selected else current_theme.border_color
        border_width = 3 if is_selected else 1

        card = ft.Container(
            content=card_content,
            width=160,
            height=220,  # Aumentado para acomodar el badge de tipo
            bgcolor=current_theme.surface,
            border=ft.border.all(border_width, border_color),
            border_radius=16,
            padding=ft.padding.all(16),
            on_click=lambda e, t=theme_type: self.select_theme(t),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12 if is_selected else 6,
                color=current_theme.shadow_color,
                offset=ft.Offset(0, 4 if is_selected else 2)
            )
        )

        return card

    def create_mini_preview(self, theme: ReflectTheme) -> ft.Container:
        """Crear mini preview del tema MEJORADO"""

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
                color="#FFFFFF" if theme.is_dark else theme.text_primary,
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
        """Aplicar tema seleccionado"""
        if not self.current_selection:
            self.show_message("⚠️ Selecciona un tema primero", is_error=True)
            return

        # Cambiar tema en el manager
        success = self.theme_manager.set_theme(self.current_selection)

        if success:
            theme_name = self.theme_manager.themes[self.current_selection].display_name
            print(f"✅ Tema {theme_name} aplicado correctamente")

            # Aplicar inmediatamente a la página actual
            if self.page:
                apply_theme_to_page(self.page)

                # NUEVO: Reconstruir la vista con el nuevo tema
                self.rebuild_view_with_new_theme()

            # Mostrar mensaje de éxito
            self.show_message(f"✨ {theme_name} aplicado")

            # Callback externo si existe
            if self.on_theme_changed:
                try:
                    self.on_theme_changed(self.current_selection)
                except Exception as ex:
                    print(f"❌ Error en callback externo: {ex}")

            # Limpiar selección
            self.current_selection = None

        else:
            self.show_message("❌ Error aplicando tema", is_error=True)

    def rebuild_view_with_new_theme(self):
        """Reconstruir la vista con el nuevo tema - NUEVO MÉTODO"""
        if not self.page:
            return

        try:
            # Limpiar vistas y reconstruir
            if self.page.views:
                self.page.views.clear()

            # Construir nueva vista con tema actualizado
            new_view = self.build()
            self.page.views.append(new_view)
            self.page.update()

            print("🔄 Vista del selector reconstruida con nuevo tema")

        except Exception as e:
            print(f"❌ Error reconstruyendo vista: {e}")
            # Si hay error, al menos actualizar la página
            self.page.update()

    def show_message(self, message: str, is_error: bool = False):
        """Mostrar mensaje al usuario con tema actual"""
        if self.page:
            current_theme = get_theme()

            snack = ft.SnackBar(
                content=ft.Text(
                    message,
                    color="#FFFFFF",
                    size=14,
                    weight=ft.FontWeight.W_500
                ),
                bgcolor=current_theme.negative_main if is_error else current_theme.positive_main,
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

# Demo para probar el selector
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Selector de Temas Actualizado"
        page.window.width = 400
        page.window.height = 720

        def on_theme_changed(theme_type):
            print(f"🎨 Demo: Tema cambiado a {theme_type}")

        # Aplicar tema inicial
        apply_theme_to_page(page)

        selector = ThemeSelectorScreen(on_theme_changed=on_theme_changed)
        selector.page = page

        page.views.append(selector.build())
        page.update()

    ft.app(target=main)