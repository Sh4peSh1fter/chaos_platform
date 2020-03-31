import click
import requests
import env_config

@click.group('db')
def db():
    pass

@click.option('--collection',
              help = "The collection to which the object will be added to",type = str ,required = True)
@click.option('--new-object',
              help = "The object that will be added to the collection",type = str ,required = True)
@db.command('add')
def db_add(new_object, collection):
    output = add_data_to_db(new_object, collection)
    print(output)

def add_data_to_db(data,collection):
    db_api_url = env_config.get_db_url()
    db_api_ip_route = "{}/{}".format(db_api_url,collection)
    try :
        output = requests.post(db_api_ip_route,json= data)
    except :
        output = "Could not connect to db api on route {} check connection".format(db_api_ip_route)
    return output


def add_object_to_db():
    pass

def remove_object_from_db():
    pass

def update_object_in_db():
    pass