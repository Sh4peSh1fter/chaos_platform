from os.path import expanduser,dirname
from pathlib import Path
import json
import os

home_dir = expanduser("~")
chaos_home_dir = "{}/.chaos".format(home_dir)
config_file = "{}/config.json".format(chaos_home_dir)

Path(home_dir).mkdir(parents=True, exist_ok=True)



def get_random_picker_url():
    random_picker_url = get_object_from_json_file(config_file, "picker-url")
    return random_picker_url

def get_injector_url():
    injector_url = get_object_from_json_file(config_file, "injector-url")

    return injector_url

def get_master_url():
    master_url,result = get_object_from_json_file(config_file, "master-url")
    return master_url

def get_db_url():
    db_url = get_object_from_json_file(config_file, "db-url")
    return db_url

def set_master_url(new_url):
    #try:
        add_data_to_json_file(config_file, 'master-url' , new_url)
     #   return True
    #except :
    #    return False


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



def validate_home_dir(home_dir_addrs):
    home_dir_exists = os.path.isdir(home_dir_addrs)
    if home_dir_exists :
        return True
    else:
        try :
            os.makedirs(home_dir_addrs)
            return True
        except:
            return False


def get_config_json(file_path = config_file ):
    try :
        with open(file_path,'r') as config_file :
            json_config = json.load(config_file)
            return json_config
    except :
        return {}

def get_object_from_json_file(file_path, varible_name):
    validate_home_dir(chaos_home_dir)

    try :
        with open(file_path,'r') as json_file :
            file_data  = json.load(json_file)
            reqested_data = file_data[varible_name]
        return  reqested_data,True
    except IOError :
        return "problem accrued",False


def add_data_to_json_file(file_path, varible_name,varible_value):
    validate_home_dir(chaos_home_dir)
    json_config = get_config_json(file_path)
    with open(file_path,'w+') as json_file :
        json_config[varible_name] = varible_value
        # Rewind to the start of the file
        json_file.seek(0)
        json.dump(json_config, json_file)
        # Truncate in case new data is smaller than old data
        json_file.truncate()


