from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection

from db.schema import users_table
from db.utils import hash_password


@dataclass
class User:
    id: str
    first_name: str | None
    last_name: str | None
    email: str
    password_hash: str
    group: str | None

    @staticmethod
    async def get_by_email_and_password(conn: AsyncConnection, email: str, password: str) -> User | None:
        """
        Получение из БД юзера по email и password_hash.
        Вернет None, если такого юзера нет.
        """
        password_hash = hash_password(password)
        selected_user = (await conn.execute(sa.select(users_table).where(
            users_table.c.email == email and users_table.c.password_hash == password_hash
        ))).first()
        if not selected_user:
            return None

        user_group = selected_user[5]

        return User(
            id=selected_user[0],
            first_name=selected_user[1],
            last_name=selected_user[2],
            email=selected_user[3],
            password_hash=selected_user[4],
            group=user_group,
        )

    @staticmethod
    async def get_by_email(conn: AsyncConnection, email: str) -> User | None:
        """
        Получение из БД юзера по email и password_hash.
        Вернет None, если такого юзера нет.
        """
        selected_user = (await conn.execute(sa.select(users_table).where(users_table.c.email == email))).first()
        if not selected_user:
            return None

        user_group = selected_user[5]

        return User(
            id=selected_user[0],
            first_name=selected_user[1],
            last_name=selected_user[2],
            email=selected_user[3],
            password_hash=selected_user[4],
            group=user_group,
        )

    @staticmethod
    async def create_user(conn: AsyncConnection, first_name: str, last_name: str, email: str, password: str) -> str:
        """
        Создает в БД пользователя.
        :returns: id созданного пользователя
        """
        user_id = str(uuid.uuid4())
        password_hash = hash_password(password)
        await conn.execute(
            sa.insert(users_table).values(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash
            )
        )
        return user_id

    @staticmethod
    async def exists(conn: AsyncConnection, email: str) -> bool:
        """
        Проверяет, есть ли в БД пользователь с таким email.
        """
        existed_users = await conn.execute(sa.select(users_table).where(users_table.c.email == email))
        if len(existed_users.all()) > 0:
            return True
        return False

    @staticmethod
    async def delete_by_email(conn: AsyncConnection, email: str):
        """
        Удаляет пользователя по его email.
        """
        await conn.execute(sa.delete(users_table).where(users_table.c.email == email))
