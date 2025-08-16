from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
)
from database.config import get_config


config = get_config()


class Database:
    def __init__(self, db_name: str, host: str, user: str,
                 password: str, port: int, echo: bool = False) -> None:
        self.db_name = db_name
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker | None = None
        self.echo = echo

    async def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            url = f"postgresql+asyncpg://{self.user}:{quote_plus(self.password)}@" \
                  f"{self.host}:{self.port}/{self.db_name}"
            self._engine = create_async_engine(
                url, echo=self.echo, pool_size=10, max_overflow=20
            )
        return self._engine

    async def get_session(self) -> AsyncSession:
        if self._session_factory is None:
            engine = await self.get_engine()
            self._session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
        return self._session_factory()

    async def get_db(self):
        """Контекстный менеджер для получения сессии"""
        async with (await self.get_session()) as session:
            yield session


database = Database(
    db_name=config.database_name,
    host=config.database_host,
    user=config.database_user,
    password=config.database_password,
    port=config.database_port,
    echo=False,
)
