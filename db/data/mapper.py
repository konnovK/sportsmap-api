from typing import Any

from sqlalchemy.engine import Row, Result
from sqlalchemy.ext.asyncio import AsyncConnection


class Mapper:
    """
    Базовый класс DataMapper
    """
    _conn: AsyncConnection

    def __init__(self, conn: AsyncConnection):
        self._conn = conn

    async def _execute(self, stmt) -> None:
        await self._conn.execute(stmt)

    async def _execute_then_first(self, stmt) -> Row:
        res: Result = (await self._conn.execute(stmt))
        row: Row = res.first()
        return row

    async def _execute_then_all(self, stmt) -> list[Row]:
        res: Result = (await self._conn.execute(stmt))
        rows: list[Row] = res.all()
        return rows

    async def save(self, obj: Any) -> Any | None:
        raise NotImplementedError

    async def delete(self, obj: Any) -> None:
        raise NotImplementedError
