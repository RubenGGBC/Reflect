"""
Funciones auxiliares para diversas tareas en la aplicación
"""

def format_date(date):
    """
    Formatea una fecha en un formato legible

    Args:
        date: Objeto datetime

    Returns:
        str: Fecha formateada
    """
    if not date:
        return ""

    return date.strftime("%d %b %Y, %H:%M")


def truncate_text(text, max_length=100):
    """
    Trunca un texto a una longitud máxima

    Args:
        text (str): Texto a truncar
        max_length (int): Longitud máxima

    Returns:
        str: Texto truncado
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length] + "..."