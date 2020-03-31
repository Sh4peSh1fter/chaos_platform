import click
import requests
import env_config


@click.group('master')
def master():
    pass


@master.group('get')
def master_get():
    pass


@master.command('set')
@click.option('--timing-interval',default = None ,
              help = "Time in seconds between each fault",type = int,required = False)

def chaos_set(timing_interval):
    if timing_interval :
        output = change_fault_timer_interval(timing_interval)
        print("\n{}".format(output))



@master_get.command('info')
def chaos_info():
        output = get_master_info()
        print("\n{}".format(output))


def get_master_info():
    master_url = env_config.get_master_url()
    master_info_get_route = "{}/master-info".format(master_url)
    try :
        output = requests.get(master_info_get_route)
    except :
        output = "Could not connect to master at {} check connection ".format(master_info_get_route)
    return output


def change_fault_timer_interval(new_timing_interval):
    master_url = env_config.get_master_url()
    master_timing_interval_update_route = "{}/set-interval".format(master_url)
    try :
        output = requests.post(master_timing_interval_update_route,json= {'interval' : new_timing_interval})
    except :
        output = "Could not connect to master at {} check connection ".format(master_timing_interval_update_route)
    return output

