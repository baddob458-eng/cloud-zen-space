from pydantic_settings import BaseSettings   # ✅ new location

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ncloud.db"
    SECRET_KEY: str = "change_this_secret_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
