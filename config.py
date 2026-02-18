import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _parse_int_env(name: str) -> Optional[int]:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return None

    try:
        return int(raw_value)
    except ValueError:
        return None


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or ""
    START_STICKER_ID: str = os.getenv("START_STICKER_ID") or ""
    REGISTER_START_STICKER_ID: str = os.getenv("REGISTER_START_STICKER_ID") or ""
    REGISTER_SUCCESS_STICKER_ID: str = os.getenv("REGISTER_SUCCESS_STICKER_ID") or ""

    DB_HOST: str = os.getenv("DB_HOST") or ""
    DB_PORT: int = _parse_int_env("DB_PORT") or 5432
    DB_NAME: str = os.getenv("DB_NAME") or "bot2"
    DB_USER: str = os.getenv("DB_USER") or ""
    DB_PASSWORD: str = os.getenv("DB_PASSWORD") or ""
    ADMIN_ID: Optional[int] = _parse_int_env("ADMIN_ID")

    @property
    def TOKEN(self) -> str:
        return self.BOT_TOKEN


config = Config()
