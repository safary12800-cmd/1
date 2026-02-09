from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    TOKEN: str = os.getenv("BOT_TOKEN") or ""

    DB_HOST: str = os.getenv("DB_HOST") or ""
    DB_PORT: int = int(os.getenv("DB_PORT") or "0")
    DB_NAME: str = os.getenv("DB_NAME") or ""
    DB_USER: str = os.getenv("DB_USER") or ""
    DB_PASSWORD: str = os.getenv("DB_PASSWORD") or ""


config = Config()