import requests
import logging


logger = logging.getLogger(__name__)


class Dictionary:
    def __init__(self):
        self.__base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    def get_word(self, word: str) -> str | None:
        try:
            response = requests.get(self.__base_url.format(word=word.lower()))
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.error(e)
