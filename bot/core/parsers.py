import json
import logging


logger = logging.getLogger(__name__)


class MeaningParser:
    def __init__(self, meaning: dict):
        self.meaning = meaning

    def get_definition(self) -> str | None:
        try:
            return self.meaning.get('definitions')[0].get('definition')
        except Exception as e:
            logger.error(e)

    def get_part_of_speech(self) -> str | None:
        try:
            return self.meaning.get('partOfSpeech')
        except Exception as e:
            logger.error(e)

    def get_example(self) -> str | None:
        try:
            return self.meaning.get('definitions')[0].get('example')
        except Exception as e:
            logger.error(e)



class DictionaryJSONParser:
    def __init__(self, dictionary_resp: str):
        self.json_response = json.loads(dictionary_resp)

    def get_word(self) -> str | None:
        try:
            return self.json_response[0].get('word').capitalize()
        except Exception as e:
            logger.error(e)

    def get_phonetic(self) -> str | None:
        try:
            return self.json_response[0].get('phonetic')
        except Exception as e:
            logger.error(e)

    def get_source(self) -> str | None:
        try:
            return self.json_response[0].get('sourceUrls')[0]
        except Exception as e:
            logger.error(e)

    def get_meanings(self) -> list[MeaningParser] | None:
        try:
            meanings = []
            for meaning in self.json_response[0].get('meanings'):
                meanings.append(MeaningParser(meaning))
            return meanings
        except Exception as e:
            logger.error(e)
