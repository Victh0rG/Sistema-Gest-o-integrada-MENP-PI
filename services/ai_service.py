# Orquestra IA + revisão de dados
from infraestructure import ai_client

class AiService:
    def __init__(self):
        self.ai_client = ai_client.AiClient()

    def get_ai_service(self, file, prompt):
        file_ai = self.ai_client.connect(file, prompt)
        return file_ai