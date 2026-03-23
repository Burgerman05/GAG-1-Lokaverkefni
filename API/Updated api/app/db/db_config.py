from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    db_username: str = "username"
    db_password: str = "password"
    db_port: int = 5432
    db_name: str = "db_name"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


db_config = DBConfig()
