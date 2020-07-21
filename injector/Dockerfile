FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV SERVER_PORT 5002
ENV LISTEN_PORT 5002
ENV DB_API="http://52.255.160.180:5001"
EXPOSE 5002
COPY ./app /app
RUN yum -y install python-devel krb5-devel krb5-libs krb5-workstation
RUN yum install kinit
RUN pip install -r requirements.txt
