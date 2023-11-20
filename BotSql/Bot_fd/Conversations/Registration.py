import datetime
from PostgreSqlApi.PostgreSql_registration import SqlApiRegistration
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
)
from User_info_captured.User_info_captured import User

from Bot_fd.Conversations.Checks.SurnameChecker import SurnameChecker
from Bot_fd.Conversations.Checks.NameChecker import NameChecker
from Bot_fd.Conversations.Checks.PatronymicChecker import PatronymicChecker
from Bot_fd.Conversations.Checks.EmailChecker import EmailChecker
from Bot_fd.Conversations.Checks.PhoneChecker import PhoneChecker
from Bot_fd.Conversations.Checks.BirthdateChecker import BirthdateChecker
from Bot_fd.Conversations.Checks.GraddateChecker import GraddateChecker
from Bot_fd.Conversations.Checks.InstituteChecker import InstituteChecker
from Bot_fd.Conversations.Checks.EmployerChecker import EmployerChecker
from Bot_fd.Conversations.Checks.PositionChecker import PositionChecker


class RegistrationConversation:
    # Определяем константы этапов разговора
    PERSONAL_INFO_ACCEPTANCE, GENDER, SURNAME, NAME, PATRONYMIC, EMAIL, PHONE, BIRTHDATE, GRADDATE, INSTITUTE, EMPLOYER, \
        POSITION = range(12)

    def __init__(self, updater, dispatcher, logger):
        self.updater = updater
        self.dispatcher = dispatcher
        self.logger = logger
        self.sql_registration = SqlApiRegistration()
        self.ex_student = User()
        self.ex_student.user_date_of_first_registration = None
        self.USER_TRIES = 2
        self.SUCCESSFUL_INPUTS = 0
        # self.gender_checker = GenderChecker()
        self.surname_checker = SurnameChecker()
        self.name_checker = NameChecker()
        self.patronymic_checker = PatronymicChecker()
        self.email_checker = EmailChecker()
        self.phone_checker = PhoneChecker()
        self.birthdate_checker = BirthdateChecker()
        self.grad_checker = GraddateChecker()
        self.institute_checker = InstituteChecker()
        self.employer_checker = EmployerChecker()
        self.position_checker = PositionChecker()

    # Обрабатываем ответ по категории лекарственных препаратов

    def start_registration(self, update, context):
        # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        # определяем telegram.id пользователя
        self.ex_student.user_telegram_id = user.id
        # Обращаемся к бд, чтобы узнать зарегистрирован ли уже обращающийся за регистрацией пользователь
        user_sql_info_tuple = self.sql_registration.sql_select_all_user_info(self.ex_student.user_telegram_id)
        if user_sql_info_tuple:
            self.ex_student.fill_user_fields_from_tuple(user_sql_info_tuple)
            update.message.reply_text(
                f'Ваш профиль уже зарегистрирован в Ассоциации выпускников ГУУ.\n\n'
                f'Нам удалось найти следующую информацию о Вас:\n'
                f'{self.ex_student}\n',
            )
            update.message.reply_text(
                f'Чтобы продолжить работу с ботом, нажмите /start.',
            )
            self.ex_student = User()
            return ConversationHandler.END
        else:
            # Список кнопок для ответа
            reply_keyboard = [['Подтверждаю'], ['Не подтверждаю']]
            markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
            # Разговор
            update.message.reply_text(
                f'Перечень персональных данных, на обработку которых дается согласие:\n'
                f'1) Пол\n'
                f'2) Фамилия\n'
                f'3) Имя\n'
                f'4) Отчество\n'
                f'5) Электронный адрес\n'
                f'6) Контактный телефон\n'
                f'7) Дата рождения\n'
                f'8) Дата окончания университета\n'
                f'9) Структурное подразделение\n'
                f'10) Работодатель\n'
                f'11) Должность',
                reply_markup=markup_key, )
            return self.PERSONAL_INFO_ACCEPTANCE

    def personal_data_acceptance(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 1:
            # Разговор
            if update.message.text != "Подтверждаю":
                update.message.reply_text(
                    'Вы не подтвердили согласие на обработку Ваших персональных данных. Процесс регистрации прекращён.'
                    'Чтобы продолжить работу с ботом нажмите /start.'
                    , reply_markup=ReplyKeyboardRemove())
                self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
            else:
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                self.ex_student.user_telegram_nickname = user.first_name
                user_pdata_acceptance = update.message.text.capitalize()
                self.ex_student.user_PERSONAL_INFO_ACCEPTANCE = user_pdata_acceptance
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 1

        # Разговор
        # Список кнопок для ответа
        reply_keyboard = [['Мужской'], ['Женский']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

        update.message.reply_text(
            'Укажите свой пол:', reply_markup=markup_key,
        )

        # переходим к этапу `GENDER`
        return self.GENDER

    def reg_gender(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 2:
            # Разговор
            if update.message.text != "Мужской" and update.message.text != "Женский":
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'Просьба указывать запрашиваемую информацию. У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.personal_data_acceptance(update, context)
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'Просьба указывать запрашиваемую информацию. У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.personal_data_acceptance(update, context)
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'Просьба указывать запрашиваемую информацию. У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_gender = update.message.text.capitalize()
                self.ex_student.user_GENDER = user_gender
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 2

        # Разговор
        update.message.reply_text(
            'Укажите свою фамилию:', reply_markup=ReplyKeyboardRemove()
        )

        return self.SURNAME

    def reg_surname(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 3:
            # Разговор
            msg_for_user = self.surname_checker.checkUserInputSurname(update.message.text)
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    msg_for_user = ""
                    self.USER_TRIES -= 1
                    return self.reg_gender(update, context)
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    msg_for_user = ""
                    self.USER_TRIES -= 1
                    return self.reg_gender(update, context)
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    msg_for_user = ""
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_surname = update.message.text.capitalize()
                self.ex_student.user_SURNAME = user_surname
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 3

        # Разговор
        update.message.reply_text(
            'Укажите своё полное имя:',
        )

        return self.NAME

    def reg_name(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 4:
            msg_for_user = self.name_checker.checkUserInputName(update.message.text)
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_surname(update, context)
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_surname(update, context)
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_name = update.message.text.capitalize()
                self.ex_student.user_NAME = user_name
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 4

        # Разговор
        update.message.reply_text(
            'Укажите своё отчество:',
        )

        return self.PATRONYMIC

    def reg_patronymic(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 5:
            msg_for_user = self.patronymic_checker.checkUserInputPatronymic(update.message.text)
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_name(update, context)
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_name(update, context)
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_patronymic = update.message.text.capitalize()
                self.ex_student.user_PATRONYMIC = user_patronymic
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 5

        # Разговор
        update.message.reply_text(
            'Укажите свой электронный адрес для связи (в формате name@domain.ru):',
        )

        return self.EMAIL

    def reg_email(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 6:
            msg_for_user = self.email_checker.checkUserInputEmail(update.message.text)
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_patronymic(update, context)
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_patronymic(update, context)
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_email = update.message.text
                self.ex_student.user_EMAIL = user_email
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 6

        # Разговор
        update.message.reply_text(
            'Укажите свой телефон для связи (в формате 84953778914):',
        )

        return self.PHONE

    def reg_phone(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 7:
            msg_for_user = self.phone_checker.checkUserInputPhone(update.message.text)
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_email(update, context)
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_email(update, context)
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_phone = update.message.text
                self.ex_student.user_PHONE = user_phone
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 7

        # Разговор
        update.message.reply_text(
            'Укажите год своего рождения (в формате: 01.01.1999):',
        )

        return self.BIRTHDATE

    def reg_birthdate(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 8:  # !
            msg_for_user = self.birthdate_checker.checkUserInputBirthdate(update.message.text)  # !
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_phone(update, context)  # !
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_phone(update, context)  # !
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_birthdate = update.message.text
                day, month, year = user_birthdate.split(".")
                user_birthdate_formated_date = datetime.date.fromisoformat(f'{year}-{month}-{day}')
                self.ex_student.user_BIRTHDATE = user_birthdate_formated_date
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 8  # !

        # Разговор
        update.message.reply_text(
            'Укажите год окончания университета (в формате: 1999):',  # !
        )

        return self.GRADDATE

    def reg_graddate(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 9:  # !
            msg_for_user = self.grad_checker.checkUserInputGraddate(update.message.text)  # !
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_birthdate(update, context)  # !
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_birthdate(update, context)  # !
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_graddate = update.message.text
                self.ex_student.user_GRADDATE = user_graddate
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 9  # !

        # Разговор
        update.message.reply_text(
            'Укажите, какой институт/направление Вы оканчивали:',  # !
        )

        return self.INSTITUTE

    def reg_institute(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 10:  # !
            msg_for_user = self.institute_checker.checkUserInputInstitute(update.message.text)  # !!
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_graddate(update, context)  # !
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_graddate(update, context)  # !
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_institute = update.message.text
                self.ex_student.user_INSTITUTE = user_institute
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 10  # !

        # Разговор
        update.message.reply_text(
            'Укажите своего текущего работодателя, либо оставьте прочерк:',  # !
        )

        return self.EMPLOYER

    def reg_employer(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 11:  # !
            msg_for_user = self.employer_checker.checkUserInputEmployer(update.message.text)  # !
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_institute(update, context)  # !
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_institute(update, context)  # !
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_employer = update.message.text
                self.ex_student.user_EMPLOYER = user_employer
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 11  # !

        # Разговор
        update.message.reply_text(
            'Укажите свою должность, либо оставьте прочерк:',  # !
        )

        return self.POSITION

    def reg_position(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.ex_student.user_date_of_first_registration = None
            self.USER_TRIES = 2
            self.SUCCESSFUL_INPUTS = 0
            return self.cancel(update, context)
        if self.SUCCESSFUL_INPUTS < 12:  # !
            msg_for_user = self.position_checker.checkUserInputPosition(update.message.text)  # !
            if msg_for_user is not None:
                if self.USER_TRIES == 2:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попытки.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_employer(update, context)  # !
                if self.USER_TRIES == 1:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталась {self.USER_TRIES} попытка.'
                    )
                    self.USER_TRIES -= 1
                    return self.reg_employer(update, context)  # !
                if self.USER_TRIES == 0:
                    update.message.reply_text(
                        f'{msg_for_user}\n'
                        f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации прекращён.'
                    )
                    self.USER_TRIES = 2
                    self.SUCCESSFUL_INPUTS = 0
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2
                # определяем пользователя
                user = update.message.from_user
                # Пишем в журнал ответ пользователя
                self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
                # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
                user_position = update.message.text
                self.ex_student.user_POSITION = user_position
        else:
            # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            user = update.message.from_user
            # Пишем в журнал ответ пользователя, в случае если пользователь ввел неверные данные на следующем этапе
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        self.SUCCESSFUL_INPUTS = 12  # !

        self.ex_student.user_date_of_first_registration = datetime.datetime.now().strftime('%Y-%m-%d')  # 2023-11-05
        self.sql_registration.sql_insert_user_info(self.ex_student)
        user_sql_info_tuple = self.sql_registration.sql_select_all_user_info(self.ex_student.user_telegram_id)
        if user_sql_info_tuple:
            # Разговор
            update.message.reply_text(
                'Ассоциация выпускников ГУУ благодарит Вас, что поделились информацией о себе.\n'
                'Чтобы продолжить работу с ботом нажмите /start.',  # !
            )
        else:
            update.message.reply_text(
                f'К сожалению, нам не удалось зарегистрировать Вас в Ассоциации выпускников ГУУ из-за технической ошибки.\n'
                f'Обратитесь, пожалуйста, напрямую в Ассоциацию выпускников ГУУ '
                f'по телефону 8 (495) 377-89-14 (1410).\n'
                f'Чтобы продолжить работу с ботом нажмите /start.', )
        self.ex_student = User()
        self.ex_student.user_date_of_first_registration = None
        self.USER_TRIES = 2
        self.SUCCESSFUL_INPUTS = 0

        return ConversationHandler.END

    # Обрабатываем команду /skip для фото
    # def skip_photo(self,update, _):
    #     # определяем пользователя
    #     user = update.message.from_user
    #     # Пишем в журнал сведения о фото
    #     logger.info("Пользователь %s не отправил фото.", user.first_name)
    #     # Отвечаем на сообщение с пропущенной фотографией
    #     update.message.reply_text(
    #         'Держу пари, ты выглядишь великолепно! А теперь пришлите мне'
    #         ' свое местоположение, или /skip если параноик.'
    #     )
    #     # переходим к этапу `LOCATION`
    #     return LOCATION

    # Обрабатываем команду /cancel если пользователь отменил разговор
    def cancel(self, update, context):
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал о том, что пользователь не разговорчивый
        self.logger.info("Пользователь %s отменил разговор.", user.first_name)
        # Отвечаем на отказ поговорить
        update.message.reply_text(
            'По Вашему запросу разговор прекращён. '
            'Чтобы продолжить работу с ботом нажмите /start.',
            reply_markup=ReplyKeyboardRemove()
        )

        self.ex_student = User()
        self.ex_student.user_date_of_first_registration = None
        self.USER_TRIES = 2
        self.SUCCESSFUL_INPUTS = 0
        # Заканчиваем разговор.
        return ConversationHandler.END


if __name__ == '__main__':
    print(datetime.datetime.now().strftime('%Y-%m-%d'))  # 2023-11-05
