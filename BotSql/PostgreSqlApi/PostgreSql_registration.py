import psycopg2

from PostgreSqlApi.PostgreSQL_config import host, user, password, db_name, port, sslmode


class SqlApiRegistration:

    def __init__(self):
        self.connection = None

    def establish_sql_connection(self):
        try:
            # connect to existing database
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port,
                sslmode=sslmode,
            )
            self.connection.autocommit = True
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")

    def sql_select_all_user_info(self, ex_student_telegram_id):
        try:
            self.establish_sql_connection()
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM graduates WHERE Telegram_id = %s; 
                    """, (ex_student_telegram_id,))
                user_sql_info_tuple = cursor.fetchone()
                print(user_sql_info_tuple)  # позднее удалить!
                return user_sql_info_tuple
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
        finally:
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")

    def sql_insert_user_info(self, user):
        try:
            self.establish_sql_connection()
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO graduates (
                    Date_of_registration,
                    Telegram_id,
                    Telegram_nickname,
                    Personal_info_acceptance,
                    Gender,
                    Surname,
                    Name,
                    Patronymic,
                    Email,
                    Phone,
                    Birthdate,
                    Graduation_date,
                    EdProgram,
                    Employer,
                    Position)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); 
                    """, (user.user_date_of_first_registration,
                          user.user_telegram_id,
                          user.user_telegram_nickname,
                          user.user_PERSONAL_INFO_ACCEPTANCE,
                          user.user_GENDER,
                          user.user_SURNAME,
                          user.user_NAME,
                          user.user_PATRONYMIC,
                          user.user_EMAIL,
                          user.user_PHONE,
                          user.user_BIRTHDATE,
                          user.user_GRADDATE,
                          user.user_EDPROGRAM,
                          user.user_EMPLOYER,
                          user.user_POSITION))
                # connection.commit()
                print(f"[INFO] Following data was successfully inserted about user:\n {user}")
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
        finally:
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")