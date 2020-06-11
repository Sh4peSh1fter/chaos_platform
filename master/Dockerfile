FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV LISTEN_PORT 5003
EXPOSE 5003
COPY ./app /app
RUN pip install -r requirements.txt
