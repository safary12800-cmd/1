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
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT NOW()
        )
        """

        add_role_column_query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'user'
        """

        set_role_default_query = """
        ALTER TABLE users
        ALTER COLUMN role SET DEFAULT 'user'
        """

        normalize_roles_query = """
        UPDATE users
        SET role = CASE
            WHEN role IS NULL OR BTRIM(role) = '' THEN 'user'
            WHEN LOWER(role) = 'buyurtmachi' THEN 'user'
            WHEN LOWER(role) = 'admin' THEN 'admin'
            WHEN LOWER(role) = 'sotuvchi' THEN 'sotuvchi'
            WHEN LOWER(role) = 'user' THEN 'user'
            ELSE 'user'
        END
        """

        drop_role_check_query = """
        ALTER TABLE users
        DROP CONSTRAINT IF EXISTS users_role_check
        """

        add_role_check_query = """
        ALTER TABLE users
        ADD CONSTRAINT users_role_check
        CHECK (role IN ('admin', 'sotuvchi', 'user'))
        """

        await pool.execute(create_query)
        await pool.execute(add_role_column_query)
        await pool.execute(set_role_default_query)
        await pool.execute(normalize_roles_query)
        await pool.execute(drop_role_check_query)
        await pool.execute(add_role_check_query)
        if config.ADMIN_ID is not None:
            await pool.execute(
                "UPDATE users SET role = 'admin' WHERE telegram_id = $1",
                config.ADMIN_ID,
            )

    async def add_user(
        self,
        telegram_id: int,
        name: str,
        surename: str,
        age: int,
        phone: str,
    ):
        role = "admin" if config.ADMIN_ID is not None and telegram_id == config.ADMIN_ID else "user"
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone, role)
        VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self._pool().execute(query, telegram_id, name, surename, int(age), phone, role)

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
    async def get_user_role(self,telegram_id):
        query = "SELECT role FROM users WHERE telegram_id=$1"
        return await self._pool().fetchval(query, telegram_id)
    
    async def get_users(self):
        query = "SELECT telegram_id, name, role FROM users ORDER BY id"
        return await self._pool().fetch(query)
    
    async def set_user_role(self, telegram_id, role):
        query = "UPDATE users SET role=$1 WHERE telegram_id=$2"
        await self._pool().execute(query, role, telegram_id)

    async def get_products(self):
        query = "SELECT * FROM products WHERE is_active=TRUE"
        return await self._pool().fetch(query)
    async def get_products_admin(self):
        query = "SELECT * FROM products WHERE is_active=TRUE"
        return await self._pool().fetch(query)