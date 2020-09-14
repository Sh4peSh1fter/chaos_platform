# Things that maybe I should do and improve:
# 1) Some of the names of the vars are too long (like fault_conf_file), so maybe I should shorten "fault conf" to "fc".
# 2) Split the functions to a separated headers file.
# 3) For now, the configuration file doesn't contain the full urls.
# 4) When working with the probes, I think 'active' is not the best name to say if the probe was successful or not.
# 5) Combine all the run_something functions into one
# 6) change the name of this script to "agent"


# Imports
import json
from os import path, mkdir, getcwd, listdir, unlink
from shutil import move, rmtree
from subprocess import Popen, PIPE, check_call
from requests import get, post
from time import sleep
import socket
# from platform import system
from datetime import datetime
from wget import download
import threading
## My Files Imports
from logs_handler import *

# Constants
CONF_FILE_NAME = "fault.conf"
PROBES_FOLDER_NAME = "probes"
METHODS_FOLDER_NAME = "methods"
ROLLBACKS_FOLDER_NAME = "rollbacks"

BUFFER_SIZE = 4096
HEARTBEAT_RATE = 5000


# Globals
# os_type = system() # shouldn't be needed
curr_date = datetime.date(datetime.now())
curr_path = getcwd()
heartbeat_flag = True


# Functions
def create_default_json_event_conf_file():
    data = {}
    data['urls'] = []
    data['urls'].append({
        'db_url': 'http://chaos.db.openshift:5001',
        'fault_url': 'http://chaos.db.openshift:5001/faults/fault_1',
        'probes_url': 'http://chaos.db.openshift:5001/probes',
        'methods_url': 'http://chaos.db.openshift:5001/methods',
        'rollbacks_url': 'http://chaos.db.openshift:5001/rollbacks',
    })
    data['injector_info'] = []
    data['injector_info'].append({
        'injector_ip': '69.420.666.42',
        'injector_port': '6969'
    })

    with open(CONF_FILE_NAME, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def setup_run():
    if path.exists(CONF_FILE_NAME):
        with open(CONF_FILE_NAME, 'r') as event_conf_file:
            conf_vars = json.load(event_conf_file)
    else:
        raise FailedAccessingConfFile

    # Debug print
    print(json.dumps(conf_vars, indent=4))

    ## you need to check and agree what you exspect the names to look like
    db_url = conf_vars['urls'][0]['db_url']
    fault_url = conf_vars['urls'][0]['fault_url']
    probes_url = conf_vars['urls'][0]['probes_url']
    methods_url = conf_vars['urls'][0]['methods_url']
    rollbacks_url = conf_vars['urls'][0]['rollbacks_url']
    injector_ip = conf_vars['injector_info'][0]['injector_ip']
    injector_port = conf_vars['injector_info'][0]['injector_port']

    # Debug print
    print("db url = {}\n"
          "fault url = {}\n"
          "probes url = {}\n"
          "methods url = {}\n"
          "rollbacks utl = {}\n".format(db_url, fault_url, probes_url, methods_url, rollbacks_url))

    return db_url, fault_url, probes_url, methods_url, rollbacks_url, injector_ip, injector_port


def heartbeat(injector_ip, injector_port):
    # global heartbeat_flag
    #
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((injector_ip, injector_port))
    #
    # while heartbeat_flag:
    #     sock.send('ping')
    #     injector_msg = sock.recv(BUFFER_SIZE)
    #     sleep(HEARTBEAT_RATE)
    #
    # sock.close()

    pass


def update_status(event_url):
    # Update "status" value to "running" in the db
    post(event_url, data={'status': 'running'})  # .json()


def get_fault_info(fault_url):
    # Get the fault's info from the db
    fault_info = get(fault_url).json()

    # Debug print
    # for query_res in fault_info:
    #     print(query_res)
    print(json.dumps(fault_info, indent=4))

    # Get probes, methods and rollbacks ready
    probes_names_list = fault_info['probes']
    methods_names_list = fault_info['methods']
    rollbacks_names_list = fault_info['rollbacks']

    # Debug print
    print("probes = {}\n"
          "methods = {}\n"
          "rollbacks = {}\n".format(probes_names_list, methods_names_list, rollbacks_names_list))

    return probes_names_list, methods_names_list, rollbacks_names_list


def run_stage(type, stage_git_url, stage_names_list):
    global curr_path

    for script_name in stage_names_list:
        script_git_path = "{}\{}".format(stage_git_url, script_name)

        try:
            mkdir(type)
            #git.cmd.Git(script_full_path).pull() # i dont know how to pull into another directory
            filename = download(script_git_path)
            script_working_path = "{}\{}".format(curr_path, filename)
            move(curr_path, script_working_path)

            check_call(["python", script_working_path])  ## should i enter more arguments like PIPE?

        except:
            return False
        else:
            return True


def run_fault(probes_url, methods_url, rollbacks_url, probes_names_list, methods_names_list, rollbacks_names_list):
    # Run Probes
    if run_stage('probes', probes_url, probes_names_list):
        # If all the probes run successfully, run all methods
        run_stage('methods', methods_url, methods_names_list)
        if not run_stage('probes', probes_url, probes_names_list):
            # If some of the probes fail, the server didn't handle the event successfully and we run all rollbacks
            run_stage('rollbacks', rollbacks_url, rollbacks_names_list)
            if run_stage('probes', probes_url, probes_names_list):
                # If all the probes  run successfully, log as success and the server should be fine and stable
                raise FaultSuccessful
            else:
                raise ProbesAfterRollbacksFailed
        else:
            raise FaultSuccessful
    else:
        raise ProbesBeforeMethodsFailed


def cleanup():
    print("ping the injector to cleanup the folder(?)")

    # not sure if it deletes the agent itself.
    #
    # global curr_path
    #
    # for filename in listdir(curr_path):
    #     file_path = path.join(curr_path, filename)
    #     try:
    #         if path.isfile(file_path) or path.islink(file_path):
    #             unlink(file_path)
    #         elif path.isdir(file_path):
    #             rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))


# Main
def main():
    global heartbeat_flag

    try:
        ######################################## Preparations for the Event
        # Create default 'fault.conf' file
        create_default_json_event_conf_file()

        # Get all the vars from the fault configuration file as a dict
        db_url, fault_url, probes_url, methods_url, rollbacks_url, injector_ip, injector_port = setup_run()

        heartbeat_thread = threading.Thread(target=heartbeat, args=(injector_ip, injector_port, ))
        heartbeat_thread.start()

        ######################################## Gathering fault information
        # Get the info of the current fault
        probes_names_list, methods_names_list, rollbacks_names_list = get_fault_info(fault_url)

        # Update status to 'running' in db
        update_status(fault_url)

        ######################################## Execution of the Run
        run_fault(probes_url, methods_url, rollbacks_url, probes_names_list, methods_names_list, rollbacks_names_list)

    except FaultSuccessful: # maybe replace the error with 'else', so that if no exceptions was raised, the log that will be sent is success.
        send_log(FAULT_SUCCESSFUL)
    except FailedAccessingConfFile:
        send_log(FAILED_ACCESSING_CONF_FILE)
    except ProbesBeforeMethodsFailed:
        send_log(PROBES_BEFORE_METHODS_FAILED)
    except ProbesAfterRollbacksFailed:
        send_log(PROBES_AFTER_ROLLBACKS_FAILED)
    except Exception as e:
        print(e)
    finally:
        heartbeat_flag = False
        heartbeat_thread.join()
        cleanup()


if __name__ == '__main__':
    main()