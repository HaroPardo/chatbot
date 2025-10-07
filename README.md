# 🌤️ Weather Chatbot with Gemini AI
A modern Python-based weather chatbot that provides real-time weather information using Google's Gemini AI and WeatherAPI.com. Features a clean graphical interface built with Tkinter.

https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/Status-Functional-brightgreen.svg

## ✨ Features
🤖 AI-Powered Conversations: Uses Google Gemini AI for natural language processing

🌤️ Real Weather Data: Integrates with WeatherAPI.com for accurate forecasts

🎨 Modern GUI: Clean and intuitive Tkinter-based interface

🔐 Secure Configuration: Environment-based API key management

🌍 Multi-City Support: Get weather for any city worldwide

📱 Responsive Design: Scrollable chat interface with real-time updates

## 🛠️ Technologies Used
Core Technologies
Python 3.8+ - Primary programming language

Tkinter - GUI framework for the interface

Google Gemini AI - Large language model for natural conversations

WeatherAPI.com - Real-time weather data provider

Python Libraries
Library	Purpose	Version
google-genai	Gemini AI API integration	Latest
requests	HTTP requests for weather data	2.31+
python-dotenv	Environment variable management	1.0+
tkinter	Built-in GUI framework	Standard
datetime	Date and time handling	Standard
APIs & Services
Google AI Studio - For Gemini API access and management

WeatherAPI.com - For real-time weather data

Environment Variables - Secure credential management

## 📋 Prerequisites
Python 3.8 or higher

Google Gemini API key

WeatherAPI.com account and API key

Git (for version control)

## 🚀 Installation & Setup
   
1. Clone the Repository
bash
git clone https://github.com/your-username/weather-chatbot.git
cd weather-chatbot
    
2. Create Virtual Environment
   python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure API Keys
Create an apikey.env file in the project root:

env
apikey.env
GEMINI_API_KEY=your_gemini_api_key_here
WEATHERAPI_KEY=your_weatherapi_key_here
Getting API Keys:
Google Gemini API:

Visit Google AI Studio

Create a new project or select existing

Generate an API key

Add it to your apikey.env file

WeatherAPI.com:

Sign up at WeatherAPI.com

Verify your email

Get your API key from the dashboard

Add it to your apikey.env file

5. Run the Application
bash
python main.py
## 📁 Project Structure
text
weather-chatbot/
├── main.py                 # Main application file
├── config.py              # Configuration settings
├── weather_service.py     # Weather API integration
├── apikey.env            # API keys (NOT in version control)
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
