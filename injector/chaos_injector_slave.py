import requests
from time import sleep

class InjectionSlave():

    def __init__(self,db_ip = "192.168.56.103",db_api_port = "1738" ):
        self.db_ip = db_ip
        self.db_api_port = db_api_port
        self.db_api_url = "http://{}:{}".format(self.db_ip,self.db_api_port)

    def initiate_fault(self,dns,fault):
        return self.orchestrate_injection(dns,fault)


    def orchestrate_injection(self,dns,fault):
        # Gets server and fault full information from db
        target_info , fault_info = self.get_info(dns,fault)

        #built_script = self.build_script(target_info,fault_info)
        # Runs the probes,methods and rollbacks by order.
        injection_logs = self.run_fault(target_info,fault_info)
        #self.send_result(injection_logs)

        return target_info , fault_info

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

        fault_structure = {'probes' : probes , 'methods' : methods , 'rollbacks' : rollbacks}

        # fault_section can be the probes/methods/rollbacks part of the fault
        for fault_section in fault_structure.keys():
            fault_section_parts = []
            # section_part refers to a specific part of the probes/methods/rollbacks
            for section_part in fault_structure[fault_section]:
                section_part_info = requests.get("{}/{}/{}".format(self.db_api_url,fault_section,section_part)).json()
                fault_section_parts.append(section_part_info)
            fault_structure[fault_section] = fault_section_parts
        return fault_structure


    def build_script(self,target_info,fault_info):
        return "working"


    def run_fault(self,target_info,fault_info):
        dns = target_info['dns']
        probes = fault_info['probes']
        probes_result,probe_logs  = self.run_probes(self,probes,target_info)

        if probes_result is False :
            return {'exit_code' : '2', 'status' : 'Probes check failed on vicim server' }

        methods_wait_time = 0
        method_logs = []
        for method in fault_info['methods']:
            logs = self.inject_script(dns,method)
            method_logs.append({method['name'] : logs})
            methods_wait_time += self.get_method_wait_time(method)

        sleep(methods_wait_time)

        probes_result,probe_after_method_logs  = self.run_probes(self,probes,target_info)
        if probes_result is True :
            return {'exit_code' : '0', 'status' : 'Services self healed after injection' }

        rollback_logs = []
        for rollback in fault_info['rollbacks']:
            logs = self.inject_script(dns,rollback)
            rollback_logs.append({rollback['name'] : logs})

        self.send_result(probe_logs, method_logs, probe_after_method_logs, rollback_logs)



    def run_probes(self,probes,target_info):
        probes_output  = {}
        for probe in probes :
            probes_output[probe['name']] =  self.probe_server(target_info,probe)
        probes_result = probes_output.values()
        if False in probes_result :
            return False,probes_output

        return True,probes_output


    def get_method_wait_time(self,method):
        try:
            method_wait_time = method['method_wait_time']
        except KeyError :
            method_wait_time = 0
        return method_wait_time

    def send_logs_to_db(self,logs,collection):
        pass


    def inject_script(self,dns,script):
        output = ""
        return output

    def probe_server(self,target_info,probe):
        result  = True
        return result

    def send_result(self,probe_logs,method_logs,probe_after_method_logs,rollback_logs):
        pass


