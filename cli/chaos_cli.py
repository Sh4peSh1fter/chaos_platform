import click
import os
import requests

class ChaosSystem(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug


@click.group()
def cli_main():
    pass

@cli_main.group()
def master():
    pass

@master.command()
@click.option('--timing-interval',default = None , help = "Time in seconds between each fault",type = int,required = False)
def set(timing_interval):
    if timing_interval :
        output = change_fault_timer_interval(timing_interval)
        print("\n{}".format(output))


@cli_main.group()
def db():
    pass

@click.option('--collection', help = "The collection to which the object will be added to",type = str ,required = True)
@click.option('--object', help = "The object that will be added to the collection",type = str ,required = True)
@db.command()
def add(object,collection):
    output = add_data_to_db(object,collection)
    print(output)

def change_fault_timer_interval(new_timing_interval):
    master_ip = get_master_ip()
    master_timing_interval_update_route = "http://{}/set-interval".format(master_ip)
    try :
        output = requests.post(master_timing_interval_update_route,json= {'timing-interval' : new_timing_interval})
    except :
        output = "Could not connect to master"
    return output

def add_data_to_db(data,collection):
    db_api_ip = get_master_ip()
    db_api_ip_route = "http://{}/{}".format(db_api_ip,collection)
    try :
        output = requests.post(db_api_ip_route,json= data)
    except :
        output = "Could not connect to db api"
    return output

def get_master_ip():
    pass

def get_db_api_ip():
    pass

def add_object_to_db():
    pass

def remove_object_from_db():
    pass

def update_object_in_db():
    pass

