import re

class GraddateChecker:

    def checkUserInputGraddate(self, user_input):
        error_msg_total = ""
        if not user_input.isdigit():
            error_msg_total += "Год окончания: Должен содержать только цифры.\n"
        if len(user_input) != 4:
            error_msg_total += "Год окончания: Должен содержать 4 символа.\n"
        if error_msg_total != "":
            return error_msg_total
        else:
            return None


if __name__=="__main__":
    graddate_checker = GraddateChecker()
    msg_for_user = graddate_checker.checkUserInputGraddate("19992")
    print(msg_for_user)