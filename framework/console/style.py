import platform

from app.Config.App import App


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;46m"
    YELLOW = "\033[38;5;226m"
    BLUE = "\033[38;5;39m"
    CYAN = "\033[38;5;51m"
    GRAY = "\033[38;5;244m"
    WHITE = "\033[38;5;255m"

    FRAMEWORK_VERSION = "0.2.1"
    MODE = App.ENV

    @classmethod
    def text(cls, text, *styles):
        return "".join(styles) + text + cls.RESET

    @classmethod
    def success(cls, text):
        return cls.text(f"✓ {text}", cls.GREEN, cls.BOLD)

    @classmethod
    def error(cls, text):
        return cls.text(f"✗ {text}", cls.RED, cls.BOLD)

    @classmethod
    def warn(cls, text):
        return cls.text(f"⚠ {text}", cls.YELLOW, cls.BOLD)

    @classmethod
    def info(cls, text):
        return cls.text(f"ℹ {text}", cls.CYAN)

    @classmethod
    def muted(cls, text):
        return cls.text(text, cls.GRAY)

    @classmethod
    def brand(cls):
        lines = [
            "┌─────────────────────────────┐",
            "│       PyroDZ Framework      │",
            "└─────────────────────────────┘",
        ]

        return "\n".join(cls.text(line, cls.BLUE, cls.BOLD) for line in lines)

    @classmethod
    def system_info(cls):
        python_version = platform.python_version()

        return "\n".join([
            cls.muted(f"Python      {python_version}"),
            cls.muted(f"Framework   v{cls.FRAMEWORK_VERSION}"),
            cls.muted(f"Mode        {cls.MODE}"),
        ])