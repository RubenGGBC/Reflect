# services/simple_ai_integration.py - NUEVO ARCHIVO SIMPLE
"""
🔗 Integración Simple de IA - ReflectApp
Conecta de manera directa el chat con la IA de salud mental
"""

from datetime import datetime
from typing import Dict, List, Optional, Any

def prepare_chat_context(reflection_text: str, positive_tags: List, negative_tags: List, worth_it: Optional[bool], user_data: Dict) -> Dict:
    """
    Preparar contexto para el chat de IA de manera simple

    Args:
        reflection_text: Texto de reflexión del usuario
        positive_tags: Lista de momentos positivos
        negative_tags: Lista de momentos negativos
        worth_it: Si el día mereció la pena
        user_data: Datos del usuario

    Returns:
        Dict: Contexto preparado para el chat
    """

    print("🔄 === PREPARANDO CONTEXTO PARA CHAT IA ===")

    # Validar entrada
    if not reflection_text and not positive_tags and not negative_tags:
        print("⚠️ No hay contenido para el chat")
        return {
            "has_content": False,
            "error": "No hay reflexión ni momentos del día para analizar"
        }

    # Contar contenido
    reflection_length = len(reflection_text) if reflection_text else 0
    positive_count = len(positive_tags) if positive_tags else 0
    negative_count = len(negative_tags) if negative_tags else 0

    print(f"📊 Contenido detectado:")
    print(f"   📝 Reflexión: {reflection_length} caracteres")
    print(f"   ➕ Momentos positivos: {positive_count}")
    print(f"   ➖ Momentos negativos: {negative_count}")
    print(f"   💭 Worth it: {worth_it}")

    # Preparar contexto
    context = {
        "has_content": True,
        "user": {
            "name": user_data.get('name', 'Usuario'),
            "id": user_data.get('id'),
        },
        "reflection": reflection_text or "",
        "positive_tags": positive_tags or [],
        "negative_tags": negative_tags or [],
        "worth_it": worth_it,
        "summary": {
            "reflection_length": reflection_length,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "total_content": reflection_length + positive_count + negative_count
        },
        "timestamp": datetime.now().isoformat()
    }

    print("✅ Contexto preparado exitosamente")
    return context

def validate_chat_ready(context: Dict) -> tuple[bool, str]:
    """
    Validar que el contexto esté listo para el chat

    Returns:
        tuple: (es_válido, mensaje_error)
    """

    if not context.get("has_content", False):
        return False, "No hay contenido del día para analizar"

    summary = context.get("summary", {})
    total_content = summary.get("total_content", 0)

    if total_content == 0:
        return False, "Necesitas escribir una reflexión o añadir momentos del día"

    # Verificar que haya algo sustancial
    reflection_length = summary.get("reflection_length", 0)
    tag_count = summary.get("positive_count", 0) + summary.get("negative_count", 0)

    if reflection_length < 10 and tag_count == 0:
        return False, "Añade más contenido para tener una conversación significativa"

    return True, "Contexto válido para chat"

def format_context_for_ai(context: Dict) -> Dict:
    """
    Formatear contexto para enviar a la IA

    Returns:
        Dict: Contexto formateado para IA
    """

    if not context.get("has_content", False):
        return {}

    # Formatear tags para la IA
    formatted_positive = []
    for tag in context.get("positive_tags", []):
        if isinstance(tag, dict):
            formatted_positive.append({
                "name": tag.get("name", ""),
                "context": tag.get("context", ""),
                "emoji": tag.get("emoji", "+")
            })
        elif hasattr(tag, 'name'):
            formatted_positive.append({
                "name": getattr(tag, 'name', ''),
                "context": getattr(tag, 'context', ''),
                "emoji": getattr(tag, 'emoji', '+')
            })

    formatted_negative = []
    for tag in context.get("negative_tags", []):
        if isinstance(tag, dict):
            formatted_negative.append({
                "name": tag.get("name", ""),
                "context": tag.get("context", ""),
                "emoji": tag.get("emoji", "-")
            })
        elif hasattr(tag, 'name'):
            formatted_negative.append({
                "name": getattr(tag, 'name', ''),
                "context": getattr(tag, 'context', ''),
                "emoji": getattr(tag, 'emoji', '-')
            })

    return {
        "reflection_text": context.get("reflection", ""),
        "positive_tags": formatted_positive,
        "negative_tags": formatted_negative,
        "worth_it": context.get("worth_it"),
        "user_name": context.get("user", {}).get("name", "Usuario")
    }

