import uuid
from aiogram import Router, types, F
from bot.core.parsers import DictionaryJSONParser
from bot.core.dictionary import Dictionary
from bot.core.sessions import DictionarySession, DictionarySessionUser
from database.models import User


router = Router()
dictionary_session = DictionarySession()


@router.inline_query()
async def inline_word(inline_query: types.InlineQuery):
    if not inline_query.query:
        await inline_query.answer([], cache_time=1, is_personal=True)
        return

    dictionary = Dictionary()
    response = dictionary.get_word(inline_query.query)

    if not response:
        await inline_query.answer([
            types.InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Word not found",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"I can't find anything about word <b>{inline_query.query}</b>. Maybe you had misspelled?",
                    parse_mode="HTML"
                )
            )
        ], cache_time=1, is_personal=True)
        return

    if not await User.get(inline_query.from_user.id):
        new_user = User(
            telegram_id=inline_query.from_user.id,
            name=inline_query.from_user.first_name
        )
        await new_user.save()

    parser = DictionaryJSONParser(response)
    meanings = parser.get_meanings()

    dictionary_session_user = DictionarySessionUser(
        user_id=inline_query.from_user.id,
        dictionary_parser=parser,
        meaning_parsers=meanings
    )
    dictionary_session.add_user(dictionary_session_user)

    results = []
    for i, meaning in enumerate(meanings):
        results.append(
            types.InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"{parser.get_word()} — {meaning.get_part_of_speech()}",
                description=meaning.get_definition(),
                input_message_content=types.InputTextMessageContent(
                    message_text=f"<b>Word:</b> <i>{parser.get_word()}</i>\n"
                    f"<b>Phonetic:</b> {parser.get_phonetic()}\n\n"
                    f"<b>Definition:</b> {meaning.get_definition()}\n\n"
                    f"<b>Part of speech:</b> {meaning.get_part_of_speech()}\n\n"
                    f"<b>Example:</b> {meaning.get_example()}\n\n"
                    f"<i>Source:</i> {parser.get_source()}\n\n",
                    parse_mode="HTML"
                )
            )
        )

    await inline_query.answer(results, cache_time=1, is_personal=True)

    user = await User.get(inline_query.from_user.id)
    if inline_query.query not in user.searched_words:
            user.searched_words = user.searched_words + [inline_query.query]
            await user.save()
