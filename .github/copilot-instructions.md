This repository is a Telegram bot that manages squad registration, game records,
and simple accounting for a local league. The guidance below highlights the
project structure, common patterns, and concrete examples an AI coding agent
should follow to be productive quickly.

1) Big picture
- Entrypoint: [main.py](main.py) — registers Telegram command handlers and
  starts long‑polling. Each handler delegates to a module in the root.
- Command modules: files named `command_*.py` (for example [command_add.py](command_add.py))
  expose an `execute(message, bot)` function and are wired from `main.py`.
- Database: [database.py](database.py) — uses `psycopg2` connection pool and
  raw SQL. SQL query files live in `SQL Queries/` and constants referencing
  them are in [constants.py](constants.py).
- Scheduling & background jobs: [alerts.py](alerts.py) — uses `APScheduler`
  to schedule automated messages and backups at startup (called from `main.py`).

2) Environment & runtime
- Required env vars: `TELEGRAM_API_TOKEN` (bot token) and `DATABASE_URL` (Postgres). See [main.py](main.py) and [database.py](database.py).
- Run locally: install `requirements.txt` and run `python3 main.py` with the
  two env vars loaded (the project uses `python-dotenv` — a `.env` file is
  supported).

3) Project-specific conventions
- Command module shape: implement `execute(message, bot)` and use the `bot`
  instance methods (see [command_add.py](command_add.py) for an example).
- Database access: all DB helpers live in [database.py](database.py). The code
  frequently constructs SQL with Python `f`-strings and uses the connection
  pool via `create_connection_pool()`; when changing or adding queries,
  follow the file-level pattern (open/read SQL files in `SQL Queries/` where used).
- Templates & prompts: text templates and prompts are stored at repo root
  (e.g. [prompt_talk.txt](prompt_talk.txt), [prompt_split_squad.txt](prompt_split_squad.txt), [prompt_good_morning.txt](prompt_good_morning.txt)) and referenced from `constants.py`.
- Logging: use `log()` / `log_error()` from [logger.py](logger.py) for consistency.

4) Integration & external dependencies
- Telebot library (`telebot`) is used for Telegram interaction (handlers in
  `main.py` map commands to `command_*.py`).
- Postgres via `psycopg2-binary` and `DATABASE_URL` env var; SQL lives in
  `SQL Queries/` and is referenced by constants in [constants.py](constants.py).
- APScheduler schedules recurring jobs (`alerts.py`).
- OpenAI is present in `requirements.txt` and prompts/templates exist — check
  `good_morning_message.py`, `hot_stats_generator.py` and `deepseek.py` for usage.

5) Quick examples (copyable patterns)
- Wiring a command in `main.py`: `@bot.message_handler(commands=['add'])` → calls `command_add.execute(message, bot)`.
- Database helper usage: call functions from [database.py](database.py), e.g. `database.get_squad(matchday_date)` returns an array of players.
- Scheduled job registration: `alerts.schedule_alerts()` is executed at startup.

6) Safe editing hints (project‑specific)
- Follow existing patterns: add new command handlers as new `command_*.py` modules
  and register them in [main.py](main.py).
- When adding DB queries, prefer adding .sql files under `SQL Queries/` and
  reference them via `constants.py` (consistent with existing queries).
- Use existing logging utilities for errors and info messages so automated
  alerts and backups remain observable.

7) What to ask the maintainers (if uncertain)
- Which env vars (besides `TELEGRAM_API_TOKEN` and `DATABASE_URL`) should be set in production?
- Any preferred testing or staging workflow for the bot (a separate test DB,
  sanitized `.env`, or mocked Telegram token)?