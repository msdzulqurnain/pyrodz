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

    @classmethod
    def chosen_chat(cls, text: str, query: str = "", allow_user: bool = True, allow_bot: bool = False, allow_group: bool = True, allow_channel: bool = False):
        from pyrogram.types import InlineKeyboardButton, SwitchInlineQueryChosenChat
        return cls(
            InlineKeyboardButton(
                text=text,
                switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                    query=query,
                    allow_user_chats=allow_user,
                    allow_bot_chats=allow_bot,
                    allow_group_chats=allow_group,
                    allow_channel_chats=allow_channel,
                ),
            )
        )

    @classmethod
    def copy_text(cls, text: str, copy_text: str):
        from pyrogram.types import InlineKeyboardButton, CopyTextButton
        return cls(
            InlineKeyboardButton(
                text=text,
                copy_text=CopyTextButton(text=copy_text),
            )
        )

    @classmethod
    def pay(cls, text: str):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                pay=True,
            )
        )

    @classmethod
    def cb_pass(cls, text: str, data: str):
        from pyrogram.types import InlineKeyboardButton
        return cls(
            InlineKeyboardButton(
                text=text,
                callback_data_with_password=data.encode(),
            )
        )

    def emoji(self, emoji_id: str):
        self.button.icon_custom_emoji_id = emoji_id
        return self

    def style(self, style):
        from pyrogram.enums import ButtonStyle
        if isinstance(style, str):
            style = ButtonStyle[style.upper()]
        self.button.style = style
        return self

    def primary(self):
        return self.style("PRIMARY")

    def success(self):
        return self.style("SUCCESS")

    def danger(self):
        return self.style("DANGER")

    def default(self):
        return self.style("DEFAULT")


class _ButtonBuilder:
    def __init__(self, btn: Btn):
        self._btn = btn

    def _build(self):
        from pyrogram.types import InlineKeyboardMarkup

        rows = [[self._btn.button]]
        return InlineKeyboardMarkup(rows)

    async def write(self, client):
        markup = self._build()
        return await markup.write(client)

    @property
    def inline_keyboard(self):
        return self._build().inline_keyboard

    def emoji(self, emoji_id: str):
        self._btn.emoji(emoji_id)
        return self

    def style(self, style):
        self._btn.style(style)
        return self

    def primary(self):
        self._btn.primary()
        return self

    def success(self):
        self._btn.success()
        return self

    def danger(self):
        self._btn.danger()
        return self

    def default(self):
        self._btn.default()
        return self


class Button:
    @staticmethod
    def cb(text: str, data: str):
        return _ButtonBuilder(Btn.cb(text, data))

    @staticmethod
    def url(text: str, url: str):
        return _ButtonBuilder(Btn.url(text, url))

    @staticmethod
    def user(text: str, user_id: int):
        return _ButtonBuilder(Btn.user(text, user_id))

    @staticmethod
    def inline(text: str, value: str = ""):
        return _ButtonBuilder(Btn.inline(text, value))

    @staticmethod
    def current(text: str, value: str = ""):
        return _ButtonBuilder(Btn.current(text, value))

    @staticmethod
    def login(text: str, url: str):
        return _ButtonBuilder(Btn.login(text, url))

    @staticmethod
    def webapp(text: str, url: str):
        return _ButtonBuilder(Btn.webapp(text, url))

    @staticmethod
    def game(text: str):
        return _ButtonBuilder(Btn.game(text))

    @staticmethod
    def chosen_chat(text: str, query: str = "", allow_user: bool = True, allow_bot: bool = False, allow_group: bool = True, allow_channel: bool = False):
        return _ButtonBuilder(Btn.chosen_chat(text, query, allow_user, allow_bot, allow_group, allow_channel))

    @staticmethod
    def copy_text(text: str, copy_text: str):
        return _ButtonBuilder(Btn.copy_text(text, copy_text))

    @staticmethod
    def pay(text: str):
        return _ButtonBuilder(Btn.pay(text))

    @staticmethod
    def cb_pass(text: str, data: str):
        return _ButtonBuilder(Btn.cb_pass(text, data))


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
                elif isinstance(b, _RowBreak):
                    raise TypeError("_RowBreak not allowed inside list. Use Btn directly.")
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