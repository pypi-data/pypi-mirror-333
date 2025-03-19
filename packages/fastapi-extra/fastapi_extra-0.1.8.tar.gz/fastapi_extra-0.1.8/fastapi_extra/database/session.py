__author__ = "ziyan.yin"
__date__ = "2025-01-05"


from typing import Annotated, AsyncGenerator, Generator

from fastapi.params import Depends
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_extra.database.driver import DB, AsyncDB


async def get_async_session(db: AsyncDB) -> AsyncGenerator[AsyncSession, None]:
    async with db.session as session:
        yield session
        await session.commit()


def get_session(db: DB) -> Generator[Session, None, None]:
    with db.session as session:
        yield session
        session.commit()


DefaultSession = Annotated[AsyncSession, Depends(get_async_session)]
