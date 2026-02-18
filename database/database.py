import asyncpg

from config import config


class Database:
    USER_ROLES = ("admin", "sotuvchi", "buyurtmachi")
    DEFAULT_ROLE = "buyurtmachi"

    def __init__(self):
        self.pool = None

    def _ensure_pool(self):
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
        await self.create_users_table()

    async def create_users_table(self):
        pool = self._ensure_pool()
        allowed_roles_sql = ", ".join(f"'{role}'" for role in self.USER_ROLES)

        await pool.execute(
            f"""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                name TEXT NOT NULL,
                surename TEXT NOT NULL,
                age INT NOT NULL,
                phone TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT '{self.DEFAULT_ROLE}'
            )
            """
        )

        await pool.execute(
            """
            DELETE FROM users a
            USING users b
            WHERE a.telegram_id = b.telegram_id
              AND a.id < b.id
            """
        )
        await pool.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS users_telegram_id_uidx ON users(telegram_id)"
        )
        await pool.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS role TEXT")
        await pool.execute(
            f"""
            UPDATE users
            SET role = '{self.DEFAULT_ROLE}'
            WHERE role IS NULL OR role NOT IN ({allowed_roles_sql})
            """
        )
        await pool.execute(
            f"ALTER TABLE users ALTER COLUMN role SET DEFAULT '{self.DEFAULT_ROLE}'"
        )
        await pool.execute("ALTER TABLE users ALTER COLUMN role SET NOT NULL")
        await pool.execute(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'users_role_check'
                      AND conrelid = 'users'::regclass
                ) THEN
                    ALTER TABLE users DROP CONSTRAINT users_role_check;
                END IF;
            END;
            $$;
            """
        )
        await pool.execute(
            f"""
            ALTER TABLE users
            ADD CONSTRAINT users_role_check
            CHECK (role IN ({allowed_roles_sql}))
            """
        )

    async def add_user(self, telegram_id, name, surename, age, phone, role=None):
        pool = self._ensure_pool()

        selected_role = role if role in self.USER_ROLES else self.DEFAULT_ROLE
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone, role)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (telegram_id)
        DO UPDATE SET
            name = EXCLUDED.name,
            surename = EXCLUDED.surename,
            age = EXCLUDED.age,
            phone = EXCLUDED.phone,
            role = EXCLUDED.role
        """

        await pool.execute(
            query, telegram_id, name, surename, int(age), phone, selected_role
        )

    async def is_user_exists(self, telegram_id: int) -> bool:
        query = """
        SELECT EXISTS (
        SELECT 1 FROM users WHERE telegram_id = $1
        );
        """
        pool = self._ensure_pool()
        return await pool.fetchval(query, telegram_id)

    async def user_profile(self, telegram_id):
        query = """
        SELECT name, surename, age, phone
        FROM users
        WHERE telegram_id = $1;
        """
        pool = self._ensure_pool()
        return await pool.fetchrow(query, telegram_id)

    async def close(self):
        if self.pool is not None:
            await self.pool.close()
