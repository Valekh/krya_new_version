from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine


def singleton(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not wrapped.__result:
            wrapped.__result = func(*args, **kwargs)
        return wrapped.__result

    wrapped.__result = None
    return wrapped

@singleton
def engine_factory() -> AsyncEngine:
    return create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/krya",
    )

def session_factory() -> AsyncSession:
    engine = engine_factory()
    return AsyncSession(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )