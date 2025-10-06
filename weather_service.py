import requests
from datetime import datetime, timedelta
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.WEATHERAPI_KEY
        self.base_url = Config.WEATHERAPI_BASE_URL
    
    def get_weather_forecast(self, city_name, days=1):
        """Obtener pronóstico del tiempo real para una ciudad"""
        url = f"{self.base_url}/forecast.json"
        params = {
            'key': self.api_key,
            'q': city_name,
            'days': days,
            'aqi': 'no',
            'alerts': 'no',
            'lang': 'es'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Lanza excepción para errores HTTP
            data = response.json()
            
            return self._parse_weather_data(data, days)
                
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo datos del clima: {e}")
            return None
    
    def _parse_weather_data(self, data, days):
        """Parsear datos de la respuesta de WeatherAPI.com"""
        location = data['location']
        current = data['current']
        forecast = data['forecast']
        
        # Procesar pronóstico para el día solicitado
        forecast_day = forecast['forecastday'][0]['day'] if days == 1 else forecast['forecastday'][0]['day']
        
        weather_info = {
            'city': location['name'],
            'country': location['country'],
            'date': datetime.now().strftime('%d/%m/%Y'),
            'temp_current': current['temp_c'],
            'temp_min': forecast_day['mintemp_c'],
            'temp_max': forecast_day['maxtemp_c'],
            'feels_like': current['feelslike_c'],
            'humidity': current['humidity'],
            'description': current['condition']['text'],
            'rain_probability': forecast_day['daily_chance_of_rain'],
            'wind_speed': current['wind_kph'],
            'wind_gust': current.get('gust_kph', current['wind_kph']),
            'pressure': current['pressure_mb'],
            'visibility': current['vis_km']
        }
        
        return weather_info

# Instancia global del servicio meteorológico
weather_service = WeatherService()