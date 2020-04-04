from os.path import expanduser,dirname
from pathlib import Path
import json

home_dir = expanduser("~")
chaos_home_dir = "{}/.chaos".format(home_dir)
config_file = "{}/config.json".format(chaos_home_dir)
print(config_file)

Path(home_dir).mkdir(parents=True, exist_ok=True)



def get_random_picker_url():
    random_picker_url = get_data_from_json_file(config_file, "picker-url")
    return random_picker_url

def get_injector_url():
    injector_url = get_data_from_json_file(config_file, "injector-url")

    return injector_url

def get_master_url():
    master_url = get_data_from_json_file(config_file, "master-url")
    return master_url

def get_db_url():
    db_url = get_data_from_json_file(config_file, "db-url")
    return db_url

def set_master_url(new_url):
    try:
        add_data_to_json_file(config_file, 'master-url' , new_url)
        return True
    except :
        return False


def set_db_url(new_url):
    try:
        add_data_to_json_file(config_file, 'db-url' , new_url)
        return True
    except:
        return False

def set_injector_url(new_url):
    try:
        add_data_to_json_file(config_file, 'injector-url' , new_url)
        return True
    except :
        return False


def set_random_picker_url(new_url):
    try:
        add_data_to_json_file(config_file,'picker-url' , new_url)
        return True
    except :
        return False


def get_data_from_json_file(file_path, varible_name):
    try :
        with open(file_path,'r') as json_file :
            file_data  = json.load(json_file)
            reqested_data = file_data[varible_name]
        return  reqested_data,True
    except IOError :
        return "problem accrued",False


def add_data_to_json_file(file_path, varible_name,varible_value):
    with open(file_path,'r+') as json_file :
        file_data  = json.load(json_file)
        file_data[varible_name] = varible_value

        # Rewind to the start of the file
        json_file.seek(0)
        json.dump(file_data, json_file)
        # Truncate in case new data is smaller than old data
        file_data.truncate()



