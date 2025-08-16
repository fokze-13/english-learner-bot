from database.database_config import database
from database.models import Base
import asyncio


async def init_db(db, base) -> None:
    """Создаёт таблицы в базе данных"""
    engine = await db.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)


if __name__ == '__main__':
    asyncio.new_event_loop().run_until_complete(init_db(database, Base))
