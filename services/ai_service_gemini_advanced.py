
import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class AdvancedGeminiService:
    def __init__(self):
        # Configurar Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en .env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

        # Patrones de crisis mejorados
        self.crisis_patterns = {
            "suicidio_directo": ["suicidio", "matarme", "quitarme la vida", "no quiero vivir", "terminar con todo"],
            "suicidio_indirecto": ["ya no puedo más", "no vale la pena", "mejor desaparecer", "nadie me va a extrañar"],
            "autolesion": ["cortarme", "hacerme daño", "lastimahme", "autolesión", "dolor físico"],
            "desesperanza": ["sin esperanza", "no hay salida", "todo está perdido", "sin futuro", "sin sentido"],
            "aislamiento_extremo": ["nadie me entiende", "completamente solo", "todos me abandonaron"],
            "crisis_familiar": ["divorcio", "violencia doméstica", "abuso", "maltrato", "agresión"],
            "crisis_laboral": ["despido", "acoso laboral", "mobbing", "sin trabajo", "quiebra"],
            "adicciones": ["alcohol", "drogas", "ludopatía", "adicción", "dependencia"],
            "salud_mental": ["depresión severa", "crisis de ansiedad", "ataque de pánico", "trastorno"]
        }

    def crear_prompt_personas_avanzado(self, texto):
        """Prompt súper inteligente para análisis de relaciones y crisis"""
        return f"""
Eres un EXPERTO PSICÓLOGO CLÍNICO especializado en análisis de reflexiones personales y detección de crisis de salud mental.

ANALIZA PROFUNDAMENTE este texto buscando:
1. TODAS las personas mencionadas (incluye apodos, diminutivos, referencias indirectas)
2. Patrones de relaciones tóxicas vs saludables
3. Indicadores de crisis mental o situaciones de riesgo
4. Cambios emocionales hacia las personas
5. Dinámicas familiares disfuncionales
6. Redes de apoyo vs aislamiento

TEXTO A ANALIZAR: "{texto}"

RESPONDE ÚNICAMENTE CON JSON VÁLIDO:
{{
    "personas": [
        {{
            "nombre": "Ana" o null,
            "mote_apodo": "Anita" o null,
            "referencia_indirecta": "la rubia" o null,
            "relacion": "hermana",
            "tipo": "familia",
            "subtipo": "hermana_mayor" o null,
            "sentimiento_hacia_persona": "positivo",
            "intensidad_sentimiento": 0.8,
            "sentimiento_cambio": "mejorando" o "empeorando" o "estable",
            "contexto_completo": "mi hermana Ana me ayudó cuando estaba mal",
            "rol_en_la_situacion": "apoyo" o "conflicto" o "neutro" o "desencadenante",
            "patron_relacion": "apoyo_incondicional" o "dependencia_emocional" o "relacion_toxica" o "distanciamiento",
            "indicadores_toxicidad": ["manipulation", "control"] o [],
            "confianza": 0.9,
            "dudas": "ninguna" o "podría ser amiga, no hermana",
            "genero_probable": "femenino" o "masculino" o "indefinido",
            "frecuencia_mencion": "primera_vez" o "recurrente",
            "impacto_emocional": "muy_alto" o "alto" o "medio" o "bajo"
        }}
    ],
    "analisis_relaciones": {{
        "red_apoyo_fuerte": true o false,
        "relaciones_toxicas_detectadas": true o false,
        "aislamiento_social": "alto" o "medio" o "bajo",
        "dependencia_emocional": true o false,
        "conflictos_familiares": true o false,
        "dinamica_pareja": "saludable" o "toxica" o "ausente" o "complicada"
    }},
    "indicadores_crisis": {{
        "nivel_riesgo": "critico" o "alto" o "moderado" o "bajo" o "ninguno",
        "tipo_crisis": ["suicidio", "autolesion", "depresion_severa"] o [],
        "palabras_criticas_exactas": ["suicidio", "no puedo más"] o [],
        "contexto_crisis": "descripción del contexto específico" o null,
        "factores_protectores": ["familia_de_apoyo", "tratamiento_psicologico"] o [],
        "factores_riesgo": ["aislamiento", "perdida_trabajo"] o [],
        "urgencia_intervencion": "inmediata" o "pronta" o "seguimiento" o "ninguna"
    }},
    "patrones_emocionales": {{
        "tono_general": "muy_positivo" o "positivo" o "neutro" o "negativo" o "muy_negativo",
        "estabilidad_emocional": "estable" o "labil" o "crisis",
        "mecanismos_afrontamiento": ["busca_apoyo", "aislamiento", "negacion"] o [],
        "insight_personal": "alto" o "medio" o "bajo",
        "capacidad_expresion": "muy_buena" o "buena" o "limitada" o "bloqueada"
    }},
    "recomendaciones_inmediatas": {{
        "necesita_seguimiento": true o false,
        "derivacion_profesional": "urgente" o "recomendada" o "opcional" o "innecesaria",
        "tipo_intervencion": ["psicologia_clinica", "psiquiatria", "terapia_familiar"] o [],
        "acciones_preventivas": ["fortalecer_red_apoyo", "tecnicas_afrontamiento"] o []
    }},
    "slang_detectado": {{
        "expresiones": ["bro", "vieja", "mi loco"] o [],
        "traduccion_formal": ["hermano", "madre", "mi amigo"] o []
    }},
    "contexto_cultural": {{
        "region_probable": "españa" o "mexico" o "argentina" o "otro" o "indefinido",
        "nivel_formalidad": "muy_formal" o "formal" o "coloquial" o "muy_coloquial",
        "edad_probable": "adolescente" o "joven_adulto" o "adulto" o "indefinido"
    }}
}}

REGLAS MEJORADAS:

TIPOS DE RELACIÓN EXPANDIDOS:
- "familia": hermana/o, mamá/papá, primo/a, tío/a, abuelo/a, suegro/a, cuñado/a, hijo/a
- "amistad": amigo/a, bro, sis, mejo, pana, compa, colega, compañero/a
- "pareja": novio/a, esposo/a, marido, mujer, ex, ligue, rollo, crush
- "trabajo": jefe/a, compañero/a, cliente, profesor/a, alumno/a, socio/a
- "profesional": médico/a, psicólogo/a, terapeuta, abogado/a, coach
- "otro": vecino/a, conocido/a, desconocido/a

DETECCIÓN DE SLANG Y APODOS:
- "viejo/a" → padre/madre en contexto familiar
- "bro" → hermano o amigo muy cercano
- "sis" → hermana o amiga muy cercana  
- "mejo" → mejor amigo/a
- "jefa" → madre o pareja en contexto informal
- "mi loco/a" → amigo/a cercano/a
- "compa" → compañero/a
- "pana" → amigo/a (Venezuela/Colombia)

ANÁLISIS DE PATRONES TÓXICOS:
- Control excesivo: "no me deja", "me prohíbe", "me controla"
- Manipulación: "si me dejas te vas a arrepentir", "nadie te va a querer como yo"
- Aislamiento: "no quiere que vea a mis amigos", "dice que mi familia es mala"
- Violencia: cualquier mención de agresión física o psicológica
- Dependencia: "no puedo vivir sin", "soy nada sin él/ella"

CRISIS MENTAL - NIVELES DE RIESGO:
- CRÍTICO: Ideas suicidas activas, plan específico, autolesión reciente
- ALTO: Ideación suicida pasiva, desesperanza severa, aislamiento total
- MODERADO: Depresión severa, ansiedad incapacitante, crisis vital
- BAJO: Tristeza prolongada, estrés significativo, conflictos relacionales
- NINGUNO: Reflexión normal, emociones adaptativas

INDICADORES DE APOYO VS AISLAMIENTO:
- Red fuerte: Múltiples personas de apoyo, comunicación fluida
- Red débil: Pocas personas, contacto limitado
- Aislamiento: No menciona apoyo, "nadie me entiende"

DETECCIÓN DE CAMBIOS TEMPORALES:
- "antes era" vs "ahora es" → cambio en la relación
- "ya no" → deterioro relacional
- "cada vez más" → intensificación (positiva o negativa)

NO ASUMAS GÉNEROS - Si no hay indicadores claros, marca "indefinido"
PRESTA ATENCIÓN AL CONTEXTO - "mi jefe" puede ser apoyo o conflicto según el contexto
DETECTA RELACIONES MÚLTIPLES - Una persona puede tener varios roles

CRÍTICO: Si detectas riesgo suicida o crisis mental, márcalo claramente y recomienda intervención profesional inmediata.

SOLO JSON VÁLIDO, sin explicaciones adicionales.
"""

    def extract_personas_avanzado(self, texto):
        """Extraer personas con análisis súper avanzado"""
        try:
            # Crear prompt mejorado
            prompt_completo = self.crear_prompt_personas_avanzado(texto)

            # Llamada a Gemini
            response = self.model.generate_content(prompt_completo)
            respuesta_texto = response.text

            # Procesar JSON
            datos_procesados = self.procesar_respuesta_json_avanzada(respuesta_texto)

            # Post-procesamiento para añadir insights adicionales
            if datos_procesados:
                datos_procesados = self.post_procesar_analisis(datos_procesados, texto)

            return datos_procesados

        except Exception as e:
            print(f"Error en análisis avanzado: {e}")
            return None

    def procesar_respuesta_json_avanzada(self, respuesta_texto):
        """Procesar respuesta JSON con manejo de errores mejorado"""
        try:
            # Limpiar respuesta
            respuesta_limpia = respuesta_texto.strip()

            # Remover markdown si existe
            if respuesta_limpia.startswith('```json'):
                respuesta_limpia = respuesta_limpia[7:-3]
            elif respuesta_limpia.startswith('```'):
                respuesta_limpia = respuesta_limpia[3:-3]

            # Intentar parsear JSON
            datos = json.loads(respuesta_limpia)

            # Validar estructura esperada
            if not self.validar_estructura_respuesta(datos):
                print("⚠️ Estructura de respuesta inválida")
                return None

            return datos

        except json.JSONDecodeError as e:
            print(f"Error procesando JSON avanzado: {e}")
            print(f"Respuesta: {respuesta_texto[:200]}...")
            return None

    def validar_estructura_respuesta(self, datos):
        """Validar que la respuesta tenga la estructura esperada"""
        required_keys = [
            "personas", "analisis_relaciones", "indicadores_crisis",
            "patrones_emocionales", "recomendaciones_inmediatas"
        ]

        return all(key in datos for key in required_keys)

    def post_procesar_analisis(self, datos, texto_original):
        """Post-procesamiento para añadir insights adicionales"""
        try:
            # Añadir métricas calculadas
            datos["metricas_calculadas"] = self.calcular_metricas_texto(texto_original)

            # Evaluar consistencia del análisis
            datos["validacion_interna"] = self.validar_consistencia_analisis(datos)

            # Añadir timestamp del análisis
            datos["metadata"] = {
                "timestamp": datetime.now().isoformat(),
                "version_algoritmo": "2.0_advanced",
                "longitud_texto": len(texto_original),
                "num_personas_detectadas": len(datos.get("personas", []))
            }

            return datos

        except Exception as e:
            print(f"Error en post-procesamiento: {e}")
            return datos

    def calcular_metricas_texto(self, texto):
        """Calcular métricas adicionales del texto"""
        palabras = texto.split()

        # Contadores emocionales
        palabras_positivas = ["feliz", "alegre", "bien", "genial", "amor", "éxito", "logré"]
        palabras_negativas = ["triste", "mal", "horrible", "odio", "fracaso", "perdí"]

        positivas_count = sum(1 for palabra in palabras if any(pos in palabra.lower() for pos in palabras_positivas))
        negativas_count = sum(1 for palabra in palabras if any(neg in palabra.lower() for neg in palabras_negativas))

        return {
            "longitud_palabras": len(palabras),
            "oraciones_aproximadas": texto.count('.') + texto.count('!') + texto.count('?'),
            "ratio_emocional": (positivas_count - negativas_count) / max(len(palabras), 1),
            "densidad_personas": len(re.findall(r'\b[A-Z][a-z]+\b', texto)),
            "uso_primera_persona": texto.lower().count('yo ') + texto.lower().count('me ') + texto.lower().count('mi '),
            "interrogaciones": texto.count('?'),
            "exclamaciones": texto.count('!')
        }

    def validar_consistencia_analisis(self, datos):
        """Validar consistencia interna del análisis"""
        inconsistencias = []

        # Verificar consistencia entre nivel de riesgo y recomendaciones
        nivel_riesgo = datos.get("indicadores_crisis", {}).get("nivel_riesgo", "ninguno")
        derivacion = datos.get("recomendaciones_inmediatas", {}).get("derivacion_profesional", "innecesaria")

        if nivel_riesgo == "critico" and derivacion != "urgente":
            inconsistencias.append("riesgo_critico_sin_urgencia")

        if nivel_riesgo == "alto" and derivacion not in ["urgente", "recomendada"]:
            inconsistencias.append("riesgo_alto_sin_derivacion")

        # Verificar consistencia en red de apoyo
        personas = datos.get("personas", [])
        personas_apoyo = [p for p in personas if p.get("rol_en_la_situacion") == "apoyo"]
        red_apoyo_fuerte = datos.get("analisis_relaciones", {}).get("red_apoyo_fuerte", False)

        if len(personas_apoyo) == 0 and red_apoyo_fuerte:
            inconsistencias.append("apoyo_fuerte_sin_personas")

        return {
            "es_consistente": len(inconsistencias) == 0,
            "inconsistencias_detectadas": inconsistencias,
            "confianza_analisis": max(0.3, 1.0 - (len(inconsistencias) * 0.2))
        }

    def generar_reporte_detallado(self, datos_analisis):
        """Generar reporte detallado para profesionales"""
        if not datos_analisis:
            return "No se pudo generar reporte - análisis fallido"

        reporte = []
        reporte.append("=== REPORTE CLÍNICO AUTOMATIZADO ===\n")

        # Resumen ejecutivo
        nivel_riesgo = datos_analisis.get("indicadores_crisis", {}).get("nivel_riesgo", "indefinido")
        reporte.append(f"NIVEL DE RIESGO: {nivel_riesgo.upper()}\n")

        # Crisis detectadas
        crisis = datos_analisis.get("indicadores_crisis", {})
        if crisis.get("palabras_criticas_exactas"):
            reporte.append(f"⚠️ PALABRAS CRÍTICAS: {', '.join(crisis['palabras_criticas_exactas'])}")

        # Red de apoyo
        personas = datos_analisis.get("personas", [])
        personas_apoyo = [p for p in personas if p.get("rol_en_la_situacion") == "apoyo"]
        reporte.append(f"\nRED DE APOYO: {len(personas_apoyo)} persona(s) identificada(s)")

        for persona in personas_apoyo:
            reporte.append(f"  - {persona.get('nombre', 'N/A')} ({persona.get('relacion', 'N/A')})")

        # Recomendaciones
        recomendaciones = datos_analisis.get("recomendaciones_inmediatas", {})
        if recomendaciones.get("derivacion_profesional") != "innecesaria":
            reporte.append(f"\n🏥 DERIVACIÓN: {recomendaciones['derivacion_profesional']}")

        return "\n".join(reporte)

# Instancia global del servicio avanzado
advanced_gemini_service = AdvancedGeminiService()

# Funciones helper
def analizar_personas_avanzado(texto):
    """Función helper para análisis avanzado"""
    return advanced_gemini_service.extract_personas_avanzado(texto)

def generar_reporte_clinico(texto):
    """Función helper para generar reporte clínico"""
    analisis = advanced_gemini_service.extract_personas_avanzado(texto)
    if analisis:
        return advanced_gemini_service.generar_reporte_detallado(analisis)
    return "No se pudo generar reporte"

