from datetime import datetime

class Entry:
    """
    Modelo para las entradas de diario
    """
    def __init__(self, text, emotion=None, categories=None, user_id=None):
        self.id = None  # Se asignará cuando se guarde en la base de datos
        self.text = text
        self.emotion = emotion
        self.categories = categories or []
        self.user_id = user_id
        self.created_at = datetime.now()
        self.sentiment = None  # Se asignará después del análisis
        self.insights = None   # Se asignará después del análisis

    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenar en Firebase"""
        return {
            'text': self.text,
            'emotion': self.emotion,
            'categories': self.categories,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'sentiment': self.sentiment,
            'insights': self.insights
        }

    @classmethod
    def from_dict(cls, id, data):
        """Crea un objeto Entry a partir de un diccionario (desde Firebase)"""
        entry = cls(
            text=data.get('text'),
            emotion=data.get('emotion'),
            categories=data.get('categories', []),
            user_id=data.get('user_id')
        )
        entry.id = id
        entry.sentiment = data.get('sentiment')
        entry.insights = data.get('insights')

        # Convertir string a datetime
        if 'created_at' in data:
            try:
                entry.created_at = datetime.fromisoformat(data['created_at'])
            except (ValueError, TypeError):
                entry.created_at = datetime.now()

        return entry