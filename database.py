import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

_pool: asyncpg.Pool | None = None


async def init_db():
    """
    Инициализируй пул 1 раз при старте бота.
    """
    global _pool
    if _pool is not None:
        return

    _pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        min_size=1,
        max_size=10,
        command_timeout=10)


async def close_db():
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def _get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("DB pool not initialized. Call init_db() first.")
    return _pool


async def get_info_in_db(telegram_id: int):
    """
    Возвращает (state, found) как у тебя:
      state: str ('' если нет записи)
      found: bool
    """
    q = """
    SELECT
        COALESCE(s.state, '') AS state,
        (s.tg_id IS NOT NULL) AS found
    FROM (
        SELECT tg_id, state
        FROM "Kaspi".tg_driver_state
        WHERE tg_id = $1
        LIMIT 1
    ) s
    RIGHT JOIN (SELECT 1) dummy ON TRUE;
    """
    row = await _get_pool().fetchrow(q, telegram_id)
    return row["state"], row["found"]


async def insert_first_data(user_id: int):
    """
    Вставляет начальную запись.
    asyncpg сам коммитит каждый отдельный запрос.
    """
    q = """
    INSERT INTO "Kaspi".tg_driver_state(tg_id, state, order_id, updated_at, kaspi_order_id)
    VALUES ($1, 'WAIT_ORDER', NULL, NULL, NULL);
    """
    await _get_pool().execute(q, user_id)