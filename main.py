import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import json
import re
from datetime import datetime
import requests
from config import Config  # Importar configuración


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
            if not Config.GEMINI_API_KEY:
                raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY.")
            
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.MODEL_NAME)
            self.chat = self.model.start_chat(history=[])
            print("✅ Gemini configurado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error configurando Gemini: {str(e)}")
    
    def create_widgets(self):
        """Crear los elementos de la interfaz gráfica"""
        # Título
        title_label = tk.Label(
            self.root, 
            text="🌤️ Chatbot del Tiempo", 
            font=("Arial", 16, "bold"),
            bg=Config.BACKGROUND_COLOR,
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Área de chat
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
        
        # Frame para entrada de texto
        input_frame = tk.Frame(self.root, bg=Config.BACKGROUND_COLOR)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Campo de entrada
        self.user_input = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=50
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # Botón enviar
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
        
        # Mensaje de bienvenida
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
            
        # Mostrar mensaje del usuario
        self.add_user_message(user_text)
        self.user_input.delete(0, tk.END)
        
        # Deshabilitar botón mientras procesa
        self.send_button.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Obtener respuesta de Gemini
            response = self.get_gemini_response(user_text)
            self.add_bot_message(response)
            
        except Exception as e:
            self.add_bot_message(f"❌ Lo siento, hubo un error: {str(e)}")
        
        # Rehabilitar botón
        self.send_button.config(state=tk.NORMAL)
    
    def get_gemini_response(self, user_message):
        """Obtener respuesta de Gemini"""
        try:
            prompt = f"""
            Eres un especialista en meteorología. Responde preguntas SOBRE EL TIEMPO Y CLIMA únicamente.
            Si la pregunta no es sobre el tiempo, responde amablemente que solo puedes ayudar con temas meteorológicos.
            
            Pregunta del usuario: {user_message}
            
            Proporciona información clara y concisa sobre el clima. Si menciona una ciudad y fecha específica, 
            estructura la respuesta de manera organizada.
            """
            
            response = self.chat.send_message(prompt)
            return response.text
            
        except Exception as e:
            return f"Error al conectar con Gemini: {str(e)}"
    
    def add_user_message(self, message):
        """Añadir mensaje del usuario al chat"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"👤 Tú: {message}\n\n", "user")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def add_bot_message(self, message):
        """Añadir mensaje del bot al chat"""
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
