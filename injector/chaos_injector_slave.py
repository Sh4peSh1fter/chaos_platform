import threading
import requests

class InjectionSlave():

    def __init__(self,db_ip = "192.168.56.103",db_api_port = "1738" ):
        self.db_ip = db_ip
        self.db_api_port = db_api_port
        self.db_api_url = "http://{}:{}".format(self.db_ip,self.db_api_port)

    def initiate_fault(self,dns,fault):
        #fault_thread = threading.Thread(target=self.orchestrate_injection , args=[dns,fault])
        #fault_thread.start()
        self.orchestrate_injection(dns,fault)

    def orchestrate_injection(self,dns,fault):
        target_info , fault_info = self.get_info(dns,fault)
        built_script = self.build_script(target_info,fault_info)
        injection_logs = self.inject_script()
        self.send_result(injection_logs)

    def get_info(self,dns,fault):
        db_server_api_url = "{}/{}/{}".format(self.db_api_url,"server",dns)
        db_fault_api_url = "{}/{}/{}".format(self.db_api_url, "fault", fault)
        server_info = requests.get(db_server_api_url)
        fault_info = requests.get(db_fault_api_url)
        return server_info, fault_info

    def build_script(self,target_info,fault_info):
        print(target_info)
        print(fault_info)

    def inject_script(self):
        pass

    def send_result(self):
        pass


