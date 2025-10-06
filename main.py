import tkinter as tk
from tkinter import scrolledtext, messagebox
from config import Config, client  # Importar configuración y cliente
from weather_service import weather_service  # Servicio de clima real
import re


class WeatherChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.configure(bg=Config.BACKGROUND_COLOR)
        
        # Configurar Gemini
        self.setup_gemini()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_gemini(self):
        """Configurar la API de Gemini"""
        try:
            self.chat = client.chats.create(model=Config.MODEL_NAME)
            print("✅ Gemini configurado correctamente con modelo:", Config.MODEL_NAME)
        except Exception as e:
            messagebox.showerror("Error", f"Error configurando Gemini: {str(e)}")
    
    def create_widgets(self):
        """Crear los elementos de la interfaz gráfica"""
        title_label = tk.Label(
            self.root, 
            text="🌤️ Chatbot del Tiempo", 
            font=("Arial", 16, "bold"),
            bg=Config.BACKGROUND_COLOR,
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            width=70,
            height=20,
            font=("Arial", 10),
            wrap=tk.WORD,
            bg="white",
            fg="#2c3e50"
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(self.root, bg=Config.BACKGROUND_COLOR)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_input = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=50
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        self.send_button = tk.Button(
            input_frame,
            text="Enviar",
            command=self.send_message,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=20
        )
        self.send_button.pack(side=tk.RIGHT)
        
        self.add_bot_message(
            "¡Hola! Soy tu asistente del tiempo. 🌤️\n"
            "Pregúntame sobre el clima en cualquier ciudad. Por ejemplo:\n"
            "- ¿Qué tiempo hará en Madrid el próximo sábado?\n"
            "- ¿Cómo está el clima en Barcelona hoy?\n"
            "- Temperatura en Sevilla mañana"
        )
    
    def send_message(self):
        """Enviar mensaje del usuario"""
        user_text = self.user_input.get().strip()
        if not user_text:
            return
            
        self.add_user_message(user_text)
        self.user_input.delete(0, tk.END)
        self.send_button.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            response = self.get_gemini_response(user_text)
            self.add_bot_message(response)
        except Exception as e:
            self.add_bot_message(f"❌ Lo siento, hubo un error: {str(e)}")
        finally:
            self.send_button.config(state=tk.NORMAL)
    
    def get_gemini_response(self, user_message):
        """Obtener respuesta de Gemini integrando datos reales del tiempo"""
        try:
            if self.is_weather_question(user_message):
                weather_data = self.get_real_weather_data(user_message)
                if weather_data:
                    prompt = self.create_weather_prompt(user_message, weather_data)
                    response = self.chat.send_message(prompt)
                    return (
                        f"🌤️ {response.text}\n\n"
                        f"💡 *Nota: Datos meteorológicos obtenidos de WeatherAPI.com*"
                    )
                else:
                    return "⚠️ No pude obtener datos meteorológicos en este momento. El servicio puede estar temporalmente no disponible."
            else:
                response = self.chat.send_message(user_message)
                return response.text
        except Exception as e:
            return f"Error al conectar con los servicios: {str(e)}"
    
    def is_weather_question(self, text):
        """Detectar si el usuario pregunta sobre el tiempo"""
        keywords = [
            "tiempo", "clima", "temperatura", "lluvia",
            "viento", "nubes", "pronóstico", "meteorología"
        ]
        return any(k in text.lower() for k in keywords)
    
    def get_real_weather_data(self, user_message):
        """Obtener datos reales del clima"""
        try:
            city, days = self.extract_city_and_date(user_message)
            weather_data = weather_service.get_weather_forecast(city, days + 1)
            return weather_data
        except Exception as e:
            print(f"Error obteniendo datos del clima: {e}")
            return None
    
    def create_weather_prompt(self, user_message, weather_data):
        """Crear prompt para Gemini con datos reales del clima"""
        prompt = f"""
        El usuario preguntó: "{user_message}"
        
        Aquí tienes datos meteorológicos REALES para {weather_data['city']} ({weather_data['country']}) para {weather_data['date']}:
        
        DATOS REALES:
        - Temperatura actual: {weather_data['temp_current']}°C
        - Mínima: {weather_data['temp_min']}°C, Máxima: {weather_data['temp_max']}°C
        - Sensación térmica: {weather_data['feels_like']}°C
        - Condiciones: {weather_data['description']}
        - Probabilidad de lluvia: {weather_data['rain_probability']}%
        - Viento: {weather_data['wind_speed']} km/h (ráfagas {weather_data['wind_gust']} km/h)
        - Humedad: {weather_data['humidity']}%
        - Presión: {weather_data['pressure']} mb
        - Visibilidad: {weather_data['visibility']} km
        
        Responde en español de forma natural y útil, usando estos datos reales.
        Sé conciso, informativo y ofrece información práctica.
        No inventes datos ni uses valores ficticios.
        """
        return prompt

    def extract_city_and_date(self, text):
        """Extraer ciudad y días a futuro desde el mensaje del usuario"""
        text_lower = text.lower()
        cities = [
            'zaragoza', 'madrid', 'barcelona', 'sevilla', 'valencia',
            'bilbao', 'granada', 'mallorca', 'alicante', 'murcia',
            'oviedo', 'santiago'
        ]
        city = next((c for c in cities if c in text_lower), 'madrid')
        
        if 'pasado mañana' in text_lower or '2 días' in text_lower:
            days = 2
        elif 'mañana' in text_lower:
            days = 1
        else:
            days = 0  # hoy
            
        return city, days
    
    def add_user_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"👤 Tú: {message}\n\n", "user")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def add_bot_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"🤖 Bot: {message}\n", "bot")
        self.chat_area.insert(tk.END, "─" * 50 + "\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)


def main():
    root = tk.Tk()
    app = WeatherChatbot(root)
    root.mainloop()


if __name__ == "__main__":
    main()
