# test_mental_health_ai.py
"""
🧪 Archivo de prueba para el Chat IA de Salud Mental
Ejecuta este archivo para probar que la IA funciona antes de integrarla
"""

import sys
import os

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_ai_connection():
    """Probar conexión básica con la IA"""
    print("🧪 === PROBANDO CONEXIÓN BÁSICA CON IA ===")

    try:
        from services.mental_health_ia import MentalHealthAI

        # Crear instancia
        ai = MentalHealthAI()
        print("✅ IA inicializada correctamente")

        return True

    except Exception as e:
        print(f"❌ Error inicializando IA: {e}")
        print("\n🔧 SOLUCIONES POSIBLES:")
        print("1. Verifica que tengas GEMINI_API_KEY en tu archivo .env")
        print("2. Instala google-generativeai: pip install google-generativeai")
        print("3. Instala python-dotenv: pip install python-dotenv")
        return False

def test_day_analysis():
    """Probar análisis de día completo"""
    print("\n🧪 === PROBANDO ANÁLISIS DE DÍA ===")

    try:
        from services.mental_health_ia import analyze_daily_entry_with_ai

        # Datos de prueba realistas
        reflection_test = """
        Hoy ha sido un día bastante intenso. Por la mañana tuve una presentación 
        importante en el trabajo que me tenía muy nervioso desde hace días. 
        Al final salió bien, pero me di cuenta de que me pongo demasiado ansioso 
        con estas cosas. Mi jefe me felicitó, lo cual me hizo sentir bien.
        
        Por la tarde mi hermana me llamó preocupada por mi papá, que ha estado 
        un poco deprimido últimamente. Eso me bajó el ánimo porque no sé cómo ayudarle.
        
        En la noche salí con amigos y me relajé un poco, pero sigo pensando en todo.
        """

        # Tags de prueba (simulando objetos DynamicTag)
        class MockTag:
            def __init__(self, name, context, emoji=""):
                self.name = name
                self.context = context
                self.emoji = emoji

        positive_tags_test = [
            MockTag("Presentación exitosa", "Mi jefe me felicitó por la presentación", "🎯"),
            MockTag("Tiempo con amigos", "Salí con amigos y me relajé", "😊")
        ]

        negative_tags_test = [
            MockTag("Ansiedad", "Me pongo muy ansioso con las presentaciones", "😰"),
            MockTag("Preocupación familiar", "Mi papá está deprimido y no sé cómo ayudarle", "😔")
        ]

        worth_it_test = True  # Sintió que el día mereció la pena

        print("📝 Enviando datos de prueba a la IA...")
        print(f"📝 Reflexión: {reflection_test[:100]}...")
        print(f"➕ Tags positivos: {len(positive_tags_test)}")
        print(f"➖ Tags negativos: {len(negative_tags_test)}")
        print(f"💭 Worth it: {worth_it_test}")

        # Analizar con IA
        ai_response = analyze_daily_entry_with_ai(
            reflection_test,
            positive_tags_test,
            negative_tags_test,
            worth_it_test
        )

        print("\n✅ === RESPUESTA DE LA IA ===")
        print(ai_response)
        print("\n✅ === FIN DE RESPUESTA ===")

        return True

    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_continuation():
    """Probar continuación de conversación"""
    print("\n🧪 === PROBANDO CONTINUACIÓN DE CONVERSACIÓN ===")

    try:
        from services.mental_health_ia import continue_ai_conversation

        # Contexto previo simulado
        previous_context = """
        La IA analizó que la persona tuvo un día con ansiedad por una presentación 
        pero que salió bien, y preocupación por su padre que está deprimido.
        """

        # Mensaje de seguimiento del usuario
        user_message = """
        Gracias por tu análisis. Me identifico mucho con lo que dices sobre la ansiedad.
        ¿Tienes algún consejo específico para manejarla antes de presentaciones importantes?
        """

        print("📝 Contexto previo:", previous_context[:100], "...")
        print("📝 Mensaje del usuario:", user_message[:100], "...")

        # Continuar conversación
        ai_followup = continue_ai_conversation(previous_context, user_message)

        print("\n✅ === RESPUESTA DE SEGUIMIENTO ===")
        print(ai_followup)
        print("\n✅ === FIN DE RESPUESTA ===")

        return True

    except Exception as e:
        print(f"❌ Error en conversación: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("🚀 === INICIANDO PRUEBAS DE IA DE SALUD MENTAL ===\n")

    # Test 1: Conexión básica
    if not test_basic_ai_connection():
        print("\n❌ Error en conexión básica. No se pueden ejecutar más pruebas.")
        return False

    # Test 2: Análisis de día
    if not test_day_analysis():
        print("\n❌ Error en análisis de día.")
        return False

    # Test 3: Continuación de conversación
    if not test_conversation_continuation():
        print("\n❌ Error en continuación de conversación.")
        return False

    print("\n🎉 === TODAS LAS PRUEBAS PASARON EXITOSAMENTE ===")
    print("✅ La IA está lista para integrarse en ReflectApp")
    return True

if __name__ == "__main__":
    print("🧠💚 Probando Mental Health AI para ReflectApp")
    print("=" * 60)

    # Verificar archivos necesarios
    if not os.path.exists('.env'):
        print("❌ No se encontró archivo .env")
        print("🔧 Crea un archivo .env con tu GEMINI_API_KEY")
        sys.exit(1)

    # Ejecutar pruebas
    success = run_all_tests()

    if success:
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ejecuta tu aplicación principal (main.py)")
        print("2. Ve a la pantalla de reflexión diaria")
        print("3. Escribe una reflexión y añade algunos tags")
        print("4. Haz click en '🤖 Chat IA'")
        print("5. ¡Disfruta tu chat con el especialista en salud mental!")
    else:
        print("\n⚠️ Revisa los errores arriba antes de continuar")