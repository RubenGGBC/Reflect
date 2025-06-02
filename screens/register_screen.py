"""
📝 Register Screen MEJORADA - ReflectApp
Diseño moderno con glassmorphism, validación visual y efectos sin iconos
"""

import flet as ft
from services.reflect_themes_system import get_theme

class RegisterScreen:
    def __init__(self, app):
        self.app = app
        self.page = None

        # Campos del formulario
        self.name_field = None
        self.email_field = None
        self.password_field = None
        self.confirm_password_field = None
        self.privacy_checkbox = None

        # Estado
        self.error_container = None
        self.password_strength = 0
        self.password_strength_container = None
        self.is_loading = False

    def build(self):
        """Construir vista de registro moderna"""
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

        # Header con progreso
        header_section = self.create_header_section(theme)

        # Hero icon
        hero_section = self.create_hero_section(theme)

        # Formulario principal
        form_section = self.create_form_section(theme)

        # Quote motivacional
        quote_section = self.create_quote_section(theme)

        # Vista principal
        view = ft.View(
            "/register",
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            header_section,
                            ft.Container(height=20),
                            hero_section,
                            form_section,
                            quote_section,
                            ft.Container(height=40)
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

    def create_header_section(self, theme):
        """Crear header con botón volver y progreso"""
        return ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Botón volver
                    ft.TextButton(
                        content=ft.Row(
                            spacing=8,
                            controls=[
                                ft.Text("←", size=18, color=theme.text_secondary),
                                ft.Text("Volver", size=14, color=theme.text_secondary)
                            ]
                        ),
                        on_click=self.go_back,
                        style=ft.ButtonStyle(
                            overlay_color={"hovered": theme.text_secondary + "10"}
                        )
                    ),

                    # Indicador de progreso
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=8,
                        controls=[
                            ft.Text(
                                "Paso 1 de 2",
                                size=12,
                                color=theme.text_hint
                            ),
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Container(
                                        width=24, height=4,
                                        bgcolor=theme.accent_primary,
                                        border_radius=2
                                    ),
                                    ft.Container(
                                        width=24, height=4,
                                        bgcolor="#E2E8F0",
                                        border_radius=2
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            margin=ft.margin.only(bottom=20)
        )

    def create_hero_section(self, theme):
        """Crear sección hero con icono de crecimiento"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Icono principal
                    ft.Container(
                        content=ft.Text("🌱", size=32, text_align=ft.TextAlign.CENTER),
                        width=64,
                        height=64,
                        bgcolor=theme.positive_main + "20",
                        border_radius=16,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=16,
                            color=theme.positive_main + "30",
                            offset=ft.Offset(0, 4)
                        )
                    ),

                    ft.Container(height=16),

                    # Título
                    ft.Text(
                        "Únete a ReflectApp",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=theme.text_primary,
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Text(
                        "Crea tu cuenta y comienza tu viaje de reflexión",
                        size=14,
                        color=theme.text_secondary,
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            ),
            margin=ft.margin.only(bottom=32)
        )

    def create_form_fields(self, theme):
        """Crear campos del formulario SIN iconos"""

        # Campo Nombre (opcional)
        self.name_field = ft.TextField(
            label="👤 Nombre (opcional)",
            hint_text="¿Cómo te llamamos?",
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color=theme.accent_primary,
            border_radius=12,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary)
        )

        # Campo Email
        self.email_field = ft.TextField(
            label="📧 Email",
            hint_text="tu@email.com",
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color=theme.accent_primary,
            border_radius=12,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary)
        )

        # Campo Password con validación
        self.password_field = ft.TextField(
            label="🔒 Contraseña",
            hint_text="Contraseña segura",
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color=theme.accent_primary,
            border_radius=12,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary),
            on_change=self.on_password_change
        )

        # Medidor de fuerza de contraseña
        self.password_strength_container = ft.Container(
            content=ft.Column(
                spacing=8,
                controls=[
                    # Barras de fuerza
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.Container(width=60, height=4, bgcolor="#E2E8F0", border_radius=2),
                            ft.Container(width=60, height=4, bgcolor="#E2E8F0", border_radius=2),
                            ft.Container(width=60, height=4, bgcolor="#E2E8F0", border_radius=2),
                            ft.Container(width=60, height=4, bgcolor="#E2E8F0", border_radius=2)
                        ]
                    ),
                    # Texto de fuerza
                    ft.Text(
                        "",
                        size=12,
                        color=theme.text_hint
                    )
                ]
            ),
            visible=False,
            margin=ft.margin.only(top=8)
        )

        # Campo Confirmar Password
        self.confirm_password_field = ft.TextField(
            label="🔐 Confirmar contraseña",
            hint_text="Repite tu contraseña",
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color=theme.accent_primary,
            border_radius=12,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary),
            on_change=self.on_confirm_password_change
        )

        # Checkbox de privacidad
        self.privacy_checkbox = ft.Checkbox(
            label="Acepto mantener mis reflexiones privadas 🔐",
            value=False,
            check_color="#FFFFFF",
            fill_color=theme.positive_main,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary)
        )

    def create_form_section(self, theme):
        """Crear sección del formulario con glassmorphism"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                # Campo Nombre
                                self.name_field,

                                # Campo Email
                                self.email_field,

                                # Campo Password + Medidor
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        self.password_field,
                                        self.password_strength_container
                                    ]
                                ),

                                # Campo Confirmar Password
                                self.confirm_password_field,

                                # Checkbox privacidad
                                ft.Container(
                                    content=self.privacy_checkbox,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=8)
                                ),

                                # Error container
                                self.error_container,

                                # Botón principal
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("✨", size=20),
                                            ft.Container(width=8),
                                            ft.Text(
                                                "Crear cuenta",
                                                size=16,
                                                weight=ft.FontWeight.W_600
                                            )
                                        ]
                                    ),
                                    on_click=self.register_click,
                                    width=320,
                                    height=56,
                                    style=ft.ButtonStyle(
                                        bgcolor={"": theme.positive_main},
                                        color={"": "#FFFFFF"},
                                        elevation=8,
                                        shadow_color=theme.positive_main + "40",
                                        shape=ft.RoundedRectangleBorder(radius=16),
                                        animation_duration=300
                                    )
                                )
                            ]
                        ),
                        width=360,
                        padding=ft.padding.all(32),
                        bgcolor=theme.surface,
                        border_radius=24,
                        border=ft.border.all(1, "#E2E8F0"),
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
        """Crear sección motivacional"""
        return ft.Container(
            content=ft.Text(
                "🌸 Tu viaje de autoconocimiento comienza con un solo paso",
                size=14,
                color=theme.text_hint,
                italic=True,
                text_align=ft.TextAlign.CENTER
            )
        )

    def calculate_password_strength(self, password):
        """Calcular fuerza de contraseña (0-100)"""
        if not password:
            return 0

        strength = 0

        # Longitud
        if len(password) >= 6:
            strength += 25
        if len(password) >= 8:
            strength += 10
        if len(password) >= 12:
            strength += 10

        # Caracteres
        if any(c.islower() for c in password):
            strength += 15
        if any(c.isupper() for c in password):
            strength += 15
        if any(c.isdigit() for c in password):
            strength += 15
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 10

        return min(strength, 100)

    def update_password_strength_ui(self, strength):
        """Actualizar UI del medidor de fuerza"""
        theme = get_theme()

        # Mostrar/ocultar medidor
        self.password_strength_container.visible = strength > 0

        if strength == 0:
            return

        # Determinar colores y texto
        if strength < 25:
            color = theme.negative_main
            text = "🔓 Muy débil"
        elif strength < 50:
            color = "#F59E0B"  # Amarillo
            text = "🔒 Débil"
        elif strength < 75:
            color = "#F59E0B"  # Amarillo
            text = "🔒 Media"
        else:
            color = theme.positive_main
            text = "🔐 Fuerte"

        # Actualizar barras
        bars = self.password_strength_container.content.controls[0].controls
        filled_bars = max(1, strength // 25)

        for i, bar in enumerate(bars):
            if i < filled_bars:
                bar.bgcolor = color
            else:
                bar.bgcolor = "#E2E8F0"

        # Actualizar texto
        self.password_strength_container.content.controls[1].value = text
        self.password_strength_container.content.controls[1].color = color

    def on_password_change(self, e):
        """Manejar cambio en password"""
        password = e.control.value
        strength = self.calculate_password_strength(password)
        self.password_strength = strength
        self.update_password_strength_ui(strength)

        if self.page:
            self.page.update()

    def on_confirm_password_change(self, e):
        """Validar confirmación de password"""
        password = self.password_field.value if self.password_field.value else ""
        confirm = e.control.value if e.control.value else ""

        if confirm and password != confirm:
            e.control.error_text = "Las contraseñas no coinciden"
        else:
            e.control.error_text = None

        if self.page:
            self.page.update()

    def validate_form(self):
        """Validar formulario completo"""
        email = self.email_field.value.strip() if self.email_field.value else ""
        password = self.password_field.value if self.password_field.value else ""
        confirm = self.confirm_password_field.value if self.confirm_password_field.value else ""
        privacy = self.privacy_checkbox.value

        if not email:
            return False, "El email es obligatorio"

        if "@" not in email or "." not in email:
            return False, "Introduce un email válido"

        if not password:
            return False, "La contraseña es obligatoria"

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"

        if password != confirm:
            return False, "Las contraseñas no coinciden"

        if not privacy:
            return False, "Debes aceptar los términos de privacidad"

        return True, ""

    def show_error(self, message):
        """Mostrar mensaje de error"""
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
                content=ft.Text(f"🌱 {message}", color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
                bgcolor=theme.positive_main,
                duration=3000,
                elevation=10
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()

    def register_click(self, e):
        """Manejar click de registro"""
        self.page = e.page

        # Validar formulario
        is_valid, error_message = self.validate_form()

        if not is_valid:
            self.show_error(error_message)
            return

        self.hide_error()

        # Obtener valores
        name = self.name_field.value.strip() if self.name_field.value else ""
        email = self.email_field.value.strip()
        password = self.password_field.value

        try:
            from services import db

            # Crear usuario
            user_id = db.create_user(
                email=email,
                password=password,
                name=name if name else email.split('@')[0],
                avatar_emoji="🌱"
            )

            if user_id:
                self.show_success("🌱 ¡Cuenta creada! Bienvenido al santuario")

                # Limpiar campos
                self.clear_form()

                # Login automático
                usuario = db.login_user(email, password)
                if usuario:
                    self.app.navigate_to_entry(usuario)
                else:
                    self.page.go("/login")
            else:
                self.show_error("Este email ya está registrado")

        except Exception as ex:
            print(f"Error en registro: {ex}")
            self.show_error("Error del sistema. Intenta de nuevo")

    def clear_form(self):
        """Limpiar formulario"""
        self.name_field.value = ""
        self.email_field.value = ""
        self.password_field.value = ""
        self.confirm_password_field.value = ""
        self.privacy_checkbox.value = False
        self.password_strength_container.visible = False

        if self.page:
            self.page.update()

    def go_back(self, e):
        """Volver al login"""
        self.page = e.page
        self.page.go("/login")