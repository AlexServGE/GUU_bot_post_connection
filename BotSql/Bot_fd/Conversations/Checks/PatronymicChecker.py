import re

class PatronymicChecker:

    def checkUserInputPatronymic(self, user_input):
        error_msg_total = ""
        if not self.isUserInputLettersOnly(user_input):
            error_msg_total += "Отчество: Допустимыми символами являются только буквы из кириллицы.\n"
        if not self.isUserInputTenLetters(user_input):
            error_msg_total += f"Отчество: Допустимый размер данных равен не менее 2 и не более 16 символов (Вы ввели - {len(user_input)}.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def isUserInputLettersOnly(self, user_input):
        pattern = re.compile("^[а-яёА-ЯЁ]+$")
        return pattern.match(user_input)

    def isUserInputTenLetters(self, user_input):
        pattern = re.compile("^.{2,16}$")
        return pattern.match(user_input)
