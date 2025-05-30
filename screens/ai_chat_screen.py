"""
💬🧠 AI Chat Screen - ReflectApp - VERSIÓN SIN ICONOS
Pantalla dedicada para conversar con el especialista en salud mental
"""

import flet as ft
from datetime import datetime
from services.reflect_themes_system import (
    get_theme, create_themed_container, create_themed_button,
    create_gradient_header
)

class ChatMessage:
    """Clase para representar un mensaje en el chat"""

    def __init__(self, content, is_user=True, timestamp=None):
        self.content = content
        self.is_user = is_user  # True = usuario, False = IA
        self.timestamp = timestamp or datetime.now()
        self.is_typing = False  # Para animación de "escribiendo..."

class AIChatScreen:
    """Pantalla de chat con IA especialista en salud mental"""

    def __init__(self, app, initial_context=None):
        self.app = app
        self.page = None
        self.theme = get_theme()

        # Estado del chat
        self.messages = []
        self.conversation_context = initial_context or {}
        self.is_ai_typing = False

        # Componentes UI
        self.messages_container = None
        self.message_input = None
        self.send_button = None
        self.scroll_container = None

        print("💬 AI Chat Screen inicializada")

    def set_initial_context(self, reflection_text, positive_tags, negative_tags, worth_it):
        """Establecer contexto inicial del día para el chat"""
        self.conversation_context = {
            'reflection': reflection_text,
            'positive_tags': positive_tags,
            'negative_tags': negative_tags,
            'worth_it': worth_it,
            'day_analyzed': False  # Para saber si ya se hizo el análisis inicial
        }
        print(f"💭 Contexto inicial establecido:")
        print(f"   Reflexión: {len(reflection_text)} caracteres")
        print(f"   Tags positivos: {len(positive_tags)}")
        print(f"   Tags negativos: {len(negative_tags)}")
        print(f"   Worth it: {worth_it}")

    def build(self):
        """Construir vista de chat completa"""
        self.theme = get_theme()

        # Header del chat - SIN ICONOS
        back_button = ft.TextButton(
            "← Volver",
            on_click=self.go_back,
            style=ft.ButtonStyle(color="#FFFFFF")
        )

        header = create_gradient_header(
            title="🧠💚 Chat con Especialista IA",
            left_button=back_button,
            theme=self.theme
        )

        # Contenedor de mensajes con scroll
        self.messages_container = ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True
        )

        self.scroll_container = ft.Container(
            content=self.messages_container,
            expand=True,
            padding=ft.padding.all(16),
            bgcolor=self.theme.primary_bg
        )

        # Campo de entrada de mensaje - SIN ICONOS
        self.message_input = ft.TextField(
            hint_text="Escribe tu mensaje...",
            multiline=True,
            min_lines=1,
            max_lines=4,
            border_radius=25,
            content_padding=ft.padding.all(15),
            bgcolor=self.theme.surface,
            border_color=self.theme.border_color,
            focused_border_color=self.theme.accent_primary,
            text_style=ft.TextStyle(size=16, color=self.theme.text_primary),
            on_submit=self.send_message,
            expand=True
        )

        # Botón de enviar - SIMPLE SIN ICONOS
        self.send_button = ft.ElevatedButton(
            text="Enviar",
            on_click=self.send_message,
            style=ft.ButtonStyle(
                bgcolor=self.theme.accent_primary,
                color="#FFFFFF",
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=25)
            ),
            height=50
        )

        # Barra de entrada
        input_bar = ft.Container(
            content=ft.Row(
                [
                    self.message_input,
                    ft.Container(width=8),
                    self.send_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.END
            ),
            padding=ft.padding.all(16),
            bgcolor=self.theme.surface,
            border=ft.border.only(top=ft.BorderSide(1, self.theme.border_color))
        )

        # Vista principal
        view = ft.View(
            "/ai_chat",
            [
                header,

                # Área de mensajes
                self.scroll_container,

                # Barra de entrada
                input_bar
            ],
            bgcolor=self.theme.primary_bg,
            padding=0,
            spacing=0
        )

        # Cargar análisis inicial si hay contexto
        if self.conversation_context and not self.conversation_context.get('day_analyzed', False):
            print("🔄 Iniciando análisis inicial del día...")
            self.start_initial_analysis()
        else:
            print("ℹ️ No hay contexto para análisis inicial")

        return view

    def start_initial_analysis(self):
        """Iniciar análisis inicial del día con la IA"""
        if not self.conversation_context:
            print("⚠️ No hay contexto para análisis")
            return

        print("🔍 Iniciando análisis inicial del día...")

        # Mensaje de bienvenida
        welcome_msg = ChatMessage(
            content="¡Hola! Soy tu especialista en salud mental. He revisado tu reflexión del día y me gustaría conversar contigo sobre cómo te has sentido. Dame un momento para analizar todo...",
            is_user=False
        )
        self.add_message(welcome_msg)

        # Mostrar que la IA está "escribiendo"
        self.show_ai_typing()

        # Hacer análisis en background
        self.analyze_day_in_background()

    def analyze_day_in_background(self):
        """Analizar el día en background y mostrar respuesta"""
        try:
            from services.mental_health_ia import analyze_daily_entry_with_ai

            print("🤖 Llamando a IA para análisis...")
            print(f"📝 Reflexión: {len(self.conversation_context.get('reflection', ''))} chars")
            print(f"➕ Tags positivos: {len(self.conversation_context.get('positive_tags', []))}")
            print(f"➖ Tags negativos: {len(self.conversation_context.get('negative_tags', []))}")

            # Analizar entrada con IA
            ai_response = analyze_daily_entry_with_ai(
                reflection_text=self.conversation_context.get('reflection', ''),
                positive_tags=self.conversation_context.get('positive_tags', []),
                negative_tags=self.conversation_context.get('negative_tags', []),
                worth_it=self.conversation_context.get('worth_it')
            )

            print(f"✅ Respuesta de IA recibida: {len(ai_response)} caracteres")

            # Ocultar typing y mostrar respuesta
            self.hide_ai_typing()

            # Crear mensaje de respuesta
            analysis_msg = ChatMessage(
                content=ai_response,
                is_user=False
            )
            self.add_message(analysis_msg)

            # Marcar como analizado
            self.conversation_context['day_analyzed'] = True
            self.conversation_context['initial_analysis'] = ai_response

            print("✅ Análisis inicial completado")

        except Exception as e:
            print(f"❌ Error en análisis inicial: {e}")
            import traceback
            traceback.print_exc()

            self.hide_ai_typing()

            error_msg = ChatMessage(
                content="Disculpa, he tenido una dificultad técnica analizando tu día. Pero estoy aquí para escucharte. ¿Cómo te sientes en este momento?",
                is_user=False
            )
            self.add_message(error_msg)

    def send_message(self, e=None):
        """Enviar mensaje del usuario"""
        message_text = self.message_input.value.strip()
        if not message_text:
            return

        print(f"📤 Enviando mensaje: {message_text[:50]}...")

        # Crear mensaje del usuario
        user_msg = ChatMessage(content=message_text, is_user=True)
        self.add_message(user_msg)

        # Limpiar campo de entrada
        self.message_input.value = ""
        if self.page:
            self.page.update()

        # Mostrar que la IA está escribiendo
        self.show_ai_typing()

        # Generar respuesta de la IA
        self.generate_ai_response(message_text)

    def generate_ai_response(self, user_message):
        """Generar respuesta de la IA"""
        try:
            from services.mental_health_ia import continue_ai_conversation

            # Crear contexto de la conversación
            conversation_history = self.get_conversation_context()

            print(f"🤖 Generando respuesta para: {user_message[:30]}...")

            # Generar respuesta
            ai_response = continue_ai_conversation(conversation_history, user_message)

            print(f"✅ Respuesta generada: {len(ai_response)} caracteres")

            # Ocultar typing
            self.hide_ai_typing()

            # Crear mensaje de la IA
            ai_msg = ChatMessage(content=ai_response, is_user=False)
            self.add_message(ai_msg)

        except Exception as e:
            print(f"❌ Error generando respuesta: {e}")
            import traceback
            traceback.print_exc()

            self.hide_ai_typing()

            error_msg = ChatMessage(
                content="Disculpa, he tenido una dificultad técnica. ¿Podrías repetir lo que me querías decir?",
                is_user=False
            )
            self.add_message(error_msg)

    def get_conversation_context(self):
        """Obtener contexto de la conversación para la IA"""
        context_parts = []

        # Análisis inicial si existe
        if self.conversation_context.get('initial_analysis'):
            context_parts.append(f"Análisis inicial: {self.conversation_context['initial_analysis']}")

        # Últimos mensajes (máximo 6 para no sobrecargar)
        recent_messages = self.messages[-6:] if len(self.messages) > 6 else self.messages

        for msg in recent_messages:
            sender = "Usuario" if msg.is_user else "IA"
            context_parts.append(f"{sender}: {msg.content}")

        return "\n".join(context_parts)

    def add_message(self, message):
        """Añadir mensaje al chat"""
        self.messages.append(message)

        # Crear widget del mensaje
        message_widget = self.create_message_widget(message)
        self.messages_container.controls.append(message_widget)

        # Actualizar UI
        if self.page:
            self.page.update()

        print(f"💬 Mensaje añadido: {'Usuario' if message.is_user else 'IA'} - {len(message.content)} chars")

    def create_message_widget(self, message):
        """Crear widget visual para un mensaje - SIN ICONOS PROBLEMÁTICOS"""
        # Determinar alineación y colores
        if message.is_user:
            # Mensaje del usuario (derecha)
            alignment = ft.MainAxisAlignment.END
            bg_color = self.theme.accent_primary
            text_color = "#FFFFFF"
            avatar_text = "Tú"
            margin = ft.margin.only(left=60, right=16, top=4, bottom=4)
        else:
            # Mensaje de la IA (izquierda)
            alignment = ft.MainAxisAlignment.START
            bg_color = self.theme.surface
            text_color = self.theme.text_primary
            avatar_text = "IA"
            margin = ft.margin.only(left=16, right=60, top=4, bottom=4)

        # Timestamp
        time_str = message.timestamp.strftime("%H:%M")

        # Contenido del mensaje
        message_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        message.content,
                        size=14,
                        color=text_color,
                        selectable=True
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        time_str,
                        size=10,
                        color=text_color if message.is_user else self.theme.text_hint,
                        text_align=ft.TextAlign.RIGHT if message.is_user else ft.TextAlign.LEFT
                    )
                ],
                spacing=0,
                tight=True
            ),
            bgcolor=bg_color,
            padding=ft.padding.all(12),
            border_radius=ft.border_radius.only(
                top_left=15,
                top_right=15,
                bottom_left=3 if message.is_user else 15,
                bottom_right=15 if message.is_user else 3
            ),
            margin=margin,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=self.theme.shadow_color,
                offset=ft.Offset(0, 1)
            )
        )

        # Avatar simple con texto
        avatar_container = ft.Container(
            content=ft.Text(avatar_text, size=12, weight=ft.FontWeight.BOLD),
            width=32,
            height=32,
            border_radius=16,
            bgcolor=self.theme.accent_primary if message.is_user else self.theme.positive_main,
            alignment=ft.alignment.center
        )

        # Row con avatar y mensaje
        if message.is_user:
            return ft.Row(
                [
                    message_content,
                    avatar_container
                ],
                alignment=alignment,
                spacing=8
            )
        else:
            return ft.Row(
                [
                    avatar_container,
                    message_content
                ],
                alignment=alignment,
                spacing=8
            )

    def show_ai_typing(self):
        """Mostrar indicador de que la IA está escribiendo - SIN ICONOS"""
        self.is_ai_typing = True

        typing_indicator = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text("IA", size=12, weight=ft.FontWeight.BOLD),
                        width=32,
                        height=32,
                        border_radius=16,
                        bgcolor=self.theme.positive_main,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("Escribiendo...", size=14, color=self.theme.text_secondary, italic=True),
                                ft.ProgressRing(width=12, height=12, stroke_width=2)
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.START
                        ),
                        bgcolor=self.theme.surface,
                        padding=ft.padding.all(12),
                        border_radius=15,
                        margin=ft.margin.only(left=16, right=60, top=4, bottom=4)
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8
            )
        )

        # Añadir con ID para poder encontrarlo después
        typing_indicator.data = "typing_indicator"
        self.messages_container.controls.append(typing_indicator)

        if self.page:
            self.page.update()

    def hide_ai_typing(self):
        """Ocultar indicador de typing"""
        self.is_ai_typing = False

        # Buscar y remover el indicador de typing
        for i, control in enumerate(self.messages_container.controls):
            if hasattr(control, 'data') and control.data == "typing_indicator":
                self.messages_container.controls.pop(i)
                break

        if self.page:
            self.page.update()

    def go_back(self, e):
        """Volver a la pantalla anterior"""
        print("⬅️ Volviendo a entry screen")
        if hasattr(e, 'page'):
            e.page.go("/entry")
        elif self.page:
            self.page.go("/entry")

    def update_theme(self):
        """Actualizar tema cuando cambie"""
        self.theme = get_theme()

# Función helper para crear la pantalla desde otros módulos
def create_ai_chat_screen(app, reflection_text="", positive_tags=None, negative_tags=None, worth_it=None):
    """
    Función helper para crear pantalla de chat con contexto inicial
    """
    chat_screen = AIChatScreen(app)

    if reflection_text or positive_tags or negative_tags or worth_it is not None:
        chat_screen.set_initial_context(
            reflection_text,
            positive_tags or [],
            negative_tags or [],
            worth_it
        )

    return chat_screen