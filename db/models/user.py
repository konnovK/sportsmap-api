from __future__ import annotations

import uuid
from dataclasses import dataclass

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection

from db.schema import users_table, UserGroups
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
            users_table.c.email == email
        ))).first()
        if not selected_user:
            return None

        user_group = selected_user[5]

        user = User(
            id=selected_user[0],
            first_name=selected_user[1],
            last_name=selected_user[2],
            email=selected_user[3],
            password_hash=selected_user[4],
            group=user_group,
        )

        if user.password_hash != password_hash:
            return None

        return user

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
    async def create_user(
            conn: AsyncConnection,
            email: str,
            password: str,
            first_name: str = None,
            last_name: str = None
    ) -> str:
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

    @staticmethod
    async def set_admin(conn: AsyncConnection, email: str):
        await conn.execute(sa.update(users_table).where(users_table.c.email == email).values(group=UserGroups.Admin))

    @staticmethod
    async def set_none_group(conn: AsyncConnection, email: str):
        await conn.execute(sa.update(users_table).where(users_table.c.email == email).values(group=None))

    @staticmethod
    async def check_is_admin(conn: AsyncConnection, email: str):
        user = (await conn.execute(sa.select(users_table).where(users_table.c.email == email))).first()
        return user[5] == UserGroups.Admin

    @staticmethod
    async def update_user(
            conn: AsyncConnection,
            email: str,
            password: str = None,
            first_name: str = None,
            last_name: str = None
    ) -> User | None:
        """
        Обновляет поля password, first_name, last_name у пользователя с email
        :return: Обновленный пользователь, или None, если никого не обновили
        """
        selected_user = (await conn.execute(sa.select(users_table).where(users_table.c.email == email))).first()
        if not selected_user:
            return None
        new_user = {}
        if password:
            new_user['password_hash'] = hash_password(password)
        if first_name:
            new_user['first_name'] = first_name
        if last_name:
            new_user['last_name'] = last_name
        updated_user = (await conn.execute(
            sa.update(users_table).where(users_table.c.email == email).values(**new_user).returning(
                users_table.c.id,
                users_table.c.email,
                users_table.c.first_name,
                users_table.c.last_name,
                users_table.c.password_hash,
                users_table.c.group
            )
        )).first()

        return User(
            id=updated_user[0],
            email=updated_user[1],
            first_name=updated_user[2],
            last_name=updated_user[3],
            password_hash=updated_user[4],
            group=updated_user[5],
        )
