from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    db: SecretStr

    class Config:
        env_file = 'config.env'
        env_file_encoding = 'utf-8'


config = Settings()
