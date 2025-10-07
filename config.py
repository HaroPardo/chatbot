# config.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv('apikey.env')

class Config:
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = 'gemini-2.0-flash'
    
    # WeatherAPI.com Configuration
    WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY')
    WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1"
    
    # Interface Configuration
    WINDOW_TITLE = "🌤️ Weather Chatbot"
    WINDOW_SIZE = "600x500"
    BACKGROUND_COLOR = "#f0f0f0"

# Configure global client
client = genai.Client(api_key=Config.GEMINI_API_KEY)