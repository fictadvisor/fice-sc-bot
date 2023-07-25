from typing import Optional

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    TOKEN: SecretStr

    POSTGRES_HOST: str
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=(".env", "stack.env"), extra="ignore")


settings = Settings()
