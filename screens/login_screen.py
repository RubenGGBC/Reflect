"""
🔐 Login Screen MEJORADA - ReflectApp
✅ NUEVO: Auto-login con sesiones guardadas
✅ NUEVO: Checkbox "Recordarme"
✅ NUEVO: Diseño visual mejorado con animaciones
✅ NUEVO: Emoji de nutria en lugar de zen 🦫
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

        # Auto-login
        self.checking_auto_login = False

    def build(self):
        """Construir vista de login MEJORADA con auto-login"""
        theme = get_theme()

        # ✅ NUEVO: Verificar auto-login al cargar
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
            margin=ft.margin.only(bottom=16),
            animate_opacity=300
        )

        # ✅ NUEVO: Hero Section con nutria y mejor diseño
        hero_section = self.create_enhanced_hero_section(theme)

        # ✅ MEJORADO: Formulario con glassmorphism
        form_section = self.create_enhanced_form_section(theme)

        # ✅ NUEVO: Quote section con más estilo
        quote_section = self.create_enhanced_quote_section(theme)

        # ✅ NUEVO: Loading overlay para auto-login
        loading_overlay = self.create_loading_overlay(theme)

        # Vista principal
        main_content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=60),  # Espaciado superior
                hero_section,
                form_section,
                quote_section,
                ft.Container(height=40)   # Espaciado inferior
            ]
        )

        # Stack para overlay de loading
        content_stack = ft.Stack([
            ft.Container(
                expand=True,
                content=main_content,
                padding=ft.padding.all(24)
            ),
            loading_overlay
        ])

        view = ft.View(
            "/login",
            controls=[content_stack],
            bgcolor=theme.primary_bg,
            padding=0,
            spacing=0
        )

        return view

    def create_enhanced_hero_section(self, theme):
        """✅ NUEVO: Hero section mejorada con nutria y animaciones"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # ✅ NUEVO: Nutria con efecto de resplandor
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
                        ),
                        animate_scale=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
                        animate_opacity=300
                    ),

                    ft.Container(height=24),

                    # ✅ MEJORADO: Título con gradiente de texto simulado
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

                    # ✅ NUEVO: Subtítulo con decoraciones mejoradas
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=40, height=2,
                                    bgcolor=theme.accent_primary,
                                    border_radius=1,
                                    animate_size=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT)
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
                                    border_radius=1,
                                    animate_size=ft.animation.Animation(1000, ft.AnimationCurve.EASE_OUT)
                                ),
                            ]
                        ),
                        animate_opacity=300
                    ),

                    ft.Container(height=12),

                    # ✅ NUEVO: Iconos flotantes decorativos
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
            margin=ft.margin.only(bottom=48),
            animate_opacity=300
        )

    def create_form_fields(self, theme):
        """Crear campos del formulario con mejor diseño"""

        # ✅ MEJORADO: Campo Email con icono y mejor estilo
        self.email_field = ft.TextField(
            label="📧 Correo electrónico",
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
            label_style=ft.TextStyle(size=14, color=theme.text_secondary),
            prefix_icon=ft.icons.EMAIL,
            animate_opacity=300
        )

        # ✅ MEJORADO: Campo Password con mejor visualización
        self.password_field = ft.TextField(
            label="🔒 Contraseña",
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
            prefix_icon=ft.icons.LOCK,
            on_submit=self.login_click,
            animate_opacity=300
        )

        # ✅ NUEVO: Checkbox "Recordarme"
        self.remember_me_checkbox = ft.Checkbox(
            label="Recordar mi sesión",
            value=False,
            check_color="#FFFFFF",
            fill_color=theme.positive_main,
            label_style=ft.TextStyle(size=14, color=theme.text_secondary)
        )

    def create_enhanced_form_section(self, theme):
        """✅ MEJORADO: Sección del formulario con mejor glassmorphism"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # ✅ NUEVO: Contenedor principal con efecto glassmorphism mejorado
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Campo Email
                                self.email_field,

                                ft.Container(height=20),

                                # Campo Password
                                self.password_field,

                                ft.Container(height=16),

                                # ✅ NUEVO: Remember me checkbox con mejor styling
                                ft.Container(
                                    content=ft.Row([
                                        self.remember_me_checkbox,
                                        ft.Container(expand=True),
                                        ft.TextButton(
                                            "¿Olvidaste tu contraseña?",
                                            on_click=self.forgot_password,
                                            style=ft.ButtonStyle(
                                                color=theme.accent_primary,
                                                overlay_color={"hovered": theme.accent_primary + "10"}
                                            )
                                        )
                                    ]),
                                    padding=ft.padding.symmetric(horizontal=8)
                                ),

                                ft.Container(height=8),

                                # Error container
                                self.error_container,

                                # ✅ MEJORADO: Botón principal con gradiente
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
                                            bgcolor={"": theme.accent_primary},
                                            color={"": "#FFFFFF"},
                                            elevation=8,
                                            shadow_color=theme.accent_primary + "40",
                                            shape=ft.RoundedRectangleBorder(radius=16),
                                            animation_duration=300
                                        )
                                    ),
                                    animate_scale=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT)
                                ),

                                ft.Container(height=24),

                                # ✅ MEJORADO: Separador con mejor diseño
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(
                                            width=100,
                                            height=1,
                                            gradient=ft.LinearGradient(
                                                begin=ft.alignment.center_left,
                                                end=ft.alignment.center_right,
                                                colors=["transparent", theme.border_color, "transparent"]
                                            )
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
                                            gradient=ft.LinearGradient(
                                                begin=ft.alignment.center_left,
                                                end=ft.alignment.center_right,
                                                colors=["transparent", theme.border_color, "transparent"]
                                            )
                                        )
                                    ]
                                ),

                                ft.Container(height=24),

                                # ✅ MEJORADO: Botón registro con mejor estilo
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
                                        color={"": theme.positive_main},
                                        side=ft.BorderSide(2, theme.positive_main + "60"),
                                        shape=ft.RoundedRectangleBorder(radius=16),
                                        bgcolor={"hovered": theme.positive_main + "10"},
                                        animation_duration=200
                                    )
                                ),

                                # ✅ MEJORADO: Usuario de prueba con mejor styling
                                ft.Container(
                                    content=ft.TextButton(
                                        content=ft.Row([
                                            ft.Text("🧪", size=14),
                                            ft.Container(width=4),
                                            ft.Text(
                                                "Modo desarrollador",
                                                size=13,
                                                color=theme.text_hint
                                            )
                                        ], alignment=ft.MainAxisAlignment.CENTER),
                                        on_click=self.create_test_user,
                                        style=ft.ButtonStyle(
                                            overlay_color={"hovered": theme.text_hint + "10"},
                                            shape=ft.RoundedRectangleBorder(radius=12)
                                        )
                                    ),
                                    margin=ft.margin.only(top=16)
                                )
                            ]
                        ),
                        width=380,
                        padding=ft.padding.all(32),
                        bgcolor=theme.surface + "F0",  # Más transparencia
                        border_radius=28,
                        border=ft.border.all(1, theme.border_color + "80"),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=32,
                            color="#00000020",
                            offset=ft.Offset(0, 12)
                        ),
                        animate_opacity=300
                    )
                ]
            ),
            margin=ft.margin.only(bottom=32)
        )

    def create_enhanced_quote_section(self, theme):
        """✅ NUEVO: Sección de quote mejorada con más estilo"""
        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # ✅ Quote principal con mejor tipografía
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

                    # ✅ NUEVO: Features destacadas con iconos
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
            ),
            animate_opacity=300
        )

    def create_loading_overlay(self, theme):
        """✅ NUEVO: Overlay de loading para auto-login"""
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

    def check_auto_login(self):
        """✅ NUEVO: Verificar si hay datos de auto-login"""
        def check_in_background():
            try:
                auto_login_data = get_auto_login_data()

                if auto_login_data:
                    print(f"🔄 Auto-login disponible para: {auto_login_data.get('email')}")

                    if self.page:
                        # Mostrar loading
                        self.show_loading_overlay(True)

                        # Simular un pequeño delay para UX
                        time.sleep(1)

                        # Intentar login automático
                        self.perform_auto_login(auto_login_data)
                else:
                    print("ℹ️ No hay datos de auto-login")

            except Exception as e:
                print(f"❌ Error en auto-login: {e}")
                if self.page:
                    self.show_loading_overlay(False)

        # Ejecutar en hilo separado para no bloquear UI
        threading.Thread(target=check_in_background, daemon=True).start()

    def perform_auto_login(self, auto_login_data):
        """✅ ACTUALIZADO: Realizar auto-login con datos guardados"""
        try:
            from services import db

            # ✅ CORREGIDO: Intentar obtener datos actualizados del usuario
            email = auto_login_data.get('email')
            user_data = db.get_user_by_email(email)

            if user_data:
                print(f"✅ Auto-login exitoso para: {user_data.get('name')}")

                # Prellenar campos (opcional, para mostrar que se está auto-logueando)
                if self.email_field:
                    self.email_field.value = email

                # Navegar automáticamente
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
        """✅ NUEVO: Mostrar/ocultar overlay de loading"""
        if self.page and len(self.page.controls) > 0:
            try:
                # El overlay está en el Stack
                stack = self.page.controls[0]
                if hasattr(stack, 'controls') and len(stack.controls) > 1:
                    overlay = stack.controls[1]
                    overlay.visible = show
                    self.page.update()
            except Exception as e:
                print(f"⚠️ Error mostrando overlay: {e}")

    def show_error(self, message):
        """Mostrar mensaje de error con animación mejorada"""
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
        """Mostrar mensaje de éxito con mejor estilo"""
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
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=12)
            )
            self.page.overlay.append(snackbar)
            snackbar.open = True
            self.page.update()

    def set_loading(self, loading):
        """Cambiar estado de carga"""
        self.is_loading = loading
        if self.page:
            self.page.update()

    def login_click(self, e):
        """✅ MEJORADO: Login con sistema de sesiones"""
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
        self.set_loading(True)

        try:
            from services import db
            usuario = db.login_user(email, password)

            if usuario:
                # ✅ NUEVO: Guardar sesión con opción "recordarme"
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
        finally:
            self.set_loading(False)

    def register_click(self, e):
        """Navegar a registro"""
        self.page = e.page
        self.page.go("/register")

    def forgot_password(self, e):
        """✅ NUEVO: Función para contraseña olvidada (placeholder)"""
        if self.page:
            # TODO: Implementar recuperación de contraseña
            self.show_success("🔄 Función en desarrollo - Contacta con soporte")

    def create_test_user(self, e):
        """Crear usuario de prueba con nutria"""
        self.page = e.page
        try:
            from services import db
            email = "zen@reflect.app"
            password = "reflect123"
            name = "Viajero Zen"

            user_id = db.create_user(email, password, name, avatar_emoji="🦫")
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