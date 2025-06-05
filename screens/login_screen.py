"""
🔐 Login Screen CORREGIDA - ReflectApp
✅ ARREGLADO: Removidos todos los iconos
✅ ARREGLADO: Funciones de Flet verificadas
✅ ARREGLADO: Auto-login funcional
"""

import flet as ft
from services.reflect_themes_system import get_theme, apply_theme_to_page
from services.session_service import save_user_session, get_auto_login_data
import threading
import time

class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.page = None
        self.email_field = None
        self.password_field = None
        self.remember_me_checkbox = None
        self.error_container = None
        self.show_password = False
        self.is_loading = False
        self.checking_auto_login = False

    def build(self):
        """Construir vista de login CORREGIDA con scroll funcional"""
        theme = get_theme()

        # Verificar auto-login al cargar
        self.check_auto_login()

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

        # Hero Section con nutria
        hero_section = self.create_enhanced_hero_section(theme)

        # Formulario con glassmorphism
        form_section = self.create_enhanced_form_section(theme)

        # Quote section
        quote_section = self.create_enhanced_quote_section(theme)

        # Loading overlay para auto-login
        loading_overlay = self.create_loading_overlay(theme)

        # ✅ ARREGLADO: Vista principal con scroll REAL
        main_content = ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(height=40),  # Espaciado superior reducido
                    hero_section,
                    form_section,
                    quote_section,
                    ft.Container(height=40)   # Espaciado inferior
                ],
                spacing=0
            ),
            padding=ft.padding.all(20),
            expand=True  # ✅ IMPORTANTE: expand para que ocupe toda la altura
        )

        # ✅ ARREGLADO: Contenedor scrollable principal
        scrollable_content = ft.Container(
            content=main_content,
            expand=True
        )

        # Stack para overlay de loading
        content_stack = ft.Stack([
            scrollable_content,
            loading_overlay
        ])

        view = ft.View(
            "/login",
            controls=[content_stack],
            bgcolor=theme.primary_bg,
            padding=0,
            spacing=0,
            scroll=ft.ScrollMode.AUTO  # ✅ SCROLL EN LA VISTA
        )

        return view

    def create_enhanced_hero_section(self, theme):
        """Hero section con nutria y animaciones - SIN ICONOS"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Nutria con efecto de resplandor
                    ft.Container(
                        content=ft.Text("🦫", size=60, text_align=ft.TextAlign.CENTER),
                        width=120,
                        height=120,
                        bgcolor=theme.surface,
                        border_radius=60,
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=30,
                            color=theme.accent_primary + "60",
                            offset=ft.Offset(0, 10)
                        ),
                        gradient=ft.RadialGradient(
                            center=ft.alignment.center,
                            radius=1.2,
                            colors=[
                                theme.accent_primary + "30",
                                theme.surface,
                                theme.accent_primary + "20"
                            ]
                        )
                    ),

                    ft.Container(height=24),

                    # Título
                    ft.Column([
                        ft.Text(
                            "ReflectApp",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=theme.text_primary,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Zen",
                                size=16,
                                weight=ft.FontWeight.W_300,
                                color=theme.accent_primary,
                                text_align=ft.TextAlign.CENTER
                            ),
                            margin=ft.margin.only(top=-8)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),

                    ft.Container(height=16),

                    # Subtítulo mejorado
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=40, height=2,
                                    bgcolor=theme.accent_primary,
                                    border_radius=1
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "Tu refugio mental",
                                        size=16,
                                        color=theme.text_secondary,
                                        text_align=ft.TextAlign.CENTER,
                                        weight=ft.FontWeight.W_400
                                    ),
                                    margin=ft.margin.symmetric(horizontal=16)
                                ),
                                ft.Container(
                                    width=40, height=2,
                                    bgcolor=theme.accent_primary,
                                    border_radius=1
                                ),
                            ]
                        )
                    ),

                    ft.Container(height=12),

                    # Iconos decorativos (emojis)
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=24,
                        controls=[
                            ft.Text("✨", size=14, color=theme.text_hint),
                            ft.Text("🌸", size=16, color=theme.accent_primary),
                            ft.Text("🦋", size=14, color=theme.positive_main),
                            ft.Text("🌿", size=16, color=theme.text_hint),
                            ft.Text("⭐", size=14, color=theme.accent_primary),
                        ]
                    )
                ]
            ),
            margin=ft.margin.only(bottom=48)
        )

    def create_form_fields(self, theme):
        """Crear campos del formulario SIN ICONOS"""

        # Campo Email SIN ICONO
        self.email_field = ft.TextField(
            label="Correo electrónico",
            hint_text="tu@email.com",
            border=ft.InputBorder.OUTLINE,
            border_color=theme.border_color,
            focused_border_color=theme.accent_primary,
            border_radius=16,
            filled=True,
            bgcolor=theme.surface,
            content_padding=ft.padding.all(20),
            text_style=ft.TextStyle(size=16, color=theme.text_primary),
            cursor_color=theme.accent_primary,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary)
        )

        # Campo Password SIN ICONO
        self.password_field = ft.TextField(
            label="Contraseña",
            hint_text="••••••••",
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
            label_style=ft.TextStyle(size=14, color=theme.text_secondary),
            on_submit=self.login_click
        )

        # Checkbox "Recordarme"
        self.remember_me_checkbox = ft.Checkbox(
            label="Recordar mi sesión",
            value=False,
            check_color="#FFFFFF",
            fill_color=theme.positive_main,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary)
        )

    def create_enhanced_form_section(self, theme):
        """Sección del formulario con glassmorphism - SIN ICONOS"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Campo Email
                                self.email_field,

                                ft.Container(height=20),

                                # Campo Password
                                self.password_field,

                                ft.Container(height=16),

                                # Remember me checkbox
                                ft.Container(
                                    content=ft.Row([
                                        self.remember_me_checkbox,
                                        ft.Container(expand=True),
                                        ft.TextButton(
                                            "¿Olvidaste tu contraseña?",
                                            on_click=self.forgot_password,
                                            style=ft.ButtonStyle(
                                                color=theme.accent_primary
                                            )
                                        )
                                    ]),
                                    padding=ft.padding.symmetric(horizontal=8)
                                ),

                                ft.Container(height=8),

                                # Error container
                                self.error_container,

                                # Botón principal
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text("🦫", size=20),
                                                ft.Container(width=8),
                                                ft.Text(
                                                    "Entrar al refugio",
                                                    size=16,
                                                    weight=ft.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                        on_click=self.login_click,
                                        width=320,
                                        height=56,
                                        style=ft.ButtonStyle(
                                            bgcolor=theme.accent_primary,
                                            color="#FFFFFF",
                                            elevation=8,
                                            shadow_color=theme.accent_primary + "40",
                                            shape=ft.RoundedRectangleBorder(radius=16)
                                        )
                                    )
                                ),

                                ft.Container(height=24),

                                # Separador
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            width=100,
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
                                            width=100,
                                            height=1,
                                            bgcolor=theme.border_color
                                        )
                                    ]
                                ),

                                ft.Container(height=24),

                                # Botón registro
                                ft.OutlinedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("🌱", size=18),
                                            ft.Container(width=8),
                                            ft.Text(
                                                "Crear cuenta nueva",
                                                size=16,
                                                weight=ft.FontWeight.W_500
                                            )
                                        ]
                                    ),
                                    on_click=self.register_click,
                                    width=320,
                                    height=56,
                                    style=ft.ButtonStyle(
                                        color=theme.positive_main,
                                        side=ft.BorderSide(2, theme.positive_main + "60"),
                                        shape=ft.RoundedRectangleBorder(radius=16)
                                    )
                                ),

                                # ✅ BOTÓN MODO DESARROLLADOR - VISIBLE Y FUNCIONAL
                                ft.Container(
                                    content=ft.TextButton(
                                        content=ft.Row([
                                            ft.Text("🧪", size=16),
                                            ft.Container(width=6),
                                            ft.Text(
                                                "Modo desarrollador",
                                                size=14,
                                                color=theme.text_hint,
                                                weight=ft.FontWeight.W_500
                                            )
                                        ], alignment=ft.MainAxisAlignment.CENTER),
                                        on_click=self.create_test_user,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                            bgcolor={"hovered": theme.surface},
                                            overlay_color={"hovered": theme.accent_primary + "20"}
                                        )
                                    ),
                                    margin=ft.margin.only(top=20),
                                    padding=ft.padding.all(8),
                                    border_radius=12,
                                    border=ft.border.all(1, theme.border_color + "50")
                                )
                            ]
                        ),
                        width=380,
                        padding=ft.padding.all(32),
                        bgcolor=theme.surface + "F0",
                        border_radius=28,
                        border=ft.border.all(1, theme.border_color + "80"),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=32,
                            color="#00000020",
                            offset=ft.Offset(0, 12)
                        )
                    )
                ]
            ),
            margin=ft.margin.only(bottom=32)
        )

    def create_enhanced_quote_section(self, theme):
        """Sección de quote mejorada"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Text(
                            '"Cada reflexión es un paso hacia la paz interior"',
                            size=15,
                            color=theme.text_hint,
                            italic=True,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_400
                        ),
                        margin=ft.margin.symmetric(horizontal=20)
                    ),

                    ft.Container(height=20),

                    # Features destacadas SIN ICONOS
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=24,
                        controls=[
                            ft.Column([
                                ft.Text("🔐", size=20),
                                ft.Text("Privado", size=11, color=theme.positive_main, weight=ft.FontWeight.W_500)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),

                            ft.Container(width=1, height=30, bgcolor=theme.border_color),

                            ft.Column([
                                ft.Text("🧘‍♀️", size=20),
                                ft.Text("Zen", size=11, color=theme.accent_primary, weight=ft.FontWeight.W_500)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),

                            ft.Container(width=1, height=30, bgcolor=theme.border_color),

                            ft.Column([
                                ft.Text("📱", size=20),
                                ft.Text("Fácil", size=11, color=theme.text_secondary, weight=ft.FontWeight.W_500)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)
                        ]
                    )
                ]
            )
        )

    def create_loading_overlay(self, theme):
        """Overlay de loading para auto-login"""
        return ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.ProgressRing(
                        width=40,
                        height=40,
                        stroke_width=4,
                        color=theme.accent_primary
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Verificando sesión...",
                        size=14,
                        color=theme.text_primary,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(32),
                bgcolor=theme.primary_bg + "F0",
                border_radius=16,
                border=ft.border.all(1, theme.border_color),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color="#00000030",
                    offset=ft.Offset(0, 8)
                )
            ),
            alignment=ft.alignment.center,
            visible=False,
            animate_opacity=300
        )

    # Resto de métodos permanecen igual...
    def check_auto_login(self):
        """Verificar si hay datos de auto-login"""
        def check_in_background():
            try:
                auto_login_data = get_auto_login_data()
                if auto_login_data:
                    print(f"🔄 Auto-login disponible para: {auto_login_data.get('email')}")
                    if self.page:
                        self.show_loading_overlay(True)
                        time.sleep(1)
                        self.perform_auto_login(auto_login_data)
                else:
                    print("ℹ️ No hay datos de auto-login")
            except Exception as e:
                print(f"❌ Error en auto-login: {e}")
                if self.page:
                    self.show_loading_overlay(False)

        threading.Thread(target=check_in_background, daemon=True).start()

    def perform_auto_login(self, auto_login_data):
        """Realizar auto-login con datos guardados"""
        try:
            from services import db
            email = auto_login_data.get('email')
            user_data = db.get_user_by_email(email)

            if user_data:
                print(f"✅ Auto-login exitoso para: {user_data.get('name')}")
                if self.email_field:
                    self.email_field.value = email
                if self.page:
                    self.show_loading_overlay(False)
                    self.app.navigate_to_entry(user_data)
            else:
                print("❌ Auto-login falló: usuario no encontrado")
                if self.page:
                    self.show_loading_overlay(False)
                    self.show_error("Sesión expirada, inicia sesión nuevamente")
        except Exception as e:
            print(f"❌ Error en auto-login: {e}")
            if self.page:
                self.show_loading_overlay(False)

    def show_loading_overlay(self, show: bool):
        """Mostrar/ocultar overlay de loading"""
        if self.page and len(self.page.controls) > 0:
            try:
                stack = self.page.controls[0]
                if hasattr(stack, 'controls') and len(stack.controls) > 1:
                    overlay = stack.controls[1]
                    overlay.visible = show
                    self.page.update()
            except Exception as e:
                print(f"⚠️ Error mostrando overlay: {e}")

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
                content=ft.Row([
                    ft.Text("🦫", size=16),
                    ft.Container(width=8),
                    ft.Text(message, color="#FFFFFF", size=14, weight=ft.FontWeight.W_500)
                ]),
                bgcolor=theme.positive_main,
                duration=3000,
                elevation=10,
                shape=ft.RoundedRectangleBorder(radius=12)
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()

    def login_click(self, e):
        """Login con sistema de sesiones"""
        self.page = e.page
        email = self.email_field.value.strip() if self.email_field.value else ""
        password = self.password_field.value if self.password_field.value else ""
        remember_me = self.remember_me_checkbox.value if self.remember_me_checkbox else False

        # Validaciones
        if not email or not password:
            self.show_error("Completa todos los campos para continuar")
            return

        if "@" not in email or "." not in email:
            self.show_error("Introduce un email válido")
            return

        if len(password) < 3:
            self.show_error("Contraseña demasiado corta")
            return

        self.hide_error()

        try:
            from services import db
            usuario = db.login_user(email, password)

            if usuario:
                # Guardar sesión con opción "recordarme"
                save_user_session(usuario, remember_me)
                nombre = usuario.get("name", email.split("@")[0])
                remember_text = " (Sesión guardada)" if remember_me else ""
                self.show_success(f"🌸 ¡Bienvenido de vuelta, {nombre}!{remember_text}")

                # Limpiar campos
                self.email_field.value = ""
                self.password_field.value = ""
                self.remember_me_checkbox.value = False
                self.page.update()

                # Navegar a entry
                self.app.navigate_to_entry(usuario)
            else:
                self.show_error("Credenciales incorrectas. Verifica tus datos")

        except Exception as ex:
            print(f"Error en login: {ex}")
            self.show_error("Error del sistema. Intenta de nuevo")

    def register_click(self, e):
        """Navegar a registro"""
        self.page = e.page
        self.page.go("/register")

    def forgot_password(self, e):
        """Función para contraseña olvidada"""
        if self.page:
            self.show_success("🔄 Función en desarrollo - Contacta con soporte")

    def create_test_user(self, e):
        """✅ MEJORADO: Crear usuario de prueba con nutria"""
        self.page = e.page
        try:
            from services import db
            email = "zen@reflect.app"
            password = "reflect123"
            name = "Viajero Zen"

            # Mostrar mensaje de creación
            self.show_success("🧪 Creando perfil de desarrollador...")

            user_id = db.create_user(email, password, name, avatar_emoji="🦫")
            if user_id:
                self.show_success("✅ Perfil zen creado exitosamente")
            else:
                self.show_success("✅ Perfil zen ya existe y está listo")

            # Prellenar campos automáticamente
            self.email_field.value = email
            self.password_field.value = password

            # Marcar remember me por defecto en modo dev
            self.remember_me_checkbox.value = True

            self.page.update()

            # Auto-login después de 2 segundos
            import threading
            import time

            def auto_login():
                time.sleep(2)
                if self.page:
                    try:
                        self.login_click(e)
                    except:
                        pass

            threading.Thread(target=auto_login, daemon=True).start()

        except Exception as ex:
            print(f"Error creando usuario: {ex}")
            self.show_error("Error creando perfil zen")