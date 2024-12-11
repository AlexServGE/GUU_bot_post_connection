from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from Bot_fd.Conversations.Registration import RegistrationConversation
from Bot_fd.Conversations.Change_profile import ChangeProfileConversation
from Bot_fd.Conversations.Delete_profile import DeleteProfileConversation


class ConversationBot:

    def __init__(self, updater, dispatcher, logger):
        self.updater = updater
        self.dispatcher = dispatcher
        self.logger = logger
        self.registration_conversation = RegistrationConversation(self.updater, self.dispatcher, self.logger)
        self.change_profile_conversation = ChangeProfileConversation(self.updater, self.dispatcher, self.logger)
        self.delete_profile_conversation = DeleteProfileConversation(self.updater, self.dispatcher, self.logger)

    def start(self, update, context):
        reply_keyboard = [['Зарегистрироваться'], ['Обновить'], ['Удалить']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

        # Начинаем разговор с вопроса
        update.message.reply_text(
            f'Доброго времени суток!\n'
            f'Вас приветствует официальный бот\n'
            f'\U0001F393Клуба выпускников\n'
            f'\U00002696Факультета права\n'
            f'\U0001F3DBНИУ ВШЭ.\n'
            f'Мы здесь, чтобы помочь '
            f'\U00002794Зарегистрировать\n'
            f'\U00002794Обновить\n'
            f'\U00002794Удалить\n'
            f'контактную информацию о Вас, которая позволит нам оставаться на связи с Вами '
            f'\U0001F469\U0000200D\U00002696\U0000FE0F \U0001F468\U0000200D\U00002696\U0000FE0F.\n'
            f'Команда \U000023F9/cancel, чтобы прекратить разговор.', )
        update.message.reply_text(
            f'Уточните, пожалуйста, что бы Вы хотели сделать, выбрав нужную опцию на появившейся клавиатуре⌨:',
            reply_markup=markup_key, )
        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал ответ пользователя
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

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

    def bot_session(self):
        conv_handler_registration = ConversationHandler(  # здесь строится логика разговора
            # точка входа в разговор
            entry_points=[MessageHandler(filters.regex('^(Зарегистрироваться|зарегистрироваться)$'),
                                         self.registration_conversation.start_registration)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states={
                self.registration_conversation.PERSONAL_INFO_ACCEPTANCE: [
                    MessageHandler(filters.text, self.registration_conversation.personal_data_acceptance)],
                self.registration_conversation.GENDER: [
                    MessageHandler(filters.text, self.registration_conversation.reg_gender)],
                self.registration_conversation.SURNAME: [
                    MessageHandler(filters.text, self.registration_conversation.reg_surname)],
                self.registration_conversation.NAME: [
                    MessageHandler(filters.text, self.registration_conversation.reg_name)],
                self.registration_conversation.PATRONYMIC: [
                    MessageHandler(filters.text, self.registration_conversation.reg_patronymic)],
                self.registration_conversation.EMAIL: [
                    MessageHandler(filters.text, self.registration_conversation.reg_email)],
                self.registration_conversation.PHONE: [
                    MessageHandler(filters.text, self.registration_conversation.reg_phone)],
                self.registration_conversation.BIRTHDATE: [
                    MessageHandler(filters.text, self.registration_conversation.reg_birthdate)],
                self.registration_conversation.GRADDATE: [
                    MessageHandler(filters.text, self.registration_conversation.reg_graddate)],
                self.registration_conversation.INSTITUTE: [
                    MessageHandler(filters.text, self.registration_conversation.reg_institute)],
                self.registration_conversation.EMPLOYER: [
                    MessageHandler(filters.text, self.registration_conversation.reg_employer)],
                self.registration_conversation.POSITION: [
                    MessageHandler(filters.text, self.registration_conversation.reg_position)],
            },
            # точка выхода из разговора
            fallbacks=[CommandHandler('cancel', self.registration_conversation.cancel)],  ##что-то другое нужно
        )

        conv_handler_change_profile = ConversationHandler(  # здесь строится логика разговора
            # точка входа в разговор
            entry_points=[MessageHandler(filters.regex('^(Обновить|обновить)$'),
                                         # Обновить|обновить соответствует выбору в методе start
                                         self.change_profile_conversation.start_change_profile)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states={
                self.change_profile_conversation.CHANGE_PROFILE_ONE_FIELD: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_profile_one_field)],
                self.change_profile_conversation.GENDER: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_gender)],
                self.change_profile_conversation.SURNAME: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_surname)],
                self.change_profile_conversation.NAME: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_name)],
                self.change_profile_conversation.PATRONYMIC: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_patronymic)],
                self.change_profile_conversation.EMAIL: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_email)],
                self.change_profile_conversation.PHONE: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_phone)],
                self.change_profile_conversation.BIRTHDATE: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_birthdate)],
                self.change_profile_conversation.GRADDATE: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_graddate)],
                self.change_profile_conversation.INSTITUTE: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_institute)],
                self.change_profile_conversation.EMPLOYER: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_employer)],
                self.change_profile_conversation.POSITION: [
                    MessageHandler(filters.text, self.change_profile_conversation.change_position)],
            },
            # точка выхода из разговора
            fallbacks=[CommandHandler('cancel', self.registration_conversation.cancel)],  ##что-то другое нужно
        )

        conv_handler_delete_profile = ConversationHandler(  # здесь строится логика разговора
            # точка входа в разговор
            entry_points=[MessageHandler(filters.regex('^(Удалить|удалить)$'),
                                         # Удалить|удалить соответствует выбору в методе start
                                         self.delete_profile_conversation.start_delete_profile)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states={
                self.delete_profile_conversation.DELETE_PROFILE: [
                    MessageHandler(filters.text, self.delete_profile_conversation.delete_profile)],
            },
            # точка выхода из разговора
            fallbacks=[CommandHandler('cancel', self.registration_conversation.cancel)],  ##что-то другое нужно
        )

        # Добавляем обработчик разговоров `conv_handler`
        self.dispatcher.add_handler(conv_handler_registration)
        self.dispatcher.add_handler(conv_handler_change_profile)
        self.dispatcher.add_handler(conv_handler_delete_profile)
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("cancel", self.cancel))


if __name__ == '__main__':
    pass
