from bot.bot import BotSingleton
from services.searched_words_reminder.reminder import main_timer
import asyncio


async def main():
    bot = BotSingleton()

    await asyncio.gather(
        bot.start_polling(),
        main_timer()
    )


if __name__ == '__main__':
    asyncio.run(main())
    