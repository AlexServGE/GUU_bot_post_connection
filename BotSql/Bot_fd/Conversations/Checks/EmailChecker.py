import re


class EmailChecker:

    def checkUserInputEmail(self, user_input):
        error_msg_total = ""
        if not self.is_user_input_contains_spec_symbol(user_input):
            error_msg_total += "Email: Должен содержать один символ @.\n"
        if not self.is_user_input_contains_dot(user_input):
            error_msg_total += "Email: Должен содержать точку после доменного имени.\n"
        if not self.is_user_input_contains_only_latin(user_input):
            error_msg_total += "Email: Должен содержать только латинские буквы.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None

    def is_user_input_contains_spec_symbol(self, user_input):
        pattern = re.compile(r'^\w+@\w+\.\w+$|^\w+\.\w+@\w+\.\w+$|^\w+@\w+$')  # sas@ya.ru | sas.ser@ya.ru | sas@ya
        return pattern.match(user_input)

    def is_user_input_contains_dot(self, user_input):
        pattern = re.compile(r'^\w+\.\w+@\w+\.\w+$|^\w+@\w+\.\w+$|^\w+\.\w+\.\w+$')  # sas.sas@ya.ru| sas@ya.ru | sas.ser.ru
        return pattern.match(user_input)

    def is_user_input_contains_only_latin(self, user_input):
        pattern = re.compile(
            r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
            r'|^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
            r'|^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@$'
            r'|^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
            r'|^[a-zA-Z0-9]+@[a-zA-Z0-9]+$'
            r'|^[a-zA-Z0-9]+\.@[a-zA-Z0-9]+$'
            r'|^[a-zA-Z0-9]+\.@[a-zA-Z0-9]+\.$'
            r'|^[a-zA-Z0-9]+\.@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')  # [sas].[sas]@[ya].[ru] |
        # [sas]@[ya].[ru] | [sas].[sas]@ | [sas].[sas]
        # |[sas]@[sas] | [sas].@[ya] | [sas].@[ya]. | [sas].@[ya].[ru]
        return pattern.match(user_input)


if __name__ == "__main__":
    email_checker = EmailChecker()
    msg_for_user = email_checker.checkUserInputEmail("alexandr@fhdhd.ru")
    print(msg_for_user)
