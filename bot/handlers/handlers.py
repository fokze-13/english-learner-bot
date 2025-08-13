from aiogram import Router, types
from aiogram import F
from aiogram.filters import CommandStart
from bot.core.parsers import DictionaryJSONParser
from bot.core.dictionary import Dictionary
from bot.keyboards.inline_kbs import get_meanings_kb


router = Router()


users = {}


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

        #TODO adequate user dict
        users[message.from_user.id] = [parser, meanings, 0]

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
    user = users.get(callback.from_user.id)
    #TODO get rid of warning
    #TODO use variables instead of list indexes
    if user[-1] > 0:
        user[-1] -= 1

        await callback.message.edit_text(
            f"<b>Word:</b> <i>{user[0].get_word()}</i>\n"
            f"<b>Phonetic:</b> {user[0].get_phonetic()}\n\n"
            f"<b>Definition:</b> {user[1][user[-1]].get_definition()}\n\n"
            f"<b>Part of speech:</b> {user[1][user[-1]].get_part_of_speech()}\n\n"
            f"<b>Example:</b> {user[1][user[-1]].get_example()}\n\n"
            f"<i>Source:</i> {user[0].get_source()}\n\n",
            reply_markup=get_meanings_kb(user[-1] + 1)
        )
    else:
        await callback.answer("That's the all!")


@router.callback_query(F.data == "next")
async def next_meaning(callback: types.CallbackQuery):
    user = users.get(callback.from_user.id)
    if user[-1] < 2:
        user[-1] += 1

        await callback.message.edit_text(
            f"<b>Word:</b> <i>{user[0].get_word()}</i>\n"
            f"<b>Phonetic:</b> {user[0].get_phonetic()}\n\n"
            f"<b>Definition:</b> {user[1][user[-1]].get_definition()}\n\n"
            f"<b>Part of speech:</b> {user[1][user[-1]].get_part_of_speech()}\n\n"
            f"<b>Example:</b> {user[1][user[-1]].get_example()}\n\n"
            f"<i>Source:</i> {user[0].get_source()}\n\n",
            reply_markup=get_meanings_kb(user[-1] + 1)
        )
    else:
        await callback.answer("That's the all!")
