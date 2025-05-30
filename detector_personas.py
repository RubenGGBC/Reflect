# Define estas listas según tu criterio:
from services.ai_service import ZenAIService

RELACIONES_FAMILIA = [
    "hermana", "hermano", "mamá", "mamá", "papá", "padre",
    "primo", "prima", "tío", "tía", "abuelo", "abuela"
    # ¿Qué más añadirías?
]

SLANG_RELACIONES = {
    "bro": "hermano",
    "sis": "hermana",
    "mejo": "mejor_amigo",
    "viejo": "padre",
    "vieja": "madre"
    # ¿Qué otros slangs conoces?
}

RELACIONES_SOCIALES = [
    "amigo", "amiga", "novio", "novia", "pareja",
    "compañero", "vecino", "jefe", "colega"
    # ¿Qué más?
]


def detectar_personas(texto):
    personas_encontrados=[]
    return personas_encontrados

def es_nombre_propio(palabra, texto=""):

    if not (palabra[0].isupper() and palabra[1:].islower()):
        return False

    if len(palabra) < 2 or len(palabra) > 15:
        return False

    PALABRAS_COMUNES = [
        "Casa", "Trabajo", "Universidad", "Hospital",
        "Lunes", "Martes", "Enero", "Febrero",
        "España", "Madrid", "Barcelona"
    ]

    if palabra in PALABRAS_COMUNES:
        return False

    if texto:
        patrones_nombre = [
            f"mi hermana {palabra}",
            f"mi hermano {palabra}",
            f"con {palabra}",
            f"{palabra} me",
            f"llamé a {palabra}"
        ]

        for patron in patrones_nombre:
            if patron.lower() in texto.lower():
                return True


    return len(palabra) >= 3 and len(palabra) <= 10



def buscar_relaciones_familia(texto):
    relaciones_encontradas = []
    texto_lower = texto.lower()

    for relacion in RELACIONES_FAMILIA:
        patron = f"mi {relacion}"
        if patron in texto_lower:
            # EN VEZ DE: relaciones_encontradas.append(patron)
            # MEJOR:
            relaciones_encontradas.append({
                "relacion": relacion,           # "hermana"
                "contexto": patron,             # "mi hermana"
                "tipo": "familia",              # categoría
                "confianza": 0.9                # alta confianza
            })

    return relaciones_encontradas



def buscar_slang(texto):
    slang_encontradas = []  # Nombre consistente
    texto_lower = texto.lower()

    for slang in SLANG_RELACIONES:  # 'slang' es la clave (ej: "bro")
        patron = f"mi {slang}"
        if patron in texto_lower:
            slang_encontradas.append({
                "slang": slang,                      # "bro"
                "significado": SLANG_RELACIONES[slang],  # "hermano"
                "contexto": patron,                  # "mi bro"
                "tipo": "slang",
                "confianza": 0.7
            })

    return slang_encontradas  # Nombre consistente

# Código de prueba:
texto_test = "mi hermana Ana me ayudó y mi papá está bien"
resultado = buscar_relaciones_familia(texto_test)

for rel in resultado:
    print(f"Relación: {rel['relacion']}, Contexto: '{rel['contexto']}'")

# Salida esperada:
# Relación: hermana, Contexto: 'mi hermana'
# Relación: papá, Contexto: 'mi papá'