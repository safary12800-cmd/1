import asyncpg

from config import config


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    def _pool(self) -> asyncpg.Pool:
        if self.pool is None:
            raise RuntimeError("Database bilan aloqa o'rnatilmagan")
        return self.pool

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )
        await self.create_tables()

    async def create_tables(self):
        pool = self._pool()

        create_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            surename TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT '',
            created_at TIMESTAMP DEFAULT NOW()
        )
        """

        alter_query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'user'
        """

        await pool.execute(create_query)
        await pool.execute(alter_query)

    async def add_user(
        self,
        telegram_id: int,
        name: str,
        surename: str,
        age: int,
        phone: str,
    ):
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone)
        VALUES ($1, $2, $3, $4, $5)
        """
        await self._pool().execute(query, telegram_id, name, surename, int(age), phone)

    async def is_user_exists(self, telegram_id: int) -> bool:
        query = """
        SELECT EXISTS (
            SELECT 1 FROM users WHERE telegram_id = $1
        )
        """
        return await self._pool().fetchval(query, telegram_id)

    async def get_user_by_telegram_id(self, telegram_id: int):
        query = """
        SELECT telegram_id, name, surename, age, phone, role
        FROM users
        WHERE telegram_id = $1
        """
        return await self._pool().fetchrow(query, telegram_id)
