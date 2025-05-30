# services/mental_health_ai.py
"""
🧠💚 Chat IA de Salud Mental - ReflectApp
Experto en salud mental que analiza entradas diarias y proporciona apoyo
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class MentalHealthAI:
    """IA especializada en salud mental para ReflectApp"""

    def __init__(self):
        # Configurar Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en .env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        print("🧠 Mental Health AI inicializada correctamente")

    def analyze_daily_entry(self, reflection_text, positive_tags, negative_tags, worth_it):
        """
        Analizar entrada diaria completa y generar respuesta de apoyo

        Args:
            reflection_text (str): Texto libre de reflexión
            positive_tags (list): Lista de momentos positivos
            negative_tags (list): Lista de momentos negativos
            worth_it (bool): Si el día mereció la pena

        Returns:
            str: Respuesta empática y analítica de la IA
        """

        print("🔍 === ANALIZANDO ENTRADA DIARIA ===")
        print(f"📝 Reflexión: {reflection_text[:100]}...")
        print(f"➕ Tags positivos: {len(positive_tags)}")
        print(f"➖ Tags negativos: {len(negative_tags)}")
        print(f"💭 Worth it: {worth_it}")

        try:
            # Crear prompt especializado
            prompt = self._create_mental_health_prompt(
                reflection_text, positive_tags, negative_tags, worth_it
            )

            print("🤖 Enviando consulta a Gemini...")

            # Generar respuesta
            response = self.model.generate_content(prompt)
            ai_response = response.text

            print("✅ Respuesta recibida de Gemini")
            print(f"📄 Longitud de respuesta: {len(ai_response)} caracteres")

            return ai_response

        except Exception as e:
            print(f"❌ Error en análisis de IA: {e}")
            return self._get_fallback_response()

    def _create_mental_health_prompt(self, reflection, positive_tags, negative_tags, worth_it):
        """Crear prompt especializado para análisis de salud mental"""

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
Eres un EXPERTO EN SALUD MENTAL con años de experiencia ayudando a personas a procesar sus emociones y experiencias diarias. Tu rol es analizar la entrada de reflexión diaria de una persona y proporcionar apoyo empático, insights profundos y herramientas prácticas.

INFORMACIÓN DE HOY:

=== REFLEXIÓN LIBRE ===
{reflection if reflection else "No hay reflexión escrita para hoy."}

=== MOMENTOS POSITIVOS ===
{positive_text}

=== MOMENTOS NEGATIVOS ===  
{negative_text}

=== EVALUACIÓN DEL DÍA ===
{worth_it_text}

INSTRUCCIONES IMPORTANTES:
1. **SÉ EMPÁTICO Y CÁLIDO**: Usa un tono comprensivo, nunca juzgues
2. **ANALIZA PROFUNDAMENTE**: Identifica patrones, emociones subyacentes, y conexiones entre diferentes aspectos
3. **PREGUNTA SI TIENES DUDAS**: Si algo no está claro o necesitas más contexto, pregunta específicamente
4. **PROPORCIONA HERRAMIENTAS**: Ofrece técnicas prácticas de bienestar mental cuando sea apropiado
5. **VALIDA LAS EMOCIONES**: Reconoce que todos los sentimientos son válidos
6. **SÉ ESPECÍFICO**: Refiérete a elementos concretos de su día, no hables en generalidades

ESTRUCTURA DE TU RESPUESTA:
1. **Reconocimiento empático** de cómo se sintió la persona
2. **Análisis profundo** de los patrones y temas que observas
3. **Validación** de sus experiencias y emociones
4. **Herramientas o sugerencias** prácticas si es apropiado
5. **Preguntas específicas** si necesitas más claridad sobre algo

EJEMPLO DE TONO:
"Veo que has tenido un día con altibajos interesantes. Me llama la atención que..."

NO hagas:
- Diagnósticos médicos
- Recomendaciones de medicamentos
- Juicios sobre las decisiones de la persona
- Respuestas genéricas o frías

RESPONDE EN ESPAÑOL, con empatía y profundidad profesional:
"""

        return prompt

    def _tags_to_text(self, tags, tipo):
        """Convertir lista de tags a texto legible"""
        if not tags:
            return f"No hay momentos {tipo} registrados para hoy."

        texto_tags = []
        for i, tag in enumerate(tags, 1):
            if hasattr(tag, 'name') and hasattr(tag, 'context'):
                # Es un objeto DynamicTag
                emoji = getattr(tag, 'emoji', '•')
                texto_tags.append(f"{i}. {emoji} {tag.name}: {tag.context}")
            elif isinstance(tag, dict):
                # Es un diccionario
                emoji = tag.get('emoji', '•')
                name = tag.get('name', 'Sin nombre')
                context = tag.get('context', 'Sin contexto')
                texto_tags.append(f"{i}. {emoji} {name}: {context}")
            else:
                # Es otra cosa, convertir a string
                texto_tags.append(f"{i}. {str(tag)}")

        return "\n".join(texto_tags)

    def _get_fallback_response(self):
        """Respuesta de respaldo en caso de error"""
        return """🌸 Me disculpo, pero he tenido una dificultad técnica analizando tu día. 
        
Sin embargo, quiero que sepas que el simple hecho de que hayas tomado tiempo para reflexionar sobre tu día es valioso. La autoobservación es el primer paso hacia el bienestar emocional.

¿Te gustaría contarme algo específico sobre cómo te has sentido hoy? Estoy aquí para escucharte.

💚 Recuerda: cada día es una oportunidad de crecimiento, y tus sentimientos siempre son válidos."""

    def continue_conversation(self, previous_context, user_message):
        """
        Continuar conversación con contexto previo

        Args:
            previous_context (str): Contexto de la conversación anterior
            user_message (str): Nuevo mensaje del usuario

        Returns:
            str: Respuesta de seguimiento de la IA
        """

        print("💬 === CONTINUANDO CONVERSACIÓN ===")
        print(f"💭 Mensaje del usuario: {user_message}")

        try:
            prompt = f"""
Eres un experto en salud mental continuando una conversación con una persona sobre su día.

CONTEXTO PREVIO:
{previous_context}

NUEVO MENSAJE DE LA PERSONA:
{user_message}

Responde de manera empática, profunda y personalizada. Haz referencia al contexto previo y proporciona apoyo específico basado en lo que la persona acaba de compartir.

Si es apropiado, puedes:
- Hacer preguntas de seguimiento
- Ofrecer técnicas de bienestar específicas
- Validar sus emociones
- Ayudar a procesar lo que está sintiendo

Mantén un tono cálido y profesional. Responde en español:
"""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(f"❌ Error en conversación continua: {e}")
            return "Me disculpo, pero he tenido una dificultad técnica. ¿Podrías repetir lo que me querías decir? Estoy aquí para escucharte."

# Función principal para usar desde otros módulos
def analyze_daily_entry_with_ai(reflection_text, positive_tags, negative_tags, worth_it):
    """
    Función helper para analizar entrada diaria con IA

    Returns:
        str: Análisis de salud mental de la IA
    """
    try:
        ai = MentalHealthAI()
        return ai.analyze_daily_entry(reflection_text, positive_tags, negative_tags, worth_it)
    except Exception as e:
        print(f"❌ Error creando MentalHealthAI: {e}")
        return "Lo siento, el servicio de IA no está disponible en este momento. Tu reflexión es igualmente valiosa. 💚"

# Función para continuar conversación
def continue_ai_conversation(previous_context, user_message):
    """
    Función helper para continuar conversación con IA

    Returns:
        str: Respuesta de seguimiento de la IA
    """
    try:
        ai = MentalHealthAI()
        return ai.continue_conversation(previous_context, user_message)
    except Exception as e:
        print(f"❌ Error en conversación de IA: {e}")
        return "Me disculpo por la dificultad técnica. ¿Podrías repetir tu mensaje? 💚"