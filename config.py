# config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde apikey.env
load_dotenv('apikey.env')

class Config:
    # Configuración de Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Validar que la API key esté presente
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY no encontrada. Verifica tu archivo apikey.env")
    
    # Configuración del modelo
    MODEL_NAME = 'gemini-1.5-flash'  # Puedes cambiar a 'gemini-1.5-pro' si prefieres
    
    # Configuración de la interfaz
    WINDOW_TITLE = "🌤️ Chatbot del Tiempo - Gemini"
    WINDOW_SIZE = "600x500"
    BACKGROUND_COLOR = "#f0f0f0"