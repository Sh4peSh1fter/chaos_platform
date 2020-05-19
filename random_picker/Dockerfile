FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV API_PORT 5001
ENV API_DB_HOST "52.255.160.180"
ENV LISTEN_PORT 5005
EXPOSE 5005
COPY ./app /app
RUN pip install -r requirements.txt
