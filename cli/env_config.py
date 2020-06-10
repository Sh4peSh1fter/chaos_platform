import os

def get_random_picker_url():
    random_picker_url = os.environ.get("PICKER_API", "http://127.0.0.1:5001")
    return random_picker_url

def get_injector_url():
    injector_url = os.environ.get("INJECTOR_API", "http://127.0.0.1:5002")
    return injector_url

def get_master_url():
    master_url = os.environ.get("MASTER_API", "http://127.0.0.1:5003")
    return master_url

def get_db_url():
    db_url = os.environ.get("DB_API", "http://127.0.0.1:5004")
    return db_url

def set_master_url(new_url):
    try:
        os.environ["MASTER_API"] = new_url
        return True
    except :
        return False


def set_db_url(new_url):
    try:
        os.environ["DB_API"] = new_url
        return True
    except:
        return False

def set_injector_url(new_url):
    try:
        os.environ["INJECTOR_API"] = new_url
        return True
    except :
        return False


def set_random_picker_url(new_url):
    try:
        os.environ["PICKER_API"] = new_url
        return True
    except :
        return False