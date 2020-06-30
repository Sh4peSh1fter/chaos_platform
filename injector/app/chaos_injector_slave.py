import requests
from time import sleep
import subprocess
import os
import time

class InjectionSlave():

    def __init__(self,db_api_url = "http://chaos.db.openshift:5001"):
        self.db_api_url = db_api_url


    def initiate_fault(self,dns,fault):
        print("#######################################################")
        return self._orchestrate_injection(dns,fault)

    def _orchestrate_injection(self,dns,fault_name):
        try :
            # Gets fault full information from db
            fault_info = self._get_fault_info(fault_name)
            print(fault_info)
        except Exception as E :
            print({ "exit_code":"1" ,"status": "Injector failed gathering facts" })

            return { "exit_code":"1" ,"status": "Injector failed gathering facts" }
        try :
            # Runs the probes,methods and rollbacks by order.
            logs_object = self._run_fault(dns, fault_info)
            print(logs_object)
        except :
            print({ "exit_code":"1" ,"status": "Injector failed injecting fault" })

            return { "exit_code":"1" ,"status": "Injector failed injecting fault" }
        try :
            # Sends logs to db to be stored in the "logs" collection
            db_response = self._send_result(dns,logs_object,"logs")
            return db_response
        except Exception as E:
            return { "exit_code":"1" ,"status": "Injector failed sending logs to db" }



    def _get_fault_info(self,fault_name):
        # Get json object for db rest api
        db_fault_api_url = f"{self.db_api_url}/fault/{fault_name}"

        fault_info = requests.get(db_fault_api_url).json()
        # Get the names of the parts of the fault
        name  = fault_info["name"]
        parts = ["probes", "methods", "rollbacks", "name"]
        fault_structure = {key: value for key, value in fault_info.items() if key in parts}


        # fault_section can be the probes/methods/rollbacks part of the fault
        for fault_section in fault_structure.keys():
            fault_section_parts = []

            # section_part refers to a specific part of the probes/methods/rollbacks
            for section_part in fault_structure[fault_section]:
                section_part_info = requests.get("{}/{}/{}".format(self.db_api_url,fault_section,section_part)).json()
                fault_section_parts.append(section_part_info)

            fault_structure[fault_section] = fault_section_parts

        fault_structure["name"] =  name
        return fault_structure


    def _run_fault(self,dns,fault_info):
        try:

            # Gets fault parts from fault_info
            fault_name = fault_info['name']
            probes = fault_info['probes']
            methods = fault_info['methods']
            rollbacks = fault_info['rollbacks']

        except Exception as E :
            logs_object = {'name': fault_name ,'exit_code' : '1' ,
                           'status' : 'expirement failed because parameters in db were missing ', 'error' : E}
            return logs_object

        try :

            method_log, rollback_logs, probe_after_method_logs, probe_after_rollback_logs= {}

            # Run probes and get logs and final probes result
            probes_result,probe_logs  = self._run_probes(probes,dns)

            probe_logs = self._update_exit_status(probe_logs, probes_result, "begining")
            # If probes all passed continue
            if probes_result is True :
                # Run methods and  get logs and how much time to wait until checking self recovery
                methods_wait_time, method_logs = self._run_methods(methods, dns)

                # Wait the expected recovery wait time
                sleep(methods_wait_time)

                probes_result, probe_after_method_logs = self._run_probes(probes, dns)

                # Check if server self healed after injection
                probe_after_method_logs = self._update_exit_status(probe_after_method_logs, probes_result, "method")

                if probes_result is False:

                    # If server didnt self heal run rollbacks
                    for rollback in rollbacks:
                        part_name = rollback['name']
                        part_log = self._run_fault_part(rollback, dns)
                        rollback_logs[part_name] = part_log

                    sleep(methods_wait_time)

                    probes_result, probe_after_rollback_logs = self._run_probes(probes, dns)

                    # Check if server healed after rollbacks
                    probe_after_rollback_logs = self._update_exit_status(probe_after_method_logs, probes_result, "rollback")

            logs_object = {'name': fault_name ,'exit_code' : '0' ,
                           'status' : 'expirement ran as expected',
                           'probes' : probe_logs ,
                           'method_logs' : method_logs,
                           'probe_after_method_logs' : probe_after_method_logs,
                           'rollbacks': rollback_logs,
                           'probe_after_rollback_logs' : probe_after_rollback_logs
}

            logs_object["successful"] = probe_after_method_logs["exit_code"] == "0"


        except Exception as E:
            logs_object = {'name': fault_name ,'exit_code' : '1' ,
                           'status' : 'expirement failed because of an unexpected reason', 'error' : E}

        return logs_object

    def _update_exit_status(log, succssessful, status=""):
        if not status:
            if succssessful:
                status_message = f"probes checked after {label}"
            else:
                status_message = f"probes failed after {label}"

        log["exit_code"] = "0" if succssessful else  "1"
        log["status"] = status_message
        return log

    def _get_script(self,fault_part):
        file_share_url = fault_part['path']
        script_name = fault_part['name']
        script = requests.get(file_share_url).content.decode('ascii')
        return script,script_name

    def _create_script_file(self,script,script_name):
        injector_home_dir = "/root"
        script_file_path = '{}/{}'.format(injector_home_dir,script_name)
        with open(script_file_path,'w') as script_file :
            script_file.write(script)
        return script_file_path


    def _inject_script(self,dns,script_path):
        # Run script
        proc = subprocess.Popen("python {} -dns {}".format(script_path,dns), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, shell=True)
        # get output from proc turn it from binary to ascii and then remove /n if there is one
        output = proc.communicate()[0].decode('ascii').rstrip()
        return output


    def _remove_script_file(self,script_file_path):
        os.remove(script_file_path)

    def _run_fault_part(self,fault_part,dns):
        script, script_name = self._get_script(fault_part)
        script_file_path = self._create_script_file(script, script_name)
        logs = self._inject_script(dns, script_file_path)
        self._remove_script_file(script_file_path)
        return logs


    def _str2bool(self,output):
        return output.lower() in ("yes", "true", "t", "1")

    def _probe_server(self,probe,dns):
        output = self._run_fault_part(probe,dns)
        result  = self._str2bool(output)
        return result

    def _run_probes(self,probes,dns):
        probes_output  = {}
        for probe in probes :
            probes_output[probe['name']] =  self._probe_server(probe,dns)
        probes_result = probes_output.values()

        if False in probes_result :
            return False,probes_output

        return True,probes_output



    def _get_method_wait_time(self,method):
        try:
            return  method['method_wait_time']
        except Exception as E :
            return 0


    def _get_current_time(self):
        current_time =  time.strftime('%Y%m%d%H%M%S')
        return current_time


    def _run_methods(self,methods,dns):
        method_logs = {}
        methods_wait_time = 0

        for method in methods:
            part_name = method['name']
            part_log = self._run_fault_part(method, dns)
            method_wait_time = self._get_method_wait_time(method)
            method_logs[part_name] = part_log
            methods_wait_time += method_wait_time

        return  methods_wait_time,method_logs




    def _send_result(self,dns,logs_object,collection = "logs"):
        # Get current time to timestamp the object
        current_time = self._get_current_time()


        # Creating object we will send to the db
        db_log_object = {}
        db_log_object['date'] = current_time
        db_log_object['name'] = "{}-{}".format(logs_object['name'],current_time)
        db_log_object['logs'] = logs_object
        db_log_object['successful'] = logs_object['successful']
        db_log_object['target'] = dns

        # Send POST request to db api in the logs collection
        db_api_logs_url = "{}/{}".format(self.db_api_url,collection)
        response = requests.post(db_api_logs_url, json = db_log_object)

        return  response.content.decode('ascii')


