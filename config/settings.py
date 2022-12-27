from pydantic import BaseSettings

# import the .env in the root directory
from dotenv import load_dotenv
import os

load_dotenv()


class CommonSettings(BaseSettings):
    APP_NAME: str = "aq-experi"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int | str | None = int(os.environ.get("PORT"))  # type: ignore TODO: the port is broken, and the app defaults to using 8000 as in the library code


class DatabaseSettings(BaseSettings):
    DB_URL: str | None
    DB_NAME: str | None


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings(
    DB_NAME=os.getenv("DB_NAME"),
    DB_URL=os.getenv("DB_URL"),  # type: ignore
)
# print("settings object created")
