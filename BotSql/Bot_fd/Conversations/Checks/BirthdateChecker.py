import re

class BirthdateChecker:

    def checkUserInputBirthdate(self, user_input):
        error_msg_total = ""
        if not self.is_user_input_contains_dots(user_input):
            error_msg_total += "Год рождения: формат не соответствует требуемому (01.01.1999).\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def is_user_input_contains_dots(self, user_input):
        pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
        return pattern.match(user_input)


if __name__=="__main__":
    birthdate_checker = BirthdateChecker()
    msg_for_user = birthdate_checker.checkUserInputBirthdate("23.d4.1989")
    print(msg_for_user)