import os

def stop_service(service_name):
    service_status = os.system("sudo service {} stop".format(service_name))
    return service_status


if __name__ == '__main__':
    stop_service("httpd")