from pydantic_settings import BaseSettings
from typing import Set

class Settings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 10
    MIN_WIDTH: int = 256
    MIN_HEIGHT: int = 256
    ALLOWED_FORMATS: Set[str] = {"jpeg", "png"}
    
    OUTPUT_FOLDER: str = "images/"
    
    class Config:
        env_file = ".env"

# Instância global das configurações
settings = Settings()