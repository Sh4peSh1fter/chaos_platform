from flask import Flask, request
import os
from master.app.chaos_master import ChaosMaster

random_picker_url = os.environ.get("PICKER_API", "http://127.0.0.1:5001")
injector_url = os.environ.get("INJECTOR_API", "http://127.0.0.1:5002")
server_port = int(os.environ.get("SERVER_PORT", 5003))

master = {}
app = Flask(__name__)

@app.route('/set-interval',methods=['POST'])
def set_new_interval():
    json_object = request.get_json()
    try:
        new_interval = json_object["interval"]
        uid = json_object["uid"]
    except:
        return "interval and uid are required parameters", 400
    return master[str(uid)].set_interval(new_interval), 200

@app.route('/set-group',methods=['POST'])
def set_new_group():
    json_object = request.get_json()
    try:
        new_group = json_object["group"]
        uid = json_object["uid"]
    except:
        return "group and uid are required parameters", 400
    return master[str(uid)].set_group(new_group), 200

@app.route('/add-master', methods=['POST'])
def add_master():
    json_object = request.get_json()
    print(json_object)
    try:
        uid = json_object["uid"]
        print(uid)
        interval = json_object["interval"]
        print(interval)
        group = json_object["group"]
        print(group)
        master[str(uid)] = ChaosMaster(injector_url=injector_url, random_picker_url=random_picker_url, interval=int(interval), group=str(group))
        print(master)
    except:
        print("Error - adding master instance.")

    return "Succeed creating master instance", 200


@app.route('/remove-master', methods=['POST'])
def remove_master():
    json_object = request.get_json()
    try:
        uid = json_object["uid"]
        del master[str(uid)]
    except:
        print("Error - removing master instance.")

@app.route('/test',methods=['GET'])
def test():
    return "hello world"

if __name__ == '__main__':
    app.run(port=server_port, host='0.0.0.0', debug=True)