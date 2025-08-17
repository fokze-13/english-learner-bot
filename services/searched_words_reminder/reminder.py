from datetime import datetime, timedelta
from database.models import User
from bot.bot import BotSingleton
import asyncio
import random
import logging


logger = logging.getLogger(__name__)


class ReminderObserver:
    def __init__(self, user: User):
        self.user_id = user.telegram_id
        self.searched_words = user.searched_words

    async def remind(self):
        bot = BotSingleton().bot
        word = random.choice(self.searched_words)

        if word:
            await bot.send_message(self.user_id, f'<b>{word}</b>')


class ReminderTrigger:
    def __init__(self):
        self.reminder_observers: list[ReminderObserver] = []

    def get_reminder_observer(self, user: User) -> ReminderObserver:
        return self.reminder_observers[self.reminder_observers.index(ReminderObserver(user))]

    def add_reminder_observer(self, reminder_observer: ReminderObserver):
        self.reminder_observers.append(reminder_observer)

    async def remind_all(self):
        for observer in self.reminder_observers:
            await observer.remind()


INTERVAL = timedelta(seconds=60)

trigger = ReminderTrigger()


async def main_timer():
    next_reminder = datetime.now() + INTERVAL

    while True:
        try:
            if datetime.now() >= next_reminder:
                next_reminder += INTERVAL

                await trigger.remind_all()

            await asyncio.sleep(60)
        except Exception as e:
            logger.error(e)
