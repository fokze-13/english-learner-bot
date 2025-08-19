from aiogram import Router, types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from bot.core.parsers import DictionaryJSONParser
from bot.core.dictionary import Dictionary
from bot.keyboards.inline_kbs import get_meanings_kb
from bot.core.sessions import DictionarySession, DictionarySessionUser
from fsm.question_fsm import QuestionFSM
from services.searched_words_reminder.reminder import ReminderObserver, trigger
from database.models import User


router = Router()
dictionary_session = DictionarySession()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("<b>Hello!</b>\nWrite me a word in English, and I will answer you with the definition of it!")

    if not await User.get(message.from_user.id):
        new_user = User(
            telegram_id=message.from_user.id,
            name=message.from_user.first_name,
        )
        await new_user.save()

    if not trigger.reminder_in_list(user := await User.get(message.from_user.id)):
        reminder_observer = ReminderObserver(user)
        trigger.add_reminder_observer(reminder_observer)


@router.message(Command("stats"))
async def stats(message: types.Message):
    user = await User.get(message.from_user.id)
    questions = user.questions

    if user.questions == 0:
        questions = 1
    correct_answers_percent = round(user.answers / questions, 2) * 100

    await message.answer(
        f"<b>Your statistics</b>\n\n"
        f"Searched words: {len(user.searched_words)}\n"
        f"Total questions: {questions}\n"
        f"Total correct answers: {user.answers}\n"
        f"Correct answers per question: {correct_answers_percent}%"
    )


@router.callback_query(F.data.split("_")[0] == "guess")
async def word_guess(callback: types.CallbackQuery, state: FSMContext):
    guessing_word = callback.data.split("_")[1]

    dictionary = Dictionary()
    response = dictionary.get_word(guessing_word)

    if response:
        parser = DictionaryJSONParser(response)
        meaning = parser.get_meanings()[0]

        await state.update_data(guessing_word = guessing_word)
        await state.set_state(QuestionFSM.guessing)
        await callback.message.answer(
            f"<b>Definition</b>: {meaning.get_definition()}\n\n"
            f"<b>Part of speech</b>: {meaning.get_part_of_speech()}\n\n"
            "What is the word?"
        )


@router.message(F.text, QuestionFSM.guessing)
async def guess(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user = await User.get(message.from_user.id)
    user.questions += 1

    guessing_word = data["guessing_word"]

    if message.text == guessing_word:
        await message.answer(f"Correct! The word is <b>{guessing_word}</b>!")
        user.answers += 1
    else:
        await message.answer(f"Incorrect, the word is <b>{guessing_word}</b>!\nTry better next time!")


    await state.clear()
    await user.save()


@router.message(F.text)
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

        user = await User.get(message.from_user.id)

        if message.text not in user.searched_words:
            user.searched_words = user.searched_words + [message.text]
            await user.save()

        await message.answer(
            f"<b>Word:</b> <i>{parser.get_word()}</i>\n"
            f"<b>Phonetic:</b> {parser.get_phonetic()}\n\n"
            f"<b>Definition:</b> {meanings[0].get_definition()}\n\n"
            f"<b>Part of speech:</b> {meanings[0].get_part_of_speech()}\n\n"
            f"<b>Example:</b> {meanings[0].get_example()}\n\n"
            f"<i>Source:</i> {parser.get_source()}\n\n",
            reply_markup=get_meanings_kb(0) if len(meanings) > 1 else None
        )
    else:
        await message.answer(
            f"I can't find anything about word <b>{message.text}</b>. Maybe you had misspelled?"
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
