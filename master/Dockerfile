FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV PICKER_API "http://127.0.0.1:5005"
ENV INJECTOR_API "http://127.0.0.1:5002"
ENV SERVER_PORT 5003
ENV LISTEN_PORT 5003
EXPOSE 5003
COPY ./app /app
RUN pip install -r requirements.txt
