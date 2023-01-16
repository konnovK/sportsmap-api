from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa

from db.data.mapper import Mapper
from db.data.record import Record
from db.schema import users_table
from db.utils import hash_password


@dataclass
class User(Record):
    """
    Класс сущности БД user
    """
    id: str
    email: str
    password_hash: str
    first_name: str | None
    last_name: str | None

    def __repr__(self):
        return f'User(email={self.email})'

    def __str__(self):
        return f'User(email={self.email})'

    def dict(self) -> dict[str, Any]:
        res = {}
        if self.id:
            res['id'] = self.id
        if self.email:
            res['email'] = self.email
        if self.password_hash:
            res['password_hash'] = self.password_hash
        if self.first_name:
            res['first_name'] = self.first_name
        if self.last_name:
            res['last_name'] = self.last_name
        return res

    @staticmethod
    def from_dict(as_dict) -> User:
        return User(
            id=as_dict.get('id'),
            email=as_dict.get('email'),
            password_hash=as_dict.get('password_hash'),
            first_name=as_dict.get('first_name'),
            last_name=as_dict.get('last_name'),
        )

    @staticmethod
    def new(email: str, password: str, first_name: str | None = None, last_name: str | None = None) -> User:
        id = str(uuid.uuid4())
        password_hash = hash_password(password)
        return User(
            id=id,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )

    def set_password(self, password: str):
        self.password_hash = hash_password(password)


class UserMapper(Mapper):
    """
    DataMapper для сущности user
    """
    def __init__(self, conn: AsyncConnection):
        super().__init__(conn)

    async def save(self, user: User) -> str | None:
        """
        Сохраняет пользователя в БД. Если его там не было, то он создается, если он там был, то обновляется.

        Возвращает id пользователя, если он был добавлен в БД, или None, если он был обновлен в БД
        """
        select_id_stmt = sa.select(users_table.c.id).where(users_table.c.id == user.id)
        selected_user = await self._execute_then_first(select_id_stmt)
        if not selected_user:
            insert_user_stmt = sa.insert(users_table).values(**user.dict()).returning(users_table.c.id)
            inserted_user = await self._execute_then_first(insert_user_stmt)
            return inserted_user._mapping['id']
        else:
            update_user_stmt = sa.update(users_table).where(users_table.c.email == user.email).values(**user.dict())
            await self._execute(update_user_stmt)
            return None

    async def get_by_email(self, email: str) -> User | None:
        stmt = sa.select(users_table).where(users_table.c.email == email)
        selected = await self._execute_then_first(stmt)
        if selected:
            return User.from_dict(selected._mapping)
        return None

    async def get_by_email_and_password(self, email: str, password: str) -> User | None:
        password_hash = hash_password(password)
        stmt = sa.select(users_table)\
            .where(users_table.c.email == email)\
            .where(users_table.c.password_hash == password_hash)
        selected = await self._execute_then_first(stmt)
        if selected:
            return User.from_dict(selected._mapping)
        return None

    async def delete(self, user: User) -> None:
        stmt = sa.delete(users_table).where(users_table.c.email == user.email)
        await self._execute(stmt)
