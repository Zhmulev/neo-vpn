from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "default-secret-key-change-me"
    DATABASE_URL: str = "sqlite:///./vpn_proxy.db"
    TELEGRAM_BOT_TOKEN: str = ""
    BACKEND_URL: str = "http://127.0.0.1:8000"

    # 3x-ui Panel
    PANEL_URL: str = "http://127.0.0.1:54321"
    PANEL_USERNAME: str = "admin"
    PANEL_PASSWORD: str = "admin"
    DEFAULT_VLESS_INBOUND_ID: int = 1

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()