import os
import traceback
from datetime import datetime

from framework.console.style import Style


class Log:
    _levels = {
        "debug": 0,
        "info": 1,
        "warning": 2,
        "error": 3,
    }

    _level_colors = {
        "INFO": Style.GREEN,
        "WARNING": Style.YELLOW,
        "ERROR": Style.RED,
    }

    _level = None

    @classmethod
    def _get_level(cls):
        if cls._level is None:
            level = os.getenv("LOG_LEVEL", "info").lower()
            cls._level = cls._levels.get(level, 1)
        return cls._level

    @classmethod
    def _should_log(cls, level_name):
        return cls._levels.get(level_name.lower(), 0) >= cls._get_level()

    @classmethod
    def _format(cls, level, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{now}] {level:<8} {message}"

    @classmethod
    def _write_file(cls, text):
        os.makedirs("storage/logs", exist_ok=True)
        date = datetime.now().strftime("%Y-%m-%d")
        path = f"storage/logs/pyrodz-{date}.log"
        with open(path, "a") as f:
            f.write(text + "\n")

    @classmethod
    def _write_console(cls, level, text):
        color = cls._level_colors.get(level, "")
        print(Style.text(text, color))

    @classmethod
    def _log(cls, level, message):
        if not cls._should_log(level):
            return
        text = cls._format(level, message)
        cls._write_console(level, text)
        cls._write_file(text)

    @classmethod
    def info(cls, message):
        cls._log("INFO", message)

    @classmethod
    def warning(cls, message):
        cls._log("WARNING", message)

    @classmethod
    def error(cls, message):
        cls._log("ERROR", message)

    @classmethod
    def exception(cls, message):
        tb = traceback.format_exc()
        if tb and tb != "NoneType: None\n":
            cls._log("ERROR", f"{message}\n{tb}")
        else:
            cls._log("ERROR", message)
