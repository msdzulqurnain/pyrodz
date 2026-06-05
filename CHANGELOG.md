# Changelog

## Unreleased

### Added

- **Update system** — `pyrodz update` fetches and applies latest framework code from the original GitHub repository; supports `--check` flag for dry-run version checking
- **Version info** — `pyrodz --version` / `pyrodz -v` displays current framework version and mode

### Changed

- Sessions folder tracked via `.gitkeep`; only `.session` files are ignored

### Fixed

- `App.ENV` now reads from `.env` correctly via `load_dotenv()` in `App.py`

## v0.2.0-beta (2026-05-26)

Database, logging, MongoDB, and project restructuring.

### Added

- **Multi-driver SQL database** — SQLite (stdlib), MySQL (`pymysql`), PostgreSQL (`psycopg2-binary`); grammar-per-driver architecture
  - QueryBuilder with fluent API (insert, select, update, delete, count, chain)
  - Model ORM with `fillable`, `guarded`, `timestamps`, dirty tracking
  - Schema Builder with column types and modifiers
  - Migration runner with `up()` and `rollback()` support
- **MongoDB** — Native PyMongo support via `from framework.database import mongo`
- **Logging** — Dual-output logger (`Log.info`, `Log.warning`, `Log.error`, `Log.exception`); styled console output + auto-rotating file logs at `storage/logs/`
- **CLI commands** — `make:model`, `make:migration`, `migrate`, `migrate rollback`, `make:db`

### Changed

- CLI renamed from `dz` to `pyrodz`, command `serve` → `start`
- Pyrogram session files moved to `storage/sessions/`
- CLI help grouped by category with descriptions

## v0.1.0 (2026-05-26)

Initial release — foundation of the framework.

### Added

- **CLI system** — Artisan-style `pyrodz` commands: `start`, `route:list`, `make:command`, `make:callback`
- **Routing** — `Route.command()`, `Route.callback()`, `Route.inline()`, `Route.regex()` with `$` data markers for dynamic callback extraction
- **Handlers** — Structured handler classes in `app/Handlers/`; screen-returning handlers via `screen()` helper
- **Screens** — Rendering modules in `screen/` directory; separation of display logic from handler logic
- **Data extraction** — `data(callback_query, _1)` helper with `_1`–`_5` constants for regex capture groups
- **Inline keyboard builder** — `Btn` and `Buttons` classes; `Button` shorthand for single-button markup; row breaks via `/` operator; 8 button types: `cb`, `url`, `user`, `inline`, `current`, `login`, `webapp`, `game`
- **Filters** — Composable filters (`private`, `group`, `supergroup`, `text`, `photo`, `video`, `document`) with `&`, `|`, `~` operators
- **Scaffolding** — `make:command` and `make:callback` generate handler boilerplate with route registration
- **Config** — `.env`-driven configuration via `app/Config/` classes for app, bot, and database settings
- **Project structure** — Clean Laravel-like directory layout with `core/`, `framework/`, `app/`, `routes/`, `screen/`, `storage/`

### License

- MIT License
