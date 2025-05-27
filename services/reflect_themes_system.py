"""
🌙 Sistema de Temas Profesionales - ReflectApp
Sistema centralizado de colores y estilos para modo noche elegante
"""

import flet as ft
from enum import Enum
from typing import Dict, Any
import json
import os

class ThemeType(Enum):
    """Tipos de temas disponibles"""
    DEEP_OCEAN = "deep_ocean"
    MIDNIGHT_PROFESSIONAL = "midnight_professional"
    NORDIC_NIGHT = "nordic_night"
    ELECTRIC_DARK = "electric_dark"

class ReflectTheme:
    """Clase base para definir un tema completo"""

    def __init__(self, name: str, display_name: str, icon: str, description: str):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.description = description

        # Colores base - deben ser sobrescritos por cada tema
        self.primary_bg = "#000000"
        self.secondary_bg = "#111111"
        self.surface = "#222222"
        self.surface_variant = "#333333"

        # Acentos
        self.accent_primary = "#666666"
        self.accent_secondary = "#777777"

        # Textos
        self.text_primary = "#FFFFFF"
        self.text_secondary = "#CCCCCC"
        self.text_hint = "#999999"

        # Estados
        self.positive_main = "#10B981"
        self.positive_light = "#10B98120"
        self.positive_glow = "#10B98140"

        self.negative_main = "#EF4444"
        self.negative_light = "#EF444420"
        self.negative_glow = "#EF444440"

        # Gradientes
        self.gradient_header = ["#666666", "#777777"]
        self.gradient_button = ["#555555", "#666666"]

        # Efectos
        self.shadow_color = "#00000030"
        self.border_color = "#444444"
        self.glass_bg = "#FFFFFF10"

class DeepOceanTheme(ReflectTheme):
    """🌊 Deep Ocean - Azul profundo minimalista"""

    def __init__(self):
        super().__init__(
            name="deep_ocean",
            display_name="🌊 Deep Ocean",
            icon="🌊",
            description="Tranquilo y minimalista"
        )

        # Fondo principal
        self.primary_bg = "#0A0E1A"
        self.secondary_bg = "#141B2D"
        self.surface = "#141B2D"
        self.surface_variant = "#1E2A3F"

        # Acentos azules
        self.accent_primary = "#1E3A8A"
        self.accent_secondary = "#3B82F6"

        # Textos
        self.text_primary = "#E8EAF0"
        self.text_secondary = "#B3B8C8"
        self.text_hint = "#8691A8"

        # Estados
        self.positive_main = "#10B981"
        self.positive_light = "#10B98120"
        self.positive_glow = "#10B98140"

        self.negative_main = "#EF4444"
        self.negative_light = "#EF444420"
        self.negative_glow = "#EF444440"

        # Gradientes azules
        self.gradient_header = ["#1E3A8A", "#3B82F6"]
        self.gradient_button = ["#1E3A8A", "#2563EB"]

        # Efectos
        self.shadow_color = "#1E3A8A30"
        self.border_color = "#1E3A8A"
        self.glass_bg = "#1E3A8A20"

class MidnightProfessionalTheme(ReflectTheme):
    """💼 Midnight Professional - Negro azulado corporativo"""

    def __init__(self):
        super().__init__(
            name="midnight_professional",
            display_name="💼 Midnight Pro",
            icon="💼",
            description="Corporativo y elegante"
        )

        # Fondo GitHub style
        self.primary_bg = "#0D1117"
        self.secondary_bg = "#161B22"
        self.surface = "#161B22"
        self.surface_variant = "#21262D"

        # Acentos grises
        self.accent_primary = "#21262D"
        self.accent_secondary = "#30363D"

        # Textos
        self.text_primary = "#F0F6FC"
        self.text_secondary = "#8B949E"
        self.text_hint = "#6E7681"

        # Estados GitHub style
        self.positive_main = "#238636"
        self.positive_light = "#23863620"
        self.positive_glow = "#23863640"

        self.negative_main = "#DA3633"
        self.negative_light = "#DA363320"
        self.negative_glow = "#DA363340"

        # Gradientes profesionales
        self.gradient_header = ["#21262D", "#30363D"]
        self.gradient_button = ["#238636", "#2EA043"]

        # Efectos
        self.shadow_color = "#00000050"
        self.border_color = "#21262D"
        self.glass_bg = "#F0F6FC10"

