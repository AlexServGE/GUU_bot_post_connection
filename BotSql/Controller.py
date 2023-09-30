import logging

from telegram.ext import (
    Updater,
)

from Bot_fd.ConversationBot import ConversationBot


class Controller:

    def __init__(self, token):
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.logger = self.start_logging()
        self.conversation_bot = ConversationBot(self.updater, self.dispatcher, self.logger)
        self.start_bot()


    def start_logging(self):
        # Ведение логов
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        return logging.getLogger(__name__)

    def start_bot(self):
        # Запуск бота
        self.conversation_bot.bot_session()
        self.updater.start_polling()
        self.updater.idle()
