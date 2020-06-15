FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV DB_URI="mongodb://52.255.160.180:8080/chaos"
ENV DB_NAME="chaos"
ENV LISTEN_PORT 5001

EXPOSE 5001
COPY ./app /app
RUN pip install -r requirements.txt
