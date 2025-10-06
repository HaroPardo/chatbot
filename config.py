# config.py
import os
from dotenv import load_dotenv
from google import genai

# Cargar variables de entorno desde apikey.env
load_dotenv('apikey.env')

class Config:
    # Configuración de Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Validar que la API key esté presente
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY no encontrada. Verifica tu archivo apikey.env")
    
    # Configuración del modelo - ELIGE UNO:
    MODEL_NAME = 'gemini-2.0-flash'  # Modelo bien establecido
    # MODEL_NAME = 'gemini-2.5-flash'  # Modelo más reciente
    
    # Configuración de la interfaz
    WINDOW_TITLE = "🌤️ Chatbot del Tiempo - Gemini"
    WINDOW_SIZE = "600x500"
    BACKGROUND_COLOR = "#f0f0f0"

# Configurar el cliente global
client = genai.Client(api_key=Config.GEMINI_API_KEY)