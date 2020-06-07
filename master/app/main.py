from flask import Flask, request
import os
from chaos_master import ChaosMaster
#from master.app.chaos_master import ChaosMaster

random_picker_url = os.environ.get("PICKER_API", "http://127.0.0.1:5001")
injector_url = os.environ.get("INJECTOR_API", "http://127.0.0.1:5002")
server_port = int(os.environ.get("SERVER_PORT", 5003))

master = ChaosMaster(random_picker_url = random_picker_url, injector_url = injector_url)
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
    app.run(port=server_port, host='0.0.0.0', debug=True, use_reloader=Flase)
