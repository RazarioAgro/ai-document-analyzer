from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# URL для подключения к базе (в реальности логин/пароль прячут в переменные окружения .env)
# Формат: драйвер://пользователь:пароль@хост:порт/название_базы
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/ai_analyzer"

# Создаем асинхронный движок (engine). 
# echo=True означает, что SQLAlchemy будет печатать в консоль все SQL-запросы, которые генерирует (полезно для отладки).
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий. Будет генерировать нам объекты AsyncSession для работы с БД.
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс, от которого мы будем наследовать все наши модели (таблицы)
Base = declarative_base()

# Зависимость (Dependency) для FastAPI, которая будет выдавать сессию для каждого запроса пользователя
async def get_async_session():
    async with async_session_maker() as session:
        yield session

