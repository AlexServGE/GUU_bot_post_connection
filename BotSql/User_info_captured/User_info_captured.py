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
        self.user_INSTITUTE = user_INSTITUTE
        self.user_EMPLOYER = user_EMPLOYER
        self.user_POSITION = user_POSITION
