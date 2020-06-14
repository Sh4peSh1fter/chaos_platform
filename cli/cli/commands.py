import click
import file_config as config

@click.group('cli')
def cli():
    pass


@cli.group('config')
def cli_config():
    pass

@click.option('--db-url',default = None ,
              help = "Time in seconds between each fault",type = str ,required = False)
@click.option('--master-url',default = None ,
              help = "Time in seconds between each fault",type = str ,required = False)
@cli_config.command('set')
def config_set(master_url,db_url):
    if master_url :
        print(config.set_master_url(master_url))
    if db_url :
        print(config.set_db_url(db_url))

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
        print_output("\n master-url = {}".format(master_url))

    if db_url :
        db_url = config.get_db_url()
        print_output("\n db-url = {}".format(db_url))


    if random_picker_url :
        random_picker_url = config.get_random_picker_url()
        print_output("\n random-picker-url = {}".format(random_picker_url))


    if injector_url :
        injector_url = config.get_injector_url()
        print_output("\n injector-url = {}".format(injector_url))


    if all :
        config_json = config.get_config_json()
        for varible in config_json.keys():
            print_output("\n {} = {}".format(varible,config_json[varible]))


def print_output(output):
    print(output)
