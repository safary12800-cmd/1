# OrderlyBot

Telegram bot with registration and profile flow (aiogram + PostgreSQL).

## Features
- User registration flow with validation
- Profile view (`Profile` button)
- PostgreSQL storage via `asyncpg`
- GitHub Actions CI syntax check

## Requirements
- Python 3.11+
- PostgreSQL

## Setup
```bash
python -m venv myenv
source myenv/bin/activate
pip install -r kutubxonalar.txt
```

Create `.env` file:
```env
BOT_TOKEN=your_telegram_bot_token
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bot2
DB_USER=postgres
DB_PASSWORD=your_password
```

## Run
```bash
source myenv/bin/activate
python bot.py
```

## GitHub Push Commands
```bash
git init
git add .
git commit -m "feat: improve bot ui ux and add profile flow"
git branch -M main
git remote add origin https://github.com/<USERNAME>/<REPO>.git
git push -u origin main
```
