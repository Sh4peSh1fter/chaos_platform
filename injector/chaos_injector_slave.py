import requests

class InjectionSlave():

    def __init__(self,db_ip = "192.168.56.103",db_api_port = "1738" ):
        self.db_ip = db_ip
        self.db_api_port = db_api_port
        self.db_api_url = "http://{}:{}".format(self.db_ip,self.db_api_port)

    def initiate_fault(self,dns,fault):
        return self.orchestrate_injection(dns,fault)

    def orchestrate_injection(self,dns,fault):
        target_info , fault_info = self.get_info(dns,fault)
        #built_script = self.build_script(target_info,fault_info)
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
        fault_parts = fault_info.keys()
        dns = target_info['dns']
        probes_output  = []
        for probe in fault_info['probes'] :
            probes_output.append(self.probe_server(target_info,probe))
        if False in probes_output :
            return {'status': 'injection failed on probes', 'exit_code' : '2'}

        for method in fault_info['methods']:
            logs = self.inject_script(dns,method)
            self.send_logs_to_db(logs,"methods_logs")
        for rollback in fault_info['rollbacks']:
            logs = self.inject_script(dns,rollback)
            self.send_logs_to_db(logs,"rollbacks_logs")
            

    def send_logs_to_db(self,logs,collection):
        pass


    def inject_script(self,dns,script):
        output = ""
        return output

    def probe_server(self,target_info,probe):
        result  = True
        return result

    def send_result(self):
        pass


