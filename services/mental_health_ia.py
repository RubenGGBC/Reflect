# services/mental_health_ai.py - VERSIÓN CORREGIDA Y SIMPLIFICADA
"""
🧠💚 Chat IA de Salud Mental - ReflectApp - VERSIÓN CORREGIDA
Experto en salud mental que analiza entradas diarias y proporciona apoyo
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class MentalHealthAI:
    """IA especializada en salud mental para ReflectApp - CORREGIDA"""

    def __init__(self):
        # Configurar Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY no encontrada en .env")

        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Mental Health AI inicializada correctamente")
        except Exception as e:
            print(f"❌ Error configurando Gemini: {e}")
            raise

    def analyze_daily_entry(self, reflection_text, positive_tags, negative_tags, worth_it):
        """
        Analizar entrada diaria completa y generar respuesta de apoyo

        Args:
            reflection_text (str): Texto libre de reflexión
            positive_tags (list): Lista de momentos positivos
            negative_tags (list): Lista de momentos negativos/difíciles
            worth_it (bool): Si el día mereció la pena

        Returns:
            str: Respuesta empática y analítica de la IA
        """

        print("🔍 === ANALIZANDO ENTRADA DIARIA ===")
        print(f"📝 Reflexión: {len(reflection_text)} caracteres")
        print(f"➕ Tags positivos: {len(positive_tags)}")
        print(f"➖ Tags negativos: {len(negative_tags)}")
        print(f"💭 Worth it: {worth_it}")

        try:
            # Validar entrada
            if not reflection_text and not positive_tags and not negative_tags:
                return self._get_empty_input_response()

            # Crear prompt especializado
            prompt = self._create_mental_health_prompt(
                reflection_text, positive_tags, negative_tags, worth_it
            )

            print("🤖 Enviando consulta a Gemini...")

            # Generar respuesta con configuración específica
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7,
                )
            )

            ai_response = response.text

            print("✅ Respuesta recibida de Gemini")
            print(f"📄 Longitud de respuesta: {len(ai_response)} caracteres")

            # Validar respuesta
            if not ai_response or len(ai_response.strip()) < 50:
                print("⚠️ Respuesta de IA muy corta, usando fallback")
                return self._get_fallback_response()

            return ai_response

        except Exception as e:
            print(f"❌ Error en análisis de IA: {e}")
            import traceback
            traceback.print_exc()
            return self._get_fallback_response()

    def _create_mental_health_prompt(self, reflection, positive_tags, negative_tags, worth_it):
        """Crear prompt especializado para análisis de salud mental - MEJORADO"""

        # Convertir tags a texto legible
        positive_text = self._tags_to_text(positive_tags, "positivos")
        negative_text = self._tags_to_text(negative_tags, "negativos")

        # Determinar estado del día
        worth_it_text = ""
        if worth_it is True:
            worth_it_text = "La persona siente que su día SÍ mereció la pena."
        elif worth_it is False:
            worth_it_text = "La persona siente que su día NO mereció la pena."
        else:
            worth_it_text = "La persona no ha decidido si su día mereció la pena."

        prompt = f"""
Eres un PSICÓLOGO CLÍNICO EXPERTO con años de experiencia ayudando a personas a procesar sus emociones y experiencias diarias. 

Tu rol es analizar la reflexión diaria de una persona y proporcionar apoyo empático, insights profundos y herramientas prácticas para su bienestar mental.

INFORMACIÓN DEL DÍA DE HOY:

=== REFLEXIÓN LIBRE ===
{reflection if reflection else "La persona no escribió una reflexión textual hoy."}

=== MOMENTOS POSITIVOS DEL DÍA ===
{positive_text}

=== MOMENTOS DIFÍCILES/NEGATIVOS DEL DÍA ===  
{negative_text}

=== EVALUACIÓN PERSONAL DEL DÍA ===
{worth_it_text}

INSTRUCCIONES ESPECÍFICAS:

1. **SÉ CÁLIDO Y EMPÁTICO**: Usa un tono comprensivo y profesional, nunca juzgues
2. **ANALIZA PROFUNDAMENTE**: Identifica patrones emocionales, conexiones entre eventos
3. **SÉ ESPECÍFICO**: Refiérete a elementos concretos de su día, no generalidades
4. **VALIDA EMOCIONES**: Reconoce que todos los sentimientos son válidos
5. **OFRECE HERRAMIENTAS**: Proporciona técnicas prácticas cuando sea apropiado
6. **HAZ PREGUNTAS**: Si necesitas más claridad, pregunta específicamente

