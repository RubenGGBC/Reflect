# services/__init__.py
"""
🌸 Servicios zen para ReflectApp
Inicialización de servicios de base de datos e IA contemplativos
"""

from .ai_service import analyze_tag, get_daily_summary, get_mood_score, get_zen_quote
from .database_service import DatabaseService

# Instancia global de la base de datos zen
print("🧘‍♀️ Inicializando servicios zen...")

try:
    db = DatabaseService()
    print("✨ Base de datos zen conectada")
except Exception as e:
    print(f"❌ Error inicializando base de datos zen: {e}")
    # Crear instancia de respaldo
    db = DatabaseService("reflect_zen_backup.db")

# Verificar funcionamiento zen
try:
    # Prueba básica de funcionamiento
    test_count = db.get_entry_count(user_id=999999)  # Usuario inexistente
    print("🌸 Servicios zen funcionando en armonía")
except Exception as e:
    print(f"⚠️ Advertencia en servicios zen: {e}")

# Exportar servicios principales zen
__all__ = [
    'db',
    'analyze_tag',
    'get_daily_summary',
    'get_mood_score',
    'get_zen_quote'
]

print("🌺 ReflectApp zen services ready - Namaste 🙏")