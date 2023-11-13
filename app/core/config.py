import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=f'{os.path.dirname(os.path.abspath(__file__))}/../../.env',
		env_file_encoding='utf-8',
		extra='ignore'
	)
	API_V1_STR: str = "/api/v1"
	SERVER_HOST: str = "0.0.0.0"
	SERVER_PORT: int = 9090
	CLICKHOUSE_URI: str


settings = Settings()