class NordicNightTheme(ReflectTheme):
    """🏔️ Nordic Night - Inspirado en temas nórdicos"""

    def __init__(self):
        super().__init__(
            name="nordic_night",
            display_name="🏔️ Nordic Night",
            icon="🏔️",
            description="Cálido y acogedor"
        )

        # Fondo nórdico
        self.primary_bg = "#2E3440"
        self.secondary_bg = "#3B4252"
        self.surface = "#3B4252"
        self.surface_variant = "#434C5E"

        # Acentos nórdicos
        self.accent_primary = "#434C5E"
        self.accent_secondary = "#4C566A"

        # Textos nórdicos
        self.text_primary = "#ECEFF4"
        self.text_secondary = "#D8DEE9"
        self.text_hint = "#A5A9B8"

        # Estados nórdicos
        self.positive_main = "#A3BE8C"
        self.positive_light = "#A3BE8C20"
        self.positive_glow = "#A3BE8C40"

        self.negative_main = "#BF616A"
        self.negative_light = "#BF616A20"
        self.negative_glow = "#BF616A40"

        # Gradientes cálidos
        self.gradient_header = ["#434C5E", "#4C566A"]
        self.gradient_button = ["#A3BE8C", "#B8CC9B"]

        # Efectos
        self.shadow_color = "#2E344040"
        self.border_color = "#434C5E"
        self.glass_bg = "#ECEFF410"

class ElectricDarkTheme(ReflectTheme):
    """⚡ Electric Dark - Tecnológico con acentos neón"""

    def __init__(self):
        super().__init__(
            name="electric_dark",
            display_name="⚡ Electric Dark",
            icon="⚡",
            description="Futurista y moderno"
        )

        # Fondo eléctrico
        self.primary_bg = "#0C0C0F"
        self.secondary_bg = "#1A1A23"
        self.surface = "#1A1A23"
        self.surface_variant = "#24243A"

        # Acentos eléctricos
        self.accent_primary = "#6366F1"
        self.accent_secondary = "#8B5CF6"

        # Textos brillantes
        self.text_primary = "#F8FAFC"
        self.text_secondary = "#CBD5E1"
        self.text_hint = "#94A3B8"

        # Estados eléctricos
        self.positive_main = "#06D6A0"
        self.positive_light = "#06D6A020"
        self.positive_glow = "#06D6A040"

        self.negative_main = "#F72585"
        self.negative_light = "#F7258520"
        self.negative_glow = "#F7258540"

        # Gradientes vibrantes
        self.gradient_header = ["#6366F1", "#8B5CF6"]
        self.gradient_button = ["#06D6A0", "#00E5C7"]

        # Efectos neón
        self.shadow_color = "#6366F130"
        self.border_color = "#6366F1"
        self.glass_bg = "#6366F120"

class ThemeManager:
    """Gestor central de temas"""

    def __init__(self, storage_path: str = "data/theme_settings.json"):
        self.storage_path = storage_path
        self.current_theme = None

        # Registrar todos los temas disponibles
        self.themes = {
            ThemeType.DEEP_OCEAN: DeepOceanTheme(),
            ThemeType.MIDNIGHT_PROFESSIONAL: MidnightProfessionalTheme(),
            ThemeType.NORDIC_NIGHT: NordicNightTheme(),
            ThemeType.ELECTRIC_DARK: ElectricDarkTheme()
        }

        # Cargar tema guardado o usar por defecto
        self.load_theme()

    def get_available_themes(self) -> Dict[ThemeType, ReflectTheme]:
        """Obtener todos los temas disponibles"""
        return self.themes.copy()

    def get_current_theme(self) -> ReflectTheme:
        """Obtener tema actual"""
        return self.current_theme

    def set_theme(self, theme_type: ThemeType) -> bool:
        """Cambiar tema actual"""
        if theme_type in self.themes:
            self.current_theme = self.themes[theme_type]
            self.save_theme(theme_type)
            return True
        return False

    def load_theme(self) -> None:
        """Cargar tema guardado"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    theme_name = data.get('current_theme', 'deep_ocean')

                    # Buscar tema por nombre
                    for theme_type, theme in self.themes.items():
                        if theme.name == theme_name:
                            self.current_theme = theme
                            return

            # Si no se encuentra, usar Deep Ocean por defecto
            self.current_theme = self.themes[ThemeType.DEEP_OCEAN]

        except Exception as e:
            print(f"Error cargando tema: {e}")
            self.current_theme = self.themes[ThemeType.DEEP_OCEAN]

    def save_theme(self, theme_type: ThemeType) -> None:
        """Guardar tema actual"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

            data = {
                'current_theme': self.themes[theme_type].name,
                'last_updated': str(ft.datetime.now())
            }

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error guardando tema: {e}")

# Instancia global del gestor de temas
theme_manager = ThemeManager()

def get_theme() -> ReflectTheme:
    """Función helper para obtener el tema actual"""
    return theme_manager.get_current_theme()

