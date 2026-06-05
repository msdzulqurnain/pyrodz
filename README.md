# PyroDZ 🔥

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-beta-green)
[![Pyrogram](https://img.shields.io/badge/pyrogram-v2-blueviolet)](https://github.com/pyrogram/pyrogram)

PyroDZ is a Python framework for building Telegram bots, built on top of [Pyrogram](https://github.com/pyrogram/pyrogram). It provides a structured, CLI-driven development experience with routing, handler scaffolding, database abstraction, screen rendering, and more — so you can focus on your bot's logic instead of boilerplate.

- **🏷 CLI-first** — `pyrodz start`, `pyrodz make:command`, `pyrodz route:list`, `pyrodz migrate` — all bot management from the terminal
- **📁 Structured project** — Handlers, config, routes, models, migrations, and screens in a clean directory layout
- **🗄 Multi-database** — SQLite, MySQL, PostgreSQL via QueryBuilder + Model + Schema, plus native MongoDB support
- **🖱 Inline keyboard builder** — Compose Telegram inline keyboards with a clean, chainable API
- **📺 Screen rendering** — Separate display logic from handler logic with screen modules
- **📋 Regex data markers** — Extract callback data using `$` placeholders in route patterns
- **🔨 Scaffolding** — Generate handlers, models, and migrations with a single command
- **📝 Logging** — Dual console + file logging with styled output

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/msdzul/pyrodz.git
cd pyrodz

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.sample .env
# Edit .env — fill in API_ID, API_HASH, BOT_TOKEN

# Start the bot
python3 pyrodz start
```

> All CLI commands (`pyrodz start`, `pyrodz route:list`, etc.) must be run inside the virtual environment.

## 🎯 CLI Commands

| Command | Description |
|---|---|
| `pyrodz start` | Start the Telegram bot |
| `pyrodz route:list` | Display all registered routes |
| `pyrodz make:command <Name>` | Scaffold a new command handler and route |
| `pyrodz make:callback <Name>` | Scaffold a new callback handler and route |
| `pyrodz make:model <Name>` | Generate a new model class |
| `pyrodz make:migration <Name>` | Create a new migration file |
| `pyrodz migrate` | Run all pending migrations |
| `pyrodz migrate rollback` | Rollback the last migration batch |
| `pyrodz make:db` | Initialize the database |
| `pyrodz update` | Update the framework to the latest version |
| `pyrodz update --check` | Check for updates without applying |
| `pyrodz --version` | Show framework version |
| `pyrodz -v` | Show framework version (short) |

## 🏗 Architecture

### Request Flow

```
Telegram ──► Pyrogram Client
                   │
            App.wrap_handler()
                   │
              ┌────▼────┐
              │  Router  │  match by command / callback / regex / inline
              └────┬────┘
                   │
              ┌────▼──────┐
              │   Handler  │  app/Handlers/*.py
              └────┬──────┘
                   │
            ┌──────▼──────┐
            │  Inspect     │
            │  return      │
            └──────┬──────┘
                   │
         ┌─────────▼──────────┐
         │                    │
   return ScreenResponse    reply directly
         │                    │
    ┌────▼────┐               │
    │  Screen  │  screen/     │
    │  module  │  *.py        │
    └────┬────┘               │
         │                    │
         ▼                    ▼
    messages.edit_text()   message.reply()
         │                    │
         └────────┬───────────┘
                  ▼
          Telegram Response
```

### Key Components

| Component | Path | Role |
|---|---|---|
| **Router** | `framework/router.py` | Matches incoming updates to registered routes |
| **Handlers** | `app/Handlers/*.py` | Business logic — decides what to respond |
| **Screens** | `screen/*.py` | Rendering — builds the actual message content |
| **Filters** | `app/Support/Filters.py` | Pre-conditions for route matching (`private`, `group`, `text`, etc.) |
| **App** | `core/app.py` | Wraps Pyrogram Client, hooks into update handling |
| **Database** | `framework/database/` | QueryBuilder, Model, Schema, Migration, MongoDB |

## 🧰 Routing

Routes map incoming updates (commands, callbacks, inline queries, regex patterns) to handler methods. Every route is registered in `routes/bot.py`.

```python
from framework.route import Route
```

### Route Types

| Method | Triggered by | Use Case |
|---|---|---|
| `Route.command(cmd, handler, filter)` | `/command` in chat | Bot commands like `/start`, `/help` |
| `Route.callback(data, handler)` | Callback button tap | Button click handling |
| `Route.inline(handler)` | `@bot query` in chat | Inline mode queries |
| `Route.regex(pattern, handler)` | Callback data matching regex | Dynamic callback data with `$` markers |

### Examples

#### Command route with filter

```python
from app.Support.Filters import private, text, group

Route.command("start", StartHandler.start, private & text)
```

The optional third parameter is a filter. Only updates that pass the filter trigger the handler. Import filters directly from `app.Support.Filters`:

- `private` — only private chats
- `group` — only groups
- `supergroup` — only supergroups
- `text` — only text messages

Composable with `&` (AND), `|` (OR), `~` (NOT).

#### Callback route

```python
Route.callback("menu", MenuHandler.menu)
```

Fires when a callback query with data `"menu"` is received.

#### Inline route

```python
Route.inline(SearchHandler.inline)
```

Fires when a user types `@bot query...` in any chat.

#### Regex route with data markers

```python
Route.regex("broadcast_$_$", BroadcastHandler.handle)
```

The `$` marker is automatically converted to a capture group `(.+)`. Use the `data()` helper in your screen to extract the captured groups.

## 📋 Handlers

All handlers live in `app/Handlers/` and follow a simple convention: the method name matches the command or callback name (lowercase).

### Command handler

```python
class StartHandler:
    async def start(self, client, message):
        await message.reply("Hello!")
```

### Callback handler

```python
class MenuHandler:
    async def menu(self, client, callback_query):
        await callback_query.message.edit_text("Menu")
```

### Screen-returning handler

Returning a `ScreenResponse` delegates rendering to a screen module:

```python
class HelpHandler:
    async def help(self, client, message):
        return screen("help", "help")
```

The `screen()` helper takes two arguments:
1. **Module name** — the file in `screen/` (without `.py`), e.g. `"help"` loads `screen/help.py`
2. **Function name** — the async function to call in that module, e.g. `"help"` calls `screen/help.help()`

> Behind the scenes, `screen()` uses `importlib` to dynamically import the module, then calls the function with `(client, message_or_callback_query)`. The called function is responsible for sending or editing the message.

### Regex callback handler

```python
class BroadcastHandler:
    async def broadcast(self, client, callback_query):
        return screen("broadcast", "broadcast")
```

## 📺 Screens

Screens are rendering modules in the `screen/` directory. They separate display logic from handler logic, keeping handlers clean and screens reusable.

```python
# screen/help.py
from framework import Button


async def help(client, message):
    await message.reply("Help text here", reply_markup=Button.url("GitHub", "https://github.com/..."))
```

### Extracting data from callback regex matches

When a route uses `$` markers, the matched capture groups are available through `data()`:

```python
from framework import data, _1, _2, _3, _4, _5


async def broadcast(client, callback_query):
    target = data(callback_query, _1)
    action = data(callback_query, _2)
```

| Helper | Maps to | Example pattern | Captured value |
|---|---|---|---|
| `_1` | `match.group(1)` | `"user_$"` | `123` (from `"user_123"`) |
| `_2` | `match.group(2)` | `"$_$"` | `"delete"` (from `"user_delete"`) |
| `_3` | `match.group(3)` | `"$_$_$"` | Third segment |
| `_4` | `match.group(4)` | `"$_$_$_$"` | Fourth segment |
| `_5` | `match.group(5)` | `"$_$_$_$_$"` | Fifth segment |

The `data(callback_query, n)` function internally retrieves the cached regex match from the callback query's state and calls `.group(n)`.

## 🖱 Inline Keyboard Builder

### Single button

```python
from framework import Button

await message.reply("Welcome!", reply_markup=Button.url("GitHub", "https://github.com/..."))
```

### Multiple buttons with row breaks

```python
from framework import Btn, Buttons

Buttons(
    Btn.cb("Yes", "confirm_yes"),
    Btn.cb("No", "confirm_no"),
    /
    Btn.url("Cancel", "https://...")
)
```

| Method | Payload | Description |
|---|---|---|
| `Btn.cb(label, data)` / `Button.cb(label, data)` | `callback_data` | Button that sends a callback query |
| `Btn.url(label, url)` / `Button.url(label, url)` | `url` | Button that opens a URL |
| `Btn.user(label, user_id)` / `Button.user(label, user_id)` | `user_id` | Button that mentions a user |
| `Btn.inline(label, query)` / `Button.inline(label, query)` | `switch_inline_query` | Button that switches to inline mode with a pre-filled query |
| `Btn.current(label, query)` / `Button.current(label, query)` | `switch_inline_query_current_chat` | Button that switches to inline mode in the current chat |
| `Btn.login(label, url)` / `Button.login(label, url)` | `login_url` | Button for authorization |
| `Btn.webapp(label, url)` / `Button.webapp(label, url)` | `web_app` | Button that opens a Web App |
| `Btn.game(label)` / `Button.game(label)` | `callback_game` | Button that launches a game |

Use `Btn` inside `Buttons(...)` for composing multiple buttons. Use `Button` shorthand for a single button — it returns the markup directly.

Use `/` to start a new row. `Buttons(...)` returns a list of lists ready for `reply_markup=`.

## 🚫 Filters

```python
from app.Support.Filters import private, text, group, supergroup

private & text               # private chat + text only
group | supergroup           # all group types
```

Filters are composable with `&` (AND), `|` (OR), and `~` (NOT).

### Available filters

| Filter | Description |
|---|---|
| `private` | Private chat only |
| `group` | Group chat |
| `supergroup` | Supergroup chat |
| `text` | Text message |
| `photo` | Photo message |
| `video` | Video message |
| `document` | Document/file message |

## 🗄 Database

PyroDZ provides a full SQL database layer (QueryBuilder, Model, Schema, Migration) plus native MongoDB support. Configure via `.env`.

```python
from framework.database import DB, Model, Schema, mongo
```

### Connection

Set `DB_CONNECTION` in `.env` to choose the driver:

| Driver | `DB_CONNECTION` | Dependencies | Default port |
|---|---|---|---|
| SQLite | `sqlite` | None (stdlib) | — |
| MySQL | `mysql` | `pymysql` | 3306 |
| PostgreSQL | `pgsql` | `psycopg2-binary` | 5432 |

```env
DB_CONNECTION=sqlite
DB_DATABASE=storage/database.sqlite
```

Missing optional dependencies raise a clear error with install instructions.

### Query Builder

```python
# Insert
DB.table("users").insert({"name": "John", "email": "john@example.com"})

# Select
user = DB.table("users").where("email", "john@example.com").first()

# Update
DB.table("users").where("id", 1).update({"name": "Jane"})

# Delete
DB.table("users").where("id", 1).delete()

# Count
count = DB.table("users").count()

# Chain
users = DB.table("users").where("age", ">", 17).order_by("name").limit(10).get()
```

All values use parameter binding — no SQL injection.

### Model

```python
from framework.database import Model


class User(Model):
    table = "users"
    fillable = ["name", "email"]
    guarded = ["id"]
    timestamps = True


# Find by primary key
user = User.find(1)

# Update and save
user.name = "Jane"
user.save()

# Create new record
new_user = User.create(name="John", email="john@example.com")
```

| Model option | Description |
|---|---|
| `table` | Database table name |
| `fillable` | Attributes that can be mass-assigned |
| `guarded` | Attributes that are protected from mass-assignment |
| `timestamps` | Auto-manage `created_at` and `updated_at` |

### Schema & Migrations

```python
Schema.create("users", [
    Schema.increments("id"),
    Schema.string("name", 100),
    Schema.string("email").set_unique(),
    Schema.timestamps(),
])
```

#### Column types

| Method | SQL type |
|---|---|
| `Schema.increments("id")` | Auto-increment integer (driver-appropriate) |
| `Schema.string("name", 100)` | `VARCHAR(100)` |
| `Schema.integer("age")` | `INTEGER` |
| `Schema.boolean("active")` | `BOOLEAN` |
| `Schema.text("bio")` | `TEXT` |
| `Schema.timestamps()` | `created_at` + `updated_at` `DATETIME` |

#### Column modifiers

| Method | Description |
|---|---|
| `.set_nullable()` | Allow `NULL` |
| `.set_default(value)` | Set default value |
| `.set_unique()` | Add `UNIQUE` constraint |
| `.set_primary()` | Set as primary key |

#### Schema operations

```python
Schema.drop("users")                          # Drop table
Schema.has_table("users")                     # Check if table exists
Schema.drop_column("users", "old_field")      # Remove a column
Schema.rename_column("users", "old", "new")   # Rename a column
```

#### Migrations

```bash
python3 pyrodz make:migration create_users_table
python3 pyrodz migrate
python3 pyrodz migrate rollback
```

Migration files are stored in `app/Migrations/` with timestamp prefixes (e.g., `2025_01_15_143021_create_users_table.py`). Each migration has `up()` and `rollback()` methods that contain raw SQL.

### MongoDB

PyroDZ supports MongoDB as a secondary database via native PyMongo. No abstraction layer — use the full PyMongo API directly.

```python
from framework.database import mongo

mongo.users.find_one({"user_id": 123})
mongo.logs.insert_one({"user_id": 123, "action": "start"})
mongo.users.create_index("email", unique=True)
```

Configure in `.env`:

```env
MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DATABASE=pyrodz
```

The `mongo` object is a lazy singleton — it only connects to MongoDB on the first access.

## 📝 Logging

```python
from framework.support.Log import Log

Log.info("Bot started")
Log.warning("Slow query detected")
Log.error("Connection failed")
Log.exception("Handler error")   # includes traceback
```

Output goes to both console (styled with colors) and `storage/logs/pyrodz-YYYY-MM-DD.log`.

Configure level in `.env`:

```env
LOG_LEVEL=info
```

Levels: `debug` < `info` < `warning` < `error`

## 📋 Environment Variables

```env
APP_ENV=development
APP_DEBUG=true
LOG_LEVEL=info

BOT_NAME=mybot
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=123456789:ABC

DB_CONNECTION=sqlite
DB_DATABASE=storage/database.sqlite

MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DATABASE=pyrodz
```

## 📁 Project Structure

```
├── pyrodz                  # CLI entry point
├── LICENSE                 # MIT License
├── core/
│   └── app.py              # App class (extends Pyrogram Client)
├── framework/
│   ├── support/            # Screen, Buttons, Log, helpers
│   ├── console/            # CLI kernel and commands
│   └── database/           # QueryBuilder, Model, Schema, Migration
├── routes/
│   └── bot.py              # Route registrations
├── app/
│   ├── Config/             # Configuration from .env
│   ├── Handlers/           # Command and callback handlers
│   ├── Models/             # Database models
│   ├── Migrations/         # Database migration files
│   └── Support/            # FilterProxy and app-specific helpers
├── screen/                 # Screen rendering modules
└── storage/                # Logs, sessions, database files
    ├── logs/
    └── sessions/
```

## 🏷 Requirements

- Python 3.8+
- [Pyrogram](https://github.com/pyrogram/pyrogram)
- [Tgcrypto](https://github.com/pyrogram/tgcrypto)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

Optional (uncomment in `requirements.txt`):
- `pymysql` — MySQL driver
- `psycopg2-binary` — PostgreSQL driver
- `pymongo` — MongoDB driver

## 📝 Changelog

### v0.2.0 (beta)

- Added multi-driver SQL database (SQLite, MySQL, PostgreSQL) with QueryBuilder, Model, Schema, and Migrations
- Added MongoDB support via native PyMongo
- Added CLI commands: `make:model`, `make:migration`, `migrate`, `migrate rollback`, `make:db`
- Added Logging system with dual console + file output
- Added grammar-per-driver architecture for SQL compilation
- Moved Pyrogram sessions to `storage/sessions/`
- Renamed CLI from `dz` to `pyrodz`, `serve` to `start`
- CLI help now grouped by category

### v0.1.0

- Foundation: routing, CLI, screen rendering, button builder, filters
- CLI commands: `start`, `route:list`, `make:command`, `make:callback`
- Regex data markers (`$`) and `data()` helper (`_1`–`_5`)
- FilterProxy with composable filters
- Inline keyboard builder (`Btn`, `Buttons`)
- Screen-returning handlers with dynamic module import
- Scaffolding via `make:command` and `make:callback`

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
