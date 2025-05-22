"""
🧠 Servicio de IA Zen para ReflectApp
Proporciona análisis específico de tags y resúmenes diarios contemplativos
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

class ZenAIService:
    """Servicio de IA con personalidad zen y contemplativa"""

    def __init__(self):
        # Patrones de análisis por tipo de tag
        self.positive_patterns = {
            "trabajo": {
                "keywords": ["trabajo", "oficina", "proyecto", "reunión", "logro", "éxito", "ascenso", "equipo"],
                "insights": [
                    "🌟 Tu energía profesional está en un buen momento. Aprovecha esta motivación.",
                    "💼 Es hermoso ver cómo encuentras satisfacción en tu trabajo. Esto alimenta tu crecimiento.",
                    "✨ Tu dedicación profesional está dando frutos. Celebra estos momentos.",
                    "🎯 Cuando el trabajo fluye, todo en la vida se siente más alineado."
                ]
            },
            "relaciones": {
                "keywords": ["familia", "amigos", "pareja", "amor", "conexión", "apoyo", "compartir"],
                "insights": [
                    "💕 Las conexiones humanas que nutres son tu mayor tesoro.",
                    "🤗 Es precioso ver cómo valoras tus relaciones. Esto habla de tu corazón generoso.",
                    "👥 Los momentos compartidos que describes alimentan tu alma.",
                    "💫 Tu capacidad de conectar con otros es un regalo tanto para ti como para ellos."
                ]
            },
            "personal": {
                "keywords": ["yo", "logré", "aprendí", "crecí", "reflexión", "paz", "equilibrio"],
                "insights": [
                    "🌱 Tu crecimiento personal es evidente en estas palabras. Sigue cultivándote.",
                    "✨ Es hermoso verte florecer. Cada pequeño paso cuenta.",
                    "🧘‍♀️ Tu capacidad de autorreflexión es una fortaleza increíble.",
                    "🌸 Los momentos de conexión contigo mismo son sagrados."
                ]
            }
        }

        self.growth_patterns = {
            "trabajo": {
                "keywords": ["estrés", "presión", "conflicto", "frustración", "cansancio", "sobrecarga"],
                "advice": [
                    "🌱 Los desafíos laborales son oportunidades disfrazadas. ¿Qué te está enseñando esta situación?",
                    "💼 Considera tomar pequeños descansos durante el día para reconectar contigo mismo.",
                    "🧘 Antes de reaccionar, respira profundo. Tu bienestar es más importante que cualquier deadline.",
                    "📝 Documenta tus logros. A veces olvidamos cuánto hemos crecido.",
                    "🤝 ¿Hay alguien en tu equipo con quien puedas hablar sobre esto?"
                ]
            },
            "emocional": {
                "keywords": ["triste", "ansioso", "solo", "abrumado", "confundido", "perdido"],
                "advice": [
                    "🌊 Las emociones fluyen como las olas. Esta sensación también pasará.",
                    "💙 Ser compasivo contigo mismo es el primer paso hacia la sanación.",
                    "🌱 Los momentos difíciles nos enseñan sobre nuestra propia resistencia.",
                    "🤗 Date permiso para sentir sin juzgarte. Eres humano.",
                    "🌟 Mañana será un nuevo día, con nuevas posibilidades."
                ]
            },
            "salud": {
                "keywords": ["cansado", "enfermo", "dolor", "agotado", "sin energía"],
                "advice": [
                    "🌿 Tu cuerpo te está enviando un mensaje. Escúchalo con amor.",
                    "💚 Pequeños actos de autocuidado pueden marcar una gran diferencia.",
                    "🛌 El descanso no es un lujo, es una necesidad. Date permiso para parar.",
                    "🥗 Nutrir tu cuerpo es nutrir tu espíritu. ¿Qué necesitas hoy?",
                    "🚶‍♀️ A veces un paseo corto puede cambiar completamente tu energía."
                ]
            }
        }

        # Frases contemplativas para resúmenes
        self.contemplative_phrases = [
            "Cada día es una página nueva en tu historia personal",
            "La reflexión es el puente entre la experiencia y la sabiduría",
            "En la quietud de la contemplación encontramos claridad",
            "Cada momento difícil es una invitación al crecimiento",
            "La gratitud transforma lo ordinario en extraordinario",
            "Tu viaje interior es tan importante como cualquier destino externo"
        ]

def analyze_tag(tag_name: str, context: str, tag_type: str) -> str:
    """
    Analizar un tag específico y proporcionar consejo personalizado

    Args:
        tag_name: Nombre del tag (ej: "Trabajo")
        context: Contexto específico de lo que pasó
        tag_type: "positive" o "growth"

    Returns:
        String con consejo personalizado de la IA
    """

    ai = ZenAIService()
    context_lower = context.lower()
    tag_lower = tag_name.lower()

    if tag_type == "positive":
        return _generate_positive_insight(ai, tag_lower, context_lower)
    else:
        return _generate_growth_advice(ai, tag_lower, context_lower)

def _generate_positive_insight(ai: ZenAIService, tag_name: str, context: str) -> str:
    """Generar insight para momento positivo"""

    # Detectar categoría
    category = "personal"  # default
    for cat, pattern in ai.positive_patterns.items():
        if any(keyword in context or keyword in tag_name for keyword in pattern["keywords"]):
            category = cat
            break

    # Seleccionar insight base
    insights = ai.positive_patterns[category]["insights"]
    base_insight = random.choice(insights)

    # Personalizar según el contexto
    if "logré" in context or "conseguí" in context:
        personalization = "\n\n🎉 Es maravilloso celebrar tus logros. Este éxito es fruto de tu dedicación."
    elif "compartí" in context or "junto" in context:
        personalization = "\n\n🤝 Los momentos compartidos crean recuerdos que perduran. Qué hermoso."
    elif "aprendí" in context or "descubrí" in context:
        personalization = "\n\n📚 Cada aprendizaje te acerca más a quien estás destinado a ser."
    else:
        personalization = "\n\n💫 Guarda este momento en tu corazón. Los días luminosos nos sostienen en los oscuros."

    return base_insight + personalization

def _generate_growth_advice(ai: ZenAIService, tag_name: str, context: str) -> str:
    """Generar consejo para área de crecimiento"""

    # Detectar categoría de desafío
    category = "emocional"  # default
    for cat, pattern in ai.growth_patterns.items():
        if any(keyword in context or keyword in tag_name for keyword in pattern["keywords"]):
            category = cat
            break

    # Seleccionar consejo base
    advice_list = ai.growth_patterns[category]["advice"]
    base_advice = random.choice(advice_list)

    # Añadir pregunta reflexiva específica
    if category == "trabajo":
        reflection = "\n\n🤔 Pregúntate: ¿Qué puedes controlar en esta situación? Enfócate en eso."
    elif category == "emocional":
        reflection = "\n\n💭 Reflexiona: ¿Qué necesita tu corazón en este momento?"
    elif category == "salud":
        reflection = "\n\n🌱 Considera: ¿Qué pequeño paso puedes dar hoy para cuidarte mejor?"
    else:
        reflection = "\n\n✨ Recuerda: Los desafíos son maestros disfrazados. ¿Qué te está enseñando esto?"

    return base_advice + reflection

def get_daily_summary(reflection: str, positive_tags: List, growth_tags: List, worth_it: Optional[bool]) -> str:
    """
    Generar resumen contemplativo del día completo

    Args:
        reflection: Texto de reflexión libre
        positive_tags: Lista de tags positivos
        growth_tags: Lista de tags de crecimiento
        worth_it: Si el día mereció la pena (True/False/None)

    Returns:
        Resumen contemplativo personalizado
    """

    ai = ZenAIService()

    # Analizar el tono general
    word_count = len(reflection.split())
    positive_words = ["bien", "feliz", "logré", "disfruté", "amor", "alegre", "éxito", "genial"]
    growth_words = ["difícil", "problema", "estrés", "cansado", "frustrado", "preocupado"]

    positive_count = sum(1 for word in positive_words if word in reflection.lower())
    growth_count = sum(1 for word in growth_words if word in reflection.lower())

    # Construir resumen
    summary_parts = []

    # Apertura contemplativa
    opening = random.choice(ai.contemplative_phrases)
    summary_parts.append(f"🌸 {opening}.")

    # Análisis de la reflexión
    if word_count > 50:
        summary_parts.append("\n\n📝 Veo que te has tomado tiempo para reflexionar profundamente. Esto habla de tu sabiduría interior.")
    elif word_count < 20:
        summary_parts.append("\n\n💭 A veces las reflexiones más breves contienen las verdades más profundas.")

    # Análisis de los tags
    if positive_tags and growth_tags:
        summary_parts.append(f"\n\n⚖️ Has identificado {len(positive_tags)} momentos luminosos y {len(growth_tags)} áreas de crecimiento. Esta consciencia equilibrada es el corazón de la sabiduría.")
    elif positive_tags:
        summary_parts.append(f"\n\n✨ Has reconocido {len(positive_tags)} momentos positivos. Celebrar lo bueno alimenta tu alma.")
    elif growth_tags:
        summary_parts.append(f"\n\n🌱 Has identificado {len(growth_tags)} áreas de crecimiento. Tu honestidad contigo mismo es valiente.")

    # Análisis del "worth_it"
    if worth_it is True:
        summary_parts.append("\n\n🙏 Sientes que tu día ha merecido la pena. Esta gratitud es un regalo que te das a ti mismo.")
    elif worth_it is False:
        summary_parts.append("\n\n🌊 Sientes que el día no ha merecido la pena, y está bien. Algunos días son para aprender, no para brillar.")
    else:
        summary_parts.append("\n\n🤔 Aún no has decidido si el día mereció la pena. A veces la respuesta viene con el tiempo.")

    # Mensaje específico según el balance
    if positive_count > growth_count:
        insight = "\n\n🌟 Tu día parece haber estado lleno de luz. Lleva esta energía contigo como un faro interior."
    elif growth_count > positive_count:
        insight = "\n\n🌱 Has enfrentado desafíos hoy. Cada dificultad es una semilla de fortaleza que crece en tu interior."
    else:
        insight = "\n\n⚖️ Tu día ha tenido luces y sombras, como todos los días hermosos de una vida auténtica."

    summary_parts.append(insight)

    # Cierre contemplativo
    closing = "\n\n💫 Recuerda: cada día que reflexionas sobre tu experiencia es un día de crecimiento. Estás exactamente donde necesitas estar."
    summary_parts.append(closing)

    return "".join(summary_parts)

def get_mood_score(reflection: str, positive_tags: List, growth_tags: List, worth_it: Optional[bool]) -> int:
    """
    Calcular puntuación de ánimo del 1-10 basada en el día completo

    Returns:
        Puntuación del 1 (muy bajo) al 10 (excelente)
    """

    base_score = 5.0  # Neutral

    # Análisis del texto libre
    positive_words = ["bien", "feliz", "logré", "disfruté", "amor", "alegre", "éxito", "genial", "maravilloso"]
    negative_words = ["mal", "triste", "difícil", "problema", "estrés", "cansado", "frustrado", "preocupado"]

    text_lower = reflection.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    # Ajustar por contenido del texto
    if positive_count > negative_count:
        base_score += 1.5
    elif negative_count > positive_count:
        base_score -= 1.5

    # Ajustar por balance de tags
    positive_tag_count = len(positive_tags)
    growth_tag_count = len(growth_tags)

    if positive_tag_count > growth_tag_count:
        base_score += 1.0
    elif growth_tag_count > positive_tag_count:
        base_score -= 0.5

    # Ajustar por "worth_it"
    if worth_it is True:
        base_score += 1.5
    elif worth_it is False:
        base_score -= 1.0

    # Bonus por reflexión profunda
    if len(reflection.split()) > 50:
        base_score += 0.5

    # Asegurar rango 1-10
    final_score = max(1, min(10, round(base_score)))
    return final_score

def get_zen_quote() -> str:
    """Obtener una cita zen aleatoria"""
    quotes = [
        "🌸 'La paz viene de dentro. No la busques fuera.' - Buda",
        "🧘‍♀️ 'Ayer es historia, mañana es un misterio, hoy es un regalo.'",
        "🌱 'El río que sobrevive es el que se adapta al terreno.'",
        "✨ 'No camines delante de mí, puede que no te siga. No camines detrás de mí, puede que no te guíe. Camina junto a mí y sé mi amigo.'",
        "🌊 'En la calma del agua reflejamos mejor la luna.'",
        "🎋 'El bambú que se dobla es más fuerte que el roble que se quiebra.'",
        "🌺 'Cada flor debe pasar por tierra antes de florecer.'",
        "🕊️ 'La libertad no se da, se toma con consciencia.'"
    ]
    return random.choice(quotes)

# Funciones principales exportadas
__all__ = [
    'analyze_tag',
    'get_daily_summary',
    'get_mood_score',
    'get_zen_quote'
]