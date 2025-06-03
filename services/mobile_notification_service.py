"""
📱 Sistema de Notificaciones Móvil - ReflectApp Android
Notificaciones push locales para dispositivos móviles usando Flet
"""

import flet as ft
import asyncio
import threading
import time
import json
import os
from datetime import datetime, timedelta, time as dt_time
from typing import List, Dict, Optional, Callable
import schedule

class MobileNotificationService:
    """Servicio de notificaciones para dispositivos móviles Android/iOS"""

    def __init__(self, page: ft.Page = None, db_service=None):
        self.page = page
        self.db_service = db_service
        self.is_running = False
        self.scheduler_thread = None

        # Configuración por defecto
        self.settings = {
            "daily_reminder_enabled": True,
            "daily_reminder_time": "20:00",  # 8 PM
            "morning_motivation_enabled": True,
            "morning_motivation_time": "09:00",  # 9 AM
            "goodnight_enabled": True,
            "goodnight_time": "22:30",  # 10:30 PM
            "wellbeing_checks_enabled": True,
            "notification_sound": True,
            "notification_vibration": True
        }

        # Cola de notificaciones pendientes
        self.notification_queue = []
        self.notification_history = []

        print("📱 MobileNotificationService inicializado para móvil")

    def initialize_mobile_notifications(self, page: ft.Page):
        """Inicializar notificaciones móviles con la página de Flet"""
        self.page = page

        # Configurar página para recibir notificaciones
        if hasattr(page, 'platform'):
            print(f"📱 Plataforma detectada: {page.platform}")

        # Solicitar permisos de notificación (en móvil real)
        self.request_notification_permissions()

        print("✅ Notificaciones móviles inicializadas")

    def request_notification_permissions(self):
        """Solicitar permisos de notificación al usuario"""
        try:
            # En Flet móvil, esto se maneja automáticamente
            # Pero podemos mostrar un diálogo explicativo
            print("🔐 Solicitando permisos de notificación...")

            # TODO: En producción, aquí iría la solicitud real de permisos
            # Para desarrollo, asumimos que están concedidos

            return True
        except Exception as e:
            print(f"⚠️ Error solicitando permisos: {e}")
            return False

    def start_notification_scheduler(self):
        """Iniciar programador de notificaciones en background para móvil"""
        if self.is_running:
            print("⚠️ Scheduler ya está ejecutándose")
            return

        self.is_running = True

        # Configurar horarios de notificaciones
        self._schedule_mobile_notifications()

        # Ejecutar en hilo separado (compatible con móvil)
        def run_mobile_scheduler():
            print("🔄 Iniciando scheduler móvil...")
            while self.is_running:
                try:
                    schedule.run_pending()
                    time.sleep(30)  # Revisar cada 30 segundos (más eficiente en móvil)
                except Exception as e:
                    print(f"❌ Error en scheduler móvil: {e}")
                    time.sleep(60)

        self.scheduler_thread = threading.Thread(target=run_mobile_scheduler, daemon=True)
        self.scheduler_thread.start()

        print("✅ Scheduler móvil iniciado")

    def stop_notification_scheduler(self):
        """Detener programador de notificaciones"""
        self.is_running = False
        schedule.clear()
        print("🛑 Scheduler móvil detenido")

    def _schedule_mobile_notifications(self):
        """Configurar horarios específicos para móvil"""

        # 🌅 Motivación matutina
        morning_time = self.settings.get("morning_motivation_time", "09:00")
        schedule.every().day.at(morning_time).do(self._send_morning_notification)

        # 📝 Recordatorio de reflexión
        daily_time = self.settings.get("daily_reminder_time", "20:00")
        schedule.every().day.at(daily_time).do(self._send_daily_reminder_notification)

        # 🌙 Buenas noches
        goodnight_time = self.settings.get("goodnight_time", "22:30")
        schedule.every().day.at(goodnight_time).do(self._send_goodnight_notification)

        # 💚 Verificación de bienestar (cada 3 días)
        schedule.every(3).days.at("14:00").do(self._send_wellbeing_notification)

        print("📅 Horarios móviles configurados")

    def send_mobile_notification(self, title: str, message: str, icon: str = "🧘‍♀️",
                                 action_route: str = None, priority: str = "normal"):
        """
        Enviar notificación móvil usando las capacidades de Flet

        Args:
            title: Título de la notificación
            message: Mensaje principal
            icon: Emoji o icono
            action_route: Ruta a la que navegar al tocar (opcional)
            priority: Prioridad (low, normal, high)
        """

        notification_data = {
            "id": int(datetime.now().timestamp() * 1000),
            "title": f"{icon} {title}",
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "action_route": action_route,
            "priority": priority,
            "read": False
        }

        try:
            # MÉTODO 1: Notificación nativa si está disponible
            if self.page and hasattr(self.page, 'show_notification'):
                self.page.show_notification(
                    title=notification_data["title"],
                    message=message,
                    action=action_route
                )

            # MÉTODO 2: SnackBar como fallback (siempre visible)
            elif self.page:
                self._show_snackbar_notification(notification_data)

            # MÉTODO 3: Guardar en cola para mostrar cuando se abra la app
            else:
                self.notification_queue.append(notification_data)

            # Guardar en historial
            self.notification_history.append(notification_data)
            self._save_notification_history()

            print(f"📤 Notificación móvil enviada: {title}")

        except Exception as e:
            print(f"❌ Error enviando notificación móvil: {e}")
            # Fallback: guardar en cola
            self.notification_queue.append(notification_data)

    def _show_snackbar_notification(self, notification_data: Dict):
        """Mostrar notificación como SnackBar elegante"""
        if not self.page:
            return

        def handle_notification_tap(e):
            """Manejar tap en la notificación"""
            if notification_data.get("action_route"):
                self.page.go(notification_data["action_route"])
            self._mark_notification_as_read(notification_data["id"])

        # SnackBar elegante con acción
        snackbar_content = ft.Row([
            ft.Column([
                ft.Text(
                    notification_data["title"],
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF"
                ),
                ft.Text(
                    notification_data["message"],
                    size=12,
                    color="#FFFFFF90"
                )
            ], expand=True, spacing=4),

            ft.IconButton(
                icon=ft.icons.OPEN_IN_NEW,
                icon_color="#FFFFFF",
                on_click=handle_notification_tap,
                tooltip="Abrir"
            ) if notification_data.get("action_route") else ft.Container()
        ], alignment=ft.CrossAxisAlignment.CENTER)

        # Determinar color según prioridad
        bg_color = "#2196F3"  # Azul por defecto
        if notification_data["priority"] == "high":
            bg_color = "#FF5722"  # Rojo
        elif notification_data["priority"] == "low":
            bg_color = "#607D8B"  # Gris

        snackbar = ft.SnackBar(
            content=snackbar_content,
            bgcolor=bg_color,
            duration=5000,  # 5 segundos
            action="Ver",
            action_color="#FFFFFF",
            on_action=handle_notification_tap if notification_data.get("action_route") else None
        )

        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()

    def show_pending_notifications(self):
        """Mostrar notificaciones pendientes cuando se abre la app"""
        if not self.notification_queue:
            return

        print(f"📬 Mostrando {len(self.notification_queue)} notificaciones pendientes")

        for notification in self.notification_queue[:3]:  # Máximo 3 a la vez
            self._show_snackbar_notification(notification)
            time.sleep(1)  # Espaciar las notificaciones

        # Limpiar cola
        self.notification_queue.clear()

    def _mark_notification_as_read(self, notification_id: int):
        """Marcar notificación como leída"""
        for notification in self.notification_history:
            if notification["id"] == notification_id:
                notification["read"] = True
                break

        self._save_notification_history()

    def _save_notification_history(self):
        """Guardar historial de notificaciones"""
        try:
            os.makedirs("data", exist_ok=True)

            # Mantener solo las últimas 50 notificaciones
            recent_notifications = self.notification_history[-50:]

            with open("data/notification_history.json", "w", encoding="utf-8") as f:
                json.dump(recent_notifications, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"⚠️ Error guardando historial: {e}")

    def _load_notification_history(self):
        """Cargar historial de notificaciones"""
        try:
            if os.path.exists("data/notification_history.json"):
                with open("data/notification_history.json", "r", encoding="utf-8") as f:
                    self.notification_history = json.load(f)
                    print(f"📚 Cargadas {len(self.notification_history)} notificaciones del historial")
        except Exception as e:
            print(f"⚠️ Error cargando historial: {e}")
            self.notification_history = []

    # ===============================
    # NOTIFICACIONES ESPECÍFICAS MÓVILES
    # ===============================

    def _send_morning_notification(self):
        """Notificación motivacional matutina para móvil"""
        if not self.settings.get("morning_motivation_enabled", True):
            return

        messages = [
            "¡Buenos días! 🌅 Un nuevo día lleno de posibilidades",
            "✨ Cada mañana es una oportunidad de comenzar de nuevo",
            "🌱 Hoy es un buen día para crecer y aprender",
            "☀️ Tu bienestar mental importa. ¿Cómo te sientes?",
            "🎯 Establece una intención positiva para este día"
        ]

        import random
        message = random.choice(messages)

        self.send_mobile_notification(
            title="ReflectApp - Buenos días",
            message=message,
            icon="🌅",
            action_route="/entry",
            priority="normal"
        )

    def _send_daily_reminder_notification(self):
        """Recordatorio diario para hacer reflexión"""
        if not self.settings.get("daily_reminder_enabled", True):
            return

        # Verificar si ya reflexionó hoy
        if self._user_already_reflected_today():
            self.send_mobile_notification(
                title="¡Excelente trabajo!",
                message="🎉 Ya completaste tu reflexión de hoy",
                icon="⭐",
                action_route="/calendar",
                priority="low"
            )
            return

        # Recordatorio para reflexionar
        messages = [
            "🌙 Es hora de reflexionar sobre tu día",
            "📝 Dedica unos minutos a registrar tus momentos",
            "💭 Tu reflexión diaria te está esperando",
            "🧘‍♀️ Conéctate contigo mismo por unos minutos",
            "✨ Cada reflexión es un paso hacia el autoconocimiento"
        ]

        import random
        message = random.choice(messages)

        self.send_mobile_notification(
            title="Reflexión Diaria",
            message=message,
            icon="📝",
            action_route="/entry",
            priority="high"  # Alta prioridad porque es el recordatorio principal
        )

    def _send_goodnight_notification(self):
        """Mensaje de buenas noches"""
        if not self.settings.get("goodnight_enabled", True):
            return

        messages = [
            "🌙 Que tengas una noche reparadora y sueños tranquilos",
            "💤 Descansa bien. Mañana será un nuevo día",
            "✨ Agradece por los momentos buenos antes de dormir",
            "🕯️ Deja que la paz de la noche calme tu mente",
            "🌟 Has hecho lo que pudiste hoy, y eso es suficiente"
        ]

        import random
        message = random.choice(messages)

        self.send_mobile_notification(
            title="Buenas noches",
            message=message,
            icon="🌙",
            priority="low"
        )

    def _send_wellbeing_notification(self):
        """Verificación de bienestar"""
        if not self.settings.get("wellbeing_checks_enabled", True):
            return

        messages = [
            "💚 ¿Cómo ha sido tu bienestar emocional últimamente?",
            "🤗 Recuerda: está bien no estar bien todos los días",
            "🌱 Tu crecimiento personal es un proceso, no una carrera",
            "💝 Sé compasivo contigo mismo",
            "🌈 Los momentos difíciles también son parte del viaje"
        ]

        import random
        message = random.choice(messages)

        self.send_mobile_notification(
            title="Verificación de Bienestar",
            message=message,
            icon="💚",
            action_route="/entry",
            priority="normal"
        )

    def _user_already_reflected_today(self) -> bool:
        """Verificar si el usuario ya reflexionó hoy"""
        if not self.db_service:
            return False

        try:
            # TODO: Obtener ID del usuario actual
            # Por ahora retorna False (siempre enviar recordatorio)
            return False
        except Exception as e:
            print(f"❌ Error verificando reflexión: {e}")
            return False

    # ===============================
    # NOTIFICACIONES PERSONALIZADAS MÓVILES
    # ===============================

    def send_reflection_saved_notification(self):
        """Notificación cuando se guarda una reflexión"""
        self.send_mobile_notification(
            title="¡Reflexión guardada!",
            message="🎉 Tu momento de autoconocimiento ha sido registrado",
            icon="💾",
            action_route="/calendar",
            priority="normal"
        )

    def send_milestone_notification(self, days_count: int):
        """Notificación de hito alcanzado"""
        self.send_mobile_notification(
            title=f"🏆 ¡{days_count} días reflexionando!",
            message="Increíble constancia en tu crecimiento personal",
            icon="🎯",
            action_route="/calendar",
            priority="normal"
        )

    def send_encouragement_notification(self):
        """Notificación de ánimo cuando no ha reflexionado en varios días"""
        self.send_mobile_notification(
            title="Te extrañamos 💙",
            message="Está bien tomarse un descanso. ¿Qué tal una reflexión rápida?",
            icon="🤗",
            action_route="/entry",
            priority="normal"
        )

    def send_custom_notification(self, title: str, message: str, icon: str = "🔔",
                                 route: str = None, priority: str = "normal"):
        """Enviar notificación personalizada"""
        self.send_mobile_notification(
            title=title,
            message=message,
            icon=icon,
            action_route=route,
            priority=priority
        )

    # ===============================
    # CONFIGURACIÓN Y GESTIÓN
    # ===============================

    def update_settings(self, new_settings: Dict):
        """Actualizar configuración de notificaciones"""
        self.settings.update(new_settings)

        # Reconfigurar horarios si el scheduler está activo
        if self.is_running:
            schedule.clear()
            self._schedule_mobile_notifications()

        print(f"⚙️ Configuración móvil actualizada: {new_settings}")

    def get_settings(self) -> Dict:
        """Obtener configuración actual"""
        return self.settings.copy()

    def get_notification_history(self, limit: int = 20) -> List[Dict]:
        """Obtener historial de notificaciones"""
        return self.notification_history[-limit:]

    def clear_notification_history(self):
        """Limpiar historial de notificaciones"""
        self.notification_history.clear()
        self._save_notification_history()
        print("🗑️ Historial de notificaciones limpiado")

    def test_notification(self):
        """Enviar notificación de prueba"""
        self.send_mobile_notification(
            title="Prueba ReflectApp",
            message="🧪 ¡El sistema de notificaciones móvil funciona perfectamente!",
            icon="🔔",
            action_route="/entry",
            priority="normal"
        )


