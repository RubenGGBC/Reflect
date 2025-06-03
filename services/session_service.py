"""
🔐 Sistema de Sesiones - ReflectApp
Maneja login automático, recordar usuario y logout seguro
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class SessionService:
    """Servicio para manejar sesiones de usuario y recordar cuenta"""

    def __init__(self, session_file: str = "data/user_session.json"):
        self.session_file = session_file
        self.current_session = None
        self._ensure_directory()

    def _ensure_directory(self):
        """Crear directorio de datos si no existe"""
        session_dir = os.path.dirname(self.session_file)
        if session_dir and not os.path.exists(session_dir):
            os.makedirs(session_dir, exist_ok=True)
            print(f"📁 Directorio de sesiones creado: {session_dir}")

    def save_session(self, user_data: Dict[str, Any], remember_me: bool = False) -> bool:
        """
        Guardar sesión de usuario

        Args:
            user_data: Datos del usuario (id, email, name, etc.)
            remember_me: Si true, guarda credenciales para auto-login

        Returns:
            bool: True si se guardó correctamente
        """
        try:
            # Crear datos de sesión
            session_data = {
                "user_id": user_data.get("id"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_emoji": user_data.get("avatar_emoji", "🦫"),
                "last_login": datetime.now().isoformat(),
                "remember_me": remember_me,
                "session_token": self._generate_session_token(user_data),
                "expires_at": (datetime.now() + timedelta(days=30)).isoformat() if remember_me else None
            }

            # Guardar en archivo
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)

            self.current_session = session_data
            print(f"💾 Sesión guardada para: {user_data.get('name')} (Remember: {remember_me})")
            return True

        except Exception as e:
            print(f"❌ Error guardando sesión: {e}")
            return False

    def load_session(self) -> Optional[Dict[str, Any]]:
        """
        Cargar sesión guardada si es válida

        Returns:
            Dict con datos de usuario si la sesión es válida, None si no
        """
        try:
            if not os.path.exists(self.session_file):
                print("ℹ️ No hay archivo de sesión")
                return None

            with open(self.session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            # Verificar si la sesión es válida
            if not self._is_session_valid(session_data):
                print("⏰ Sesión expirada, eliminando...")
                self.clear_session()
                return None

            self.current_session = session_data
            print(f"🔄 Sesión cargada para: {session_data.get('name')}")
            return session_data

        except Exception as e:
            print(f"❌ Error cargando sesión: {e}")
            return None

    def _is_session_valid(self, session_data: Dict[str, Any]) -> bool:
        """Verificar si una sesión es válida"""
        if not session_data:
            return False

        # Si no es "remember me", la sesión expira al cerrar la app
        if not session_data.get("remember_me", False):
            return True

        # Si es "remember me", verificar fecha de expiración
        expires_at = session_data.get("expires_at")
        if expires_at:
            try:
                expiry_date = datetime.fromisoformat(expires_at)
                return datetime.now() < expiry_date
            except:
                return False

        return False

    def _generate_session_token(self, user_data: Dict[str, Any]) -> str:
        """Generar token de sesión único"""
        data_string = f"{user_data.get('id')}_{user_data.get('email')}_{datetime.now().timestamp()}"
        return hashlib.sha256(data_string.encode()).hexdigest()[:32]

    def clear_session(self) -> bool:
        """
        Limpiar sesión actual (logout)

        Returns:
            bool: True si se limpió correctamente
        """
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)

            self.current_session = None
            print("🚪 Sesión eliminada (logout)")
            return True

        except Exception as e:
            print(f"❌ Error eliminando sesión: {e}")
            return False

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """Obtener sesión actual"""
        return self.current_session

    def is_logged_in(self) -> bool:
        """Verificar si hay una sesión activa"""
        return self.current_session is not None

    def update_last_activity(self) -> bool:
        """Actualizar timestamp de última actividad"""
        if not self.current_session:
            return False

        try:
            self.current_session["last_activity"] = datetime.now().isoformat()

            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_session, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"❌ Error actualizando actividad: {e}")
            return False

    def get_auto_login_data(self) -> Optional[Dict[str, Any]]:
        """
        Obtener datos para auto-login si están disponibles

        Returns:
            Dict con email y datos para auto-login, None si no disponible
        """
        session = self.load_session()
        if session and session.get("remember_me", False):
            return {
                "email": session.get("email"),
                "user_id": session.get("user_id"),
                "name": session.get("name"),
                "avatar_emoji": session.get("avatar_emoji", "🦫")
            }
        return None

# Instancia global del servicio de sesiones
session_service = SessionService()

# Funciones helper para uso fácil
def save_user_session(user_data: Dict[str, Any], remember_me: bool = False) -> bool:
    """Guardar sesión de usuario"""
    return session_service.save_session(user_data, remember_me)

def load_user_session() -> Optional[Dict[str, Any]]:
    """Cargar sesión guardada"""
    return session_service.load_session()

def logout_user() -> bool:
    """Hacer logout del usuario actual"""
    return session_service.clear_session()

def is_user_logged_in() -> bool:
    """Verificar si hay usuario logueado"""
    return session_service.is_logged_in()

def get_auto_login_data() -> Optional[Dict[str, Any]]:
    """Obtener datos de auto-login"""
    return session_service.get_auto_login_data()