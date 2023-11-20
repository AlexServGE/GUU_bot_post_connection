import re

class EmployerChecker:

    def checkUserInputEmployer(self, user_input):
        error_msg_total = ""
        if not self.isUserInputTenLetters(user_input):
            error_msg_total += f"Работодатель: Допустимый размер данных равен не более 255 символов (Вы ввели - {len(user_input)}.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def isUserInputTenLetters(self, user_input):
        pattern = re.compile("^.{,255}$")
        return pattern.match(user_input)
