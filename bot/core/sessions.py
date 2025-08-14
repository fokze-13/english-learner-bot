from abc import ABC, abstractmethod
from bot.core.parsers import MeaningParser, DictionaryJSONParser


class SessionUser(ABC):
    @abstractmethod
    def __init__(self):
        pass


class Session(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_user(self, user: SessionUser):
        pass

    @abstractmethod
    def get_session_user(self, user_id: int) -> SessionUser:
        pass




class DictionarySessionUser(SessionUser):
    def __init__(self,
                 user_id: int,
                 dictionary_parser: DictionaryJSONParser,
                 meaning_parsers: list[MeaningParser]):
        self.user_id = user_id
        self.dictionary_parser = dictionary_parser
        self.meaning_parsers = meaning_parsers
        self.meaning_page = 0

    def prev_page(self):
        if self.meaning_page > 0:
            self.meaning_page -= 1

    def next_page(self):
        if self.meaning_page < len(self.meaning_parsers) - 1:
            self.meaning_page += 1

    def get_meaning(self) -> MeaningParser:
        return self.meaning_parsers[self.meaning_page]


class DictionarySession(Session):
    def __init__(self):
        super().__init__()
        self.users: dict[int, DictionarySessionUser] = {}

    def add_user(self, user: DictionarySessionUser):
        self.users[user.user_id] = user

    def get_session_user(self, user_id: int) -> DictionarySessionUser:
        return self.users[user_id]
