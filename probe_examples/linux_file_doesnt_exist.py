import os

def get_service_status(service_name):
    service_status = os.system("service {} status".format(service_name))
    if service_status == 0 :
        return True
    else :
        return False

if __name__ == '__main__':
    get_service_status("httpd")