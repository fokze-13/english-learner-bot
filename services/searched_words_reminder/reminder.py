from database.models import User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import logging


logger = logging.getLogger(__name__)


class ReminderObserver:
    def __init__(self, user: User):
        self.user_id = user.telegram_id
        self.searched_words = user.searched_words

    async def remind(self, bot):
        if self.searched_words:
            word = random.choice(self.searched_words)

            await bot.send_message(
                self.user_id,
                f"<b>Let's remind the word!</b>\n"
                "Do you want to try a guess?",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="Guess", callback_data=f"guess_{word}")]]
                )
            )


class ReminderTrigger:
    def __init__(self):
        self.reminder_observers: list[ReminderObserver] = []

    def reminder_in_list(self, user: User) -> ReminderObserver:
        for reminder_observer in self.reminder_observers:
            if reminder_observer.user_id == user.telegram_id:
                return reminder_observer

    def add_reminder_observer(self, reminder_observer: ReminderObserver):
        self.reminder_observers.append(reminder_observer)

    async def remind_all(self, bot):
        for observer in self.reminder_observers:
            await observer.remind(bot)


trigger = ReminderTrigger()
