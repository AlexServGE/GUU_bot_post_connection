import re


class EmailChecker:

    def checkUserInputEmail(self, user_input):
        error_msg_total = ""
        if not self.is_user_input_contains_spec_symbol(user_input):
            error_msg_total += "Email: Должен содержать @ до доменного имени.\n"
            error_msg_total += "Email: Должен содержать точку после доменного имени.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def is_user_input_contains_spec_symbol(self, user_input):
        pattern = re.compile(r'^.+@.+\..+$')  # sas@ya.ru | sas.ser@ya.ru | sas@ya
        return pattern.match(user_input)
