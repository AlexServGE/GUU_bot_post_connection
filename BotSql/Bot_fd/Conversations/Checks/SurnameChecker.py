import re

class SurnameChecker:

    def checkUserInputSurname(self, user_input):
        error_msg_total = ""
        if not self.isUserInputLettersOnly(user_input):
            error_msg_total += "Фамилия: Допустимыми символами являются только буквы из кириллицы.\n"
        if not self.isUserInputTenLetters(user_input):
            error_msg_total += f"Фамилия: Допустимый размер данных равен не менее 2 и не более 10 символов (Вы ввели - {len(user_input)}.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def isUserInputLettersOnly(self, user_input):
        pattern = re.compile("^[а-яёА-ЯЁ]+$")
        return pattern.match(user_input)

    def isUserInputTenLetters(self, user_input):
        pattern = re.compile("^.{2,10}$")
        return pattern.match(user_input)


if __name__=="__main__":
    surname_checker = SurnameChecker()
    msg_for_user = surname_checker.checkUserInputSurname("серг342")
    print(msg_for_user)