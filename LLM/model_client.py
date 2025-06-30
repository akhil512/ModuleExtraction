import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

class ModelClient:
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model = os.getenv("MODEL_NAME"),
            api_key = os.getenv("OPENAI_KEY")
        )

    def get_model_client(self):
        return self.model_client
