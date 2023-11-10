import logging

from User_info_captured.User_info_captured import User
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from .Conversations.Registration import RegistrationConversation


class ConversationBot:

    def __init__(self, updater, dispatcher, logger):
        self.ex_student = User()
        self.updater = updater
        self.dispatcher = dispatcher
        self.logger = logger
        self.registration_conversation = RegistrationConversation(self.updater, self.dispatcher, self.logger,
                                                                  self.ex_student)

    def start(self, update, context):
        reply_keyboard = [['Зарегистрироваться', 'Обновить', 'Удалить']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        # Начинаем разговор с вопроса
        update.message.reply_text(
            f'Доброго времени суток!\n'
            f'<Тестовая версия. Может быть отключена в любой момент>\n'
            f'Вас приветствует официальный бот Ассоциации выпускников Государственного Университета Управления.\n'
            f'Я здесь, чтобы помочь зарегистрироваться/обновить/удалить контактную информацию о Вас, которая позволит Ассоциации выпускников оставаться на связи с Вами.\n'
            f'Команда /cancel, чтобы прекратить разговор.\n'
            f'Уточните, что бы Вы хотели осуществить, выбрав необходимую Вам опцию:',
            reply_markup=markup_key, )

        # определяем пользователя
        user = update.message.from_user
        # Пишем в журнал ответ пользователя
        self.logger.info("Пользователь %s - %s", user.first_name, update.message.text)

        # if update.message.text == "Зарегистрировать":
        #     # Здесь важно установить проверку по telegram id есть ли уже такой пользователь в базе данных
        #     return RegistrationConversation()
        # elif update.message.text == "Обновить":
        #     return update.message.reply_text("Данная секция бота находится в разработке")
        # elif update.message.text == "Удалить":
        #     return update.message.reply_text("Данная секция бота находится в разработке")

    def bot_session(self):
        conv_handler_registration = ConversationHandler(  # здесь строится логика разговора
            # точка входа в разговор
            entry_points=[MessageHandler(Filters.regex('^(Зарегистрироваться|зарегистрироваться)$'),
                                         self.registration_conversation.start_registration)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states={
                self.registration_conversation.PERSONAL_INFO_ACCEPTANCE: [
                    MessageHandler(Filters.text, self.registration_conversation.personal_data_acceptance)],
                self.registration_conversation.GENDER: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_gender)],
                self.registration_conversation.SURNAME: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_surname)],
                self.registration_conversation.NAME: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_name)],
                self.registration_conversation.PATRONYMIC: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_patronymic)],
                self.registration_conversation.EMAIL: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_email)],
                self.registration_conversation.PHONE: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_phone)],
                self.registration_conversation.BIRTHDATE: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_birthdate)],
                self.registration_conversation.GRADDATE: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_graddate)],
                self.registration_conversation.INSTITUTE: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_institute)],
                self.registration_conversation.EMPLOYER: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_employer)],
                self.registration_conversation.POSITION: [
                    MessageHandler(Filters.text, self.registration_conversation.reg_position)],
            },
            # точка выхода из разговора
            fallbacks=[CommandHandler('cancel', self.registration_conversation.cancel)],  ##что-то другое нужно
        )

        # Добавляем обработчик разговоров `conv_handler`
        self.dispatcher.add_handler(conv_handler_registration)
        self.dispatcher.add_handler(CommandHandler("start", self.start))




if __name__ == '__main__':
    pass
