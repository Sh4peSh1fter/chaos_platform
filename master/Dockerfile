FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV LISTEN_PORT 5003
ENV PICKER_API="http://52.255.160.180:5005"
ENV INJECTOR_API="http://52.255.160.180:5002"
EXPOSE 5003
COPY ./app /app
RUN pip install -r requirements.txt
