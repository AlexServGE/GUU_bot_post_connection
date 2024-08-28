class User:

    def __init__(self, user_date_of_first_registration=None, user_telegram_id=None, telegram_nickname=None,
                 user_PERSONAL_INFO_ACCEPTANCE=None, user_GENDER=None, user_SURNAME=None,
                 user_NAME=None, user_PATRONYMIC=None, user_EMAIL=None, user_PHONE=None, user_BIRTHDATE=None,
                 user_GRADDATE=None, user_INSTITUTE=None,
                 user_EMPLOYER=None, user_POSITION=None):
        self.user_date_of_first_registration = user_date_of_first_registration  # 2023-11-05
        self.user_telegram_id = user_telegram_id
        self.user_telegram_nickname = telegram_nickname
        self.user_PERSONAL_INFO_ACCEPTANCE = user_PERSONAL_INFO_ACCEPTANCE
        self.user_GENDER = user_GENDER
        self.user_SURNAME = user_SURNAME
        self.user_NAME = user_NAME
        self.user_PATRONYMIC = user_PATRONYMIC
        self.user_EMAIL = user_EMAIL
        self.user_PHONE = user_PHONE
        self.user_BIRTHDATE = user_BIRTHDATE
        self.user_GRADDATE = user_GRADDATE
        # self.user_INSTITUTE = user_INSTITUTE
        self.user_EMPLOYER = user_EMPLOYER
        self.user_POSITION = user_POSITION

    def fill_user_fields_from_tuple(self, sql_tuple):
        self.user_date_of_first_registration = sql_tuple[1]
        self.user_telegram_nickname = sql_tuple[3]
        self.user_PERSONAL_INFO_ACCEPTANCE = sql_tuple[4]
        self.user_GENDER = sql_tuple[5]
        self.user_SURNAME = sql_tuple[6]
        self.user_NAME = sql_tuple[7]
        self.user_PATRONYMIC = sql_tuple[8]
        self.user_EMAIL = sql_tuple[9]
        self.user_PHONE = sql_tuple[10]
        self.user_BIRTHDATE = sql_tuple[11]
        self.user_GRADDATE = sql_tuple[12]
        # self.user_INSTITUTE = sql_tuple[13]
        self.user_EMPLOYER = sql_tuple[13]
        self.user_POSITION = sql_tuple[14]

    # На будущее: когда буду писать ветку обновления информации, необходимо добавить поле дата_последнего_обновления
    def __str__(self):
        return f"Фамилия: {self.user_SURNAME}\n" \
               f"Имя: {self.user_NAME}\n" \
               f"Отчество: {self.user_PATRONYMIC}\n" \
               f"Пол: {self.user_GENDER}\n" \
               f"Емейл: {self.user_EMAIL}\n" \
               f"Телефон: {self.user_PHONE}\n" \
               f"День рождения: {self.user_BIRTHDATE}\n" \
               f"Год выпуска: {self.user_GRADDATE}\n" \
               f"Институт: {self.user_INSTITUTE}\n" \
               f"Работодатель: {self.user_EMPLOYER}\n" \
               f"Позиция: {self.user_POSITION}\n"
