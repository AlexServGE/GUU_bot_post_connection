#! /bin/bash

touch Token.txt
touch ./PostgreSqlApi/PostgreSQL_config.py
echo "host = '127.0.0.1'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "user = 'None'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "password = 'None'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "db_name = 'None'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "port = 5432" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "sslmode = 'require'" >> ./PostgreSqlApi/PostgreSQL_config.py
