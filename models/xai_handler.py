import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class XAIHandler:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        if not self.api_key:
            print("Warning: XAI_API_KEY not found in environment variables.")
        
        # xAI uses the OpenAI SDK but with a different base URL
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )

    def generate_response(self, user_query, player_context):
        """
        Generates a response using xAI's Grok model.
        """
        if not self.api_key:
            return "Error: XAI API Key is missing. Please check your .env file."

        system_prompt = (
            "Sen bir futbol uzmanısın. Sana verilen oyuncu verisini kullanarak "
            "kullanıcının sorusunu nazikçe ve kısa bir şekilde cevapla. "
            f"Oyuncu Bilgisi: {player_context}"
        )

        try:
            response = self.client.chat.completions.create(
                model="grok-4-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response from xAI: {e}"

