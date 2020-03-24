from flask import Flask, request
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
import json

random_picker_url = os.environ.get("PICKER_API", "http://127.0.0.1:5001")
injector_url = os.environ.get("INJECTOR_API", "http://127.0.0.1:5002")

class ChaosMaster:
    def __init__(self, interval = 30, group = "all"):
        self._interval = interval
        self._group = group
        self.__job_id = "fabulous_inject_id"
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._scheduler.add_job(self.inject, 'interval', seconds=self.get_interval(), id=self.__job_id)
        self.__last_injection = ""

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
        url = "{0}/inject_fault".format(injector_url)
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
        url = "{0}/get-fault".format(random_picker_url)
        response = requests.post(url, json=server_entry)
        dict_res = None

        # Check if the request succeed
        if "200" in str(response):
            dict_res = json.loads(response.content)

        return dict_res

    def _acquire_server(self):
        url = "{0}/get-server".format(random_picker_url)
        data = {"group": self._group}
        response = requests.post(url, json=data)
        dict_res = None

        # Check if the request succeed
        if "200" in str(response):
            dict_res = json.loads(response.content)

        return dict_res

    def info(self):
        return {"interval": self.get_interval(), "group": self.get_group(), "last injection": self.__get_last_injection()}


master = ChaosMaster()
app = Flask(__name__)

@app.route('/set-interval',methods=['POST'])
def set_new_interval():
    json_object = request.get_json()
    try:
        new_interval = json_object["interval"]
    except KeyError:
        return "interval is a required parameter", 400
    return master.set_interval(new_interval), 200

@app.route('/set-group',methods=['POST'])
def set_new_group():
    json_object = request.get_json()
    try:
        new_group = json_object["group"]
    except KeyError:
        return "group is a required parameter", 400
    return master.set_group(new_group), 200

@app.route('/master-info',methods=['GET'])
def master_info():
    #return json.dumps(master.info())
    return master.info()

@app.route('/test',methods=['GET'])
def test():
    return "hello world"

if __name__ == '__main__':
    app.run(port=5003, host='0.0.0.0')