import requests
from apscheduler.schedulers.background import BackgroundScheduler
import json

class ChaosMaster:
    def __init__(self, injector_url, random_picker_url, interval = 30, group = "all"):
        self._interval = interval
        self._group = group
        self.__job_id = "fabulous_inject_id"
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._scheduler.add_job(self.inject, 'interval', seconds=self.get_interval(), id=self.__job_id)
        self.__last_injection = ""
        self.__injector_url = injector_url
        self.__random_picker_url = random_picker_url

    def get_group(self):
        return self._group

    def set_group(self, new_group):
        self._group = new_group
        return ""

    def __set_last_injection(self, data):
        self.__last_injection = data

    def __get_last_injection(self):
        return self.__last_injection

    def set_interval(self, new_interval):
        self._interval = int(new_interval)
        if self._interval > 0:
            self._change_scheduler()

        return ""

    def get_interval(self):
        return self._interval

    def _change_scheduler(self):
        self._scheduler.reschedule_job(self.__job_id, trigger='interval', seconds=self.get_interval())

    def inject(self):
        url = "{0}/inject_fault".format(self.__injector_url)
        victim_server = self._acquire_server()

        if victim_server != None:
            picked_fault = self._acquire_fault(victim_server)

            data = {"dns": victim_server['dns'], "fault": picked_fault['name']}
            try:
                res = requests.post(url, json=data)
                data["inject_res"] = res.content.decode("utf-8")
                self.__set_last_injection(data)
            except Exception as e:
                print("exeption while sending request to injection\n", e)


    def _acquire_fault(self, server_entry):
        url = "{0}/get-fault".format(self.__random_picker_url)
        response = requests.post(url, json=server_entry)
        dict_res = None

        # Check if the request succeed
        if "200" in str(response):
            dict_res = json.loads(response.content)

        return dict_res

    def _acquire_server(self):
        url = "{0}/get-server".format(self.__random_picker_url)
        data = {"group": self._group}
        response = requests.post(url, json=data)
        dict_res = None

        # Check if the request succeed
        if "200" in str(response):
            dict_res = json.loads(response.content)

        return dict_res

    def info(self):
        return {"interval": self.get_interval(), "group": self.get_group(), "last injection": self.__get_last_injection()}


