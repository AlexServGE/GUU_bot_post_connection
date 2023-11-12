import psycopg2

from PostgreSqlApi.PostgreSQL_config import host, user, password, db_name, port
from datetime import datetime, timedelta


class SqlApiChangeProfile:

    def __init__(self):
        self.connection = None
        self.establish_sql_connection()

    def establish_sql_connection(self):
        try:
            # connect to existing database
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port,
            )
            self.connection.autocommit = True
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")

    def connection_close(self):
        if self.connection:
            self.connection.close()

    def sql_select_all_user_info(self, ex_student_telegram_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM graduates WHERE Telegram_id = %s; 
                    """, (ex_student_telegram_id,))
                user_sql_info_tuple = cursor.fetchone()
                print(user_sql_info_tuple) #позднее удалить!
                return user_sql_info_tuple
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")

    def sql_update_user_info(self, sql_field_updated, user_attrib_to_update,user_telegram_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE graduates SET {sql_field_updated} = %s WHERE Telegram_id = %s; 
                    """, (user_attrib_to_update,
                          user_telegram_id,))
                # connection.commit()
        except Exception as _ex:
            print(f"[INFO] Error while working with PostgreSQL - {_ex}")
            if self.connection:
                # cursor.close()  #необходимо указывать, если не используется with .. as
                self.connection.close()
                print(f"[INFO] PostgreSQL connection closed")

    # def sql_select_daily_procurements(self, user_filters):
    #     cursorObj = self.con.cursor()
    #
    #     today = datetime.today().date().strftime("%d.%m.%Y")
    #     yesterday = (datetime.today().date() - timedelta(days=1)).strftime("%d.%m.%Y")
    #     yesterdaytwice = (datetime.today().date() - timedelta(days=2)).strftime("%d.%m.%Y")
    #     today_week_day = datetime.today().weekday()
    #     if today_week_day == 0:
    #         cursorObj.execute(
    #             f'SELECT procurement_id,procurement_publication_date,procurement_customer,procurement_total_value,procurement_object,procurement_link FROM daily_new_procurements WHERE pharma_category_title = "{user_filters[0]}" AND procurement_federal_region = "{user_filters[1]}" AND procurement_publication_date BETWEEN "{(datetime.today().date() - timedelta(days=3)).strftime("%d.%m.%Y")}" AND "{yesterday}"')  ## необходимо использовать функцию, которая передаёт текущий день в where
    #     elif today_week_day == 1:
    #         cursorObj.execute(
    #             f'SELECT procurement_id,procurement_publication_date,procurement_customer,procurement_total_value,procurement_object,procurement_link FROM daily_new_procurements WHERE pharma_category_title = "{user_filters[0]}" AND procurement_federal_region = "{user_filters[1]}" AND procurement_publication_date BETWEEN "{(datetime.today().date() - timedelta(days=4)).strftime("%d.%m.%Y")}" AND "{yesterday}"')  ## необходимо использовать функцию, которая передаёт текущий день в where
    #     else:
    #         cursorObj.execute(
    #             f'SELECT procurement_id,procurement_publication_date,procurement_customer,procurement_total_value,procurement_object,procurement_link FROM daily_new_procurements WHERE pharma_category_title = "{user_filters[0]}" AND procurement_federal_region = "{user_filters[1]}" AND procurement_publication_date BETWEEN "{yesterdaytwice}" AND "{yesterday}"')  ## необходимо использовать функцию, которая передаёт текущий день в where
    #     selected_data_list = cursorObj.fetchall()
    #     return selected_data_list


if __name__ == '__main__':
    pass
