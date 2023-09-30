import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta


class SqlApiSel:

    def __init__(self):
        self.con = None
        self.establish_sql_connection()

    def establish_sql_connection(self):
        try:
            self.con = sqlite3.connect("../ProcurementsDB/Procurements.db")
            print("Connection is established: Database is created in memory")
        except Error:
            print(Error)
            self.con.close()

    def sql_select_daily_procurements(self,user_filters):
        cursorObj = self.con.cursor()

        today = datetime.today().date().strftime("%d.%m.%Y")
        yesterday = (datetime.today().date() - timedelta(days=1)).strftime("%d.%m.%Y")
        yesterdaytwice = (datetime.today().date() - timedelta(days=2)).strftime("%d.%m.%Y")
        today_week_day = datetime.today().weekday()
        if today_week_day == 0:
            cursorObj.execute(
                f'SELECT procurement_id,procurement_publication_date,procurement_customer,procurement_total_value,procurement_object,procurement_link FROM daily_new_procurements WHERE pharma_category_title = "{user_filters[0]}" AND procurement_federal_region = "{user_filters[1]}" AND procurement_publication_date BETWEEN "{(datetime.today().date() - timedelta(days=3)).strftime("%d.%m.%Y")}" AND "{yesterday}"')  ## необходимо использовать функцию, которая передаёт текущий день в where
        elif today_week_day == 1:
            cursorObj.execute(
                f'SELECT procurement_id,procurement_publication_date,procurement_customer,procurement_total_value,procurement_object,procurement_link FROM daily_new_procurements WHERE pharma_category_title = "{user_filters[0]}" AND procurement_federal_region = "{user_filters[1]}" AND procurement_publication_date BETWEEN "{(datetime.today().date() - timedelta(days=4)).strftime("%d.%m.%Y")}" AND "{yesterday}"')  ## необходимо использовать функцию, которая передаёт текущий день в where
        else:
            cursorObj.execute(
                f'SELECT procurement_id,procurement_publication_date,procurement_customer,procurement_total_value,procurement_object,procurement_link FROM daily_new_procurements WHERE pharma_category_title = "{user_filters[0]}" AND procurement_federal_region = "{user_filters[1]}" AND procurement_publication_date BETWEEN "{yesterdaytwice}" AND "{yesterday}"')  ## необходимо использовать функцию, которая передаёт текущий день в where
        selected_data_list = cursorObj.fetchall()
        return selected_data_list


if __name__ == '__main__':
    sql_api_sel = SqlApiSel()
    print(sql_api_sel.sql_select_daily_procurements())


