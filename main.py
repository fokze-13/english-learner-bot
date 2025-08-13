from bot.bot import BotSingleton
import asyncio


if __name__ == '__main__':
    bot = BotSingleton()
    asyncio.run(bot.start_polling())
    