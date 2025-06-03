# services/__init__.py
"""
🌸 Servicios zen para ReflectApp - CON SISTEMA DE SESIONES
✅ NUEVO: Servicios de sesiones y perfil de usuario
✅ NUEVO: Auto-login y recordar cuenta
✅ ACTUALIZADO: Base de datos con métodos de usuario mejorados
"""

from .database_service import DatabaseService
from .session_service import (
    SessionService, session_service,
    save_user_session, load_user_session, logout_user,
    is_user_logged_in, get_auto_login_data
)
from .mobile_notification_service import (
    initialize_mobile_notifications,
    get_mobile_notification_service,
    start_mobile_notifications,
    stop_mobile_notifications,
    send_mobile_notification,
    test_mobile_notifications
)

# ✅ Instancia global de la base de datos zen CON MÉTODOS DE SESIONES
print("🧘‍♀️ Inicializando servicios zen CON SISTEMA DE SESIONES...")

try:
    db = DatabaseService()
    print("✨ Base de datos zen conectada CON SESIONES")
except Exception as e:
    print(f"❌ Error inicializando base de datos zen: {e}")
    # Crear instancia de respaldo
    db = DatabaseService("reflect_zen_backup.db")

# ✅ Verificar funcionamiento zen CON SESIONES
try:
    # Prueba básica de funcionamiento
    test_count = db.get_entry_count(user_id=999999)  # Usuario inexistente
    print("🌸 Servicios zen funcionando en armonía CON SESIONES")
except Exception as e:
    print(f"⚠️ Advertencia en servicios zen: {e}")

# ✅ Cargar sesión existente al inicializar
try:
    existing_session = load_user_session()
    if existing_session:
        print(f"🔄 Sesión existente encontrada para: {existing_session.get('name', 'Usuario')}")
    else:
        print("ℹ️ No hay sesión existente")
except Exception as e:
    print(f"⚠️ Error verificando sesión existente: {e}")

# ✅ Exportar servicios principales zen CON SESIONES
__all__ = [
    # Base de datos
    'db',
    'DatabaseService',

    # Sistema de sesiones
    'SessionService',
    'session_service',
    'save_user_session',
    'load_user_session',
    'logout_user',
    'is_user_logged_in',
    'get_auto_login_data',

    # Notificaciones móviles
    'initialize_mobile_notifications',
    'get_mobile_notification_service',
    'start_mobile_notifications',
    'stop_mobile_notifications',
    'send_mobile_notification',
    'test_mobile_notifications'
]

print("🌺 ReflectApp zen services ready CON SESIONES - Namaste 🙏")
print("✅ SERVICIOS DISPONIBLES:")
print("   🗄️ Base de datos con métodos de usuario")
print("   🔐 Sistema de sesiones y auto-login")
print("   📱 Notificaciones móviles avanzadas")
print("   👤 Gestión completa de perfiles de usuario")