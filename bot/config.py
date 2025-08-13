from dataclasses import dataclass
from environs import Env


@dataclass
class BotConfig:
    token: str
    logger_format: str
    parse_mode: str


def get_config() -> BotConfig:
    env = Env()
    env.read_env()

    return BotConfig(
        token = env.str("BOT_TOKEN"),
        parse_mode = "HTML",
        logger_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
