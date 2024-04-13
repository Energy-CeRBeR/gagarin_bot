from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from messages.messages import BUTTONS_TEXT


def create_pages_keyboard(pages: list[dict]):
    buttons = list()
    for page in pages:
        cur_page = InlineKeyboardButton(
            text=page["name"],
            callback_data=f"get_page{page['slug']}"
        )
        buttons.append([cur_page])

    buttons.append(
        [
            InlineKeyboardButton(text=BUTTONS_TEXT["back_button"], callback_data="back")
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
