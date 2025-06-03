"""
⚙️ Configuración de ReflectApp
Configuraciones centralizadas para la aplicación
"""

import os
from datetime import timedelta

class AppConfig:
    """Configuración centralizada de ReflectApp"""

    # ===============================
    # CONFIGURACIÓN GENERAL
    # ===============================
    APP_NAME = "ReflectApp"
    APP_VERSION = "2.0.0"
    APP_DESCRIPTION = "Tu refugio mental 🦫"
    DEFAULT_AVATAR = "🦫"  # ✅ NUEVO: Nutria por defecto

    # ===============================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ===============================
    DATABASE_PATH = "data/reflect_zen.db"
    BACKUP_DATABASE_PATH = "data/reflect_zen_backup.db"
    DATA_DIRECTORY = "data"

    # ===============================
    # CONFIGURACIÓN DE SESIONES
    # ===============================
    SESSION_FILE = "data/user_session.json"
    SESSION_DURATION_DAYS = 30  # Cuántos días recordar la sesión
    AUTO_LOGIN_ENABLED = True

    # ===============================
    # CONFIGURACIÓN DE UI
    # ===============================
    WINDOW_WIDTH = 390
    WINDOW_HEIGHT = 844
    WINDOW_RESIZABLE = False

    # Temas disponibles
    AVAILABLE_THEMES = [
        "deep_ocean",
        "electric_dark",
        "spring_light",
        "sunset_warm"
    ]
    DEFAULT_THEME = "deep_ocean"

    # ===============================
    # CONFIGURACIÓN DE NOTIFICACIONES
    # ===============================
    NOTIFICATIONS_ENABLED = True
    DEFAULT_NOTIFICATION_SETTINGS = {
        "daily_reminder_enabled": True,
        "daily_reminder_time": "20:00",
        "morning_motivation_enabled": True,
        "morning_motivation_time": "09:00",
        "goodnight_enabled": True,
        "goodnight_time": "22:30",
        "wellbeing_checks_enabled": True,
        "notification_sound": True,
        "notification_vibration": True,
        "priority_mode": "normal"
    }

    # ===============================
    # CONFIGURACIÓN DE DESARROLLO
    # ===============================
    DEBUG_MODE = True
    TEST_USER_EMAIL = "zen@reflect.app"
    TEST_USER_PASSWORD = "reflect123"
    TEST_USER_NAME = "Viajero Zen"

    # ===============================
    # MENSAJES Y TEXTOS
    # ===============================
    WELCOME_MESSAGES = [
        "🦫 ¡Bienvenido de vuelta a tu refugio mental!",
        "🌸 Tu espacio zen te estaba esperando",
        "✨ Listo para reflexionar y crecer",
        "🧘‍♀️ Conecta contigo mismo en este momento",
        "🌿 Tu bienestar mental es nuestra prioridad"
    ]

    LOGOUT_MESSAGES = [
        "👋 Hasta luego, cuida tu paz interior",
        "🦫 Nos vemos pronto en tu refugio zen",
        "🌸 Que tengas un día lleno de consciencia",
        "✨ Lleva contigo lo aprendido hoy"
    ]

    MOTIVATIONAL_QUOTES = [
        "La paz viene de dentro. No la busques fuera.",
        "Cada momento de reflexión es un regalo para ti mismo.",
        "Tu bienestar mental importa más que cualquier otra cosa.",
        "Pequeños pasos diarios llevan a grandes transformaciones.",
        "Eres exactamente donde necesitas estar en este momento.",
        "La autocompasión es el primer paso hacia la sanación.",
        "Cada día es una nueva oportunidad de conectar contigo.",
        "Tu crecimiento personal no tiene límites."
    ]

    # ===============================
    # CONFIGURACIÓN DE FUNCIONALIDADES
    # ===============================

    # Momentos Interactivos
    MAX_MOMENTS_PER_DAY = 50
    DEFAULT_MOMENT_INTENSITY = 5
    MOMENT_CATEGORIES = ["general", "work", "personal", "health", "relationships"]

    # Emojis disponibles por categoría
    POSITIVE_EMOJIS = ['😊', '🎉', '💪', '☕', '🎵', '🤗', '😄', '🥳', '💖', '🌟', '🚀', '🎯']
    NEGATIVE_EMOJIS = ['😰', '😔', '😤', '💼', '😫', '🤯', '😩', '🙄', '😞', '😣', '🤦', '💔']

    # Calendario
    MAX_ENTRIES_PER_LOAD = 100
    CALENDAR_COLORS = {
        "positive": "#10B981",
        "negative": "#EF4444",
        "neutral": "#6B7280",
        "current": "#3B82F6"
    }

    # ===============================
    # MÉTODOS DE UTILIDAD
    # ===============================

    @classmethod
    def ensure_directories(cls):
        """Crear directorios necesarios"""
        directories = [
            cls.DATA_DIRECTORY,
            os.path.dirname(cls.SESSION_FILE),
            "config",
            "logs"
        ]

        for directory in directories:
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"📁 Directorio creado: {directory}")

    @classmethod
    def get_session_duration(cls):
        """Obtener duración de sesión como timedelta"""
        return timedelta(days=cls.SESSION_DURATION_DAYS)

    @classmethod
    def is_debug_mode(cls):
        """Verificar si está en modo debug"""
        return cls.DEBUG_MODE or os.getenv("REFLECT_DEBUG", "false").lower() == "true"

    @classmethod
    def get_random_welcome_message(cls):
        """Obtener mensaje de bienvenida aleatorio"""
        import random
        return random.choice(cls.WELCOME_MESSAGES)

    @classmethod
    def get_random_logout_message(cls):
        """Obtener mensaje de logout aleatorio"""
        import random
        return random.choice(cls.LOGOUT_MESSAGES)

    @classmethod
    def get_random_quote(cls):
        """Obtener cita motivacional aleatoria"""
        import random
        return random.choice(cls.MOTIVATIONAL_QUOTES)

    @classmethod
    def validate_config(cls):
        """Validar configuración"""
        errors = []

        # Verificar que los directorios sean válidos
        if not cls.DATA_DIRECTORY:
            errors.append("DATA_DIRECTORY no puede estar vacío")

        # Verificar configuración de sesión
        if cls.SESSION_DURATION_DAYS < 1:
            errors.append("SESSION_DURATION_DAYS debe ser al menos 1")

        # Verificar configuración de ventana
        if cls.WINDOW_WIDTH < 300 or cls.WINDOW_HEIGHT < 400:
            errors.append("Dimensiones de ventana demasiado pequeñas")

        if errors:
            print("❌ Errores de configuración encontrados:")
            for error in errors:
                print(f"   • {error}")
            return False

        print("✅ Configuración validada correctamente")
        return True

    @classmethod
    def initialize(cls):
        """Inicializar configuración completa"""
        print(f"⚙️ Inicializando configuración de {cls.APP_NAME} v{cls.APP_VERSION}")

        # Crear directorios necesarios
        cls.ensure_directories()

        # Validar configuración
        if not cls.validate_config():
            raise ValueError("Configuración inválida")

        print(f"✅ {cls.APP_NAME} configurado correctamente")
        print(f"🦫 Avatar por defecto: {cls.DEFAULT_AVATAR}")
        print(f"📱 Auto-login: {'Habilitado' if cls.AUTO_LOGIN_ENABLED else 'Deshabilitado'}")
        print(f"🔔 Notificaciones: {'Habilitadas' if cls.NOTIFICATIONS_ENABLED else 'Deshabilitadas'}")

        return True

# ===============================
# CONFIGURACIÓN DE DESARROLLO
# ===============================

class DevConfig(AppConfig):
    """Configuración para desarrollo"""
    DEBUG_MODE = True
    DATABASE_PATH = "data/reflect_zen_dev.db"
    SESSION_FILE = "data/user_session_dev.json"

# ===============================
# CONFIGURACIÓN DE PRODUCCIÓN
# ===============================

class ProdConfig(AppConfig):
    """Configuración para producción"""
    DEBUG_MODE = False

# ===============================
# SELECCIONAR CONFIGURACIÓN
# ===============================

def get_config():
    """Obtener configuración según el entorno"""
    env = os.getenv("REFLECT_ENV", "development").lower()

    if env == "production":
        return ProdConfig
    else:
        return DevConfig

# Configuración activa
config = get_config()