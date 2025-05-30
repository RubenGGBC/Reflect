"""
🔗 Sistema de Integración IA Avanzada - ReflectApp
Conecta la IA inteligente con la interfaz de usuario y base de datos
"""

import flet as ft
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from services.ai_service_gemini_advanced import advanced_gemini_service
from services.reflect_themes_system import get_theme

class AIIntegrationService:
    """Servicio que integra la IA avanzada con ReflectApp"""

    def __init__(self):
        self.analysis_cache = {}  # Cache para evitar re-análisis
        self.analysis_history = []  # Historial de análisis
        self.user_patterns = {}  # Patrones detectados por usuario

    def analyze_reflection_complete(self, user_id: int, reflection_text: str,
                                    positive_tags: List, negative_tags: List) -> Dict:
        """Análisis completo de una reflexión con IA avanzada"""

        print(f"🧠 Iniciando análisis IA avanzado para usuario {user_id}")

        try:
            # Combinar texto de reflexión con contexto de tags
            texto_completo = self._prepare_analysis_text(reflection_text, positive_tags, negative_tags)

            # Análisis principal con IA
            ai_analysis = advanced_gemini_service.extract_personas_avanzado(texto_completo)

            if not ai_analysis:
                return self._generate_fallback_analysis()

            # Enriquecer análisis con contexto histórico
            enriched_analysis = self._enrich_with_history(user_id, ai_analysis)

            # Generar recomendaciones personalizadas
            recommendations = self._generate_smart_recommendations(enriched_analysis)

            # Detectar patrones emergentes
            patterns = self._detect_emerging_patterns(user_id, enriched_analysis)

            # Preparar resultado final
            complete_analysis = {
                "ai_analysis": enriched_analysis,
                "smart_recommendations": recommendations,
                "detected_patterns": patterns,
                "intervention_needed": self._assess_intervention_need(enriched_analysis),
                "user_insights": self._generate_user_insights(enriched_analysis),
                "timestamp": datetime.now().isoformat(),
                "analysis_version": "advanced_2.0"
            }

            # Guardar en cache y historial
            self._save_analysis(user_id, complete_analysis)

            return complete_analysis

        except Exception as e:
            print(f"❌ Error en análisis IA completo: {e}")
            return self._generate_fallback_analysis()

    def _prepare_analysis_text(self, reflection: str, positive_tags: List, negative_tags: List) -> str:
        """Preparar texto enriquecido para análisis"""
        text_parts = [f"Reflexión: {reflection}"]

        if positive_tags:
            positive_context = ". ".join([f"{tag.get('name', '')}: {tag.get('context', '')}" for tag in positive_tags])
            text_parts.append(f"Momentos positivos: {positive_context}")

        if negative_tags:
            negative_context = ". ".join([f"{tag.get('name', '')}: {tag.get('context', '')}" for tag in negative_tags])
            text_parts.append(f"Momentos difíciles: {negative_context}")

        return ". ".join(text_parts)

    def _enrich_with_history(self, user_id: int, current_analysis: Dict) -> Dict:
        """Enriquecer análisis con historial del usuario"""
        try:
            # Obtener análisis previos del usuario
            user_history = [a for a in self.analysis_history if a.get("user_id") == user_id]

            if len(user_history) > 0:
                # Detectar cambios en relaciones
                current_analysis["relationship_changes"] = self._detect_relationship_changes(user_history, current_analysis)

                # Detectar tendencias emocionales
                current_analysis["emotional_trends"] = self._detect_emotional_trends(user_history, current_analysis)

                # Evaluar progreso en salud mental
                current_analysis["mental_health_progress"] = self._assess_mental_health_progress(user_history, current_analysis)

            return current_analysis

        except Exception as e:
            print(f"⚠️ Error enriqueciendo con historial: {e}")
            return current_analysis

    def _generate_smart_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generar recomendaciones inteligentes basadas en el análisis"""
        recommendations = []

        # Recomendaciones basadas en crisis detectada
        crisis_info = analysis.get("indicadores_crisis", {})
        risk_level = crisis_info.get("nivel_riesgo", "ninguno")

        if risk_level == "critico":
            recommendations.extend([
                {
                    "type": "emergency",
                    "priority": "critical",
                    "title": "🚨 Busca ayuda profesional inmediata",
                    "description": "Tu bienestar es prioritario. Contacta con un profesional de salud mental urgentemente.",
                    "actions": ["Llamar a línea de crisis", "Ir a urgencias", "Contactar psicólogo"],
                    "contacts": ["Teléfono de emergencias: 112", "Línea de crisis: 717 003 717"]
                }
            ])

        elif risk_level == "alto":
            recommendations.append({
                "type": "professional_help",
                "priority": "high",
                "title": "🏥 Considera buscar apoyo profesional",
                "description": "Detectamos indicadores que sugieren que podrías beneficiarte de apoyo psicológico.",
                "actions": ["Buscar psicólogo", "Hablar con médico de familia", "Explorar terapia online"]
            })

        # Recomendaciones basadas en relaciones
        relations_analysis = analysis.get("analisis_relaciones", {})

        if relations_analysis.get("relaciones_toxicas_detectadas"):
            recommendations.append({
                "type": "relationship_health",
                "priority": "medium",
                "title": "💔 Evalúa tus relaciones",
                "description": "Hemos detectado posibles patrones tóxicos en tus relaciones. Considera establecer límites saludables.",
                "actions": ["Reflexionar sobre límites", "Buscar apoyo", "Considerar terapia de pareja/familiar"]
            })

        if relations_analysis.get("aislamiento_social") == "alto":
            recommendations.append({
                "type": "social_connection",
                "priority": "medium",
                "title": "🤝 Fortalece tus conexiones",
                "description": "Parece que te sientes aislado/a. Conectar con otros puede mejorar tu bienestar.",
                "actions": ["Contactar un amigo", "Unirse a actividades grupales", "Explorar nuevos hobbies sociales"]
            })

        # Recomendaciones basadas en patrones emocionales
        emotional_patterns = analysis.get("patrones_emocionales", {})

        if emotional_patterns.get("estabilidad_emocional") == "labil":
            recommendations.append({
                "type": "emotional_regulation",
                "priority": "medium",
                "title": "🧘‍♀️ Técnicas de regulación emocional",
                "description": "Tu estabilidad emocional fluctúa. Estas técnicas pueden ayudarte.",
                "actions": ["Practicar mindfulness", "Ejercicio regular", "Técnicas de respiración", "Journaling diario"]
            })

        # Recomendaciones preventivas y de crecimiento
        if risk_level in ["bajo", "ninguno"] and len(recommendations) == 0:
            recommendations.append({
                "type": "growth",
                "priority": "low",
                "title": "🌱 Continúa creciendo",
                "description": "Tu reflexión muestra autoconocimiento. Sigue cultivando tu bienestar mental.",
                "actions": ["Mantener rutina de reflexión", "Explorar nuevas técnicas de bienestar", "Establecer objetivos personales"]
            })

        return recommendations

    def _detect_emerging_patterns(self, user_id: int, analysis: Dict) -> Dict:
        """Detectar patrones emergentes en el comportamiento del usuario"""
        patterns = {
            "relationship_patterns": [],
            "emotional_patterns": [],
            "behavioral_patterns": [],
            "risk_patterns": []
        }

        # Analizar patrones de relaciones
        personas = analysis.get("personas", [])
        for persona in personas:
            if persona.get("patron_relacion") == "relacion_toxica":
                patterns["relationship_patterns"].append({
                    "type": "toxic_relationship",
                    "person": persona.get("nombre", "persona desconocida"),
                    "relation": persona.get("relacion", ""),
                    "confidence": persona.get("confianza", 0)
                })

        # Analizar patrones emocionales
        emotional = analysis.get("patrones_emocionales", {})
        if emotional.get("tono_general") in ["negativo", "muy_negativo"]:
            patterns["emotional_patterns"].append({
                "type": "persistent_negativity",
                "tone": emotional.get("tono_general"),
                "stability": emotional.get("estabilidad_emocional")
            })

        # Patrones de riesgo
        crisis = analysis.get("indicadores_crisis", {})
        if crisis.get("nivel_riesgo") not in ["ninguno", "bajo"]:
            patterns["risk_patterns"].append({
                "type": "mental_health_risk",
                "level": crisis.get("nivel_riesgo"),
                "factors": crisis.get("factores_riesgo", [])
            })

        return patterns

    def _assess_intervention_need(self, analysis: Dict) -> Dict:
        """Evaluar necesidad de intervención"""
        crisis = analysis.get("indicadores_crisis", {})
        recommendations = analysis.get("recomendaciones_inmediatas", {})

        intervention = {
            "needed": False,
            "urgency": "none",
            "type": "none",
            "reason": ""
        }

        risk_level = crisis.get("nivel_riesgo", "ninguno")

        if risk_level == "critico":
            intervention = {
                "needed": True,
                "urgency": "immediate",
                "type": "crisis_intervention",
                "reason": "Indicadores de crisis mental crítica detectados"
            }
        elif risk_level == "alto":
            intervention = {
                "needed": True,
                "urgency": "within_24h",
                "type": "professional_referral",
                "reason": "Alto riesgo de salud mental detectado"
            }
        elif risk_level == "moderado":
            intervention = {
                "needed": True,
                "urgency": "within_week",
                "type": "professional_consultation",
                "reason": "Indicadores de riesgo moderado que requieren seguimiento"
            }

        return intervention

    def _generate_user_insights(self, analysis: Dict) -> List[str]:
        """Generar insights comprensibles para el usuario"""
        insights = []

        # Insights sobre relaciones
        relations = analysis.get("analisis_relaciones", {})
        if relations.get("red_apoyo_fuerte"):
            insights.append("💪 Tienes una red de apoyo sólida que te respalda")
        else:
            insights.append("🤝 Considera fortalecer tus conexiones sociales")

        # Insights sobre patrones emocionales
        emotional = analysis.get("patrones_emocionales", {})
        tone = emotional.get("tono_general", "neutro")

        if tone == "muy_positivo":
            insights.append("🌟 Tu perspectiva actual es muy positiva y optimista")
        elif tone == "positivo":
            insights.append("😊 Mantienes una actitud generalmente positiva")
        elif tone == "negativo":
            insights.append("🌧️ Pareces estar pasando por un momento difícil")
        elif tone == "muy_negativo":
            insights.append("💙 Este parece ser un período particularmente desafiante para ti")

        # Insights sobre mecanismos de afrontamiento
        coping = emotional.get("mecanismos_afrontamiento", [])
        if "busca_apoyo" in coping:
            insights.append("🤗 Tienes la fortaleza de buscar apoyo cuando lo necesitas")
        if "aislamiento" in coping:
            insights.append("🏠 Tiendes a aislarte cuando estás estresado/a - considera otras estrategias")

        # Insights sobre autoconocimiento
        insight_level = emotional.get("insight_personal", "medio")
        if insight_level == "alto":
            insights.append("🎯 Demuestras un alto nivel de autoconocimiento")
        elif insight_level == "medio":
            insights.append("🔍 Tu capacidad de introspección está desarrollándose")
        else:
            insights.append("🌱 Reflexionar más profundamente puede ayudarte a conocerte mejor")

        return insights

    def _save_analysis(self, user_id: int, analysis: Dict):
        """Guardar análisis en historial y cache"""
        analysis_entry = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }

        self.analysis_history.append(analysis_entry)
        self.analysis_cache[f"{user_id}_{datetime.now().date()}"] = analysis

        # Mantener solo los últimos 100 análisis en memoria
        if len(self.analysis_history) > 100:
            self.analysis_history = self.analysis_history[-100:]

    def _generate_fallback_analysis(self) -> Dict:
        """Generar análisis básico en caso de fallo de IA"""
        return {
            "ai_analysis": {
                "personas": [],
                "analisis_relaciones": {"red_apoyo_fuerte": False},
                "indicadores_crisis": {"nivel_riesgo": "indefinido"},
                "patrones_emocionales": {"tono_general": "neutro"},
                "recomendaciones_inmediatas": {"necesita_seguimiento": False}
            },
            "smart_recommendations": [{
                "type": "fallback",
                "priority": "low",
                "title": "📝 Continúa reflexionando",
                "description": "Sigue registrando tus pensamientos y emociones.",
                "actions": ["Escribir más detalles", "Identificar emociones específicas"]
            }],
            "detected_patterns": {},
            "intervention_needed": {"needed": False, "urgency": "none"},
            "user_insights": ["🌱 Cada reflexión es un paso hacia el autoconocimiento"],
            "analysis_status": "fallback"
        }

    def _detect_relationship_changes(self, history: List, current: Dict) -> List:
        """Detectar cambios en relaciones a lo largo del tiempo"""
        # Implementación simplificada - se puede expandir
        changes = []

        if len(history) > 0:
            last_analysis = history[-1].get("analysis", {}).get("ai_analysis", {})
            last_persons = last_analysis.get("personas", [])
            current_persons = current.get("personas", [])

            # Detectar personas que aparecen por primera vez
            last_names = {p.get("nombre") for p in last_persons if p.get("nombre")}
            current_names = {p.get("nombre") for p in current_persons if p.get("nombre")}

            new_people = current_names - last_names
            lost_people = last_names - current_names

            for person in new_people:
                changes.append({
                    "type": "new_person_mentioned",
                    "person": person,
                    "significance": "medium"
                })

            for person in lost_people:
                changes.append({
                    "type": "person_no_longer_mentioned",
                    "person": person,
                    "significance": "low"
                })

        return changes

    def _detect_emotional_trends(self, history: List, current: Dict) -> Dict:
        """Detectar tendencias emocionales"""
        if len(history) < 2:
            return {"trend": "insufficient_data"}

        # Analizar últimos 5 análisis
        recent_history = history[-5:]
        tones = []

        for analysis_entry in recent_history:
            tone = analysis_entry.get("analysis", {}).get("ai_analysis", {}).get("patrones_emocionales", {}).get("tono_general")
            if tone:
                tones.append(tone)

        current_tone = current.get("patrones_emocionales", {}).get("tono_general")
        if current_tone:
            tones.append(current_tone)

        # Mapear tonos a valores numéricos
        tone_values = {
            "muy_negativo": -2,
            "negativo": -1,
            "neutro": 0,
            "positivo": 1,
            "muy_positivo": 2
        }

        numeric_tones = [tone_values.get(tone, 0) for tone in tones]

        if len(numeric_tones) >= 3:
            trend = "stable"
            if numeric_tones[-1] > numeric_tones[0]:
                trend = "improving"
            elif numeric_tones[-1] < numeric_tones[0]:
                trend = "declining"

            return {
                "trend": trend,
                "current_tone": current_tone,
                "tone_history": tones,
                "average_mood": sum(numeric_tones) / len(numeric_tones)
            }

        return {"trend": "insufficient_data"}

    def _assess_mental_health_progress(self, history: List, current: Dict) -> Dict:
        """Evaluar progreso en salud mental"""
        if len(history) < 3:
            return {"status": "insufficient_data"}

        # Analizar niveles de riesgo históricos
        risk_history = []
        for analysis_entry in history[-10:]:  # Últimos 10 análisis
            risk = analysis_entry.get("analysis", {}).get("ai_analysis", {}).get("indicadores_crisis", {}).get("nivel_riesgo")
            if risk:
                risk_history.append(risk)

        current_risk = current.get("indicadores_crisis", {}).get("nivel_riesgo")
        if current_risk:
            risk_history.append(current_risk)

        # Mapear riesgos a valores numéricos
        risk_values = {
            "critico": 4,
            "alto": 3,
            "moderado": 2,
            "bajo": 1,
            "ninguno": 0
        }

        numeric_risks = [risk_values.get(risk, 2) for risk in risk_history]

        if len(numeric_risks) >= 3:
            progress = "stable"
            recent_avg = sum(numeric_risks[-3:]) / 3
            older_avg = sum(numeric_risks[:-3]) / max(len(numeric_risks) - 3, 1)

            if recent_avg < older_avg:
                progress = "improving"
            elif recent_avg > older_avg:
                progress = "concerning"

            return {
                "status": progress,
                "current_risk": current_risk,
                "risk_trend": "decreasing" if recent_avg < older_avg else ("increasing" if recent_avg > older_avg else "stable"),
                "needs_attention": recent_avg >= 2.5
            }

        return {"status": "insufficient_data"}

# Instancia global del servicio de integración
ai_integration_service = AIIntegrationService()

# Funciones helper para usar en EntryScreen
def analyze_reflection_with_ai(user_id: int, reflection_text: str, positive_tags: List, negative_tags: List) -> Dict:
    """Función helper para análisis completo con IA"""
    return ai_integration_service.analyze_reflection_complete(user_id, reflection_text, positive_tags, negative_tags)

def get_user_insights(analysis_result: Dict) -> List[str]:
    """Función helper para obtener insights del usuario"""
    return analysis_result.get("user_insights", [])

def get_smart_recommendations(analysis_result: Dict) -> List[Dict]:
    """Función helper para obtener recomendaciones inteligentes"""
    return analysis_result.get("smart_recommendations", [])

def check_intervention_needed(analysis_result: Dict) -> Dict:
    """Función helper para verificar si se necesita intervención"""
    return analysis_result.get("intervention_needed", {"needed": False})