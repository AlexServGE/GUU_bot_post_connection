FROM python:3.9
RUN mkdir ./BotSql/
COPY ./ ./BotSql/
RUN apt update && apt install -y tzdata
RUN mkdir /root/.postgresql
COPY ./ca/server.crt /root/.postgresql/root.crt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN python -m pip install -r ./BotSql/requirements.txt
WORKDIR ./BotSql/
CMD [ "python", "main.py" ]
