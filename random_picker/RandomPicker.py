import requests
import random
import json
from flask import Flask, request
import os
# from apscheduler.schedulers.background import BackgroundScheduler


db_port = os.environ.get("API_PORT", 5000)
mongo_host = os.environ.get("API_DB_HOST", "127.0.0.1")
db_host = "http://{0}:{1}".format(mongo_host, db_port)

class Picker:
    def __init__(self):
        self.pick_interval = 300
        self.group_pick = "all"

    def set_interval(self, new_interval):
        self.pick_interval = new_interval

    def set_group(self, new_group):
        self.group_pick = new_group

    def show_data(self):
        return json.dumps({"Interval": self.pick_interval, "Group to pick": self.group_pick}, indent=2)

    def get_fault(self, server):
        response = requests.get("{0}/fault".format(db_host))
        filtered_fault_list = []
        # Check if request succeeded
        if "200" in str(response):
            all_faults = json.loads(response.content.decode("utf-8"))["result"]
            for fault in all_faults:
                for server_group in server["groups"]:
                    if fault["active"]:
                        if server_group in fault["targets"]:
                            filtered_fault_list.append(fault)
                            break

        return random.choice(filtered_fault_list)

    def get_server(self, new_group = "all"):
        response = requests.get("{0}/server".format(db_host))
        single_server = None
        # Check if request succeeded
        if "200" in str(response):
            server_list = json.loads(response.content.decode("utf-8"))["result"]
            # Check if the servers have to be filtered by group
            if self.group_pick != new_group:
                filter_groups = lambda server: server if new_group in server["groups"] else None
                filtered_server_list = list(map(filter_groups, server_list))
                server_list = list(filter(None, filtered_server_list))

            if len(server_list) != 0:
                single_server = random.choice(server_list)

        return single_server


app = Flask(__name__)
the_picker = Picker()


@app.route('/get-server', methods=['POST'])
def get_server():
    json_object = request.get_json()
    try:
        group = json_object["group"]
    except KeyError:
        return "group is a required parameter", 400
    return the_picker.get_server(group), 200

@app.route('/get-fault', methods=['POST'])
def get_fault():
    json_object = request.get_json()

    return the_picker.get_fault(json_object), 200

@app.route('/pick-data',methods=['GET'])
def get_picker_data():
    return the_picker.show_data()

@app.route('/test',methods=['GET'])
def test():
    return "hello world"

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(port=5001, host='0.0.0.0')
    #app.run(host='0.0.0.0')
