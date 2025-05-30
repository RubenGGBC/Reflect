# test_config.py
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Probar si puede leer la key
api_key = os.getenv('DEEPSEEK_API_KEY')

if api_key:
    print("✅ API Key cargada correctamente")
    print(f"✅ Primeros 10 caracteres: {api_key[:10]}...")
else:
    print("❌ No se pudo cargar la API Key")
    print("❌ Verifica tu archivo .env")