from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from bot.handlers import handlers, inline_handlers
from bot.config import get_config
import logging


config = get_config()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=config.logger_format)


class BotSingleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=config.parse_mode))
        self.dp = Dispatcher()
        self.is_working = False

        self.add_routers(
            handlers.router,
            inline_handlers.router
        )

    async def start_polling(self):
        if not self.is_working:
            await self.dp.start_polling(self.bot)
            self.is_working = True

    def add_routers(self, *routers: Router):
        self.dp.include_routers(*routers)
