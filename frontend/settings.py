import pathlib
from functools import lru_cache
from typing import Union
import os
from aiohttp import ClientTimeout
from pydantic import validator, BaseSettings

BASE_DIR = pathlib.Path(__file__).parent


class EnvSettings(BaseSettings):
    class Config(BaseSettings.Config):
        if os.environ.get("STAGE", "DEV") == "DEV":
            env_file = "../.env"


class BotSettings(EnvSettings):
    BOT_API_TOKEN: str


class RedisSettings(EnvSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def storage_config(self) -> dict:
        return {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
        }

    @property
    def dsn(self) -> str:
        return f"redis://{self.REDIS_HOST}/"


class HTTPSettings(EnvSettings):
    RAISE_FOR_STATUS: bool = True
    TIMEOUT: Union[float, ClientTimeout] = ClientTimeout(10)

    @validator("TIMEOUT")
    def timeout_to_correct_class(cls, v) -> ClientTimeout:
        if isinstance(v, ClientTimeout):
            return v
        return ClientTimeout(v)

    MAX_TRIES: int = 2
    MAX_TIME: int = 10

    class Config(BaseSettings.Config):
        arbitrary_types_allowed = True


class Settings:
    bot: BotSettings = BotSettings()
    redis: RedisSettings = RedisSettings()
    http: HTTPSettings = HTTPSettings()


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    return Settings()
