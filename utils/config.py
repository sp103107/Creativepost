from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("CONTENT_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "default-model")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000")) 