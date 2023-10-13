from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # возвращение адреса БД
    @property
    def get_database_url(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:'
                f'{self.DB_PASS}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}'
        )
    

    # Данные для тестовой БД
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    # возвращение адреса тестовой БД
    @property
    def get_test_database_url(self):
        return (f'postgresql+asyncpg://{self.TEST_DB_USER}:'
                f'{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:'
                f'{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        )

    # указание файла с закрытыми данными для подключения к ДБ
    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str 
    ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int


settings = Settings()

