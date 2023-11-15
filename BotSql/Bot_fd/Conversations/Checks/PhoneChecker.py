import re

class PhoneChecker:

    def checkUserInputPhone(self, user_input):
        error_msg_total = ""
        if not self.isUserInputNumbersOnly(user_input):
            error_msg_total += "Телефон: Допустимыми символами являются только цифры.\n"
        if not self.isUserInputElevenNumbers(user_input):
            error_msg_total += f"Телефон: Допустимое количество символов - 11 символов (Вы ввели - {len(user_input)}.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def isUserInputNumbersOnly(self, user_input):
        pattern = re.compile("^[0-9]+$")
        return pattern.match(user_input)

    def isUserInputElevenNumbers(self, user_input):
        pattern = re.compile("^.{11}$")
        return pattern.match(user_input)


if __name__=="__main__":
    phone_checker = PhoneChecker()
    msg_for_user = phone_checker.checkUserInputPhone("21703266123")
    print(msg_for_user)