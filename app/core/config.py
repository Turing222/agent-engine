from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")
    llm_provider: str = "openai"
    llm_api_key: str = ""
    tavily_api_key: str = ""
    logfire_token: str = ""
    mlops_api_url: str = "http://localhost:8000/v1"

settings = Settings()
