from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do .env"""
    
    # App
    app_name: str = "NBA Trade Fit Simulator"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./nba_simulator.db"
    
    # API
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações"""
    return Settings()