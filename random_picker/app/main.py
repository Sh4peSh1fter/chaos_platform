import requests
import random
import json
from flask import Flask, request
import os
from RandomPicker import Picker
#from random_picker.app.RandomPicker import Picker

listen_port = os.environ.get("LISTEN_PORT", 5005)
db_port = os.environ.get("API_PORT", 5001)
mongo_host = os.environ.get("API_DB_HOST", "52.255.160.180")
queue_size = os.environ.get("QUEUE_SIZE", 1)
db_host = "http://{0}:{1}".format(mongo_host, db_port)

app = Flask(__name__)
the_picker = Picker(db_host = db_host, queue_size = queue_size)


@app.route('/get-server', methods=['POST'])
def get_server():
    json_object = request.get_json()
    try:
        group = json_object["group"]
        print(group)
        print(the_picker.get_server(group))
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
    app.run(port=listen_port, host='0.0.0.0', debug=True)
