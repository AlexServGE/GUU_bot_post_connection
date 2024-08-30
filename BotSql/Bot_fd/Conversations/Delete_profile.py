from PostgreSqlApi.PostgreSQL_delete_profile import SqlApiDeleteProfile
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
)

from User_info_captured.User_info_captured import User


class DeleteProfileConversation:
    # Определяем константы этапов разговора
    DELETE_PROFILE = range(0)

    def __init__(self, updater, dispatcher, logger):
        self.updater = updater
        self.dispatcher = dispatcher
        self.logger = logger
        self.sql_delete_profile = SqlApiDeleteProfile()
        self.ex_student = User()

    def start_delete_profile(self, update, context):
        # определяем пользователя, в случае если пользователь ввел неверные данные на следующем этапе
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        # определяем telegram.id пользователя
        self.ex_student.user_telegram_id = user.id
        # подключаемся к бд, чтобы проверить/найти выпускника
        user_sql_info_tuple = self.sql_delete_profile.sql_select_all_user_info(self.ex_student.user_telegram_id)
        if not user_sql_info_tuple:
            update.message.reply_text(
                f'Ваш профиль не зарегистрирован в \U0001F393Ассоциации выпускников.\n' \
                f'Чтобы продолжить работу с ботом, нажмите \U000025B6/start.',
            )
            return ConversationHandler.END
        else:
            self.ex_student.fill_user_fields_from_tuple(user_sql_info_tuple)
            # Список кнопок для ответа
            reply_keyboard = [['Да, прошу удалить мой профиль'],
                              ['Нет, прошу не удалять мой профиль']]
            markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
            # Разговор
            update.message.reply_text(
                f'Нам удалось найти следующую информацию о Вас:\n'
                f'{self.ex_student}\n'
                f'Вы уверены, что хотели бы удалить информацию о себе из \U0001F393Ассоциации выпускников?',
                reply_markup=markup_key)
            return self.DELETE_PROFILE

    def delete_profile(self, update, context):
        if update.message.text == "/cancel":  # почему-то /cancel не срабатывает в handler
            self.ex_student = User()
            return self.cancel(update, context)
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал ответ пользователя,
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)
        user_reply = update.message.text
        if user_reply == 'Да, прошу удалить мой профиль':
            self.sql_delete_profile.sql_delete_user(self.ex_student.user_telegram_id)
            user_sql_info_tuple = self.sql_delete_profile.sql_select_all_user_info(self.ex_student.user_telegram_id)
            if not user_sql_info_tuple:
                update.message.reply_text(
                    f'Процедура удаления Вашего профиля прошла успешно. '
                    f'Чтобы продолжить работу с ботом, нажмите \U000025B6/start.', reply_markup=ReplyKeyboardRemove())
            else:
                update.message.reply_text(
                    f'Процедура удаления Вашего профиля завершилась с u"\U0001F6D1"ошибкой.\n'
                    f'Обратитесь, пожалуйста, напрямую в \U0001F393Ассоциацию выпускников \U00002696Факультета права НИУ ВШЭ:\n'
                    f'\U0001F4DE +7(495)772-95-90 *23024,\n'
                    f'\U0001F4E9 lawfacult@hse.ru\n'
                    f'Чтобы продолжить работу с ботом, нажмите 	\U000025B6/start.', reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text(
                f'Мы не удалили информацию о Вас. '
                f'Процедура удаления отменена. '
                f'Чтобы продолжить работу с ботом, нажмите 	\U000025B6/start.', reply_markup=ReplyKeyboardRemove())
        self.ex_student = User()
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

        # Заканчиваем разговор.
        return ConversationHandler.END
