from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    VAD_MODEL_PATH: str = ""

settings = Settings()
