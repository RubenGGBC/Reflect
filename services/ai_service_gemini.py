# services/ai_service_gemini.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiService:
    def __init__(self):
        # Configurar Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en .env")

        genai.configure(api_key=api_key)

        # ✅ MODELO CORREGIDO
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Más rápido y gratuito

    def extract_personas(self, texto):
        try:
            # Crear prompt completo
            prompt_completo = self.crear_prompt_personas(texto)

            # ✅ LLAMADA SIMPLIFICADA
            response = self.model.generate_content(prompt_completo)

            # Extraer respuesta
            respuesta_texto = response.text

            # Procesar JSON
            datos_procesados = self.procesar_respuesta_json(respuesta_texto)
            return datos_procesados

        except Exception as e:
            print(f"Error llamando a Gemini: {e}")
            return None

    def crear_prompt_personas(self, texto):
        return f"""
Analiza este texto y extrae personas mencionadas.

TEXTO: "{texto}"

Responde solo con JSON válido:
{{
    "personas": [
        {{
            "nombre": "Ana",
            "relacion": "hermana",
            "tipo": "familia",
            "sentimiento_hacia_persona": "positivo",
            "confianza": 0.9
        }}
    ],
    "palabras_criticas": [],
    "necesita_seguimiento": false
}}

Tipos: "familia", "amistad", "pareja", "trabajo", "otro"
Sentimientos: "muy_positivo", "positivo", "neutro", "negativo", "muy_negativo"
Solo JSON, sin explicaciones.
"""

    def procesar_respuesta_json(self, respuesta_texto):
        try:
            respuesta_limpia = respuesta_texto.strip()
            if respuesta_limpia.startswith('```json'):
                respuesta_limpia = respuesta_limpia[7:-3]
            elif respuesta_limpia.startswith('```'):
                respuesta_limpia = respuesta_limpia[3:-3]

            datos = json.loads(respuesta_limpia)
            return datos

        except json.JSONDecodeError as e:
            print(f"Error procesando JSON: {e}")
            print(f"Respuesta: {respuesta_texto}")
            return None

    def listar_modelos_disponibles(self):
        """Función helper para ver qué modelos están disponibles"""
        try:
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    print(f"✅ Modelo disponible: {model.name}")
        except Exception as e:
            print(f"Error listando modelos: {e}")


def test_casos_potentes():
    """Función de prueba potente CON MANEJO DE ERRORES"""

    # Casos de prueba progresivos
    casos_potentes = [
        # ===== BÁSICOS =====
        "mi hermana Ana me ayudó con la mudanza",

        # ===== MÚLTIPLES PERSONAS =====
        "mi bro Carlos me traicionó pero mi mejo Luis me apoyó, y mi vieja me regañó por confiar en Carlos",

        # ===== EMOCIONES CONTRADICTORIAS =====
        "amo a mi novio pero a veces me frustra mucho, y mi hermana Sofía siempre me dice que lo deje",

        # ===== CRISIS MENTAL =====
        "no puedo más, estoy pensando en hacerme daño, solo mi psicóloga me entiende pero cuesta mucho",

        # ===== SITUACIÓN LABORAL COMPLEJA =====
        "mi jefe Miguel me humilló delante de todos, mi compañera Sara me consoló, pero mi mamá dice que renuncie",

        # ===== RELACIONES AMBIGUAS =====
        "JJ me escribió anoche, no sé si quiere volver conmigo, mi prima dice que es mala idea",

        # ===== MÚLTIPLES CRISIS =====
        "después del divorcio mi ex me acosa, mis hijos están confundidos, mi hermano me ayuda con dinero pero mi suegra me culpa de todo",

        # ===== LENGUAJE INFORMAL + ERRORES =====
        "mi ermanita me yudo cn la tarea pero mi papi sta enojao conmigo x las notas",

        # ===== CASO EXTREMO =====
        "mi madre murió el mes pasado, mi hermano se volvió alcohólico, mi ex pareja me dejó cuando más la necesitaba, mi jefe no entiende por qué falto tanto, y mi psiquiatra aumentó la medicación pero siento que no sirve, a veces pienso que no vale la pena seguir",

        # ===== IRONÍA/SARCASMO =====
        "mi 'mejor amigo' David me robó la novia, qué gran persona, y mi hermana me dice que sea 'comprensivo'",

        # ===== REFERENCIAS INDIRECTAS =====
        "la mamá de mi novia no me soporta, el papá de mi mejor amigo me ofreció trabajo, pero la hermana de mi ex me advirtió que es una trampa"
    ]

    try:
        service = GeminiService()

        for i, texto in enumerate(casos_potentes, 1):
            print(f"\n{'='*60}")
            print(f"🧪 CASO {i}: {texto[:50]}...")
            print(f"📝 TEXTO COMPLETO: {texto}")
            print("-" * 60)

            try:
                # Intentar procesar cada caso
                resultado = service.extract_personas(texto)

                if resultado:
                    print(f"👥 PERSONAS DETECTADAS: {len(resultado.get('personas', []))}")

                    for j, persona in enumerate(resultado.get('personas', []), 1):
                        print(f"  {j}. {persona.get('nombre', 'SIN_NOMBRE')} → {persona.get('relacion', '?')} → {persona.get('sentimiento_hacia_persona', '?')} (confianza: {persona.get('confianza', 0)})")

                    criticas = resultado.get('palabras_criticas', [])
                    if criticas:
                        print(f"🚨 PALABRAS CRÍTICAS: {criticas}")

                    seguimiento = resultado.get('necesita_seguimiento', False)
                    if seguimiento:
                        print(f"⚠️ NECESITA SEGUIMIENTO: {seguimiento}")

                else:
                    print("❌ FALLÓ EL PROCESAMIENTO")

            except Exception as e:
                print(f"❌ ERROR EN CASO {i}: {e}")
                continue  # Continúa con el siguiente caso

            finally:
                print(f"⏱️ Caso {i} procesado")

    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")

    finally:
        print("\n🏁 PRUEBAS COMPLETADAS")


# Código de ejecución principal
if __name__ == "__main__":
    try:
        # Crear servicio para pruebas básicas
        service = GeminiService()

        # Ejecutar pruebas completas
        test_casos_potentes()

    except Exception as e:
        print(f"Error inicializando el servicio: {e}")
        print("Verifica que tengas GEMINI_API_KEY en tu archivo .env")