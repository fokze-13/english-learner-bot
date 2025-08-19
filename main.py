from bot.bot import BotSingleton
from datetime import datetime, timedelta
from services.searched_words_reminder.reminder import trigger
import asyncio
import logging


logger = logging.getLogger(__name__)

bot = BotSingleton()

INTERVAL = timedelta(minutes=10)


async def main_timer():
    next_reminder = datetime.now() + INTERVAL

    while True:
        try:
            if datetime.now() >= next_reminder:
                next_reminder += INTERVAL

                await trigger.remind_all(bot.bot)

            await asyncio.sleep(600)
        except Exception as e:
            logger.error(e)



async def main():
    await asyncio.gather(
        bot.start_polling(),
        main_timer()
    )


if __name__ == '__main__':
    asyncio.run(main())
    