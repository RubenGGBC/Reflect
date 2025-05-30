# memory_system.py - Clase principal
class MemorySystem:
    def __init__(self, db_service, ai_service):
        self.db = db_service
        self.ai = ai_service
        self.extractor = MemoryExtractor(ai_service)

    # MÉTODO PRINCIPAL - se llama después de cada entrada
    def process_entry(self, user_id, entry_text, positive_tags, negative_tags):
        """Procesa una entrada y extrae/almacena insights"""
        pass

    # MÉTODO DE CONSULTA - se llama antes de responder al usuario
    def get_context_for_user(self, user_id, current_text=""):
        """Obtiene contexto relevante para personalizar respuesta"""
        pass

    # MÉTODO DE GESTIÓN
    def cleanup_old_memories(self, user_id, days_old=90):
        """Limpia recuerdos antiguos poco importantes"""
        pass