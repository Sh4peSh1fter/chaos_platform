import requests
from time import sleep, strftime
import subprocess
import json

class Injector :

    def __init__(self,db_api_url = "http://chaos.db.openshift:5001"):
        self.db_api_url = db_api_url

    def start_expirement(self, dns, fault_name):
        experiment_id = self._set_object_in_db(dns, fault_name, "loading")
        self._create_config_file(dns, experiment_id, fault_name)
        self._run_playbook('insert_agent.yaml', dns)

        # Set vars that decide how often to check if experiment is finished
        experiment_finished = False
        pause = 5
        waited_time = 0
        max_waited_time = 600
        # Wait for experiment to finish and then clean the victim.
        while not experiment_finished :
            experiment_finished = self._is_expirement_finished(experiment_id)
            sleep(pause)
            waited_time = waited_time + pause
            if max_waited_time <= waited_time :
                break

        self._run_playbook('remove_agent.yaml', dns)
        self._set_object_in_db(dns, fault_name, "completed")

    def _set_object_in_db(self, dns, fault_name, status, http_method):
        experiment_object = {'timestamp' : self._get_current_time(),
                             'victim' : dns, "fault_name" : fault_name,
                             'status' : status
                             }
        experiment_id = requests.post(f"{self.db_api_url}/experiments", json = experiment_object)
        return experiment_id

    @staticmethod
    def _get_current_time():
        current_time = strftime('%Y%m%d%H%M%S')
        return current_time

    @staticmethod
    def _create_config_file(dns, experiment_id, fault_name):
        conf_file = "/etc/chaos_files/tmp/fault.conf"
        data = {'dns' : dns , 'experiment_id' : experiment_id,
                'fault_name' : fault_name}

        with open(conf_file, 'w') as outfile:
            json.dump(data, outfile)

    def _run_playbook(self, dns, playbook_name):
        os_type = self._get_os_type(dns)
        subprocess.run(["ansible-playbook", f"{playbook_name}", f'-e "host={dns} os_type={os_type}"'])

    def _get_os_type(self,dns):
        os_type = "linux"
        return os_type
    
    def _is_expirement_finished(self, experiment_id):
        experiment_obj = requests.get(f"{self.db_api_url}/experiments/{experiment_id}").json()
        if experiment_obj['status'] == 'finished_injection':
            return True
        else:
            return False

