from dataclasses import dataclass
from environs import Env


@dataclass(frozen=True)
class DatabaseConfig:
    database_name: str
    database_password: str
    database_host: str
    database_port: int
    database_user: str


def get_config() -> DatabaseConfig:
    env = Env()
    env.read_env()

    return DatabaseConfig(
        database_name=env.str("DB_NAME"),
        database_password=env.str("DB_PASSWORD"),
        database_host=env.str("DB_URL"),
        database_port=env.int("DB_PORT"),
        database_user=env.str("DB_USER"),
    )
