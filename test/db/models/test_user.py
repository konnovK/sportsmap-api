from db.data.user import User, UserMapper


async def test_user_create(connection):
    conn = connection
    user_mapper = UserMapper(conn)

    # Создание обычного пользователя
    user1 = User.new(email='user1@example.com', password='hackme', first_name='k', last_name='konnov')
    print(str(user1))
    print(repr(user1))
    inserted_user_id = await user_mapper.save(user1)
    assert inserted_user_id is not None

    # Создание пользователя без first_name, last_name
    user2 = User.new(email='user2@example.com', password='hackme')
    inserted_user_id = await user_mapper.save(user2)
    assert inserted_user_id is not None

    # Создание пользователя, который уже должен существовать
    updated_user_id = await user_mapper.save(user2)
    assert updated_user_id is None

    # Создание пользователя с паролем-числом
    user2 = User.new(email='user3@example.com', password=12345)
    inserted_user_id = await user_mapper.save(user2)
    assert inserted_user_id is not None


async def test_user_get(connection):
    conn = connection
    user_mapper = UserMapper(conn)

    # В пустой бд не должно быть пользователя INVALID_EMAIL
    assert not await user_mapper.get_by_email('INVALID')
    assert not await user_mapper.get_by_email_and_password('INVALID', 'INVALID')

    # Создание обычного пользователя
    user1 = User.new(email='user1@example.com', password='hackme')
    inserted_user_id = await user_mapper.save(user1)
    assert inserted_user_id is not None

    # Созданный пользователь должен быть в базе, его можно получить по мэйлу
    selected_user = await user_mapper.get_by_email('user1@example.com')
    assert selected_user.id == inserted_user_id
    assert hasattr(selected_user, 'email')
    assert hasattr(selected_user, 'password_hash')
    assert hasattr(selected_user, 'first_name')
    assert hasattr(selected_user, 'last_name')

    # Созданный пользователь должен быть в базе, его можно получить по мэйлу и паролю
    selected_user = await user_mapper.get_by_email_and_password('user1@example.com', 'hackme')
    assert selected_user.id == inserted_user_id
    assert hasattr(selected_user, 'email')
    assert hasattr(selected_user, 'password_hash')
    assert hasattr(selected_user, 'first_name')
    assert hasattr(selected_user, 'last_name')

    # Неправильный пароль не должен давать пользователя
    selected_user = await user_mapper.get_by_email_and_password('user1@example.com', 'INVALID')
    assert selected_user is None


async def test_user_delete(connection):
    conn = connection
    user_mapper = UserMapper(conn)

    # Создание обычного пользователя
    user1 = User.new(email='user1@example.com', password='hackme', first_name='k', last_name='konnov')
    inserted_user_id = await user_mapper.save(user1)
    assert inserted_user_id is not None

    # удаление пользователя, которого нет в бд
    user2 = User.new(email='user2@example.com', password='hackme')
    assert await user_mapper.get_by_email('user2@example.com') is None
    await user_mapper.delete(user2)

    # успешное удаление пользователя
    await user_mapper.delete(user1)

    # удаленного пользователя нет в бд
    assert await user_mapper.get_by_email('user1@example.com') is None


async def test_user_update(connection):
    conn = connection
    user_mapper = UserMapper(conn)

    # Создание обычного пользователя
    user1 = User.new(email='user1@example.com', password='hackme', first_name='k', last_name='konnov')
    inserted_user_id = await user_mapper.save(user1)
    assert inserted_user_id is not None

    # обновим поля first_name, last_name
    user1.first_name = 'ilnar'
    user1.last_name = 'mirhaev'
    updated_user_id = await user_mapper.save(user1)
    assert updated_user_id is None
    user = await user_mapper.get_by_email('user1@example.com')
    assert user.first_name == 'ilnar'
    assert user.last_name == 'mirhaev'
