from aiogram.filters import BaseFilter
from aiogram.types import Message

class RoleFilter(BaseFilter):
    def __init__(self, role: str):
        self.role = role

    async def __call__(self, message: Message, db):
        if message.from_user is None:
            return False
        role = await db.get_user_role(message.from_user.id)
        return role == self.role