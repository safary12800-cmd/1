import asyncpg
from config import config
class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT
        )

    async def add_user(self, telegram_id, name, surename, age, phone):
        query = """
        INSERT INTO users (telegram_id, name, surename, age, phone)
        VALUES ($1, $2, $3, $4, $5)
        """
        
        if self.pool is None:
            raise RuntimeError("data base bilan aloqa o'rnatilmagan")

        await self.pool.execute(
            query, telegram_id, name, surename, int(age), phone
        )