# ===============================
# INSTANCIA GLOBAL PARA MÓVIL
# ===============================

mobile_notification_service = None

def initialize_mobile_notifications(page: ft.Page, db_service=None):
    """Inicializar servicio de notificaciones móvil"""
    global mobile_notification_service

    mobile_notification_service = MobileNotificationService(page, db_service)
    mobile_notification_service.initialize_mobile_notifications(page)
    mobile_notification_service._load_notification_history()

    print("📱 Servicio de notificaciones móvil inicializado")
    return mobile_notification_service

def get_mobile_notification_service():
    """Obtener instancia del servicio móvil"""
    global mobile_notification_service

    if mobile_notification_service is None:
        print("⚠️ Servicio de notificaciones móvil no inicializado")

    return mobile_notification_service

# Funciones helper para uso fácil
def start_mobile_notifications():
    """Iniciar notificaciones móviles"""
    service = get_mobile_notification_service()
    if service:
        service.start_notification_scheduler()

def stop_mobile_notifications():
    """Detener notificaciones móviles"""
    service = get_mobile_notification_service()
    if service:
        service.stop_notification_scheduler()

def send_mobile_notification(title: str, message: str, icon: str = "🔔", route: str = None):
    """Enviar notificación móvil rápida"""
    service = get_mobile_notification_service()
    if service:
        service.send_mobile_notification(title, message, icon, route)

def test_mobile_notifications():
    """Probar notificaciones móviles"""
    service = get_mobile_notification_service()
    if service:
        service.test_notification()