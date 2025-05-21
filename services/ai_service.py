"""
Servicio de integración con IA para análisis de entradas.
Actualmente usa versiones simuladas para desarrollo.
"""

def analyze_mock(text):
    """
    Versión simulada del análisis de sentimiento e insights
    para desarrollo y pruebas.
    
    Args:
        text (str): Texto de entrada del usuario
        
    Returns:
        tuple: (sentimiento, insights)
    """
    # Análisis de sentimiento simulado
    sentiment = "positivo"
    if any(word in text.lower() for word in ["triste", "mal", "difícil", "problema", "preocupado"]):
        sentiment = "negativo"
    elif all(word not in text.lower() for word in ["feliz", "bueno", "bien", "alegre", "éxito", "logro"]):
        sentiment = "neutro"

    # Generación de insights simulados
    insights = ""
    if sentiment == "positivo":
        insights = """- Parece que hoy tuviste un buen día que contribuyó a tu bienestar emocional
- Tu lenguaje positivo sugiere que estás enfrentando bien los desafíos
- Considera reflexionar sobre qué hizo que este día fuera especial"""
    elif sentiment == "negativo":
        insights = """- Reconocer tus emociones es el primer paso para procesarlas
- Considera qué aspectos específicos te afectaron y si puedes influir en ellos
- Recuerda que los días difíciles también ofrecen oportunidades de aprendizaje"""
    else:
        insights = """- Tu entrada es relativamente neutral en tono
- Podrías beneficiarte de explorar más tus emociones específicas
- Intenta identificar momentos destacados y desafíos de tu día"""

    return sentiment, insights