# services/__init__.py
"""
🌸 Servicios zen para ReflectApp - SIN IA
Inicialización de servicios de base de datos y notificaciones SIN IA
"""

from .database_service import DatabaseService
from .mobile_notification_service import (
    initialize_mobile_notifications,
    get_mobile_notification_service,
    start_mobile_notifications,
    stop_mobile_notifications,
    send_mobile_notification,
    test_mobile_notifications
)

# ✅ Instancia global de la base de datos zen SIN IA
print("🧘‍♀️ Inicializando servicios zen SIN IA...")

try:
    db = DatabaseService()
    print("✨ Base de datos zen conectada SIN IA")
except Exception as e:
    print(f"❌ Error inicializando base de datos zen: {e}")
    # Crear instancia de respaldo
    db = DatabaseService("reflect_zen_backup.db")

# ✅ Verificar funcionamiento zen SIN IA
try:
    # Prueba básica de funcionamiento
    test_count = db.get_entry_count(user_id=999999)  # Usuario inexistente
    print("🌸 Servicios zen funcionando en armonía SIN IA")
except Exception as e:
    print(f"⚠️ Advertencia en servicios zen: {e}")

# ✅ Exportar servicios principales zen SIN IA
__all__ = [
    'db',
    'DatabaseService',
    'initialize_mobile_notifications',
    'get_mobile_notification_service',
    'start_mobile_notifications',
    'stop_mobile_notifications',
    'send_mobile_notification',
    'test_mobile_notifications'
]

print("🌺 ReflectApp zen services ready SIN IA - Namaste 🙏")
print("❌ TODAS LAS REFERENCIAS A IA HAN SIDO COMPLETAMENTE REMOVIDAS")
print("✅ Solo servicios esenciales: Base de datos + Notificaciones móviles")