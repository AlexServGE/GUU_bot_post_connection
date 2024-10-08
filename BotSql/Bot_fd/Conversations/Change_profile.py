from PostgreSqlApi.PostgreSQL_change_profile import SqlApiChangeProfile
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
)
import datetime

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


class ChangeProfileConversation:
    # Определяем константы этапов разговора
    CHANGE_PROFILE_ONE_FIELD, GENDER, SURNAME, NAME, PATRONYMIC, EMAIL, PHONE, BIRTHDATE, GRADDATE, INSTITUTE, \
        EMPLOYER, POSITION = range(12)

    def __init__(self, updater, dispatcher, logger):
        self.updater = updater
        self.dispatcher = dispatcher
        self.logger = logger
        self.sql_change_profile = SqlApiChangeProfile()
        self.ex_student = User()
        self.user_selected_field = None
        self.USER_TRIES = 2
        self.INPUTS = 0
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

    def start_change_profile(self, update, context):
        # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        # определяем telegram.id пользователя
        self.ex_student.user_telegram_id = user.id
        # подключаемся к бд, чтобы проверить/найти выпускника
        user_sql_info_tuple = self.sql_change_profile.sql_select_all_user_info(self.ex_student.user_telegram_id)
        if not user_sql_info_tuple:
            update.message.reply_text(
                f'К сожалению, нам не удалось найти информацию о Вашем профиле в \U0001F393Клубе выпускников.\n' \
                f'Вы можете пройти регистрацию. Для этого нажмите \U000025B6/start.',
            )
            return ConversationHandler.END
        else:
            self.ex_student.fill_user_fields_from_tuple(user_sql_info_tuple)
            # Список кнопок для ответа
            reply_keyboard = [['Фамилия', 'Имя', 'Отчество'],
                              ['\U00002709Емейл', '\U0001F4F1Телефон', '\U0001F468\U0001F3FB\U0000200D\U00002696\U0000FE0F \U0001F469\U0001F3FB\U0000200D\U00002696\U0000FE0FПол'],
                              ['\U0001F382Дата рождения', '\U0001F393Год выпуска'],
                              ['\U0001F3EDМесто работы', '\U0001F4BCОбразовательная программа','\U0001F464Должность']]
            markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            # Разговор
            update.message.reply_text(
                f'Нам удалось найти следующую информацию о Вас	\U0001F516:\n'
                f'{self.ex_student}', )
            # Разговор
            update.message.reply_text(
                f'Укажите поле, которое хотели бы обновить о себе. Команда \U000023F9/cancel, чтобы прекратить разговор.',
                reply_markup=markup_key, )
            return self.CHANGE_PROFILE_ONE_FIELD

    def change_profile_one_field(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        user_reply = update.message.text
        if self.INPUTS < 1:
            self.user_selected_field = user_reply
        if self.user_selected_field == 'Фамилия':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите свою фамилию:', reply_markup=ReplyKeyboardRemove()
            )
            return self.SURNAME
        elif self.user_selected_field == 'Имя':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите своё полное имя:', reply_markup=ReplyKeyboardRemove()
            )
            return self.NAME
        elif self.user_selected_field == 'Отчество':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите своё отчество:', reply_markup=ReplyKeyboardRemove()
            )
            return self.PATRONYMIC
        elif self.user_selected_field == '\U00002709Емейл':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите свой \U00002709электронный адрес для связи (в формате name@domain.ru):', reply_markup=ReplyKeyboardRemove()
            )
            return self.EMAIL
        elif self.user_selected_field == '\U0001F4F1Телефон':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите свой \U0001F4F1телефон для связи (в формате 89992221100):', reply_markup=ReplyKeyboardRemove()
            )
            return self.PHONE
        elif self.user_selected_field == '\U0001F468\U0001F3FB\U0000200D\U00002696\U0000FE0F \U0001F469\U0001F3FB\U0000200D\U00002696\U0000FE0FПол':
            self.INPUTS = 1
            reply_keyboard = [['\U0001F468\U0001F3FB\U0000200D\U00002696\U0000FE0FМужской'], ['\U0001F469\U0001F3FB\U0000200D\U00002696\U0000FE0FЖенский']]
            markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text(
                f'Укажите свой пол:', reply_markup=markup_key,
            )
            return self.GENDER
        elif self.user_selected_field == '\U0001F382Дата рождения':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите дату своего \U0001F382рождения (в формате: 01.01.1999):', reply_markup=ReplyKeyboardRemove()
            )
            return self.BIRTHDATE
        elif self.user_selected_field == '\U0001F393Год выпуска':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите год \U0001F393окончания университета (в формате: 1999):', reply_markup=ReplyKeyboardRemove()
            )
            return self.GRADDATE
        elif self.user_selected_field == '\U0001F4BCОбразовательная программа':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите, какую образовательную программу Вы оканчивали:', reply_markup=ReplyKeyboardRemove()
            )
            return self.INSTITUTE
        elif self.user_selected_field == '\U0001F3EDМесто работы':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите свое текущее \U0001F3EDместо работы, либо оставьте прочерк:', reply_markup=ReplyKeyboardRemove()
            )
            return self.EMPLOYER
        elif self.user_selected_field == '\U0001F464Должность':
            self.INPUTS = 1
            update.message.reply_text(
                f'Укажите свою 	\U0001F464должность, либо оставьте прочерк:', reply_markup=ReplyKeyboardRemove()
            )
            return self.POSITION

        return ConversationHandler.END

    def change_gender(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        if update.message.text != "Мужской" and update.message.text != "Женский":
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'Просьба указывать запрашиваемую информацию. У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'Просьба указывать запрашиваемую информацию. У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'Просьба указывать запрашиваемую информацию. У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Gender", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.', reply_markup=ReplyKeyboardRemove()
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_surname(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.surname_checker.checkUserInputSurname(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Surname", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_name(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.name_checker.checkUserInputName(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Name", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_patronymic(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.patronymic_checker.checkUserInputPatronymic(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Patronymic", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_email(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.email_checker.checkUserInputEmail(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Email", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_phone(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.phone_checker.checkUserInputPhone(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Phone", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_birthdate(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.birthdate_checker.checkUserInputBirthdate(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            day, month, year = user_attrib_to_update.split(".")
            user_attrib_to_update_formatted_date = datetime.date.fromisoformat(f'{year}-{month}-{day}')
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Birthdate", user_attrib_to_update_formatted_date,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_graddate(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.grad_checker.checkUserInputGraddate(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Graduation_date", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_institute(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.institute_checker.checkUserInputInstitute(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Edprogram", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_employer(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.employer_checker.checkUserInputEmployer(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Employer", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def change_position(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return self.cancel(update, context)
        # Разговор
        msg_for_user = self.position_checker.checkUserInputPosition(update.message.text)
        if msg_for_user is not None:
            if self.USER_TRIES == 2:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попытки.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 1:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталась {self.USER_TRIES} попытка.'
                )
                self.USER_TRIES -= 1
                return self.change_profile_one_field(update, context)
            if self.USER_TRIES == 0:
                update.message.reply_text(
                    f'{msg_for_user}\n'
                    f'У Вас осталось {self.USER_TRIES} попыток. Процесс регистрации \U000023F9прекращён.'
                )
                # self.USER_TRIES = 2
                # self.SUCCESSFUL_INPUTS = 0
                return self.cancel(update, context)
        else:
            # определяем пользователя
            user = update.message.from_user
            # Пишем в журнал ответ пользователя
            self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
            # Наполняем список фильтров, выбранных пользователем для передачи в SqlApiSel
            user_attrib_to_update = update.message.text.capitalize()
            # подключаемся к бд, чтобы проверить/найти выпускника
            self.sql_change_profile.sql_update_user_info("Position", user_attrib_to_update,
                                                         self.ex_student.user_telegram_id)
            update.message.reply_text(
                f'Мы обновили ({self.user_selected_field}). Чтобы продолжить работу с ботом, нажмите \U000025B6/start.'
            )
            self.ex_student = User()
            self.user_selected_field = None
            self.USER_TRIES = 2
            self.INPUTS = 0
            return ConversationHandler.END

    def cancel(self, update, context):
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал о том, что пользователь не разговорчивый
        self.logger.info("Пользователь %s отменил разговор.", user.first_name)
        # Отвечаем на отказ поговорить
        update.message.reply_text(
            'По Вашему запросу разговор \U000023F9 прекращён. '
            'Чтобы продолжить работу с ботом нажмите \U000025B6/start.',
            reply_markup=ReplyKeyboardRemove()
        )
        self.ex_student = User()
        self.user_selected_field = None
        self.USER_TRIES = 2
        self.INPUTS = 0

        # Заканчиваем разговор.
        return ConversationHandler.END
