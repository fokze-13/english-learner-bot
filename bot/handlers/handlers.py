from aiogram import Router, types
from aiogram import F
from aiogram.filters import CommandStart
from bot.core.parsers import DictionaryJSONParser
from bot.core.dictionary import Dictionary
from bot.keyboards.inline_kbs import get_meanings_kb
from bot.core.sessions import DictionarySession, DictionarySessionUser


router = Router()
dictionary_session = DictionarySession()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("<b>Hello!</b>\nWrite me a word in English, and I will answer you with the definition of it!")


@router.message(F.text)
@router.message(lambda x: len(x.text.split()) == 1)
async def word(message: types.Message):
    dictionary = Dictionary()
    response = dictionary.get_word(message.text)

    if response:
        parser = DictionaryJSONParser(response)
        meanings = parser.get_meanings()

        dictionary_session_user = DictionarySessionUser(
            user_id=message.from_user.id,
            dictionary_parser=parser,
            meaning_parsers=meanings
        )
        dictionary_session.add_user(dictionary_session_user)

        await message.answer(
            f"<b>Word:</b> <i>{parser.get_word()}</i>\n"
            f"<b>Phonetic:</b> {parser.get_phonetic()}\n\n"
            f"<b>Definition:</b> {meanings[0].get_definition()}\n\n"
            f"<b>Part of speech:</b> {meanings[0].get_part_of_speech()}\n\n"
            f"<b>Example:</b> {meanings[0].get_example()}\n\n"
            f"<i>Source:</i> {parser.get_source()}\n\n",
            reply_markup=get_meanings_kb(1) if len(meanings) > 1 else None
        )


@router.callback_query(F.data == "prev")
async def prev_meaning(callback: types.CallbackQuery):
    dictionary_session_user = dictionary_session.get_session_user(callback.from_user.id)
    dictionary_session_user.prev_page()

    await callback.message.edit_text(
        f"<b>Word:</b> <i>{dictionary_session_user.dictionary_parser.get_word()}</i>\n"
        f"<b>Phonetic:</b> {dictionary_session_user.dictionary_parser.get_phonetic()}\n\n"
        f"<b>Definition:</b> {dictionary_session_user.get_meaning().get_definition()}\n\n"
        f"<b>Part of speech:</b> {dictionary_session_user.get_meaning().get_part_of_speech()}\n\n"
        f"<b>Example:</b> {dictionary_session_user.get_meaning().get_example()}\n\n"
        f"<i>Source:</i> {dictionary_session_user.dictionary_parser.get_source()}\n\n",
        reply_markup=get_meanings_kb(dictionary_session_user.meaning_page)
    )


@router.callback_query(F.data == "next")
async def next_meaning(callback: types.CallbackQuery):
    dictionary_session_user = dictionary_session.get_session_user(callback.from_user.id)
    dictionary_session_user.next_page()

    await callback.message.edit_text(
        f"<b>Word:</b> <i>{dictionary_session_user.dictionary_parser.get_word()}</i>\n"
        f"<b>Phonetic:</b> {dictionary_session_user.dictionary_parser.get_phonetic()}\n\n"
        f"<b>Definition:</b> {dictionary_session_user.get_meaning().get_definition()}\n\n"
        f"<b>Part of speech:</b> {dictionary_session_user.get_meaning().get_part_of_speech()}\n\n"
        f"<b>Example:</b> {dictionary_session_user.get_meaning().get_example()}\n\n"
        f"<i>Source:</i> {dictionary_session_user.dictionary_parser.get_source()}\n\n",
        reply_markup=get_meanings_kb(dictionary_session_user.meaning_page)
    )
