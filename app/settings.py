from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    db_user: str
    db_password: SecretStr
    db_name: str
    db_url: PostgresDsn

    jwt_secret_key: SecretStr


settings = Settings()
