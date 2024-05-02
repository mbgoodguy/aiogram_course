import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str = os.getenv('TOKEN')
    admin_ids: frozenset[int] = frozenset({1063870782})


settings = Settings()
