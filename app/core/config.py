from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "0.1.0"
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://localhost",
        "https://localhost:3000",
        "https://localhost:8080",
    ]
    SQLALCHEMY_DATABASE_URI: str = None
    LOG_LEVEL: str = "debug"
    FETCH_ARTIST_DELAY: float = 30.0

    # Spotify
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str


settings = Settings()
