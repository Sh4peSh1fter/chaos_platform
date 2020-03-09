import requests
from time import sleep
import subprocess
import base64
import os
import time

class InjectionSlave():

    def __init__(self,db_ip = "192.168.56.103",db_api_port = "1738" ):
        self.db_ip = db_ip
        self.db_api_port = db_api_port
        self.db_api_url = "http://{}:{}".format(self.db_ip,self.db_api_port)

    def initiate_fault(self,dns,fault):
        return self.orchestrate_injection(dns,fault)


    def orchestrate_injection(self,dns,fault):
        try :
            # Gets server and fault full information from db
            target_info , fault_info = self.get_info(dns,fault)
        except:
            return { "exit_code":"1" ,"status": "Injector failed gathering facts" }
        try :
            # Runs the probes,methods and rollbacks by order.
            logs_object = self.run_fault(target_info,fault_info)
        except :
            return { "exit_code":"1" ,"status": "Injector failed injecting fault" }
        try :
            # Sends logs to db to be stored in the "logs" collection
            self.send_result(logs_object,"logs")
        except :
            return { "exit_code":"1" ,"status": "Injector failed sending logs to db" }
        return logs_object

    def get_info(self,dns,fault):
        db_server_api_url = "{}/{}/{}".format(self.db_api_url,"server",dns)
        db_fault_api_url = "{}/{}/{}".format(self.db_api_url, "fault", fault)

        fault_info = self.get_fault_info(db_fault_api_url)

        # Getting server and fault info and turning them into json
        server_info = requests.get(db_server_api_url).json()

        return server_info, fault_info


    def get_fault_info(self,db_fault_api_url):
        fault_info = requests.get(db_fault_api_url).json()
        probes = fault_info["probes"]
        methods = fault_info["methods"]
        rollbacks = fault_info["rollbacks"]
        name  = fault_info["name"]
        fault_structure = {'probes' : probes , 'methods' : methods , 'rollbacks' : rollbacks}

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



    def run_fault(self,target_info,fault_info):
        try:
            # Gets dns and fault parts from fault_info
            fault_name = fault_info['name']
            dns = target_info['dns']
            probes = fault_info['probes']
            methods = fault_info['methods']
            rollbacks = fault_info['rollbacks']
        except :
            logs_object = {'name': "failed_fault" ,'exit_code' : '1' , 'status' : 'expirement failed because parameters in db were missing '}
            return logs_object

        try :
            method_logs = {}
            rollback_logs = {}
            probe_after_method_logs = {}

            probes_result,probe_logs  = self.run_probes(probes,dns)
            if probes_result is True :

                probe_logs['exit_code']  =  "0"
                probe_logs['status'] = "Probes checked on victim server successfully"
                methods_wait_time, method_logs = self.run_methods(methods, dns)

                # Wait the expected recovery wait time
                sleep(methods_wait_time)

                probes_result, probe_after_method_logs = self.run_probes(probes, dns)
                # Check if server self healed after injection
                if probes_result is True:
                    probe_after_method_logs['exit_code'] = "0"
                    probe_after_method_logs['status'] = "victim succsessfully self healed after injection"
                else:
                    probe_after_method_logs['exit_code'] = "1"
                    probe_after_method_logs['status'] = "victim failed self healing after injection"

                    # If server didnt self heal run rollbacks
                    for rollback in rollbacks:
                        part_name = rollback['name']
                        part_log = self.run_fault_part(rollback, dns)
                        rollback_logs[part_name] = part_log

                    sleep(methods_wait_time)

                    # Check if server healed after rollbacks
                    if probes_result is True:
                        rollbacks['exit_code'] = "0"
                        rollbacks['status'] = "victim succsessfully  healed after rollbacks"
                    else:
                        rollbacks['exit_code'] = "1"
                        rollbacks['status'] = "victim failed healing after rollbacks"
            else :
                probe_logs['exit_code'] = "1"
                probe_logs['status'] = "Probes check failed on victim server"

            logs_object = {'name': fault_name ,'exit_code' : '0' , 'status' : 'expirement ran as unexpected','rollbacks' : rollback_logs , 'probes' : probe_logs , 'method_logs' : method_logs,'probe_after_method_logs' : probe_after_method_logs}

        except :
            logs_object = {'name': fault_name ,'exit_code' : '1' , 'status' : 'expirement failed because of an unexpected reason'}

        return logs_object



    def run_probes(self,probes,dns):
        probes_output  = {}
        for probe in probes :
            probes_output[probe['name']] =  self.probe_server(probe,dns)
        probes_result = probes_output.values()
        if False in probes_result :
            return False,probes_output

        return True,probes_output

    def run_methods(self,methods,dns):
        method_logs = {}
        methods_wait_time = 0
        for method in methods:
            part_name = method['name']
            part_log = self.run_fault_part(method, dns)
            method_wait_time = self.get_method_wait_time(method)
            method_logs[part_name] = part_log
            methods_wait_time += method_wait_time

        return  methods_wait_time,method_logs

    def get_script(self,fault_part):
        script_name = fault_part['name']
        script_in_base64 = fault_part['content']
        binary_script_in_ascii = base64.b64decode(script_in_base64)
        script_in_ascii = binary_script_in_ascii.decode('ascii')
        return script_in_ascii,script_name

    def create_script_file(self,script,script_name):
        injector_home_dir = "/home/injector"
        #script_file_path = '{}/{}'.format(injector_home_dir,script_name)
        script_file_path = r"c:\users\borat\{}".format(script_name)
        with open(script_file_path,'w') as script_file :
            script_file.write(script)
        return script_file_path

    def remove_script_file(self,script_file_path):
        os.remove(script_file_path)

    def get_method_wait_time(self,method):
        return 0

    def send_logs_to_db(self,logs,collection):
        pass


    def inject_script(self,dns,script_path):
        proc = subprocess.Popen("python {} -dns {}".format(script_path,dns), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, shell=True)
        output = proc.communicate()[0]
        return output

    def probe_server(self,probe,dns):
        output = self.run_fault_part(probe,dns)
        result  = self.str2bool(output)
        return result

    def str2bool(self,output):
        return output.lower() in ("yes", "true", "t", "1")

    def run_fault_part(self,fault_part,dns):
        script, script_name = self.get_script(fault_part)
        script_file_path = self.create_script_file(script, script_name)
        logs = self.inject_script(dns, script_file_path)
        self.remove_script_file(script_file_path)
        return logs

    def get_current_time(self):
        current_time =  time.strftime('%Y%m%d%H%M%S')
        return current_time


    def send_result(self,logs_object,collection = "logs"):
        current_time = self.get_current_time()
        logs_object['date'] = current_time
        db_api_logs_url = "{}/{}".format(self.db_api_url,collection)
        response = requests.post(db_api_logs_url, json = logs_object)
        return  response

