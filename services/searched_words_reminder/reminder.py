from database.models import User
import random
import logging


logger = logging.getLogger(__name__)


class ReminderObserver:
    def __init__(self, user: User):
        self.user_id = user.telegram_id
        self.searched_words = user.searched_words

    async def remind(self, bot):
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

    async def remind_all(self, bot):
        for observer in self.reminder_observers:
            await observer.remind(bot)


trigger = ReminderTrigger()