ESTRUCTURA DE TU RESPUESTA:
1. **Reconocimiento empático** de cómo se sintió
2. **Análisis de patrones** que observas en su día
3. **Validación** de sus experiencias
4. **Herramientas prácticas** si es apropiado
5. **Pregunta específica** para profundizar

EJEMPLO DE INICIO:
"Veo que has tenido un día con experiencias variadas. Me llama la atención que..."

IMPORTANTE:
- NO hagas diagnósticos médicos
- NO recomiende medicamentos
- NO juzgues sus decisiones
- SÍ sé específico sobre su día
- SÍ ofrece técnicas de bienestar mental
- Responde en ESPAÑOL con empatía profesional

LONGITUD: Entre 200-400 palabras para ser útil pero no abrumador.

RESPUESTA:
"""

        return prompt

    def _tags_to_text(self, tags, tipo):
        """Convertir lista de tags a texto legible - MEJORADO"""
        if not tags:
            return f"No registró momentos {tipo} específicos para hoy."

        texto_tags = []
        for i, tag in enumerate(tags, 1):
            try:
                if hasattr(tag, 'name') and hasattr(tag, 'context'):
                    # Es un objeto DynamicTag
                    emoji = getattr(tag, 'emoji', '•')
                    nombre = tag.name
                    contexto = tag.context
                elif isinstance(tag, dict):
                    # Es un diccionario
                    emoji = tag.get('emoji', '•')
                    nombre = tag.get('name', 'Sin nombre')
                    contexto = tag.get('context', 'Sin descripción')
                else:
                    # Es otra cosa, convertir a string
                    emoji = '•'
                    nombre = str(tag)
                    contexto = "Sin detalles adicionales"

                texto_tags.append(f"   {i}. {emoji} {nombre}: {contexto}")

            except Exception as e:
                print(f"⚠️ Error procesando tag: {e}")
                texto_tags.append(f"   {i}. • Tag no procesable")

        return "\n".join(texto_tags)

    def _get_empty_input_response(self):
        """Respuesta cuando no hay entrada"""
        return """🌸 Hola, veo que aún no has compartido mucho sobre tu día de hoy.

Está perfectamente bien si no tienes ganas de escribir mucho, o si ha sido un día tranquilo sin eventos particulares. 

¿Te gustaría contarme algo específico sobre cómo te has sentido hoy? Puede ser algo muy simple, como:
- ¿Cómo fue tu estado de ánimo general?
- ¿Hubo algún momento que te hizo sonreír?
- ¿Algo te preocupó o te hizo sentir incómodo/a?

No hay presión - estoy aquí para escucharte cuando estés listo/a para compartir. 💚"""

    def _get_fallback_response(self):
        """Respuesta de respaldo en caso de error - MEJORADA"""
        return """🌸 Me disculpo, pero he tenido una dificultad técnica analizando tu día en detalle. 

Sin embargo, quiero reconocer algo importante: el simple hecho de que hayas tomado tiempo para reflexionar sobre tu día demuestra tu compromiso con tu bienestar emocional. Eso ya es valioso.

💚 Algunas reflexiones generales que podrían ayudarte:

• **Autocompasión**: Sé amable contigo mismo/a, especialmente en los días difíciles
• **Perspectiva**: Tanto los momentos positivos como los desafiantes forman parte del crecimiento
• **Conexión**: Considera hablar con alguien de confianza si sientes que lo necesitas

¿Hay algo específico de tu día sobre lo que te gustaría hablar? Estoy aquí para escucharte, incluso si mi análisis automático no funcionó perfectamente.

🌱 Recuerda: cada día que reflexionas es un día de crecimiento."""

    def continue_conversation(self, previous_context, user_message):
        """
        Continuar conversación con contexto previo - CORREGIDO

        Args:
            previous_context (str): Contexto de la conversación anterior
            user_message (str): Nuevo mensaje del usuario

        Returns:
            str: Respuesta de seguimiento de la IA
        """

        print("💬 === CONTINUANDO CONVERSACIÓN ===")
        print(f"💭 Mensaje del usuario: {user_message[:100]}...")

        try:
            # Validar entrada
            if not user_message.strip():
                return "Me gustaría escuchar lo que tienes que decir. ¿Puedes contarme un poco más?"

            prompt = f"""
Eres un psicólogo clínico experto continuando una conversación con una persona sobre su bienestar mental y emocional.