def apply_theme_to_page(page: ft.Page) -> None:
    """Aplicar tema actual a una página"""
    theme = get_theme()

    page.bgcolor = theme.primary_bg
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=theme.accent_primary,
            primary_container=theme.surface,
            secondary=theme.accent_secondary,
            surface=theme.surface,
            background=theme.primary_bg,
            on_primary=theme.text_primary,
            on_surface=theme.text_primary,
            on_background=theme.text_primary
        )
    )

def create_themed_container(
        content: ft.Control,
        theme: ReflectTheme = None,
        is_surface: bool = True,
        add_shadow: bool = True,
        add_border: bool = True,
        border_radius: int = 16
) -> ft.Container:
    """Crear contenedor con tema aplicado"""
    if not theme:
        theme = get_theme()

    container = ft.Container(
        content=content,
        bgcolor=theme.surface if is_surface else theme.surface_variant,
        border_radius=border_radius,
        padding=ft.padding.all(20)
    )

    if add_border:
        container.border = ft.border.all(1, theme.border_color)

    if add_shadow:
        container.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=theme.shadow_color,
            offset=ft.Offset(0, 4)
        )

    return container

def create_themed_button(
        text: str,
        on_click,
        theme: ReflectTheme = None,
        button_type: str = "primary",  # "primary", "positive", "negative"
        width: int = None,
        height: int = 50
) -> ft.ElevatedButton:
    """Crear botón con tema aplicado"""
    if not theme:
        theme = get_theme()

    # Seleccionar colores según tipo
    if button_type == "positive":
        bg_color = theme.positive_main
        text_color = "#FFFFFF"
    elif button_type == "negative":
        bg_color = theme.negative_main
        text_color = "#FFFFFF"
    else:  # primary
        bg_color = theme.accent_primary
        text_color = theme.text_primary

    button = ft.ElevatedButton(
        text=text,
        on_click=on_click,
        width=width,
        height=height,
        style=ft.ButtonStyle(
            bgcolor=bg_color,
            color=text_color,
            elevation=4,
            shadow_color=theme.shadow_color,
            shape=ft.RoundedRectangleBorder(radius=12),
            text_style=ft.TextStyle(
                size=16,
                weight=ft.FontWeight.W_500
            )
        )
    )

    return button

def create_gradient_header(
        title: str,
        left_button: ft.Control = None,
        right_button: ft.Control = None,
        theme: ReflectTheme = None
) -> ft.Container:
    """Crear header con gradiente temático"""
    if not theme:
        theme = get_theme()

    header_content = ft.Row(
        [
            left_button if left_button else ft.Container(width=80),
            ft.Text(
                title,
                size=20,
                weight=ft.FontWeight.W_500,
                color="#FFFFFF",
                expand=True,
                text_align=ft.TextAlign.CENTER
            ),
            right_button if right_button else ft.Container(width=80)
        ]
    )

    return ft.Container(
        content=header_content,
        padding=ft.padding.all(20),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=theme.gradient_header
        ),
        border_radius=ft.border_radius.only(bottom_left=24, bottom_right=24),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=12,
            color=theme.shadow_color,
            offset=ft.Offset(0, 6)
        )
    )

# Funciones de compatibilidad para mantener el código existente
class ZenColors:
    """Clase de compatibilidad que usa el tema actual"""

    @property
    def positive_main(self):
        return get_theme().positive_main

    @property
    def positive_light(self):
        return get_theme().positive_light

    @property
    def positive_glow(self):
        return get_theme().positive_glow

    @property
    def negative_main(self):
        return get_theme().negative_main

    @property
    def negative_light(self):
        return get_theme().negative_light

    @property
    def negative_glow(self):
        return get_theme().negative_glow

    @property
    def background(self):
        return get_theme().primary_bg

    @property
    def surface(self):
        return get_theme().surface

    @property
    def text_primary(self):
        return get_theme().text_primary

    @property
    def text_secondary(self):
        return get_theme().text_secondary

    @property
    def text_hint(self):
        return get_theme().text_hint

# Instancia global para compatibilidad
zen_colors = ZenColors()

if __name__ == "__main__":
    # Ejemplo de uso
    print("🌙 Sistema de Temas - ReflectApp")
    print("================================")

    for theme_type, theme in theme_manager.get_available_themes().items():
        print(f"{theme.icon} {theme.display_name}: {theme.description}")
        print(f"   Fondo: {theme.primary_bg}")
        print(f"   Superficie: {theme.surface}")
        print(f"   Positivo: {theme.positive_main}")
        print(f"   Negativo: {theme.negative_main}")
        print()