from Controller import Controller
from telegram.error import InvalidToken

with open('Token.txt', 'r', encoding='utf-8') as file:
    token = file.read().strip("\n")

try:
    controller = Controller(token)
except InvalidToken as e:
    if token == "":
        print(
            "В файле Token.txt отсутствует токен. \n"
            "Зайдите в телеграм и получите токен у BotFather. Затем скопируйте и сохраните токен в Token.txt")
    else:
        print(
            f"В файле Token.txt указан некорректный токен : >>>{token}<<<. \n"
            "Зайдите в телеграм и получите токен у BotFather. Затем скопируйте и сохраните токен в Token.txt")

