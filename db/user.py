from __future__ import annotations

import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .schema import Base
from utils import hash_password


class User(Base):
    __tablename__ = 'users'

    id = sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = sa.Column('first_name', sa.String)
    last_name = sa.Column('last_name', sa.String)
    email = sa.Column('email', sa.String, nullable=False, unique=True)
    password_hash = sa.Column('password_hash', sa.String, nullable=False)

    created_at = sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now())
    updated_at = sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())

    ix_id = sa.Index('ix__users__id', id, postgresql_using='hash')

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.password_hash = hash_password(kwargs.get('password'))

    def check_password(self, password: str):
        return self.password_hash == hash_password(password)

    @staticmethod
    def hash_password(password: str):
        return hash_password(password)

    @staticmethod
    async def get_by_email_and_password(session: AsyncSession, email: str, password: str) -> User | None:
        user = (
            await session.execute(
                sa.select(User)
                .where(User.email == email)
                .where(User.password_hash == User.hash_password(password))
            )
        ).scalars().first()
        return user

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        user = (
            await session.execute(
                sa.select(User)
                .where(User.email == email)
            )
        ).scalars().first()
        return user

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str) -> User | None:
        user = (
            await session.execute(
                sa.select(User)
                .where(User.id == id)
            )
        ).scalars().first()
        return user
