# services/__init__.py
from .ai_service import analyze_mock
from .database_service import DatabaseService

# Instancia global de la base de datos
db = DatabaseService()