"""
Инициализация БД для окружения разработки (не прода)
"""

import asyncio

from api_config import get_config
from db.utils import debug_db_init


async def main():
    config = get_config()
    config.API_DEBUG_MODE = True
    await debug_db_init(config)


if __name__ == '__main__':
    asyncio.run(main())
