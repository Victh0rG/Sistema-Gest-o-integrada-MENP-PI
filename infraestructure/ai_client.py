# Cliente API OpenAI (GPT + Whisper)
import os
import dotenv
from google import genai
from google.genai import types

dotenv.load_dotenv()

class AiClient:
    def __init__(self):
        self.client = None

    def connect(self, image, prompt: str):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        with open(image, 'rb') as f:
            image_bytes = f.read()

        response = self.client.models.generate_content(
            model = "gemini-3-flash-preview",
            contents= [
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                # PROMPT IA
                prompt,
            ]
        )

        print(response.text)