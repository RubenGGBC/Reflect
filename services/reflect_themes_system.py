"""
🌙 Sistema de Temas MEJORADO - ReflectApp
Sistema con temas oscuros y claros elegantes
"""

import flet as ft
from enum import Enum
from typing import Dict, Any, List, Callable
import json
import os

class ThemeType(Enum):
    """Tipos de temas disponibles - ACTUALIZADOS"""
    DEEP_OCEAN = "deep_ocean"
    ELECTRIC_DARK = "electric_dark"
    SPRING_LIGHT = "spring_light"        # NUEVO: Tema claro primaveral
    SUNSET_WARM = "sunset_warm"          # NUEVO: Tema claro cálido

class ReflectTheme:
    """Clase base para definir un tema completo"""

    def __init__(self, name: str, display_name: str, icon: str, description: str, is_dark: bool = True):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.description = description
        self.is_dark = is_dark  # NUEVO: Indica si es tema oscuro o claro

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
            description="Tranquilo y minimalista",
            is_dark=True
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

class ElectricDarkTheme(ReflectTheme):
    """⚡ Electric Dark - Tecnológico con acentos neón"""

    def __init__(self):
        super().__init__(
            name="electric_dark",
            display_name="⚡ Electric Dark",
            icon="⚡",
            description="Futurista y moderno",
            is_dark=True
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

class SpringLightTheme(ReflectTheme):
    """🌸 Spring Light - Tema claro primaveral y fresco"""

    def __init__(self):
        super().__init__(
            name="spring_light",
            display_name="🌸 Spring Light",
            icon="🌸",
            description="Fresco y primaveral",
            is_dark=False  # ¡TEMA CLARO!
        )

        # Fondos claros
        self.primary_bg = "#F8FAFC"      # Gris muy claro
        self.secondary_bg = "#FFFFFF"     # Blanco puro
        self.surface = "#FFFFFF"          # Blanco puro
        self.surface_variant = "#F1F5F9"  # Gris muy suave

        # Acentos verdes primaveral
        self.accent_primary = "#059669"   # Verde esmeralda
        self.accent_secondary = "#10B981" # Verde menta

        # Textos oscuros para contraste en fondo claro
        self.text_primary = "#1F2937"     # Gris oscuro
        self.text_secondary = "#4B5563"   # Gris medio
        self.text_hint = "#9CA3AF"        # Gris claro

        # Estados con colores vibrantes
        self.positive_main = "#059669"    # Verde esmeralda
        self.positive_light = "#ECFDF5"   # Verde muy claro
        self.positive_glow = "#A7F3D0"    # Verde suave

        self.negative_main = "#DC2626"    # Rojo coral
        self.negative_light = "#FEF2F2"   # Rosa muy claro
        self.negative_glow = "#FECACA"    # Rosa suave

        # Gradientes suaves
        self.gradient_header = ["#059669", "#10B981"]
        self.gradient_button = ["#059669", "#047857"]

        # Efectos suaves
        self.shadow_color = "#05966920"
        self.border_color = "#D1D5DB"     # Borde gris suave
        self.glass_bg = "#05966910"

class SunsetWarmTheme(ReflectTheme):
    """🌅 Sunset Warm - Tema claro cálido y acogedor"""

    def __init__(self):
        super().__init__(
            name="sunset_warm",
            display_name="🌅 Sunset Warm",
            icon="🌅",
            description="Cálido y acogedor",
            is_dark=False  # ¡TEMA CLARO!
        )

        # Fondos cálidos claros
        self.primary_bg = "#FFF7ED"       # Naranja muy claro
        self.secondary_bg = "#FFFFFF"      # Blanco puro
        self.surface = "#FFFFFF"           # Blanco puro
        self.surface_variant = "#FEF3C7"   # Amarillo muy suave

        # Acentos naranjas cálidos
        self.accent_primary = "#EA580C"    # Naranja vibrante
        self.accent_secondary = "#F97316"  # Naranja brillante

        # Textos oscuros para contraste
        self.text_primary = "#292524"      # Marrón oscuro
        self.text_secondary = "#57534E"    # Marrón medio
        self.text_hint = "#A8A29E"         # Marrón claro

        # Estados cálidos
        self.positive_main = "#059669"     # Verde esmeralda (contraste)
        self.positive_light = "#F0FDF4"    # Verde muy claro
        self.positive_glow = "#BBF7D0"     # Verde suave

        self.negative_main = "#DC2626"     # Rojo intenso
        self.negative_light = "#FEF2F2"    # Rosa muy claro
        self.negative_glow = "#FECACA"     # Rosa suave

        # Gradientes cálidos
        self.gradient_header = ["#EA580C", "#F97316"]
        self.gradient_button = ["#EA580C", "#C2410C"]

        # Efectos cálidos
        self.shadow_color = "#EA580C20"
        self.border_color = "#E5E7EB"      # Borde gris neutro
        self.glass_bg = "#EA580C10"

class ThemeManager:
    """Gestor central de temas ACTUALIZADO"""

    def __init__(self, storage_path: str = "data/theme_settings.json"):
        self.storage_path = storage_path
        self.current_theme = None
        self.theme_change_callbacks: List[Callable] = []

        # Registrar todos los temas disponibles - ACTUALIZADOS
        self.themes = {
            ThemeType.DEEP_OCEAN: DeepOceanTheme(),
            ThemeType.ELECTRIC_DARK: ElectricDarkTheme(),
            ThemeType.SPRING_LIGHT: SpringLightTheme(),    # NUEVO
            ThemeType.SUNSET_WARM: SunsetWarmTheme()       # NUEVO
        }

        # Cargar tema guardado o usar por defecto
        self.load_theme()

    def register_callback(self, callback: Callable):
        """Registrar callback para cambios de tema"""
        self.theme_change_callbacks.append(callback)
        print(f"📝 Callback registrado. Total: {len(self.theme_change_callbacks)}")

    def unregister_callback(self, callback: Callable):
        """Desregistrar callback"""
        if callback in self.theme_change_callbacks:
            self.theme_change_callbacks.remove(callback)

    def notify_theme_change(self, theme_type: ThemeType):
        """Notificar a todos los callbacks sobre cambio de tema"""
        print(f"📢 Notificando cambio de tema a {len(self.theme_change_callbacks)} callbacks")
        for callback in self.theme_change_callbacks:
            try:
                callback(theme_type)
            except Exception as e:
                print(f"❌ Error en callback de tema: {e}")

    def get_available_themes(self) -> Dict[ThemeType, ReflectTheme]:
        """Obtener todos los temas disponibles"""
        return self.themes.copy()

    def get_current_theme(self) -> ReflectTheme:
        """Obtener tema actual"""
        return self.current_theme

    def set_theme(self, theme_type: ThemeType) -> bool:
        """Cambiar tema actual CON NOTIFICACIÓN"""
        if theme_type in self.themes:
            old_theme = self.current_theme.name if self.current_theme else "none"
            self.current_theme = self.themes[theme_type]
            new_theme = self.current_theme.name

            print(f"🎨 Cambio de tema: {old_theme} → {new_theme}")

            # Guardar tema
            self.save_theme(theme_type)

            # IMPORTANTE: Notificar cambio
            self.notify_theme_change(theme_type)

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
                            print(f"📖 Tema cargado: {theme.display_name}")
                            return

            # Si no se encuentra, usar Deep Ocean por defecto
            self.current_theme = self.themes[ThemeType.DEEP_OCEAN]
            print(f"📖 Tema por defecto: {self.current_theme.display_name}")

        except Exception as e:
            print(f"❌ Error cargando tema: {e}")
            self.current_theme = self.themes[ThemeType.DEEP_OCEAN]

    def save_theme(self, theme_type: ThemeType) -> None:
        """Guardar tema actual"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

            data = {
                'current_theme': self.themes[theme_type].name,
                'last_updated': "now"
            }

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"💾 Tema guardado: {self.themes[theme_type].display_name}")

        except Exception as e:
            print(f"❌ Error guardando tema: {e}")

# Instancia global del gestor de temas
theme_manager = ThemeManager()

def get_theme() -> ReflectTheme:
    """Función helper para obtener el tema actual"""
    return theme_manager.get_current_theme()

def register_theme_callback(callback: Callable):
    """Registrar callback para cambios de tema"""
    theme_manager.register_callback(callback)

def apply_theme_to_page(page: ft.Page) -> None:
    """Aplicar tema actual a una página MEJORADO"""
    theme = get_theme()

    page.bgcolor = theme.primary_bg

    # Configurar tema basado en si es claro u oscuro
    brightness = ft.Brightness.LIGHT if not theme.is_dark else ft.Brightness.DARK

    page.theme = ft.Theme(
        color_scheme_seed=theme.accent_primary,
    )

    print(f"🎨 Tema aplicado: {theme.display_name} ({'Claro' if not theme.is_dark else 'Oscuro'})")

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
        text_color = "#FFFFFF" if theme.is_dark else "#FFFFFF"

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