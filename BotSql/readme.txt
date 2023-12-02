1 All commands are made from root
2 Change password for CA-certificate creation in launch_script: -passout pass:None
3 Launch by command: ./launch_script.sh
4 Specify:
/docker-compose.yml
      POSTGRES_USER: USER
      POSTGRES_PASSWORD: PASSWORD

5 Specify:
host = "172.20.0.5"
user = "USER"
password = "PASSWORD"
db_name = "project_db"
port = 5432

6 Put token:
/Token.txt
	Put:
xxxxxxxxxx:????????????????????

7 Build by command: docker-compose build
8 Launch by command: docker-compose up
9 Connect to server via pgadmine from out of the server, using root.crt
10 Create database and table

CREATE TABLE graduates (
Graduate_id SERIAL,
Date_of_registration timestamp,
Telegram_id bigint,
Telegram_nickname varchar(32),
Personal_info_acceptance varchar(16),
Gender varchar(16),
Surname varchar(16),
Name varchar(16),
Patronymic varchar(32),
Email varchar(32),
Phone bigint,
Birthdate varchar(32),
Graduation_date int,
Institute varchar(32),
Employer varchar(255),
Position varchar(32)
);

11 Share bot with the users