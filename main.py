# main.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
from config import Config, client
from weather_service import weather_service
import re

class WeatherChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.configure(bg=Config.BACKGROUND_COLOR)
        
        # Configure Gemini
        self.setup_gemini()
        
        # Create interface
        self.create_widgets()
        
    def setup_gemini(self):
        """Configure Gemini API"""
        try:
            self.chat = client.chats.create(model=Config.MODEL_NAME)
            print("✅ Gemini configured correctly with model:", Config.MODEL_NAME)
        except Exception as e:
            messagebox.showerror("Error", f"Error configuring Gemini: {str(e)}")
    
    def create_widgets(self):
        """Create GUI elements"""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="🌤️ Weather Chatbot", 
            font=("Arial", 16, "bold"),
            bg=Config.BACKGROUND_COLOR,
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Chat area
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
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=Config.BACKGROUND_COLOR)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Input field
        self.user_input = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=50
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            relief=tk.FLAT,
            padx=20
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Welcome message
        self.add_bot_message("Hello! I'm your weather assistant. 🌤️\nAsk me about the weather in any city. For example:\n- What will the weather be like in Madrid next Saturday?\n- How is the weather in Barcelona today?\n- Temperature in Seville tomorrow")
    
    def send_message(self):
        """Send user message"""
        user_text = self.user_input.get().strip()
        
        if not user_text:
            return
            
        # Show user message
        self.add_user_message(user_text)
        self.user_input.delete(0, tk.END)
        
        # Disable button while processing
        self.send_button.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Get response from Gemini
            response = self.get_gemini_response(user_text)
            self.add_bot_message(response)
            
        except Exception as e:
            self.add_bot_message(f"❌ Sorry, there was an error: {str(e)}")
        
        # Re-enable button
        self.send_button.config(state=tk.NORMAL)
    
    def get_gemini_response(self, user_message):
        """Get response from Gemini integrating real weather data"""
        try:
            # Detect if the question is about weather
            if self.is_weather_question(user_message):
                weather_data = self.get_real_weather_data(user_message)
                if weather_data:
                    # Use Gemini to format real data
                    prompt = self.create_weather_prompt(user_message, weather_data)
                    response = self.chat.send_message(prompt)
                    return f"🌤️ {response.text}\n\n💡 *Note: Weather data provided by WeatherAPI.com*"
                else:
                    return "⚠️ I couldn't get weather data at the moment. The service may be temporarily unavailable."
            else:
                # For non-weather questions, use Gemini directly
                response = self.chat.send_message(user_message)
                return response.text
            
        except Exception as e:
            return f"Error connecting to services: {str(e)}"
    
    def is_weather_question(self, text):
        """Detect if the question is about weather"""
        weather_keywords = ['weather', 'temperature', 'rain', 'wind', 'forecast', 
                          'meteorological', 'degrees', 'hot', 'cold', 'humidity',
                          'climate', 'storm', 'sunny', 'cloudy']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in weather_keywords)
    
    def extract_city_and_date(self, text):
        """Extract city and date from text"""
        text_lower = text.lower()
        
        # City (you can expand this dictionary)
        cities = ['zaragoza', 'madrid', 'barcelona', 'sevilla', 'valencia', 'bilbao',
                 'london', 'paris', 'berlin', 'rome', 'new york', 'tokyo']
        city = next((c for c in cities if c in text_lower), 'madrid')  # default
        
        # Days (simple implementation)
        if 'tomorrow' in text_lower:
            days = 1
        elif 'day after tomorrow' in text_lower or '2 days' in text_lower:
            days = 2
        else:
            days = 0  # today
            
        return city, days
    
    def get_real_weather_data(self, user_message):
        """Get real weather data"""
        try:
            city, days = self.extract_city_and_date(user_message)
            weather_data = weather_service.get_weather_forecast(city, days + 1)
            return weather_data
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return None
    
    def create_weather_prompt(self, user_message, weather_data):
        """Create prompt for Gemini with real weather data"""
        prompt = f"""
        The user asked: "{user_message}"

        Here are REAL meteorological data for {weather_data['city']} ({weather_data['country']}) for {weather_data['date']}:

        REAL DATA:
        - Current temperature: {weather_data['temp_current']}°C
        - Minimum: {weather_data['temp_min']}°C, Maximum: {weather_data['temp_max']}°C
        - Feels like: {weather_data['feels_like']}°C
        - Conditions: {weather_data['description']}
        - Rain probability: {weather_data['rain_probability']}%
        - Wind: {weather_data['wind_speed']} km/h (gusts {weather_data['wind_gust']} km/h)
        - Humidity: {weather_data['humidity']}%
        - Pressure: {weather_data['pressure']} mb
        - Visibility: {weather_data['visibility']} km

        Respond naturally and helpfully in English, using this real data.
        Be concise but informative, and offer relevant practical information for the user.
        Do not invent data or use placeholders.
        """
        return prompt

    def add_user_message(self, message):
        """Add user message to chat"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"👤 You: {message}\n\n", "user")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def add_bot_message(self, message):
        """Add bot message to chat"""
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
