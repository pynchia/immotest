from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "0.1.0"
    LOGGING_LEVEL: str = "INFO"
    SQLALCHEMY_DATABASE_URI: str = None

    # Spotify
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str


settings = Settings()
