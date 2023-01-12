import pytest

from db.models.user import User, UserAlreadyExistsException


class TestUser:
    @pytest.mark.asyncio
    async def test_user_create(self, setup_db):
        engine = setup_db

        # В пустой бд не должно быть пользователя INVALID_EMAIL
        async with engine.begin() as conn:
            assert not await User.exists(conn, 'INVALID_EMAIL')

        # Создание обычного пользователя
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

            assert await User.exists(conn, test_user1['email'])

        # Создание пользователя без first_name, last_name
        test_user2 = {
            'email': 'konnovk2@ya.ru',
            'password': 'qwerty',
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user2
            )
            assert await User.exists(conn, test_user2['email'])

        # Создание пользователя, который уже должен существовать
        async with engine.begin() as conn:
            with pytest.raises(UserAlreadyExistsException):
                await User.create_user(
                    conn,
                    **test_user2
                )

        # Создание пользователя с паролем-числом
        test_user3 = {
            'email': 'konnovk3@ya.ru',
            'password': 12345,
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user3
            )
            assert await User.exists(conn, test_user3['email'])

    @pytest.mark.asyncio
    async def test_user_get(self, setup_db):
        engine = setup_db

        async with engine.begin() as conn:
            # Не созданный пользователь не должен быть в базе
            assert await User.get_by_email(conn, 'INVALID') is None

            # Не созданный пользователь не должен быть в базе
            assert (await User.get_by_email_and_password(conn, 'INVALID', 'INVALID')) is None

        test_user1 = {
            'email': 'konnovk1@ya.ru',
            'password': 'qwerty',
        }

        async with engine.begin() as conn:
            created_user_id = await User.create_user(
                conn,
                **test_user1
            )
            # Созданный пользователь должен быть в базе, его можно получить по мэйлу
            assert (await User.get_by_email(conn, test_user1['email'])).id == created_user_id
            # Созданный пользователь должен быть в базе, его можно получить по мэйлу и паролю
            assert (
                (await User.get_by_email_and_password(conn, test_user1['email'], test_user1['password'])).id
                == created_user_id
            )
            # Неправильный пароль не должен давать пользователя
            assert await User.get_by_email_and_password(conn, test_user1['email'], 'INVALID') is None

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

    @pytest.mark.asyncio
    async def test_user_update(self, setup_db):
        engine = setup_db
        old_password = 'qwerty'
        new_password = 'hackme'
        test_user = {
            'email': 'konnovk1@ya.ru',
            'password': old_password,
            'first_name': 'konnovk1',
            'last_name': 'kon',
        }
        async with engine.begin() as conn:
            await User.create_user(
                conn,
                **test_user
            )
            assert await User.get_by_email_and_password(conn, test_user['email'], old_password) is not None

        async with engine.begin() as conn:
            await User.update_user(
                conn,
                email=test_user['email'],
                password=new_password,
                last_name='IVANOV'
            )
            assert await User.get_by_email_and_password(conn, test_user['email'], new_password) is not None
            assert await User.get_by_email_and_password(conn, test_user['email'], old_password) is None
            assert (await User.get_by_email(conn, test_user['email'])).last_name == 'IVANOV'

        async with engine.begin() as conn:
            invalid_updated_user = await User.update_user(
                conn,
                email='INVALID',
                last_name='IVANOV'
            )
            assert invalid_updated_user is None
