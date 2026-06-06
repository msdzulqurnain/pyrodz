class _RowBreak:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __truediv__(self, other):
        if isinstance(other, (Btn, _RowBreak)):
            return _RowBreak(self, other)
        raise TypeError("Btn can only be separated with Btn using /")


class Btn:
    def __init__(self, button):
        self.button = button

    def __truediv__(self, other):
        if isinstance(other, Btn):
            return _RowBreak(self, other)

        raise TypeError("Btn can only be separated with Btn using /")

    @classmethod
    def cb(cls, text: str, data: str):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                callback_data=data,
            )
        )

    @classmethod
    def url(cls, text: str, url: str):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                url=url,
            )
        )

    @classmethod
    def user(cls, text: str, user_id: int):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                user_id=user_id,
            )
        )

    @classmethod
    def inline(cls, text: str, value: str = ""):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                switch_inline_query=value,
            )
        )

    @classmethod
    def current(cls, text: str, value: str = ""):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                switch_inline_query_current_chat=value,
            )
        )

    @classmethod
    def login(cls, text: str, url: str):
        from pyrogram.types import InlineKeyboardButton, LoginUrl
        return cls(
            InlineKeyboardButton(
                text=text,
                login_url=LoginUrl(url=url),
            )
        )

    @classmethod
    def webapp(cls, text: str, url: str):
        from pyrogram.types import InlineKeyboardButton, WebAppInfo
        return cls(
            InlineKeyboardButton(
                text=text,
                web_app=WebAppInfo(url=url),
            )
        )

    @classmethod
    def game(cls, text: str):
        from pyrogram.types import InlineKeyboardButton, CallbackGame
        return cls(
            InlineKeyboardButton(
                text=text,
                callback_game=CallbackGame(),
            )
        )


class Button:
    @staticmethod
    def cb(text: str, data: str):
        return Buttons(Btn.cb(text, data))

    @staticmethod
    def url(text: str, url: str):
        return Buttons(Btn.url(text, url))

    @staticmethod
    def user(text: str, user_id: int):
        return Buttons(Btn.user(text, user_id))

    @staticmethod
    def inline(text: str, value: str = ""):
        return Buttons(Btn.inline(text, value))

    @staticmethod
    def current(text: str, value: str = ""):
        return Buttons(Btn.current(text, value))

    @staticmethod
    def login(text: str, url: str):
        return Buttons(Btn.login(text, url))

    @staticmethod
    def webapp(text: str, url: str):
        return Buttons(Btn.webapp(text, url))

    @staticmethod
    def game(text: str):
        return Buttons(Btn.game(text))


def Buttons(*items):
    from pyrogram.types import InlineKeyboardMarkup

    rows = []
    current = []

    def _process(item):
        if isinstance(item, Btn):
            current.append(item.button)

        elif isinstance(item, _RowBreak):
            _process(item.left)
            if current:
                rows.append(current[:])
                current.clear()
            _process(item.right)

        elif isinstance(item, (list, tuple)):
            if current:
                rows.append(current[:])
                current.clear()
            processed = []
            for b in item:
                if isinstance(b, Btn):
                    processed.append(b.button)
                else:
                    processed.append(b)
            rows.append(processed)

        else:
            raise TypeError("Buttons only accepts Btn objects")

    for item in items:
        _process(item)

    if current:
        rows.append(current)

    return InlineKeyboardMarkup(rows)