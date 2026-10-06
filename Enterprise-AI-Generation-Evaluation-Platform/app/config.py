from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql://aigen:aigenpassword@localhost:5436/aigen"
    ollama_url: str = "http://localhost:11434"
    default_model: str = "llama3.2:latest"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    prompt_version: int = 1
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
