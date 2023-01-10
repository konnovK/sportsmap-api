import asyncio

import pytest

from api_config import get_config
from db.models.user import User
from db.schema import metadata
from db.utils import get_db_engine
from test import TEST_DB_NAME


@pytest.fixture()
def loop():
    return asyncio.get_event_loop()


@pytest.fixture()
async def setup_db(loop):
    config = get_config()
    config.API_DB_USER = 'user123'
    config.API_DB_PASSWORD = '123'
    config.API_DB_HOST = 'localhost'
    config.API_DB_PORT = 5432
    config.API_DB_NAME = TEST_DB_NAME
    engine = await get_db_engine(config)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


class TestUser:
    @pytest.mark.asyncio
    async def test_user_create(self, setup_db):
        engine = setup_db

        async with engine.begin() as conn:
            assert not await User.exists(conn, 'INVALID_EMAIL'), 'В пустой бд не должно быть пользователя INVALID_EMAIL'

        test_user1 = {
            'email': 'konnovk1@ya.ru',
            'password': 'qwerty',
            'first_name': 'konnovk1',
            'last_name': 'kon',
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user1
            )
            assert await User.exists(conn, test_user1['email']), 'Создали пользователя, он должен существовать'
            assert not await User.get_by_email(conn, test_user1['email']) is None
            assert (
                    (await User.get_by_email(conn, test_user1['email'])).email ==
                    (await User.get_by_email_and_password(conn, test_user1['email'], test_user1['password'])).email
            )

        test_user2 = {
            'email': 'konnovk2@ya.ru',
            'password': 'qwerty',
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user2
            )
            assert await User.exists(conn, test_user2['email']), \
                'Пользователь без first_name, last_name должен существовать'
            assert not await User.get_by_email(conn, test_user2['email']) is None
            assert (
                    (await User.get_by_email(conn, test_user2['email'])).email ==
                    (await User.get_by_email_and_password(conn, test_user2['email'], test_user2['password'])).email
            )

    @pytest.mark.asyncio
    async def test_user_delete(self, setup_db):
        engine = setup_db
        test_user = {
            'email': 'konnovk1@ya.ru',
            'password': 'qwerty',
            'first_name': 'konnovk1',
            'last_name': 'kon',
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user
            )

            assert await User.exists(conn, test_user['email'])
            await User.delete_by_email(conn, test_user['email'])
            assert not await User.exists(conn, test_user['email'])

        async with engine.begin() as conn:
            await User.delete_by_email(conn, 'INVALID_EMAIL')

    @pytest.mark.asyncio
    async def test_user_set_admin(self, setup_db):
        engine = setup_db
        test_user = {
            'email': 'konnovk1@ya.ru',
            'password': 'qwerty',
            'first_name': 'konnovk1',
            'last_name': 'kon',
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user
            )
            # Сначала пользователь не имеет групп
            assert not await User.check_is_admin(conn, test_user['email'])

            # Сделаем его админом
            await User.set_admin(conn, test_user['email'])
            assert await User.check_is_admin(conn, test_user['email'])

            # Уберем ему группу
            await User.set_none_group(conn, test_user['email'])
            assert not await User.check_is_admin(conn, test_user['email'])
