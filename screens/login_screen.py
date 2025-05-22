import flet as ft

class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.email_field = None
        self.password_field = None
        self.error_container = None

    def build(self):
        self.email_field = ft.TextField(
            label="📧 Correo electrónico",
            hint_text="tu@email.com",
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#667EEA",
            border_radius=15,
            filled=True,
            bgcolor="#FFFFFF",
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color="#2D3748"),
            label_style=ft.TextStyle(size=14, color="#667EEA"),
            cursor_color="#667EEA"
        )

        self.password_field = ft.TextField(
            label="🔒 Contraseña",
            hint_text="••••••••",
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_color="#E2E8F0",
            focused_border_color="#667EEA",
            border_radius=15,
            filled=True,
            bgcolor="#FFFFFF",
            content_padding=ft.padding.all(16),
            text_style=ft.TextStyle(size=16, color="#2D3748"),
            label_style=ft.TextStyle(size=14, color="#667EEA"),
            cursor_color="#667EEA"
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

        view = ft.View(
            "/login",
            controls=[
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#F8FAFC", "#E8EAF6", "#F8FAFC"]
                    ),
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Header
                            ft.Container(
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(height=60),
                                        ft.Container(
                                            content=ft.Text("🧘‍♀️", size=80, text_align=ft.TextAlign.CENTER),
                                            width=100,
                                            height=100,
                                            bgcolor="#FFFFFF",
                                            border_radius=50,
                                            alignment=ft.alignment.center,
                                            shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=20,
                                                color="#667EEA",
                                                offset=ft.Offset(0, 6)  # sin opacity
                                            )
                                        ),
                                        ft.Container(height=24),
                                        ft.Text("ReflectApp", size=36, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                        ft.Text("🌸 Tu espacio de reflexión diaria", size=16, color="#E8EAF6"),
                                        ft.Container(height=16),
                                        ft.Text("✧ ✦ ✧", size=20, color="#B39DDB")
                                    ]
                                ),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.bottom_right,
                                    colors=["#667EEA", "#764BA2", "#667EEA"]
                                ),
                                border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
                                padding=ft.padding.only(bottom=40),
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=20,
                                    color="#667EEA",
                                    offset=ft.Offset(0, 10)
                                )
                            ),
                            ft.Container(height=40),
                            # Formulario
                            ft.Container(
                                margin=ft.margin.symmetric(horizontal=20),
                                content=ft.Card(
                                    elevation=12,
                                    surface_tint_color="#E8EAF6",
                                    shadow_color="#667EEA",
                                    content=ft.Container(
                                        border_radius=25,
                                        padding=30,
                                        gradient=ft.LinearGradient(
                                            begin=ft.alignment.top_center,
                                            end=ft.alignment.bottom_center,
                                            colors=["#FFFFFF", "#F8FAFC"]
                                        ),
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text("✨ Iniciar sesión", size=24, weight=ft.FontWeight.W_600, color="#2D3748"),
                                                ft.Container(height=32),
                                                self.email_field,
                                                ft.Container(height=20),
                                                self.password_field,
                                                ft.Container(height=16),
                                                self.error_container,
                                                ft.Container(height=32),
                                                ft.ElevatedButton(
                                                    "🚪 Entrar al santuario",
                                                    width=300,
                                                    height=60,
                                                    on_click=self.login_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor="#667EEA",
                                                        color="#FFFFFF",
                                                        elevation=8,
                                                        padding=ft.padding.symmetric(vertical=20, horizontal=40),
                                                        shape=ft.RoundedRectangleBorder(radius=20),
                                                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                                                    )
                                                ),
                                                ft.Container(
                                                    margin=ft.margin.symmetric(vertical=24),
                                                    content=ft.Row(
                                                        controls=[
                                                            ft.Container(expand=True, bgcolor="#E2E8F0", height=1),
                                                            ft.Text("o", size=14, color="#A0AEC0"),
                                                            ft.Container(expand=True, bgcolor="#E2E8F0", height=1)
                                                        ]
                                                    )
                                                ),
                                                ft.ElevatedButton(
                                                    "🌱 Crear cuenta",
                                                    width=300,
                                                    height=60,
                                                    on_click=self.register_click,
                                                    style=ft.ButtonStyle(
                                                        bgcolor="#48BB78",
                                                        color="#FFFFFF",
                                                        elevation=8,
                                                        padding=ft.padding.symmetric(vertical=20, horizontal=40),
                                                        shape=ft.RoundedRectangleBorder(radius=20),
                                                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600)
                                                    )
                                                ),
                                                ft.Container(height=16),
                                                ft.OutlinedButton(
                                                    width=300,
                                                    height=50,
                                                    on_click=self.create_test_user,
                                                    content=ft.Row(
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        spacing=8,
                                                        controls=[
                                                            ft.Text("🧪", size=16),
                                                            ft.Text("Usuario de prueba", size=14, weight=ft.FontWeight.W_500)
                                                        ]
                                                    ),
                                                    style=ft.ButtonStyle(
                                                        color="#A0AEC0",
                                                        side=ft.BorderSide(1, "#E2E8F0"),
                                                        padding=ft.padding.symmetric(vertical=16, horizontal=32),
                                                        shape=ft.RoundedRectangleBorder(radius=15)
                                                    )
                                                )
                                            ]
                                        )
                                    )
                                )
                            ),
                            # Footer
                            ft.Container(
                                margin=ft.margin.only(top=32, bottom=40),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "💭 Un momento de reflexión puede transformar tu día",
                                            size=12, color="#A0AEC0", text_align=ft.TextAlign.CENTER, italic=True
                                        ),
                                        ft.Container(height=8),
                                        ft.Container(
                                            content=ft.Text("🔐 Seguro y privado", size=12, color="#667EEA", weight=ft.FontWeight.W_500),
                                            bgcolor="#E8EAF6",
                                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                            border_radius=20
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )

        return view

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
            snackbar = ft.SnackBar(
                content=ft.Text(f"🌸 {message}", color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
                bgcolor="#48BB78",
                duration=3000,
                elevation=10
            )
            self.page.snack_bar = snackbar
            snackbar.open = True
            self.page.update()

    def login_click(self, e):
        self.page = e.page
        email = self.email_field.value.strip()
        password = self.password_field.value

        if not email or not password:
            self.show_error("Completa todos los campos para continuar tu viaje")
            return

        if "@" not in email or "." not in email:
            self.show_error("Introduce un email válido para acceder")
            return

        self.hide_error()

        try:
            from services import db
            usuario = db.login_user(email, password)
            if usuario:
                nombre = usuario.get("name", email.split("@")[0])
                self.show_success(f"🌸 ¡Bienvenido de vuelta, {nombre}!")
                self.email_field.value = ""
                self.password_field.value = ""
                self.page.update()
                self.app.navigate_to_entry(usuario)
            else:
                self.show_error("Credenciales incorrectas. Verifica tus datos")
        except Exception as ex:
            print(f"Error en login: {ex}")
            self.show_error("Error del sistema. Intenta de nuevo")

    def register_click(self, e):
        self.page = e.page
        self.page.go("/register")

    def create_test_user(self, e):
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
            self.email_field.value = email
            self.password_field.value = password
            self.page.update()
        except Exception as ex:
            print(f"Error creando usuario: {ex}")
            self.show_error("Error creando perfil zen")
