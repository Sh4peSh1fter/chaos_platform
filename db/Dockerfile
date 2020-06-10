FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV SERVER_PORT 5001
ENV LISTEN_PORT 5001
EXPOSE 5001
COPY ./app /app
RUN pip install -r requirements.txt
