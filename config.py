from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def _parse_admin_id(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    if value.isdigit():
        return int(value)
    return None


@dataclass
class Config:
    TOKEN: str = os.getenv("BOT_TOKEN") or ""

    DB_HOST: str = os.getenv("DB_HOST") or ""
    DB_PORT: int = int(os.getenv("DB_PORT") or "0")
    DB_NAME: str = os.getenv("DB_NAME") or ""
    DB_USER: str = os.getenv("DB_USER") or ""
    DB_PASSWORD: str = os.getenv("DB_PASSWORD") or ""
    ADMIN_ID: int | None = _parse_admin_id(os.getenv("ADMIN_ID"))


config = Config()
