from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
)
# from User_contact.Checks.GenderChecker import GenderChecker
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
    PERSONAL_INFO_ACCEPTANCE, GENDER, SURNAME, NAME, PATRONYMIC, EMAIL, PHONE, BIRTHDATE, GRADDATE, INSTITUTE, EMPLOYER,\
        POSITION = range(12)

    def __init__(self, updater, dispatcher, logger):
        self.updater = updater
        self.dispatcher = dispatcher
        self.logger = logger
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
        # Список кнопок для ответа
        reply_keyboard = [['Подтверждаю'], ['Не подтверждаю']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
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
            f'9) Работодатель\n'
            f'10) Должность',
            reply_markup=markup_key, )

        return self.PERSONAL_INFO_ACCEPTANCE

    def personal_data_acceptance(self, update, context):
        if self.SUCCESSFUL_INPUTS < 1:
            # Разговор
            if update.message.text != "Подтверждаю":
                update.message.reply_text(
                    'Вы не подтвердили согласие на обработку Ваших персональных данных. Процесс регистрации прекращён.'
                )
                return self.cancel(update, context)

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 1

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал ответ пользователя
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_pdata_acceptance = update.message.text.capitalize()
        # user_filters.append(update.message.text)

        # Разговор
        # Список кнопок для ответа
        reply_keyboard = [['Мужской'], ['Женский']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(
            'Укажите свой пол:', reply_markup=markup_key,
        )

        # переходим к этапу `GENDER`
        return self.GENDER

    def reg_gender(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 2

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_gender = update.message.text.capitalize() !!важно! создать класс пользователя
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите свою фамилию:',
        )

        return self.SURNAME

    def reg_surname(self, update, context):
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
                    msg_for_user = ""
                    return self.cancel(update, context)
                else:
                    msg_for_user = ""
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 3

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_surname = update.message.text.capitalize() !!важно! создать класс пользователя
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите своё полное имя:',
        )

        return self.NAME

    def reg_name(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2

        # блокировка успешно сработавших проверок ранее
        self.SUCCESSFUL_INPUTS = 4

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_name = update.message.text.capitalize() !!важно! создать класс пользователя
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите своё отчество:',
        )

        return self.PATRONYMIC

    def reg_patronymic(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 5

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_patronymic = update.message.text.capitalize() !!важно! создать класс пользователя
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите свой электронный адрес для связи (в формате name@domain.ru):',
        )

        return self.EMAIL

    def reg_email(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
            else:
                self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 6

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_email = update.message.text
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите свой телефон для связи (в формате 84953778914):',
        )

        return self.PHONE

    def reg_phone(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
        else:
            self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 7

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_phone = update.message.text
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите свой год рождения (в формате 01.01.1999):',
        )

        return self.BIRTHDATE

    def reg_birthdate(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
        else:
            self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 8  # !

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_birthdate = update.message.text #!
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите свой год окончания университета (в формате 4 цифр. Например: 1999):',  # !
        )

        return self.GRADDATE

    def reg_graddate(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
        else:
            self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 9  # !

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_graddate = update.message.text #!
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите, какое структурное подразделение Вы оканчивали:',  # !
        )

        return self.INSTITUTE

    def reg_institute(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
        else:
            self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 10  # !

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_institute = update.message.text #!
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите, своего текущего работодателя, либо оставьте прочерк:',  # !
        )

        return self.EMPLOYER

    def reg_employer(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
        else:
            self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 11  # !

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_employer = update.message.text #!
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Укажите, свою должность, либо оставьте прочерк:',  # !
        )

        return self.POSITION

    def reg_position(self, update, context):
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
                    return self.cancel(update, context)
                else:
                    return self.cancel(update, context)
        else:
            self.USER_TRIES = 2

        self.SUCCESSFUL_INPUTS = 12  # !

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал сведения с федеральным округом
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
        # user_position = update.message.text #!
        # user_filters.append(update.message.text)

        # Разговор
        update.message.reply_text(
            'Ассоциация выпускников ГУУ благодарит Вас, что поделились информацией о себе.\n'
            'Чтобы продолжить работу с ботом нажмите /start.',  # !
        )

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
            'Моё дело предложить - Ваше отказаться. '
            'Будет скучно - пишите.',
            reply_markup=ReplyKeyboardRemove()
        )
        # Заканчиваем разговор.
        return ConversationHandler.END
