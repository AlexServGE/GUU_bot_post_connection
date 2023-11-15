import psycopg2
from PostgreSqlApi.PostgreSQL_config import host, user, password, db_name, port, sslmode


class SqlApiDeleteProfile:

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

    def sql_delete_user(self, user_telegram_id):
        try:
            self.establish_sql_connection()
            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                    DELETE FROM graduates WHERE Telegram_id = %s; 
                    """, (user_telegram_id,))
                # connection.commit()
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
        finally:
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")
