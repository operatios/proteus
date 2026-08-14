from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_URL: PostgresDsn
    REDIS_URL: RedisDsn

    SQL_ECHO: bool

    JWT_SECRET_KEY: SecretStr
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
