from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from messages.user_messages import BUTTONS_TEXT


def create_pages_keyboard(pages: list[dict], param: str):
    buttons = list()
    for page in pages:
        cur_page = InlineKeyboardButton(
            text=page["name"],
            callback_data=f"{param}_page{page['slug']}"
        )
        buttons.append([cur_page])

    buttons.append(
        [
            InlineKeyboardButton(text=BUTTONS_TEXT["back_button"], callback_data="back")
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def create_survey_keyboard():
    survey_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Есть', callback_data='create')],
        [InlineKeyboardButton(text='Нет', callback_data='no_create')]
    ]
    )

    return survey_keyboard


def create_show_keyboard():
    show_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Просмотреть результаты', callback_data='show_results')]
    ]
    )

    return show_keyboard


def create_yes_no_keyboard(command_type: str):
    survey_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text='Да', callback_data=f'{command_type}_YES')],
        [InlineKeyboardButton(text='Нет', callback_data=f'{command_type}_NO')]
    ]
    )

    return survey_keyboard
