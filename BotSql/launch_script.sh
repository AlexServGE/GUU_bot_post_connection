#! /bin/bash

touch Token.txt
touch ./PostgreSqlApi/PostgreSQL_config.py
echo "host = '127.0.0.1'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "user = 'None'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "password = 'None'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "db_name = 'None'" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "port = 5432" >> ./PostgreSqlApi/PostgreSQL_config.py
echo "sslmode = 'verify-ca'" >> ./PostgreSqlApi/PostgreSQL_config.py
project_directory = $PWD
mkdir ./ca
cd ./ca
openssl req -new -text -passout pass:None -subj /CN=localhost -out server.req
openssl rsa -in privkey.pem -passin pass:None -out server.key
openssl req -x509 -in server.req -text -key server.key -out server.crt
chown 0:999 server.key
chmod 640 server.key
cd ~
mkdir .postgresql/
cd .postgresql/
cp $project_directory/ca/server.crt .
mv server.crt root.crt