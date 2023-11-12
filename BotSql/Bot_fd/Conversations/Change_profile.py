import datetime
from PostgreSqlApi.PostgreSQL_change_profile import SqlApiChangeProfile
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


class ChangeProfileConversation:
    # Определяем константы этапов разговора
    CHANGE_PROFILE_ONE_FIELD, \
        POSITION = range(2)

    def __init__(self, updater, dispatcher, logger):
        self.ex_student = User()

    def start_change_profile(self, update, context):
        # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        # определяем telegram.id пользователя
        self.ex_student.user_telegram_id = user.id
        # подключаемся к бд, чтобы проверить/найти выпускника
        sql_change_profile = SqlApiChangeProfile()
        # получаем кортеж с данными выпускника, либо None
        user_sql_info_tuple = sql_change_profile.sql_select_all_user_info(self.ex_student.user_telegram_id)
        sql_change_profile.connection_close()
        if not user_sql_info_tuple:
            update.message.reply_text(
                f'К сожалению, нам не удалось найти информацию о Вашем профиле в Ассоции выпускников ГУУ.\n' \
                f'Вы можете пройти регистрацию. Для этого нажмите /start.',
            )
            return ConversationHandler.END
        else:
            self.ex_student.fill_user_fields_from_tuple(user_sql_info_tuple)
            # Список кнопок для ответа
            reply_keyboard = [['Фамилия', 'Имя', 'Отчество'],
                              ['Емейл', 'Телефон'],
                              ['День рождения', 'Год выпуска'],
                              ['Институт', 'Работодатель', 'Позиция']]
            markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            # Разговор
            update.message.reply_text(
                f'Нам удалось найти следующую информацию о Вас:\n'
                f'{self.ex_student}', )
            # Разговор
            update.message.reply_text(
                f'Укажите поле, которое хотели бы обновить о себе.',
                reply_markup=markup_key, )
            return self.CHANGE_PROFILE_ONE_FIELD

    def change_profile_one_field(self, update, context):
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        user_reply = update.message.text



    def cancel(self, update, context):
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал о том, что пользователь не разговорчивый
        self.logger.info("Пользователь %s отменил разговор.", user.first_name)
        # Отвечаем на отказ поговорить
        update.message.reply_text(
            'Моё дело предложить - Ваше отказаться. '
            'Будет скучно - пишите.'
            'Чтобы продолжить работу с ботом нажмите /start.',
            reply_markup=ReplyKeyboardRemove()
        )

        self.USER_TRIES = 2
        self.SUCCESSFUL_INPUTS = 0
        self.ex_student = None

        # Заканчиваем разговор.
        return ConversationHandler.END
