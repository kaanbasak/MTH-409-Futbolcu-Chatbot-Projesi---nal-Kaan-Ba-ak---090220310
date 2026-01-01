import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiHandler:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_response(self, user_query, player_context):
        """
        Generates a response using Google's Gemini model.
        """
        if not self.api_key:
            return "Error: Google API Key is missing."

        system_prompt = (
            "Sen bir futbol uzmanısın. Sana verilen oyuncu verisini kullanarak "
            "kullanıcının sorusunu nazikçe ve kısa bir şekilde cevapla.\n"
            f"Oyuncu Bilgisi: {player_context}\n"
            f"Soru: {user_query}"
        )

        try:
            response = self.model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response from Gemini: {e}"



