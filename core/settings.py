from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    database_url: str
    access_token_minutes: int
    refresh_token_minutes: int
    algorithm: str
    secret_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Setting()