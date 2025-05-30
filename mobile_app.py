"""
📱 ReflectApp - Acceso Rápido desde Móvil
Ejecuta este archivo para acceder desde tu móvil
"""

import flet as ft
from main import create_improved_app

def main():
    """Función principal optimizada para móvil"""

    def mobile_main(page: ft.Page):
        print("📱 === REFLECTAPP MOBILE ===")

        # Configuración móvil
        page.title = "ReflectApp Zen"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.padding = 0
        page.spacing = 0
        page.scroll = ft.ScrollMode.AUTO

        # Tamaños optimizados para móvil
        page.window.width = 390   # Simular iPhone/Android
        page.window.height = 844

        # Tema móvil
        page.theme = ft.Theme(
            text_theme=ft.TextTheme(
                body_large=ft.TextStyle(size=16),
                body_medium=ft.TextStyle(size=14),
                body_small=ft.TextStyle(size=12)
            ),
            visual_density=ft.VisualDensity.COMPACT
        )

        # Mostrar mensaje de bienvenida móvil
        print("🚀 Iniciando ReflectApp para móvil...")
        print("📱 Accede desde tu móvil a la URL que aparecerá")

        # Inicializar tu app original
        app_main = create_improved_app()
        app_main(page)

    # Ejecutar como web app accesible desde móvil
    print("🌐 === INICIANDO SERVIDOR WEB ===")
    print("📱 Sigue estos pasos:")
    print("   1. Espera a que aparezca la URL")
    print("   2. Anota tu IP (ej: 192.168.1.100)")
    print("   3. En el móvil ve a: http://TU_IP:8080")
    print("   4. ¡Disfruta tu app!")
    print("")

    ft.app(
        target=mobile_main,
        view=ft.WEB_BROWSER,    # Abrir en navegador
        port=8080,              # Puerto fácil de recordar
        host="0.0.0.0"          # Accesible desde cualquier dispositivo
    )

if __name__ == "__main__":
    main()