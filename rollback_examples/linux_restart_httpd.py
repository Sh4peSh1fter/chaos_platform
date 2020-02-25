import os

def restart_service(service_name):
    service_status = os.system("sudo service {} restart".format(service_name))

    return service_status


if __name__ == '__main__':
    restart_service("httpd")