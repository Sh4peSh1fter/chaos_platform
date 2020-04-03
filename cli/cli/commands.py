import click
import env_config as config

@click.group('cli')
def cli():
    pass


@cli.group('config')
def cli_config():
    pass


@click.option('--master-url',default = None ,
              help = "Time in seconds between each fault",type = str ,required = False)
@cli_config.command('set')
def config_set(master_url):
    if master_url :
        print(config.set_master_url(master_url))


@click.option('--master-url',default = False ,
              help = "Get the url of the master", is_flag=True ,required = False)
@click.option('--db-url',default = False ,
              help = "Get the url of the db api", is_flag=True ,required = False)
@click.option('--random-picker-url',default = False ,
              help = "Get the url of the random picker", is_flag=True ,required = False)
@click.option('--injector-url',default = False ,
              help = "Get the url of the injector", is_flag=True ,required = False)
@click.option('--all',default = False ,
              help = "Get all cli configurations", is_flag=True ,required = False)
@cli_config.command('get')
def config_get(master_url,db_url,random_picker_url,injector_url,all):

    if master_url :
        master_url = config.get_master_url()
        print("\n master-url = {}".format(master_url))

    if db_url :
        db_url = config.get_db_url()
        print("\n db-url = {}".format(db_url))


    if random_picker_url :
        random_picker_url = config.get_random_picker_url()
        print("\n random-picker-url = {}".format(random_picker_url))


    if injector_url :
        injector_url = config.get_injector_url()
        print("\n injector-url = {}".format(injector_url))


    if all :
        master_url = config.get_master_url()
        print("\n master-url = {}".format(master_url))

        db_url = config.get_db_url()
        print("\n db-url = {}".format(db_url))

        random_picker_url = config.get_random_picker_url()
        print("\n random-picker-url = {}".format(random_picker_url))

        injector_url = config.get_injector_url()
        print("\n injector-url = {}".format(injector_url))