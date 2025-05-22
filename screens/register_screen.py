import flet as ft

class RegisterScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.name_field = None
        self.email_field = None
        self.password_field = None
        self.confirm_password_field = None
        self.privacy_checkbox = None
        self.error_container = None

    def build(self):
        self.name_field = ft.TextField(
            label="👤 Nombre (opcional)",
            hint_text="¿Cómo te llamas?",
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#48BB78",
            border_radius=15,
            filled=True,
            bgcolor="#FFFFFF",
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color="#2D3748"),
            label_style=ft.TextStyle(size=14, color="#48BB78"),
            cursor_color="#48BB78"
        )

        self.email_field = ft.TextField(
            label="📧 Correo electrónico",
            hint_text="tu@email.com",
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#48BB78",
            border_radius=15,
            filled=True,
            bgcolor="#FFFFFF",
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color="#2D3748"),
            label_style=ft.TextStyle(size=14, color="#48BB78"),
            cursor_color="#48BB78"
        )

        self.password_field = ft.TextField(
            label="🔒 Contraseña",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#48BB78",
            border_radius=15,
            filled=True,
            bgcolor="#FFFFFF",
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color="#2D3748"),
            label_style=ft.TextStyle(size=14, color="#48BB78"),
            cursor_color="#48BB78"
        )

        self.confirm_password_field = ft.TextField(
            label="🔐 Confirmar contraseña",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#48BB78",
            border_radius=15,
            filled=True,
            bgcolor="#FFFFFF",
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color="#2D3748"),
            label_style=ft.TextStyle(size=14, color="#48BB78"),
            cursor_color="#48BB78"
        )

        self.privacy_checkbox = ft.Checkbox(
            label="Acepto mantener mis reflexiones privadas y seguras 🔐",
            value=False,
            check_color="#FFFFFF",
            fill_color="#48BB78",
            label_style=ft.TextStyle(size=14, color="#4A5568")
        )

        self.error_container = ft.Container(
            content=ft.Text(
                "",
                color="#FFFFFF",
                size=14,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_500
            ),
            bgcolor="#F56565",
            padding=ft.padding.all(16),
            border_radius=12,
            visible=False
        )

        return ft.View(
            "/register",
            controls=[
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#F0FFF4", "#E8F5E8", "#F0FFF4"]
                    ),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Encabezado
                            ft.Container(
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.bottom_right,
                                    colors=["#48BB78", "#38A169", "#2F855A"]
                                ),
                                border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
                                padding=ft.padding.only(bottom=40),
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=20,
                                    color="#48BB78",
                                    offset=ft.Offset(0, 10)
                                ),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.TextButton("← Volver", on_click=self.go_back, style=ft.ButtonStyle(color="#FFFFFF")),
                                                    ft.Container(expand=True)
                                                ],
                                                alignment=ft.MainAxisAlignment.START
                                            ),
                                            padding=ft.padding.only(top=20, left=10, right=20)
                                        ),
                                        ft.Container(
                                            content=ft.Text("🌱", size=80),
                                            width=100,
                                            height=100,
                                            bgcolor="#FFFFFF",
                                            border_radius=50,
                                            alignment=ft.alignment.center,
                                            shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=20,
                                                color="#48BB78",
                                                offset=ft.Offset(0, 6)
                                            )
                                        ),
                                        ft.Container(height=24),
                                        ft.Text("¡Bienvenido!", size=36, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                        ft.Text("Crea tu cuenta y comienza tu", size=16, color="#E8F5E8"),
                                        ft.Text("viaje de reflexión 🌸", size=16, color="#E8F5E8"),
                                        ft.Container(height=16),
                                        ft.Text("✧ ✦ ✧", size=20, color="#A8EDEA")
                                    ]
                                )
                            ),

                            ft.Container(height=30),

                            # Formulario
                            ft.Container(
                                margin=ft.margin.symmetric(horizontal=20),
                                content=ft.Card(
                                    elevation=12,
                                    shadow_color="#48BB78",
                                    surface_tint_color="#E8F5E8",
                                    content=ft.Container(
                                        border_radius=25,
                                        padding=30,
                                        gradient=ft.LinearGradient(
                                            begin=ft.alignment.top_center,
                                            end=ft.alignment.bottom_center,
                                            colors=["#FFFFFF", "#F0FFF4"]
                                        ),
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text("🌱 Crear cuenta", size=24, weight=ft.FontWeight.W_600, color="#2D3748"),
                                                ft.Container(height=32),
                                                self.name_field,
                                                ft.Container(height=16),
                                                self.email_field,
                                                ft.Container(height=16),
                                                self.password_field,
                                                ft.Container(height=16),
                                                self.confirm_password_field,
                                                ft.Container(height=20),
                                                ft.Container(content=self.privacy_checkbox, padding=ft.padding.symmetric(horizontal=16)),
                                                ft.Container(height=16),
                                                self.error_container,
                                                ft.Container(height=24),
                                                ft.Container(
                                                    margin=ft.margin.only(bottom=24),
                                                    content=ft.ElevatedButton(
                                                        "🌱 Crear mi cuenta",
                                                        on_click=self.register_click,
                                                        width=300,
                                                        height=60,
                                                        style=ft.ButtonStyle(
                                                            bgcolor="#48BB78",
                                                            color="#FFFFFF",
                                                            elevation=8,
                                                            padding=ft.padding.symmetric(vertical=20, horizontal=40),
                                                            shape=ft.RoundedRectangleBorder(radius=20),
                                                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                                                        )
                                                    )
                                                )
                                            ]
                                        )
                                    )
                                )
                            ),

                            # Footer
                            ft.Container(
                                margin=ft.margin.only(top=24, bottom=40),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("· · ·", size=16, color="#A0AEC0"),
                                        ft.Container(height=16),
                                        ft.TextButton(
                                            content=ft.Row(
                                                spacing=8,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text("¿Ya tienes cuenta?", size=14, color="#4A5568"),
                                                    ft.Text("✨ Inicia sesión", size=14, color="#48BB78", weight=ft.FontWeight.W_600)
                                                ]
                                            ),
                                            on_click=self.go_to_login
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def show_error(self, message):
        self.error_container.content.value = f"⚠️ {message}"
        self.error_container.visible = True
        if self.page:
            self.page.update()

    def hide_error(self):
        self.error_container.visible = False
        if self.page:
            self.page.update()

    def show_success(self, message):
        if self.page:
            snack = ft.SnackBar(
                content=ft.Text(f"🌱 {message}", color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
                bgcolor="#48BB78",
                duration=3000,
                elevation=10
            )
            self.page.snack_bar = snack
            snack.open = True
            self.page.update()

    def register_click(self, e):
        self.page = e.page

        name = self.name_field.value.strip()
        email = self.email_field.value.strip()
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        if not email or not password:
            self.show_error("Email y contraseña son obligatorios")
            return

        if "@" not in email or "." not in email:
            self.show_error("Introduce un email válido")
            return

        if len(password) < 6:
            self.show_error("La contraseña debe tener al menos 6 caracteres")
            return

        if password != confirm_password:
            self.show_error("Las contraseñas no coinciden")
            return

        if not self.privacy_checkbox.value:
            self.show_error("Acepta los términos de privacidad para continuar")
            return

        self.hide_error()

        try:
            from services import db

            user_id = db.create_user(
                email=email,
                password=password,
                name=name if name else email.split('@')[0],
                avatar_emoji="🌱"
            )

            if user_id:
                self.show_success("🌱 ¡Cuenta creada! Bienvenido al santuario")
                self.name_field.value = ""
                self.email_field.value = ""
                self.password_field.value = ""
                self.confirm_password_field.value = ""
                self.privacy_checkbox.value = False
                self.page.update()

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

    def go_back(self, e):
        self.page = e.page
        self.page.go("/login")

    def go_to_login(self, e):
        self.page = e.page
        self.page.go("/login")
