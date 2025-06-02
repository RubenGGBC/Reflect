"""
🔐 Login Screen MEJORADA - ReflectApp
Basada en el diseño React moderno con glassmorphism y mejor UX
"""

import flet as ft
from services.reflect_themes_system import get_theme, apply_theme_to_page

class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.email_field = None
        self.password_field = None
        self.error_container = None
        self.show_password = False
        self.is_loading = False

    def build(self):
        """Construir vista de login moderna con glassmorphism"""
        theme = get_theme()

        # Crear campos del formulario
        self.create_form_fields(theme)

        # Crear contenedor de error
        self.error_container = ft.Container(
            content=ft.Text(
                "",
                color="#FFFFFF",
                size=14,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_500
            ),
            bgcolor=theme.negative_main,
            padding=ft.padding.all(16),
            border_radius=12,
            visible=False,
            margin=ft.margin.only(bottom=16)
        )

        # Hero Section - Icono y título principal
        hero_section = self.create_hero_section(theme)

        # Formulario con glassmorphism
        form_section = self.create_form_section(theme)

        # Quote inspiracional
        quote_section = self.create_quote_section(theme)

        # Vista principal
        view = ft.View(
            "/login",
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(height=60),  # Espaciado superior
                            hero_section,
                            form_section,
                            quote_section,
                            ft.Container(height=40)   # Espaciado inferior
                        ]
                    ),
                    padding=ft.padding.all(24)
                )
            ],
            bgcolor=theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def create_hero_section(self, theme):
        """Crear sección hero con icono y título"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Icono principal con gradiente y sombra
                    ft.Container(
                        content=ft.Text("🧘‍♀️", size=50, text_align=ft.TextAlign.CENTER),
                        width=100,
                        height=100,
                        bgcolor=theme.surface,
                        border_radius=50,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=20,
                            color=theme.accent_primary + "40",
                            offset=ft.Offset(0, 8)
                        ),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[theme.accent_primary, theme.positive_main]
                        )
                    ),

                    ft.Container(height=24),

                    # Título principal
                    ft.Text(
                        "ReflectApp",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=theme.text_primary,
                        text_align=ft.TextAlign.CENTER
                    ),

                    # Subtítulo con separadores
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(width=32, height=1, bgcolor=theme.text_hint + "30"),
                            ft.Text(
                                "Tu santuario zen",
                                size=16,
                                color=theme.text_secondary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(width=32, height=1, bgcolor=theme.text_hint + "30"),
                        ]
                    ),

                    ft.Container(height=8),

                    # Decoración
                    ft.Text(
                        "✧ ✦ ✧",
                        size=16,
                        color=theme.text_hint,
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            ),
            margin=ft.margin.only(bottom=48)
        )

    def create_form_fields(self, theme):
        """Crear campos del formulario con iconos"""

        # Campo Email con icono
        self.email_field = ft.TextField(
            label="",
            hint_text="tu@email.com",
            prefix_icon=ft.icons.EMAIL_OUTLINED,
            border=ft.InputBorder.OUTLINE,
            border_color=theme.border_color,
            focused_border_color=theme.accent_primary,
            border_radius=16,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(20),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            hint_style=ft.TextStyle(color=theme.text_hint),
            prefix_style=ft.TextStyle(color=theme.text_hint)
        )

        # Campo Password con icono y toggle de visibilidad
        self.password_field = ft.TextField(
            label="",
            hint_text="••••••••",
            prefix_icon=ft.icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_color=theme.border_color,
            focused_border_color=theme.accent_primary,
            border_radius=16,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(20),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            hint_style=ft.TextStyle(color=theme.text_hint),
            prefix_style=ft.TextStyle(color=theme.text_hint),
            on_submit=self.login_click
        )

    def create_form_section(self, theme):
        """Crear sección del formulario con glassmorphism"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Contenedor del formulario con glassmorphism
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Campo Email
                                self.email_field,

                                ft.Container(height=20),

                                # Campo Password
                                self.password_field,

                                ft.Container(height=16),

                                # Error container
                                self.error_container,

                                # Botón principal
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("🚪", size=20),
                                            ft.Container(width=8),
                                            ft.Text(
                                                "Entrar zen",
                                                size=16,
                                                weight=ft.FontWeight.W_600
                                            )
                                        ]
                                    ),
                                    on_click=self.login_click,
                                    width=320,
                                    height=56,
                                    style=ft.ButtonStyle(
                                        bgcolor={"": theme.accent_primary},
                                        color={"": "#FFFFFF"},
                                        elevation=8,
                                        shadow_color=theme.accent_primary + "40",
                                        shape=ft.RoundedRectangleBorder(radius=16),
                                        animation_duration=300
                                    )
                                ),

                                ft.Container(height=20),

                                # Separador
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            width=80,
                                            height=1,
                                            bgcolor=theme.border_color
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                "ó",
                                                size=14,
                                                color=theme.text_hint
                                            ),
                                            margin=ft.margin.symmetric(horizontal=16)
                                        ),
                                        ft.Container(
                                            width=80,
                                            height=1,
                                            bgcolor=theme.border_color
                                        )
                                    ]
                                ),

                                ft.Container(height=20),

                                # Botón registro
                                ft.OutlinedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("🌱", size=18),
                                            ft.Container(width=8),
                                            ft.Text(
                                                "Crear cuenta",
                                                size=16,
                                                weight=ft.FontWeight.W_500
                                            )
                                        ]
                                    ),
                                    on_click=self.register_click,
                                    width=320,
                                    height=56,
                                    style=ft.ButtonStyle(
                                        color={"": theme.positive_main},
                                        side=ft.BorderSide(2, theme.positive_main + "40"),
                                        shape=ft.RoundedRectangleBorder(radius=16),
                                        bgcolor={"hovered": theme.positive_main + "10"}
                                    )
                                ),

                                # Usuario de prueba
                                ft.Container(
                                    content=ft.TextButton(
                                        content=ft.Text(
                                            "🧪 Modo desarrollador",
                                            size=13,
                                            color=theme.text_hint
                                        ),
                                        on_click=self.create_test_user,
                                        style=ft.ButtonStyle(
                                            overlay_color={"hovered": theme.text_hint + "10"}
                                        )
                                    ),
                                    margin=ft.margin.only(top=16)
                                )
                            ]
                        ),
                        width=360,
                        padding=ft.padding.all(32),
                        bgcolor=theme.glass_bg,
                        border_radius=24,
                        border=ft.border.all(1, theme.border_color),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=24,
                            color="#00000020",
                            offset=ft.Offset(0, 8)
                        )
                    )
                ]
            ),
            margin=ft.margin.only(bottom=32)
        )

    def create_quote_section(self, theme):
        """Crear sección de quote inspiracional"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        '"Un momento de paz puede cambiar tu día"',
                        size=14,
                        color=theme.text_hint,
                        italic=True,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Container(height=16),

                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("🔐", size=14),
                                ft.Container(width=8),
                                ft.Text(
                                    "Privado y seguro",
                                    size=13,
                                    weight=ft.FontWeight.W_500,
                                    color=theme.positive_main
                                )
                            ]
                        ),
                        bgcolor=theme.positive_main + "20",
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        border_radius=20,
                        border=ft.border.all(1, theme.positive_main + "30")
                    )
                ]
            )
        )

    def show_error(self, message):
        """Mostrar mensaje de error con animación"""
        self.error_container.content.value = f"⚠️ {message}"
        self.error_container.visible = True
        if self.page:
            self.page.update()

    def hide_error(self):
        """Ocultar mensaje de error"""
        self.error_container.visible = False
        if self.page:
            self.page.update()

    def show_success(self, message):
        """Mostrar mensaje de éxito"""
        if self.page:
            theme = get_theme()
            snackbar = ft.SnackBar(
                content=ft.Text(f"🌸 {message}", color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
                bgcolor=theme.positive_main,
                duration=3000,
                elevation=10
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()

    def set_loading(self, loading):
        """Cambiar estado de carga"""
        self.is_loading = loading
        # Aquí podrías cambiar el botón para mostrar loading
        if self.page:
            self.page.update()

    def login_click(self, e):
        """Manejar click de login con validaciones mejoradas"""
        self.page = e.page

        email = self.email_field.value.strip() if self.email_field.value else ""
        password = self.password_field.value if self.password_field.value else ""

        # Validaciones
        if not email or not password:
            self.show_error("Completa todos los campos para continuar tu viaje")
            return

        if "@" not in email or "." not in email:
            self.show_error("Introduce un email válido para acceder")
            return

        if len(password) < 3:  # Relajamos la validación para demo
            self.show_error("Contraseña demasiado corta")
            return

        self.hide_error()
        self.set_loading(True)

        try:
            from services import db
            usuario = db.login_user(email, password)

            if usuario:
                nombre = usuario.get("name", email.split("@")[0])
                self.show_success(f"🌸 ¡Bienvenido de vuelta, {nombre}!")

                # Limpiar campos
                self.email_field.value = ""
                self.password_field.value = ""
                self.page.update()

                # Navegar a entry
                self.app.navigate_to_entry(usuario)
            else:
                self.show_error("Credenciales incorrectas. Verifica tus datos")

        except Exception as ex:
            print(f"Error en login: {ex}")
            self.show_error("Error del sistema. Intenta de nuevo")
        finally:
            self.set_loading(False)

    def register_click(self, e):
        """Navegar a registro"""
        self.page = e.page
        self.page.go("/register")

    def create_test_user(self, e):
        """Crear usuario de prueba"""
        self.page = e.page
        try:
            from services import db
            email = "zen@reflect.app"
            password = "reflect123"
            name = "Viajero Zen"

            user_id = db.create_user(email, password, name)
            if user_id:
                self.show_success("🧪 Perfil zen creado exitosamente")
            else:
                self.show_success("🧪 Perfil zen ya existe y está listo")

            # Prellenar campos
            self.email_field.value = email
            self.password_field.value = password
            self.page.update()

        except Exception as ex:
            print(f"Error creando usuario: {ex}")
            self.show_error("Error creando perfil zen")