def start_ai_chat(context: Dict) -> Dict:
    """
    Iniciar chat con IA usando el contexto preparado

    Returns:
        Dict: Resultado del análisis inicial
    """

    print("🚀 === INICIANDO CHAT CON IA ===")

    try:
        # Validar contexto
        is_valid, error_message = validate_chat_ready(context)
        if not is_valid:
            return {
                "success": False,
                "error": error_message,
                "response": None
            }

        # Formatear para IA
        ai_context = format_context_for_ai(context)

        # Importar y usar la IA
        from services.mental_health_ia import analyze_daily_entry_with_ai

        print("🤖 Enviando contexto a IA...")

        ai_response = analyze_daily_entry_with_ai(
            reflection_text=ai_context["reflection_text"],
            positive_tags=ai_context["positive_tags"],
            negative_tags=ai_context["negative_tags"],
            worth_it=ai_context["worth_it"]
        )

        if not ai_response:
            raise Exception("IA devolvió respuesta vacía")

        print("✅ Respuesta de IA recibida")

        return {
            "success": True,
            "error": None,
            "response": ai_response,
            "context_used": ai_context,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Error iniciando chat con IA: {e}")
        import traceback
        traceback.print_exc()

        return {
            "success": False,
            "error": f"Error técnico: {str(e)}",
            "response": None
        }

def continue_ai_chat(conversation_history: str, user_message: str) -> Dict:
    """
    Continuar conversación con IA

    Args:
        conversation_history: Historial de la conversación
        user_message: Nuevo mensaje del usuario

    Returns:
        Dict: Resultado de la respuesta de seguimiento
    """

    print("💬 === CONTINUANDO CHAT CON IA ===")

    try:
        if not user_message.strip():
            return {
                "success": False,
                "error": "Mensaje vacío",
                "response": None
            }

        # Importar y usar la IA
        from services.mental_health_ia import continue_ai_conversation

        print("🤖 Enviando mensaje de seguimiento a IA...")

        ai_response = continue_ai_conversation(conversation_history, user_message)

        if not ai_response:
            raise Exception("IA devolvió respuesta vacía")

        print("✅ Respuesta de seguimiento recibida")

        return {
            "success": True,
            "error": None,
            "response": ai_response,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ Error continuando chat: {e}")

        return {
            "success": False,
            "error": f"Error técnico: {str(e)}",
            "response": "Me disculpo por la dificultad técnica. ¿Podrías repetir tu mensaje?"
        }

def get_chat_summary(context: Dict) -> str:
    """
    Generar resumen del contenido para mostrar al usuario

    Returns:
        str: Resumen legible del contenido
    """

    if not context.get("has_content", False):
        return "No hay contenido del día para analizar"

    summary = context.get("summary", {})

    parts = []

    # Reflexión
    reflection_length = summary.get("reflection_length", 0)
    if reflection_length > 0:
        parts.append(f"📝 Reflexión ({reflection_length} caracteres)")

    # Tags positivos
    positive_count = summary.get("positive_count", 0)
    if positive_count > 0:
        parts.append(f"➕ {positive_count} momento{'s' if positive_count != 1 else ''} positivo{'s' if positive_count != 1 else ''}")

    # Tags negativos
    negative_count = summary.get("negative_count", 0)
    if negative_count > 0:
        parts.append(f"➖ {negative_count} momento{'s' if negative_count != 1 else ''} difícil{'es' if negative_count != 1 else ''}")

    # Worth it
    worth_it = context.get("worth_it")
    if worth_it is True:
        parts.append("💚 El día mereció la pena")
    elif worth_it is False:
        parts.append("💔 El día no mereció la pena")

    if not parts:
        return "Contenido mínimo disponible"

    return " • ".join(parts)

# ============================================================================
# FUNCIONES HELPER PARA USAR DESDE ENTRY SCREEN
# ============================================================================

def prepare_entry_for_chat(reflection_text: str, positive_tags: List, negative_tags: List, worth_it: Optional[bool], user_data: Dict) -> Dict:
    """
    Función principal para preparar entrada para chat

    Esta es la función que debería llamar EntryScreen
    """
    return prepare_chat_context(reflection_text, positive_tags, negative_tags, worth_it, user_data)

def start_chat_analysis(context: Dict) -> Dict:
    """
    Función principal para iniciar análisis de chat

    Esta es la función que debería llamar AIChatScreen
    """
    return start_ai_chat(context)

# ============================================================================
# FUNCIÓN DE PRUEBA
# ============================================================================

def test_simple_integration():
    """Probar integración simple"""
    print("🧪 === PROBANDO INTEGRACIÓN SIMPLE ===")

    try:
        # Datos de prueba
        user_data = {"name": "Usuario Prueba", "id": 123}
        reflection = "Hoy fue un día interesante con altibajos"
        positive_tags = [{"name": "Ejercicio", "context": "Fui al gimnasio", "emoji": "💪"}]
        negative_tags = [{"name": "Estrés", "context": "Mucho trabajo", "emoji": "😰"}]
        worth_it = True

        # Preparar contexto
        context = prepare_entry_for_chat(reflection, positive_tags, negative_tags, worth_it, user_data)

        if not context.get("has_content", False):
            print("❌ Error preparando contexto")
            return False

        print("✅ Contexto preparado")
        print(f"📊 Resumen: {get_chat_summary(context)}")

        # Iniciar chat
        result = start_chat_analysis(context)

        if not result.get("success", False):
            print(f"❌ Error iniciando chat: {result.get('error')}")
            return False

        print("✅ Chat iniciado exitosamente")
        print(f"🤖 Respuesta IA (primeros 100 chars): {result.get('response', '')[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

if __name__ == "__main__":
    test_simple_integration()