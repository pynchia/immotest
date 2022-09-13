from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "0.1.0"
    LOGGING_LEVEL: str = "INFO"
    SQLALCHEMY_DATABASE_URI: str = None


settings = Settings()