CONTEXTO PREVIO DE LA CONVERSACIÓN:
{previous_context[:800]}...

NUEVO MENSAJE DE LA PERSONA:
"{user_message}"

INSTRUCCIONES:
- Responde de manera empática y profesional
- Haz referencia al contexto previo cuando sea relevante
- Proporciona apoyo específico basado en su nuevo mensaje
- Puedes hacer preguntas de seguimiento si es apropiado
- Ofrece técnicas o herramientas prácticas si viene al caso
- Valida sus emociones y experiencias

IMPORTANTE:
- Mantén un tono cálido pero profesional
- No hagas diagnósticos médicos
- Enfócate en su bienestar y crecimiento personal
- Si detectas alguna crisis, sugiere buscar ayuda profesional presencial

Responde en español, entre 150-300 palabras:
"""

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=800,
                    temperature=0.7,
                )
            )

            ai_response = response.text

            if not ai_response or len(ai_response.strip()) < 30:
                return self._get_conversation_fallback()

            return ai_response

        except Exception as e:
            print(f"❌ Error en conversación continua: {e}")
            return self._get_conversation_fallback()

    def _get_conversation_fallback(self):
        """Respuesta de fallback para conversación"""
        return """Me disculpo, pero he tenido una dificultad técnica procesando tu mensaje. 

Sin embargo, quiero que sepas que valoro mucho que estés compartiendo conmigo. 

¿Podrías repetir lo que me querías decir? Me gustaría poder ayudarte y apoyarte de la mejor manera posible.

💚 Estoy aquí para escucharte."""

# ============================================================================
# FUNCIONES PRINCIPALES PARA USAR DESDE OTROS MÓDULOS - CORREGIDAS
# ============================================================================

def analyze_daily_entry_with_ai(reflection_text, positive_tags, negative_tags, worth_it):
    """
    Función helper para analizar entrada diaria con IA - CORREGIDA

    Returns:
        str: Análisis de salud mental de la IA
    """
    try:
        print("🚀 Iniciando análisis con Mental Health AI...")
        ai = MentalHealthAI()
        result = ai.analyze_daily_entry(reflection_text, positive_tags, negative_tags, worth_it)
        print("✅ Análisis completado exitosamente")
        return result
    except Exception as e:
        print(f"❌ Error creando MentalHealthAI: {e}")
        return """Lo siento, el servicio de IA no está disponible en este momento. 

Sin embargo, tu reflexión es valiosa. El simple hecho de tomarte tiempo para pensar en tu día es un acto de autocuidado.

💚 Considera seguir reflexionando por tu cuenta o compartir tus pensamientos con alguien de confianza."""

def continue_ai_conversation(previous_context, user_message):
    """
    Función helper para continuar conversación con IA - CORREGIDA

    Returns:
        str: Respuesta de seguimiento de la IA
    """
    try:
        print("🚀 Continuando conversación con Mental Health AI...")
        ai = MentalHealthAI()
        result = ai.continue_conversation(previous_context, user_message)
        print("✅ Respuesta de conversación generada")
        return result
    except Exception as e:
        print(f"❌ Error en conversación de IA: {e}")
        return """Me disculpo por la dificultad técnica. 

¿Podrías repetir tu mensaje? Me gustaría poder ayudarte mejor.

💚 Tu bienestar es importante para mí."""

# ============================================================================
# FUNCIÓN DE PRUEBA PARA VERIFICAR QUE TODO FUNCIONA
# ============================================================================

def test_mental_health_ai():
    """Función de prueba para verificar que la IA funciona"""
    print("🧪 === PROBANDO MENTAL HEALTH AI ===")

    try:
        # Datos de prueba
        reflection = "Hoy fue un día difícil en el trabajo pero mi familia me apoyó"
        positive_tags = [{"name": "Apoyo familiar", "context": "Mi familia me consoló", "emoji": "💝"}]
        negative_tags = [{"name": "Estrés laboral", "context": "Mucha presión en el trabajo", "emoji": "😰"}]
        worth_it = True

        # Probar análisis
        result = analyze_daily_entry_with_ai(reflection, positive_tags, negative_tags, worth_it)
        print(f"✅ Resultado: {result[:100]}...")

        # Probar conversación
        conversation_result = continue_ai_conversation(result, "Gracias, ¿tienes algún consejo?")
        print(f"✅ Conversación: {conversation_result[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar prueba si se ejecuta directamente
    test_mental_health_ai()