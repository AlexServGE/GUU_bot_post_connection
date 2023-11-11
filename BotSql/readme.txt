1 Specify:
/docker-compose.yml
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}

2 Create file:
/PostgreSqlApi/PostgreSQL_config

	Put:
host = "xxx.xxx.x.xx"
user = "xxxxxx"
password = "xxxxxx"
db_name = "xxxxxx"
port = 5432


3 Create file:
/Token
	Put:
xxxxxxxxxx:????????????????????
