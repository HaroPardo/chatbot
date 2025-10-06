# config.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv('apikey.env')

class Config:
    # Configuración de Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = 'gemini-2.0-flash'
    
    # Configuración de WeatherAPI.com
    WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY')
    WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1"
    
    # Configuración de la interfaz
    WINDOW_TITLE = "🌤️ Chatbot del Tiempo - Datos Reales"
    WINDOW_SIZE = "600x500"
    BACKGROUND_COLOR = "#f0f0f0"

# Configurar el cliente global
client = genai.Client(api_key=Config.GEMINI_API_KEY)