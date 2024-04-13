"""
Здесь хранится текст сообщений бота
"""

USER_MESSAGES: dict = {
    "get_password": "Введите ваш пароль от аккаунта",
    "start_survey_section_1": "Ответьте мне на несколько вопросов",
    "start_survey_section_2": "В следующих вопросах нужно выбрать один из нескольких вариантов",
}

USER_COMMANDS: dict = {
    "/start": {
        "in_base": "Мы вас уже знаем! Для создания нового страницы введите команду /menu",
        "no_base": "Приветствуем! Для входа перехода в меню введите команду /menu"
    },
    "/profile": {
        "with_token": "Список ваших страниц:",
        "no_token": "Вы не подключили данный аккаунт к сайту. Для авторизации введите /auth"
    },
    "/menu": "Основная информация о боте: что-то там...\n"
             "Cписок команд:\n"
             "/start - перезапуск бота\n"
             "/menu - главное меню\n"
             "/profile - информация о профиле\n"
             "/auth - вход в профиль 'Код памяти'\n"
             "/exit - выход из профиля 'Код памяти'\n"
             "/pages - список страниц\n"
             "/fill_page - заполнить существующую страницу",
    "/auth": {
        "already_auth": "Вы уже авторизированны! Если хотите сменить аккаунт, "
                        "то сначала пропишите команду /exit",
        "get_email": "Введите адрес электронной почты, которую привязывали к аккаунту 'Код памяти'",
        "bad_email": "Данный email-адрес некорректный. Введите email от вашего аккаунта!",
        "get_password": "Теперь введите пароль",
        "invalid_data": "Неправильно введены логин или пароль! "
                        "Для повторной попытки авторизации снова введите /auth",
        "success_auth": "Вход в аккаунт успешно выполнен! Для просмотра введите /profile"
    },
    "/fill_page": {
        "with_token": "Выберите страницу для заполнения:",
        "no_token": "Вы не авторизированны! Для заполнения страницы войдите в профиль командой /auth"
    }
}

BUTTONS_TEXT: dict = {
    "back_button": "Вернуться назад"
}
