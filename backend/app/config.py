from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=r"../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    POSTGRES_USER:str = ""
    POSTGRES_PASSWORD:str = ""
    POSTGRES_SERVER: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = ""
    SECRET_KEY: str = ""


    @property
    def POSTGRES_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/postgres"

settings = Settings()