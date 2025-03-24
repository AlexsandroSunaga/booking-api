from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Transfer Booking API"
    market: str = "default"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    default_currency: str = "GBP"


settings = Settings()
