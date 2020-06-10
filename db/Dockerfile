FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV DB_IP="52.255.160.180"
ENV DB_PORT 8080
ENV DB_NAME="chaos"

EXPOSE 5001
COPY ./app /app
RUN pip install -r requirements.txt
